from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
import os
import csv
import io
import pandas as pd
from src.config import Config
from src.database import init_db, add_translation, add_history, get_history, clear_history, delete_history_item, get_total_history_count, get_db_connection
from src.preprocessing import preprocess_text
from src.translator import MarianTranslator, TranslatorError
from src.evaluation import calculate_metrics, evaluate_samples
from src.dataset import generate_default_dataset_csv, import_csv_to_db, get_dataset_from_db, get_dataset_stats
from src.utils import get_text_stats, get_formatted_date
import difflib

app = Flask(__name__)
app.config.from_object(Config)

init_db()
generate_default_dataset_csv()
try:
    import_csv_to_db()
except Exception:
    pass

translator = MarianTranslator()
model_error = None
try:
    translator.initialize()
except Exception as e:
    model_error = str(e)

def find_reference(input_text: str) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT indonesia, english FROM dataset")
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return ""
        
    best_match_english = ""
    highest_ratio = 0.0
    input_clean = input_text.lower().strip()
    
    for row in rows:
        ratio = difflib.SequenceMatcher(None, input_clean, row["indonesia"].lower().strip()).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match_english = row["english"]
            
    if highest_ratio > 0.2:
        return best_match_english
    return rows[0]["english"] if rows else ""

@app.route("/")
def index():
    stats = get_dataset_stats()
    history_count = get_total_history_count()
    return render_template(
        "index.html",
        active_page="index",
        today_date=get_formatted_date(),
        dataset_count=stats["total_rows"],
        history_count=history_count
    )

@app.route("/dataset")
def dataset():
    page = request.args.get("page", 1, type=int)
    search_query = request.args.get("search", "", type=str)
    per_page = 15
    
    items, total_count = get_dataset_from_db(page, per_page, search_query)
    stats = get_dataset_stats()
    
    total_pages = (total_count + per_page - 1) // per_page
    
    return render_template(
        "dataset.html",
        active_page="dataset",
        today_date=get_formatted_date(),
        items=items,
        page=page,
        total_pages=total_pages,
        search_query=search_query,
        stats=stats
    )

@app.route("/dataset/upload", methods=["POST"])
def upload_dataset():
    if "file" not in request.files:
        return redirect(url_for("dataset"))
    file = request.files["file"]
    if file.filename == "":
        return redirect(url_for("dataset"))
    
    if file and file.filename.endswith(".csv"):
        os.makedirs(app.config["DATASET_DIR"], exist_ok=True)
        file_path = app.config["DATASET_PATH"]
        file.save(file_path)
        try:
            import_csv_to_db(file_path)
        except Exception:
            pass
            
    return redirect(url_for("dataset"))

@app.route("/dataset/import-default")
def import_default_dataset():
    try:
        if os.path.exists(app.config["DATASET_PATH"]):
            os.remove(app.config["DATASET_PATH"])
        generate_default_dataset_csv()
        import_csv_to_db()
    except Exception:
        pass
    return redirect(url_for("dataset"))

@app.route("/translate")
def translate():
    return render_template(
        "translate.html",
        active_page="translate",
        today_date=get_formatted_date(),
        model_error=model_error
    )

@app.route("/api/translate", methods=["POST"])
def api_translate():
    if model_error:
        return jsonify({
            "success": False,
            "message": f"Model gagal dimuat: {model_error}. Solusi: Pastikan koneksi internet aktif untuk mengunduh model dari Hugging Face pada percobaan pertama, atau periksa ruang penyimpanan Anda."
        }), 500
        
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"success": False, "message": "Silakan masukkan kalimat Bahasa Indonesia."}), 400
        
    try:
        prep = preprocess_text(text)
        final_input = prep["final"]
        
        translation = translator.translate(final_input)
        
        add_translation(text, translation)
        
        ref = find_reference(text)
        metrics = calculate_metrics(translation, ref)
        
        add_history(
            input_text=text,
            translated_text=translation,
            bleu=metrics["bleu"],
            rouge=metrics["rougeL"],
            meteor=metrics["meteor"]
        )
        
        stats = get_text_stats(translation)
        
        return jsonify({
            "success": True,
            "translation": translation,
            "stats": stats,
            "preprocess": prep
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Gagal menerjemahkan: {str(e)}"}), 500

@app.route("/api/history")
def api_history():
    history = get_history()
    return jsonify(history)

@app.route("/api/history/clear", methods=["POST"])
def api_clear_history():
    clear_history()
    return jsonify({"success": True})

@app.route("/api/history/delete/<int:item_id>", methods=["POST"])
def api_delete_history(item_id):
    delete_history_item(item_id)
    return jsonify({"success": True})

@app.route("/api/evaluation/history")
def api_evaluation_history():
    history = get_history(10)
    history.reverse()
    return jsonify(history)

@app.route("/export/history/csv")
def export_history_csv():
    history = get_history(1000)
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(["ID", "Bahasa Indonesia", "Bahasa Inggris", "BLEU", "ROUGE", "METEOR", "Tanggal"])
    
    for row in history:
        cw.writerow([
            row["id"],
            row["input_text"],
            row["translated_text"],
            row["bleu"],
            row["rouge"],
            row["meteor"],
            row["created_at"]
        ])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=history_translation.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route("/evaluation")
def evaluation():
    if model_error:
        return render_template(
            "evaluation.html",
            active_page="evaluation",
            today_date=get_formatted_date(),
            eval_results={
                "avg_bleu": 0.0,
                "avg_rouge1": 0.0,
                "avg_rouge2": 0.0,
                "avg_rougeL": 0.0,
                "avg_meteor": 0.0,
                "details": []
            },
            model_error=model_error
        )
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT indonesia, english FROM dataset LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    
    pairs = []
    for row in rows:
        indo = row["indonesia"]
        ref = row["english"]
        try:
            hyp = translator.translate(preprocess_text(indo)["final"])
        except Exception:
            hyp = ""
        pairs.append((indo, ref, hyp))
        
    eval_results = evaluate_samples(pairs)
    return render_template(
        "evaluation.html",
        active_page="evaluation",
        today_date=get_formatted_date(),
        eval_results=eval_results,
        model_error=None
    )

@app.route("/documentation")
def documentation():
    return render_template(
        "documentation.html",
        active_page="documentation",
        today_date=get_formatted_date()
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", today_date=get_formatted_date()), 404

if __name__ == "__main__":
    app.run(debug=True)

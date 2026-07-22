import datetime

def get_text_stats(text: str) -> dict:
    if not text.strip():
        return {
            "char_count": 0,
            "word_count": 0,
            "reading_time": 0.0
        }
    char_count = len(text)
    word_count = len(text.split())
    reading_time = round((word_count / 200) * 60, 1)
    if reading_time < 1.0:
        reading_time = 1.0
    return {
        "char_count": char_count,
        "word_count": word_count,
        "reading_time": reading_time
    }

def get_formatted_date() -> str:
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    months = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    now = datetime.datetime.now()
    day_name = days[now.weekday()]
    month_name = months[now.month - 1]
    return f"{day_name}, {now.day} {month_name} {now.year}"

document.addEventListener("DOMContentLoaded", function () {
    const loader = document.getElementById("loaderContainer");
    if (loader) {
        setTimeout(function () {
            loader.style.opacity = "0";
            setTimeout(function () {
                loader.style.display = "none";
            }, 300);
        }, 300);
    }

    const navbar = document.querySelector(".navbar");
    window.addEventListener("scroll", function () {
        if (window.scrollY > 50) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    });

    const scrollToTopBtn = document.getElementById("scrollToTop");
    if (scrollToTopBtn) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > 200) {
                scrollToTopBtn.style.display = "flex";
            } else {
                scrollToTopBtn.style.display = "none";
            }
        });
        scrollToTopBtn.addEventListener("click", function () {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }

    const translateForm = document.getElementById("translateForm");
    if (translateForm) {
        const inputText = document.getElementById("inputText");
        const translatedText = document.getElementById("translatedText");
        const btnTranslate = document.getElementById("btnTranslate");
        const btnReset = document.getElementById("btnReset");
        const btnUseExample = document.getElementById("btnUseExample");
        const btnCopy = document.getElementById("btnCopy");
        const btnDownload = document.getElementById("btnDownload");
        const progressBarFill = document.getElementById("progressBarFill");
        const translationAlert = document.getElementById("translationAlert");

        const charCountOut = document.getElementById("charCountOut");
        const wordCountOut = document.getElementById("wordCountOut");
        const readingTimeOut = document.getElementById("readingTimeOut");

        const stepOriginal = document.getElementById("stepOriginal");
        const stepLowercase = document.getElementById("stepLowercase");
        const stepCleaned = document.getElementById("stepCleaned");
        const stepWhitespace = document.getElementById("stepWhitespace");
        const stepTokenized = document.getElementById("stepTokenized");
        const stepFinal = document.getElementById("stepFinal");

        btnUseExample.addEventListener("click", function () {
            inputText.value = "Model transformer mengubah dunia teknologi informasi.";
        });

        btnReset.addEventListener("click", function () {
            inputText.value = "";
            translatedText.value = "";
            progressBarFill.style.width = "0%";
            charCountOut.textContent = "0";
            wordCountOut.textContent = "0";
            readingTimeOut.textContent = "0";
            
            stepOriginal.textContent = "-";
            stepLowercase.textContent = "-";
            stepCleaned.textContent = "-";
            stepWhitespace.textContent = "-";
            stepTokenized.textContent = "-";
            stepFinal.textContent = "-";
            
            if (translationAlert) {
                translationAlert.classList.add("d-none");
            }
        });

        btnCopy.addEventListener("click", function () {
            if (translatedText.value.strip !== "") {
                navigator.clipboard.writeText(translatedText.value);
                alert("Teks berhasil disalin ke clipboard.");
            }
        });

        btnDownload.addEventListener("click", function () {
            if (translatedText.value.strip !== "") {
                const element = document.createElement("a");
                const file = new Blob([translatedText.value], {type: "text/plain"});
                element.href = URL.createObjectURL(file);
                element.download = "translation.txt";
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);
            }
        });

        translateForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const text = inputText.value.trim();
            const model = document.getElementById("modelSelect").value;

            if (!text) {
                alert("Silakan masukkan kalimat Bahasa Indonesia.");
                return;
            }

            btnTranslate.disabled = true;
            progressBarFill.style.width = "30%";

            let progressInterval = setInterval(function () {
                let currentWidth = parseFloat(progressBarFill.style.width);
                if (currentWidth < 90) {
                    progressBarFill.style.width = (currentWidth + 10) + "%";
                }
            }, 400);

            fetch("/api/translate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: text,
                    model: model
                })
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.message || "Gagal memproses terjemahan."); });
                }
                return response.json();
            })
            .then(data => {
                clearInterval(progressInterval);
                progressBarFill.style.width = "100%";
                
                translatedText.value = data.translation;
                
                charCountOut.textContent = data.stats.char_count;
                wordCountOut.textContent = data.stats.word_count;
                readingTimeOut.textContent = data.stats.reading_time;

                stepOriginal.textContent = data.preprocess.original;
                stepLowercase.textContent = data.preprocess.lowercase;
                stepCleaned.textContent = data.preprocess.cleaned;
                stepWhitespace.textContent = data.preprocess.whitespace_normalized;
                stepTokenized.textContent = data.preprocess.tokenized;
                stepFinal.textContent = data.preprocess.final;

                if (translationAlert) {
                    translationAlert.classList.remove("d-none");
                    setTimeout(function () {
                        translationAlert.classList.add("d-none");
                    }, 3000);
                }
                
                btnTranslate.disabled = false;
                loadHistoryTable();
            })
            .catch(error => {
                clearInterval(progressInterval);
                progressBarFill.style.width = "0%";
                btnTranslate.disabled = false;
                alert("Error: " + error.message);
            });
        });
    }

    const historyTableBody = document.getElementById("historyTableBody");
    if (historyTableBody) {
        loadHistoryTable();

        const btnClearHistory = document.getElementById("btnClearHistory");
        if (btnClearHistory) {
            btnClearHistory.addEventListener("click", function () {
                if (confirm("Apakah Anda yakin ingin menghapus semua riwayat?")) {
                    fetch("/api/history/clear", {
                        method: "POST"
                    })
                    .then(response => response.json())
                    .then(data => {
                        loadHistoryTable();
                    });
                }
            });
        }
    }

    function loadHistoryTable() {
        const body = document.getElementById("historyTableBody");
        if (!body) return;

        fetch("/api/history")
        .then(response => response.json())
        .then(data => {
            body.innerHTML = "";
            if (data.length === 0) {
                body.innerHTML = "<tr><td colspan='7' class='text-center'>Tidak ada riwayat terjemahan.</td></tr>";
                return;
            }
            data.forEach((row, index) => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${escapeHtml(row.input_text)}</td>
                    <td>${escapeHtml(row.translated_text)}</td>
                    <td>${row.bleu.toFixed(2)}</td>
                    <td>${row.rouge.toFixed(2)}</td>
                    <td>${row.meteor.toFixed(2)}</td>
                    <td>
                        <button class="btn btn-sm btn-danger btn-delete-item" data-id="${row.id}">Hapus</button>
                    </td>
                `;
                body.appendChild(tr);
            });

            document.querySelectorAll(".btn-delete-item").forEach(button => {
                button.addEventListener("click", function () {
                    const id = this.getAttribute("data-id");
                    if (confirm("Hapus item ini dari riwayat?")) {
                        fetch(`/api/history/delete/${id}`, {
                            method: "POST"
                        })
                        .then(response => response.json())
                        .then(res => {
                            loadHistoryTable();
                        });
                    }
                });
            });
        });
    }

    function escapeHtml(text) {
        if (!text) return "";
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    const evaluationCharts = document.getElementById("evaluationBarChart");
    if (evaluationCharts) {
        const scoreBleu = parseFloat(evaluationCharts.getAttribute("data-bleu"));
        const scoreRouge1 = parseFloat(evaluationCharts.getAttribute("data-rouge1"));
        const scoreRouge2 = parseFloat(evaluationCharts.getAttribute("data-rouge2"));
        const scoreRougeL = parseFloat(evaluationCharts.getAttribute("data-rougeL"));
        const scoreMeteor = parseFloat(evaluationCharts.getAttribute("data-meteor"));

        new Chart(evaluationCharts, {
            type: "bar",
            data: {
                labels: ["BLEU", "ROUGE-1", "ROUGE-2", "ROUGE-L", "METEOR"],
                datasets: [{
                    label: "Nilai Metrik (%)",
                    data: [scoreBleu, scoreRouge1, scoreRouge2, scoreRougeL, scoreMeteor],
                    backgroundColor: [
                        "#5BAE7A",
                        "#87C9A5",
                        "#D9F2E3",
                        "#3D9C67",
                        "#4B9B69"
                    ],
                    borderColor: [
                        "#5BAE7A",
                        "#87C9A5",
                        "#87C9A5",
                        "#3D9C67",
                        "#4B9B69"
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });

        const gaugeCanvas = document.getElementById("evaluationGaugeChart");
        if (gaugeCanvas) {
            new Chart(gaugeCanvas, {
                type: "doughnut",
                data: {
                    labels: ["Skor Rata-rata", "Sisa"],
                    datasets: [{
                        data: [scoreBleu, 100 - scoreBleu],
                        backgroundColor: ["#5BAE7A", "#E9ECEF"],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    cutout: "80%",
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            enabled: false
                        }
                    }
                }
            });
        }

        const lineCanvas = document.getElementById("evaluationLineChart");
        if (lineCanvas) {
            fetch("/api/evaluation/history")
            .then(res => res.json())
            .then(data => {
                const labels = data.map((d, i) => "Sesi " + (i + 1));
                const bleuData = data.map(d => d.bleu);
                const rougeData = data.map(d => d.rouge);
                const meteorData = data.map(d => d.meteor);

                new Chart(lineCanvas, {
                    type: "line",
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: "BLEU",
                                data: bleuData,
                                borderColor: "#5BAE7A",
                                tension: 0.1,
                                fill: false
                            },
                            {
                                label: "ROUGE",
                                data: rougeData,
                                borderColor: "#3D9C67",
                                tension: 0.1,
                                fill: false
                            },
                            {
                                label: "METEOR",
                                data: meteorData,
                                borderColor: "#87C9A5",
                                tension: 0.1,
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        }
                    }
                });
            });
        }
    }
});

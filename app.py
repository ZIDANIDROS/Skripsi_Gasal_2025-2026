from flask import Flask, render_template, request
import os
from collections import defaultdict
from data_processing.apriori_logic import run_apriori
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ================= HOME =================
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["excel_file"]
        ms = float(request.form["min_support"])
        mc = float(request.form["min_confidence"])
        ml = float(request.form["min_lift"])

        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(path)

        result = run_apriori(path, ms, mc, ml)

        # ===== Simpan semua hasil ke memory =====
        app.config["LAST_RULES"] = result["rules"]
        app.config["LAST_INTERVALS"] = result["intervals"]
        app.config["PREPROCESS"] = result["preprocessing"]
        app.config["PROCESS_LOG"] = result["process"]
        app.config["L_ALL"] = result["L_all"]
        app.config["TOTAL_TRX"] = result["total_transaksi"] 

        return render_template(
            "hasil.html",
            rules=result["rules"],
            intervals=result["intervals"]
        )

    return render_template("index.html")


# ================= TAMPIL DATA ASLI =================
@app.route("/data")
def tampil_data():
    folder = "uploads"
    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".xlsx")
    ]

    latest_file = max(files, key=os.path.getmtime)

    df = pd.read_excel(latest_file)
    df = df.dropna().reset_index(drop=True)
    df.columns = df.columns.str.replace(" ", "_")

    return render_template("data.html", df=df)


# ================= HALAMAN HASIL RULE =================
@app.route("/hasil-terakhir")
def hasil_terakhir():
    rules = app.config.get("LAST_RULES", [])
    intervals = app.config.get("LAST_INTERVALS", {})
    return render_template("hasil.html", rules=rules, intervals=intervals)


# ================= HALAMAN PROSES APRIORI =================
@app.route("/proses")
def proses():
    return render_template(
        "proses.html",
        pre=app.config.get("PREPROCESS"),
        process=app.config.get("PROCESS_LOG"),
        L_all=app.config.get("L_ALL"),
        total_trx=app.config.get("TOTAL_TRX"),
        rules=app.config.get("LAST_RULES")
    )


# ================= HALAMAN KESIMPULAN / BUNDLING =================
@app.route("/kesimpulan")
def kesimpulan():
    rules = app.config.get("LAST_RULES", [])
    intervals = app.config.get("LAST_INTERVALS", {})

    grouped = defaultdict(list)
    for r in rules:
        grouped[r["k"]].append(r)

    summary = {}
    for k in range(2, 8):
        if k in grouped:
            summary[k] = sorted(grouped[k], key=lambda x: x["lift"], reverse=True)[:3]

    return render_template("kesimpulan.html", summary=summary, intervals=intervals)


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, port=5001)

import pandas as pd
import itertools
from collections import Counter

def run_apriori(filepath, min_support, min_confidence, min_lift):
    df = pd.read_excel(filepath)

    # ================= PREPROCESSING =================
    df_awal = df.copy()

    df = df.dropna().reset_index(drop=True)
    df.columns = df.columns.str.replace(" ", "_")

    df_setelah_cleaning = df.copy()

    numeric_cols = ["Genteng","Nok","Lisplang","Ujung_Atas","Ujung_Bawah","Threeway","Fourway"]
    k_interval = 3
    intervals = {}
    df_disc = df.copy()

    # === DISKRITISASI ===
    for col in numeric_cols:
        min_val = int(df[col].min())
        max_val = int(df[col].max())
        width = round((max_val - min_val) / k_interval)

        b1 = min_val + width
        b2 = min_val + 2 * width

        intervals[col] = {
            "Rendah": f"{min_val} – {b1}",
            "Sedang": f"{b1+1} – {b2}",
            "Tinggi": f">= {b2+1}"
        }

        df_disc[col+"_cat"] = df[col].apply(
            lambda x: "Rendah" if x <= b1 else ("Sedang" if x <= b2 else "Tinggi")
        )

    df_diskrit = df_disc.copy()

    # ================= TRANSAKSI =================
    transactions = []
    for _, row in df_disc.iterrows():
        itemset = set()
        for c in numeric_cols:
            itemset.add(f"{c}={row[c+'_cat']}")
        transactions.append(itemset)

    n = len(transactions)

    # ================= APRIORI =================
    process_log = {}   # <-- semua proses disimpan di sini
    L_all = {}

    # ---------- C1 ----------
    C1 = Counter()
    for t in transactions:
        for item in t:
            C1[frozenset([item])] += 1

    process_log["C1"] = {list(k)[0]: v for k, v in C1.items()}

    # ---------- L1 ----------
    L1 = {}
    for it, cnt in C1.items():
        supp = cnt / n
        if supp >= min_support:
            L1[it] = cnt

    L_all[1] = {list(k)[0]: v for k, v in L1.items()}

    freq_itemsets = L1.copy()
    current_L = set(L1.keys())
    level = 2

    # ---------- Ck & Lk ----------
    while current_L:
        Ck = set()
        for a, b in itertools.combinations(current_L, 2):
            u = a | b
            if len(u) == level:
                Ck.add(u)

        Ck_count = Counter()
        for t in transactions:
            for c in Ck:
                if c.issubset(t):
                    Ck_count[c] += 1

        process_log[f"C{level}"] = {", ".join(list(k)): v for k, v in Ck_count.items()}

        Lk = {}
        for it, cnt in Ck_count.items():
            supp = cnt / n
            if supp >= min_support:
                Lk[it] = cnt

        if not Lk:
            break

        L_all[level] = {", ".join(list(k)): v for k, v in Lk.items()}

        for c in Lk:
            freq_itemsets[c] = Ck_count[c]

        current_L = set(Lk.keys())
        level += 1

    # ================= RULE GENERATION =================
    rules = []
    for itemset, cntAB in freq_itemsets.items():
        if len(itemset) < 2:
            continue

        for r in range(1, len(itemset)):
            for A in itertools.combinations(itemset, r):
                A = frozenset(A)
                B = itemset - A

                cntA = freq_itemsets.get(A, 0)
                cntB = freq_itemsets.get(B, 0)
                if cntA == 0 or cntB == 0:
                    continue

                supp = cntAB / n
                conf = cntAB / cntA
                lift = conf / (cntB / n)

                if conf >= min_confidence and lift >= min_lift:
                    rules.append({
                        "aturan": f"{', '.join(A)} → {', '.join(B)}",
                        "support": round(supp, 3),
                        "confidence": round(conf, 3),
                        "lift": round(lift, 3),
                        "k": len(itemset)
                    })

    return {
        "rules": rules,
        "intervals": intervals,
        "preprocessing": {
            "awal": df_awal.to_dict(),
            "clean": df_setelah_cleaning.to_dict(),
            "diskrit": df_diskrit.to_dict()
        },
        "process": process_log,
        "L_all": L_all,
        "total_transaksi": n
    }

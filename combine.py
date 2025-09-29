# combine.py
import os, glob, csv
import pandas as pd

DATA_DIR = "data"

def read_any(path):
    if path.lower().endswith(".xlsx"):
        return pd.read_excel(path)  # requiere: pip install openpyxl
    with open(path, "rb") as f:
        sample = f.read(8192)
    for enc in ["utf-8","utf-8-sig","latin1","ISO-8859-1","utf-16"]:
        try:
            head = sample.decode(enc); encoding_used = enc; break
        except: pass
    else:
        head = sample.decode("latin1", errors="ignore"); encoding_used = "latin1"
    header = head.splitlines()[0] if head else ""
    for cand in [";","\t","|",","]:
        if cand in header: sep = cand; break
    else:
        try:
            sep = csv.Sniffer().sniff(head).delimiter
        except Exception:
            sep = ","
    df = pd.read_csv(path, encoding=encoding_used, sep=sep)
    df.columns = [str(c).strip() for c in df.columns]
    return df

def main():
    files = sorted(glob.glob(os.path.join(DATA_DIR,"*.csv"))) + \
            sorted(glob.glob(os.path.join(DATA_DIR,"*.xlsx")))
    if not files:
        raise SystemExit("No hay archivos en data/. Copia allí los 8 meses.")
    frames = []
    for p in files:
        print("→", os.path.basename(p))
        frames.append(read_any(p))
    df = pd.concat(frames, ignore_index=True, sort=False)
    df.columns = [str(c).strip() for c in df.columns]
    out = os.path.join(DATA_DIR, "dataset.csv")
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print("✔ Combinado:", out, "filas=", len(df), "cols=", len(df.columns))

if __name__ == "__main__":
    main()

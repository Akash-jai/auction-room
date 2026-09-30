"""Parse a host-uploaded player list (.xlsx or .csv) into auction players.
Columns (any order, header names are flexible): Name, Rating, Position, Overseas."""
import csv, io, re
from players import base

MAX_PLAYERS, MAX_BYTES = 500, 1_000_000
TRUE = {"yes", "y", "true", "1", "overseas", "foreign", "foreigner", "foreign player", "o", "t", "abroad"}
FALSE = {"no", "n", "false", "0", "", "indian", "india", "domestic", "local", "f", "-", "none"}
INDIA = {"", "india", "indian", "ind", "in"}
SYN = (("name", ("player name", "player", "name")), ("rating", ("rating", "ovr", "overall", "rate", "score")),
       ("role", ("position", "role", "type", "skill", "category")),
       ("ov", ("overseas", "foreign", "nationality", "country")))


def _txt(v):
    if isinstance(v, float) and v.is_integer(): v = int(v)
    return "" if v is None else str(v).strip()


def _rows(filename, data):
    fn = (filename or "").lower()
    if fn.endswith((".xlsx", ".xlsm")):
        try:
            from openpyxl import load_workbook
            wb = load_workbook(io.BytesIO(data), read_only=True, data_only=True)
            return [list(r) for r in wb.worksheets[0].iter_rows(max_row=MAX_PLAYERS + 50, values_only=True)]
        except Exception:
            raise ValueError("Could not read that Excel file. Save it as .xlsx (or .csv) and try again.")
    if fn.endswith((".csv", ".txt")):
        try: text = data.decode("utf-8-sig")
        except UnicodeDecodeError: text = data.decode("latin-1")
        try: dialect = csv.Sniffer().sniff(text[:2000], delimiters=",;\t")
        except csv.Error: dialect = csv.excel
        return [r for r in csv.reader(io.StringIO(text), dialect)]
    raise ValueError("Please upload an .xlsx or .csv file (old .xls files: save as .xlsx first).")


def _cols(header):
    norm, used, cols = [_txt(c).lower() for c in header], set(), {}
    for field, keys in SYN:
        for key in keys:
            hit = next((i for i, h in enumerate(norm) if i not in used and (h == key or key in h)), None)
            if hit is not None:
                cols[field] = hit; used.add(hit); break
    return cols, norm


def _role(t):
    t = t.lower().strip()
    if re.search(r"keep|wicket|^(wk|w|wkt)$", t): return "W"
    if re.search(r"all[ \-_]?round|^(ar|a)$", t): return "A"
    if re.search(r"bowl|pace|spin|seam|^(l|fast)$", t): return "L"
    if re.search(r"bat|open|order|finisher|^b$", t): return "B"
    return None


def parse_upload(filename, data):
    """Returns (players, notes). Raises ValueError with a host-friendly message."""
    if len(data) > MAX_BYTES: raise ValueError("File is too big (max 1 MB).")
    rows = [r for r in _rows(filename, data) if any(_txt(c) for c in r)]
    if not rows: raise ValueError("The file is empty.")
    cols, norm = _cols(rows[0])
    start = 1
    if "name" not in cols or "rating" not in cols:
        try:  # no header row: assume Name, Rating, Position, Overseas order
            float(_txt(rows[0][1])); cols, start = {"name": 0, "rating": 1, "role": 2, "ov": 3}, 0
        except (ValueError, IndexError):
            raise ValueError("Couldn't find the columns. The first row should be: Name, Rating, Position, Overseas.")
    missing = [lbl for f, lbl in (("name", "Name"), ("rating", "Rating"), ("role", "Position"), ("ov", "Overseas")) if f not in cols]
    if missing: raise ValueError("Missing column(s): " + ", ".join(missing) + ". The first row should be: Name, Rating, Position, Overseas.")
    nat = any(k in (norm[cols["ov"]] if start else "") for k in ("nationality", "country"))
    out, errs, seen, dups = [], [], set(), 0
    for ri, r in enumerate(rows[start:], start=start + 1):
        g = lambda f: r[cols[f]] if cols[f] < len(r) else None
        name = " ".join(_txt(g("name")).split())[:40]
        try:
            if not name: raise ValueError("name is empty")
            try: rating = float(_txt(g("rating")).replace(",", "."))
            except ValueError: raise ValueError(f"rating '{_txt(g('rating'))}' is not a number")
            if rating <= 0: raise ValueError("rating must be above 0")
            k = _role(_txt(g("role")))
            if not k: raise ValueError(f"position '{_txt(g('role'))}' not recognised (use Batter, Bowler, All-rounder or Keeper)")
            t = _txt(g("ov")).lower()
            if nat: o = 0 if t in INDIA else 1
            elif t in TRUE: o = 1
            elif t in FALSE: o = 0
            else: raise ValueError(f"overseas '{t}' not recognised (use Yes or No)")
        except ValueError as e:
            errs.append(f"Row {ri}{' (' + name + ')' if name else ''}: {e}."); continue
        if name.lower() in seen: dups += 1; continue
        seen.add(name.lower()); out.append(dict(n=name, k=k, o=o, r=rating))
    if errs:
        raise ValueError("Fix these rows and upload again: " + " ".join(errs[:5]) + (f" …and {len(errs) - 5} more." if len(errs) > 5 else ""))
    if len(out) > MAX_PLAYERS: raise ValueError(f"Too many players ({len(out)}). The limit is {MAX_PLAYERS}.")
    if len(out) < 2: raise ValueError("Need at least 2 players.")
    notes = []
    lo, hi = min(p["r"] for p in out), max(p["r"] for p in out)
    if hi <= 10 or hi > 100 or lo < 30:  # keep pricing sensible: rescale odd rating scales to 60..95
        for p in out: p["r"] = 75 if hi == lo else 60 + (p["r"] - lo) / (hi - lo) * 35
        notes.append("Ratings were on an unusual scale, so they were rescaled to 60 to 95 for pricing.")
    for p in out:
        p["r"] = int(round(p["r"]))
        p["b"] = base(p["r"])
        if p["o"]: p["b"] = max(p["b"], .5)
    if dups: notes.append(f"{dups} duplicate name(s) skipped.")
    return out, notes

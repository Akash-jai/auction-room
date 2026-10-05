"""Tournament mode: simulate a full league + playoffs between the squads.
Depth matters: every match each player can be unavailable (injury, rest), and the next-best bench players step in."""
import math, random

P_OUT = .11     # chance a squad member is unavailable for any one match
SCALE = 60.0    # XI-power difference that makes a team roughly a 73% favourite


def power(xi):
    s = sum(p["r"] for p in xi)
    s += 10 if sum(1 for p in xi if p["k"] in "LA") >= 5 else 0
    s += 6 if sum(1 for p in xi if p["k"] in "BWA") >= 5 else 0
    s += 8 if any(p["k"] == "W" for p in xi) else 0
    return s


def simulate(teams, build_xi, who):
    """teams: objects with .i .n .c .sq .final (the locked XI). who(team) -> owner name or None."""
    st = {t.i: dict(t=t, w=0, l=0, ps=[], inj=0, full=power(t.final)) for t in teams}

    def lineup(t):
        names = {p["n"] for p in t.final}
        out = {p["n"] for p in t.sq if random.random() < P_OUT}
        xi = build_xi([p for p in t.sq if p["n"] not in out], [n for n in names if n not in out])
        return power(xi), bool(names & out)

    def play(a, b):
        pa, ia = lineup(a.t if hasattr(a, "t") else a)
        pb, ib = lineup(b.t if hasattr(b, "t") else b)
        for s, p, i in ((st[a.i], pa, ia), (st[b.i], pb, ib)):
            s["ps"].append(p); s["inj"] += i
        win = random.random() < 1 / (1 + math.exp(-(pa - pb) / SCALE))
        w, l = (a, b) if win else (b, a)
        st[w.i]["w"] += 1; st[l.i]["l"] += 1
        return w

    def make_table():
        out = []
        for t in sorted(teams, key=lambda t: (-st[t.i]["w"], -sum(st[t.i]["ps"]) / max(1, len(st[t.i]["ps"])))):
            s = st[t.i]; avg = sum(s["ps"]) / max(1, len(s["ps"]))
            out.append({"n": t.n, "c": t.c, "o": who(t), "p": s["w"] + s["l"], "w": s["w"], "l": s["l"], "pts": 2 * s["w"],
                        "full": round(s["full"]), "avg": round(avg), "depth": round(s["full"] - avg), "inj": s["inj"]})
        return out

    n, playoffs, table = len(teams), [], None
    if n == 2:  # best-of-7 series
        a, b, wins = teams[0], teams[1], {teams[0].i: 0, teams[1].i: 0}
        k = 0
        while max(wins.values()) < 4:
            k += 1; w = play(a, b); wins[w.i] += 1
            playoffs.append({"round": f"Game {k}", "a": a.n, "b": b.n, "w": w.n, "ac": a.c, "bc": b.c})
        table = make_table()
        champ = a if wins[a.i] == 4 else b
        runner = b if champ is a else a
        order = [champ, runner]
        fmt = "Best-of-7 series"
    else:
        legs = 2 if n <= 6 else 1
        for i in range(n):
            for j in range(i + 1, n):
                for _ in range(legs): play(teams[i], teams[j])
        table = make_table()  # league standings, before the playoffs
        rank = sorted(teams, key=lambda t: (-st[t.i]["w"], -sum(st[t.i]["ps"]) / max(1, len(st[t.i]["ps"]))))
        def match(rnd, a, b):
            w = play(a, b); playoffs.append({"round": rnd, "a": a.n, "b": b.n, "w": w.n, "ac": a.c, "bc": b.c}); return w
        if n == 3:
            champ = match("Final", rank[0], rank[1]); runner = rank[1] if champ is rank[0] else rank[0]
            order = [champ, runner] + [t for t in rank if t not in (champ, runner)]
            fmt = "Double round-robin + final"
        else:
            w1 = match("Semi-final 1 (1st v 4th)", rank[0], rank[3]); w2 = match("Semi-final 2 (2nd v 3rd)", rank[1], rank[2])
            champ = match("Final", w1, w2); runner = w2 if champ is w1 else w1
            order = [champ, runner] + [t for t in rank if t not in (champ, runner)]
            fmt = ("Double" if legs == 2 else "Single") + " round-robin + semi-finals + final"
    return {"format": fmt, "table": table, "playoffs": playoffs, "champion": champ.n, "runner": runner.n,
            "order": [t.n for t in order]}

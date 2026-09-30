"""Player pool: ~60 well-known names (made-up ratings) + generated fictional players."""
import random

REAL = ("Virat Kohli|B|0|93|2;Rohit Sharma|B|0|90|2;Jasprit Bumrah|L|0|95|2;Rishabh Pant|W|0|90|2;KL Rahul|W|0|88|2;"
"Hardik Pandya|A|0|90|2;Ravindra Jadeja|A|0|89|2;Shubman Gill|B|0|91|2;Suryakumar Yadav|B|0|90|2;Yashasvi Jaiswal|B|0|89|2;"
"Rashid Khan|L|1|92|2;Jos Buttler|W|1|90|2;Pat Cummins|A|1|88|2;Mitchell Starc|L|1|87|2;Travis Head|B|1|89|2;"
"Heinrich Klaasen|W|1|90|2;Andre Russell|A|1|85|2;Sunil Narine|A|1|86|2;Nicholas Pooran|W|1|86|2;Trent Boult|L|1|86|2;"
"Kagiso Rabada|L|1|87|2;Mohammed Shami|L|0|87|2;Mohammed Siraj|L|0|86|2;Yuzvendra Chahal|L|0|85|2;Kuldeep Yadav|L|0|86|2;"
"Arshdeep Singh|L|0|86|2;Ruturaj Gaikwad|B|0|87|2;Sanju Samson|W|0|87|2;Ishan Kishan|W|0|82|1.5;Shreyas Iyer|B|0|86|2;"
"Axar Patel|A|0|85|2;Washington Sundar|A|0|78|1;Tilak Varma|B|0|84|1;Rinku Singh|B|0|82|1;Abhishek Sharma|A|0|84|1;"
"Nitish Reddy|A|0|76|1;Shivam Dube|A|0|80|1;Riyan Parag|B|0|79|1;Dhruv Jurel|W|0|76|1;Ravi Bishnoi|L|0|78|1;"
"Varun Chakravarthy|L|0|84|1.5;T Natarajan|L|0|78|1;Harshit Rana|L|0|77|1;Mayank Yadav|L|0|76|1;Avesh Khan|L|0|78|1;"
"Prasidh Krishna|L|0|78|1;Bhuvneshwar Kumar|L|0|82|1.5;Deepak Chahar|L|0|78|1;Mitchell Marsh|A|1|84|2;David Warner|B|1|80|1.5;"
"Glenn Maxwell|A|1|82|2;Marcus Stoinis|A|1|80|1.5;Faf du Plessis|B|1|78|1;Quinton de Kock|W|1|84|2;Phil Salt|W|1|85|2;"
"Jofra Archer|L|1|85|2;Wanindu Hasaranga|A|1|80|1.5;Liam Livingstone|A|1|80|1.5;Sam Curran|A|1|82|2;Tim David|B|1|80|1;"
"Josh Hazlewood|L|1|85|2;Noor Ahmad|L|1|80|1;Devon Conway|B|1|79|1;Rachin Ravindra|A|1|80|1.5;Mustafizur Rahman|L|1|78|1;"
"Shimron Hetmyer|B|1|79|1")

IN_F = "Aarav Vihaan Arjun Rohan Karan Aditya Dev Ishaan Kabir Manav Nikhil Pranav Sahil Tanmay Yash Harsh Siddharth Ayush Mihir Kunal Naman Ritvik Shaurya Tushar Vikram Zaid Anmol Veer Lakshya Rudra Aman Jay Parth Sameer".split()
IN_L = "Mehta Kulkarni Nair Menon Sinha Verma Joshi Patil Rawat Thakur Bose Das Khanna Malhotra Pandey Rana Saxena Trivedi Ahuja Bedi Chopra Ghosh Hooda Kapoor Lal Mishra Naik Oberoi Pillai Qureshi Rao Sethi Tiwari Uppal Wadhwa".split()
OV_F = "Jack Oliver Liam Noah Ethan Mason Lachlan Callum Riley Tom Hamish Kyle Brandon Jayden Aiden Dylan Hugo Ryan Blake Cameron Marcus Tyler Xavier Zane".split()
OV_L = "Ashworth Blackwood Carver Dalton Everett Fenwick Gallagher Holloway Ingram Jensen Kirkwood Lambert Marlow Norris Prescott Quinn Redding Sutcliffe Thornton Vance Whitlock Yardley Sinclair Pemberton Hargreaves".split()


def build_pool():
    pool = []
    for s in REAL.split(";"):
        n, k, o, r, b = s.split("|")
        pool.append(dict(n=n, k=k, o=int(o), r=int(r), b=float(b)))
    used = {p["n"] for p in pool}

    def name(F, L):
        while True:
            n = f"{random.choice(F)} {random.choice(L)}"
            if n not in used:
                used.add(n)
                return n

    def gen(cnt, ov):
        for _ in range(cnt):
            k = random.choices("BLAW", [30, 35, 20, 15])[0]
            r = max(52, min(79, int(random.gauss(68 if ov else 66, 6))))
            b = 0.2 if r < 66 else 0.3 if r < 70 else 0.5 if r < 74 else 1.0
            if ov:
                b = max(b, 0.5)
            pool.append(dict(n=name(OV_F if ov else IN_F, OV_L if ov else IN_L), k=k, o=int(ov), r=r, b=b))

    gen(150, False)
    gen(30, True)
    return pool


def order(pool):
    """Marquee set first (shuffled), then role-based sets in random order, capped players before uncapped."""
    ps = sorted(pool, key=lambda p: -p["r"])
    marquee, rest = ps[:14], ps[14:]
    random.shuffle(marquee)
    out = marquee[:]
    for group in ([p for p in rest if p["r"] >= 70], [p for p in rest if p["r"] < 70]):
        sets = [[p for p in group if p["k"] == k] for k in "BLAW"]
        random.shuffle(sets)
        for s in sets:
            random.shuffle(s)
            out += s
    return out

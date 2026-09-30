"""Player pool: real IPL-era players. Ratings are made-up estimates, not official stats.
Edit freely: each entry is 'Name:rating' inside a block that sets role and nationality."""
import random

# (role, overseas, "Name:rating, Name:rating, ...")   roles: B batter, L bowler, A all-rounder, W keeper
BLOCKS = [
("W", 0, """Rishabh Pant:90, KL Rahul:88, Sanju Samson:87, Ishan Kishan:82, MS Dhoni:80, Jitesh Sharma:78, Dhruv Jurel:78,
 Prabhsimran Singh:76, Abishek Porel:76, KS Bharat:68, Robin Minz:68, Kumar Kushagra:68, Narayan Jagadeesan:68,
 Urvil Patel:68, Anuj Rawat:66, Vishnu Vinod:64, Aryan Juyal:60, Luvnith Sisodia:60, Upendra Yadav:58"""),
("B", 0, """Virat Kohli:92, Shubman Gill:91, Suryakumar Yadav:90, Yashasvi Jaiswal:90, Rohit Sharma:89, Ruturaj Gaikwad:87,
 Shreyas Iyer:87, Sai Sudharsan:86, Tilak Varma:85, Rinku Singh:84, Rajat Patidar:82, Riyan Parag:80, Devdutt Padikkal:79,
 Shashank Singh:78, Ajinkya Rahane:76, Nitish Rana:76, Vaibhav Suryavanshi:76, Karun Nair:74, Prithvi Shaw:74,
 Naman Dhir:74, Priyansh Arya:74, Angkrish Raghuvanshi:74, Ayush Badoni:74, Ayush Mhatre:74, Ashutosh Sharma:74,
 Mayank Agarwal:72, Nehal Wadhera:72, Sameer Rizvi:72, Sarfaraz Khan:72, Rahul Tripathi:72, Shahrukh Khan:72,
 Abdul Samad:72, Aniket Verma:72, Manish Pandey:68, Abhinav Manohar:68, Shubham Dubey:66, Musheer Khan:66,
 Atharva Taide:66, Mahipal Lomror:66, Anmolpreet Singh:64, Swastik Chikara:60, Sachin Baby:60"""),
("A", 0, """Hardik Pandya:90, Ravindra Jadeja:88, Axar Patel:86, Abhishek Sharma:86, Washington Sundar:80, Shivam Dube:80,
 Nitish Kumar Reddy:79, Venkatesh Iyer:78, Krunal Pandya:78, Rahul Tewatia:76, Ramandeep Singh:74, Shardul Thakur:74,
 Deepak Hooda:70, Shahbaz Ahmed:70, Harpreet Brar:70, Vipraj Nigam:68, Vijay Shankar:66, Tanush Kotian:66,
 Raj Angad Bawa:66, Nishant Sindhu:66, Arshad Khan:64, Anukul Roy:64, Jayant Yadav:64, Yudhvir Singh:64,
 Shams Mulani:62, Lalit Yadav:62, Suyash Prabhudessai:62, Krishnappa Gowtham:62, Manoj Bhandage:60, Aman Khan:60"""),
("L", 0, """Jasprit Bumrah:95, Mohammed Shami:87, Arshdeep Singh:87, Kuldeep Yadav:87, Mohammed Siraj:86, Varun Chakravarthy:86,
 Yuzvendra Chahal:84, Bhuvneshwar Kumar:82, Prasidh Krishna:82, Harshit Rana:80, Deepak Chahar:79, Ravi Bishnoi:79,
 Akash Deep:78, Mayank Yadav:78, Avesh Khan:78, T Natarajan:78, Khaleel Ahmed:78, Harshal Patel:78, Mukesh Kumar:76,
 Yash Dayal:76, Sai Kishore:74, Anshul Kamboj:74, Sandeep Sharma:72, Tushar Deshpande:72, Vijaykumar Vyshak:72,
 Vaibhav Arora:72, Suyash Sharma:72, Umran Malik:70, Rahul Chahar:70, Digvesh Rathi:70, Mohit Sharma:68,
 Simarjeet Singh:68, Yash Thakur:68, Ashwani Kumar:68, Navdeep Saini:68, Jaydev Unadkat:68, Rasikh Salam:68,
 Vignesh Puthur:68, Umesh Yadav:66, Ishant Sharma:66, Kartik Tyagi:66, Manimaran Siddharth:66, Kumar Kartikeya:66,
 Piyush Chawla:66, Mayank Markande:66, Akash Madhwal:66, Kuldeep Sen:66, Gurnoor Brar:66, Harsh Dubey:66,
 Shivam Mavi:66, Chetan Sakariya:64, Mukesh Choudhary:64, Karn Sharma:62, Sushant Mishra:62, Ajay Mandal:62,
 Arjun Tendulkar:60, Zeeshan Ansari:60"""),
("W", 1, """Heinrich Klaasen:91, Jos Buttler:90, Nicholas Pooran:87, Phil Salt:86, Quinton de Kock:84, Tristan Stubbs:80,
 Devon Conway:79, Jake Fraser-McGurk:78, Jonny Bairstow:78, Ryan Rickelton:78, Josh Inglis:78, Rahmanullah Gurbaz:76,
 Alex Carey:72, Tim Seifert:72, Matthew Wade:68, Shai Hope:68, Lhuan-dre Pretorius:68, Kusal Mendis:66, Sam Billings:66,
 Donovan Ferreira:66, Litton Das:66, Jordan Cox:62, Tom Banton:62"""),
("B", 1, """Travis Head:90, Aiden Markram:82, David Miller:82, Harry Brook:82, David Warner:80, Tim David:80, Glenn Phillips:80,
 Shimron Hetmyer:79, Faf du Plessis:78, Dewald Brevis:78, Steve Smith:76, Kane Williamson:76, Jacob Bethell:76,
 Rovman Powell:74, Finn Allen:74, Pathum Nissanka:74, Sherfane Rutherford:74, Ben Duckett:72, Rassie van der Dussen:72,
 Matthew Short:72, Dawid Malan:68, Evin Lewis:68, Kyle Mayers:68, Rilee Rossouw:66, Cooper Connolly:66,
 Brandon King:64, Tom Kohler-Cadmore:62, Tim Robinson:62"""),
("A", 1, """Pat Cummins:88, Sunil Narine:87, Andre Russell:85, Mitchell Marsh:84, Glenn Maxwell:82, Sam Curran:82, Ben Stokes:80,
 Marcus Stoinis:80, Wanindu Hasaranga:80, Liam Livingstone:80, Rachin Ravindra:80, Will Jacks:80, Marco Jansen:80,
 Cameron Green:80, Daryl Mitchell:78, Moeen Ali:76, Romario Shepherd:76, Jason Holder:74, Azmatullah Omarzai:74,
 Mitchell Santner:74, Mohammad Nabi:72, Sikandar Raza:70, Corbin Bosch:68, Mitchell Owen:68, Chris Woakes:68,
 Sean Abbott:68, Jimmy Neesham:66, Chris Jordan:66, Daniel Sams:66, Aaron Hardie:64"""),
("L", 1, """Rashid Khan:92, Mitchell Starc:87, Kagiso Rabada:87, Trent Boult:86, Jofra Archer:85, Josh Hazlewood:85,
 Noor Ahmad:80, Anrich Nortje:80, Matheesha Pathirana:80, Mustafizur Rahman:78, Lockie Ferguson:78, Nathan Ellis:76,
 Lungi Ngidi:76, Maheesh Theekshana:74, Fazalhaq Farooqi:74, Adam Zampa:74, Alzarri Joseph:74, Matt Henry:74,
 Naveen-ul-Haq:72, Gerald Coetzee:72, Adil Rashid:72, Shamar Joseph:72, Allah Ghazanfar:72, Kwena Maphaka:72,
 Spencer Johnson:70, Tim Southee:70, Mujeeb Ur Rahman:70, Xavier Bartlett:70, Jason Behrendorff:68, Akeal Hosein:68,
 Reece Topley:68, Nuwan Thushara:68, Kyle Jamieson:68, Blessing Muzarabani:68, Tymal Mills:66, Dilshan Madushanka:66,
 Sandeep Lamichhane:66, Jhye Richardson:66, Adam Milne:66, Ottniel Baartman:64, Luke Wood:62, Riley Meredith:62"""),
]

# ---- Retired / older IPL players (played in the league at some point) ----
BLOCKS += [
("W", 0, """Dinesh Karthik:76, Robin Uthappa:72, Wriddhiman Saha:68, Parthiv Patel:66, Naman Ojha:62, Aditya Tare:58, Manvinder Bisla:58"""),
("B", 0, """Sachin Tendulkar:86, Suresh Raina:84, Shikhar Dhawan:84, Virender Sehwag:84, Gautam Gambhir:80, Rahul Dravid:74,
 Ambati Rayudu:74, Murali Vijay:72, Sourav Ganguly:72, Kedar Jadhav:66, VVS Laxman:66, Mohammad Kaif:62,
 Saurabh Tiwary:62, Cheteshwar Pujara:58, Hanuma Vihari:58"""),
("A", 0, """Yuvraj Singh:82, Yusuf Pathan:76, Irfan Pathan:72, Stuart Binny:62, Rishi Dhawan:62, Shreyas Gopal:62"""),
("L", 0, """Ravichandran Ashwin:84, Zaheer Khan:80, Ashish Nehra:78, Harbhajan Singh:76, Amit Mishra:70, Munaf Patel:66,
 Praveen Kumar:66, Varun Aaron:66, RP Singh:62, S Sreesanth:62, Dhawal Kulkarni:62, Siddharth Kaul:62,
 Vinay Kumar:62, Pragyan Ojha:62, Pravin Tambe:60, Ashok Dinda:58"""),
("W", 1, """AB de Villiers:92, Adam Gilchrist:88, Brendon McCullum:84, Kumar Sangakkara:82, Luke Ronchi:66, Mark Boucher:62,
 Kamran Akmal:60"""),
("B", 1, """Chris Gayle:88, Kevin Pietersen:82, Michael Hussey:82, Matthew Hayden:80, Chris Lynn:78, Eoin Morgan:76,
 Mahela Jayawardene:74, Aaron Finch:74, Jason Roy:74, Ricky Ponting:72, Shaun Marsh:72, Herschelle Gibbs:72,
 Tillakaratne Dilshan:72, Alex Hales:72, Colin Munro:72, Martin Guptill:72, Joe Root:72, Hashim Amla:70,
 Graeme Smith:68, Lendl Simmons:68, Michael Clarke:68, Ross Taylor:66, Jesse Ryder:66, Marlon Samuels:62,
 Misbah-ul-Haq:62, Younis Khan:58"""),
("A", 1, """Kieron Pollard:82, Shane Watson:84, Jacques Kallis:80, Dwayne Bravo:82, Andrew Symonds:78, Chris Morris:78,
 Shakib Al Hasan:74, Albie Morkel:72, James Faulkner:72, Shahid Afridi:70, JP Duminy:70, Corey Anderson:70,
 Andrew Flintoff:70, Angelo Mathews:68, Dwayne Smith:66, Thisara Perera:66, Carlos Brathwaite:66, Ben Cutting:66,
 Daniel Vettori:66, David Wiese:66, Tom Curran:66, Abdul Razzaq:62, Darren Sammy:62, Scott Styris:62,
 Paul Collingwood:60, Ravi Bopara:60, Ryan McLaren:60, Robin Peterson:58"""),
("L", 1, """Lasith Malinga:90, Shane Warne:86, Dale Steyn:84, Morne Morkel:78, Imran Tahir:78, Mitchell Johnson:78,
 Brett Lee:74, Shoaib Akhtar:74, Muttiah Muralitharan:72, Nathan Coulter-Nile:72, Mitchell McClenaghan:72,
 Glenn McGrath:68, Shaun Pollock:66, Shane Bond:66, Umar Gul:66, Sohail Tanvir:62, Shaun Tait:66, Wayne Parnell:66,
 Dushmantha Chameera:66, Marchant de Lange:62, Liam Plunkett:62, Lonwabo Tsotsobe:60, Dirk Nannes:60,
 Steven Finn:58, Rusty Theron:58"""),
]


def base(r):
    return 2.0 if r >= 88 else 1.5 if r >= 84 else 1.0 if r >= 78 else .5 if r >= 74 else .3 if r >= 68 else .2


def build_pool():
    pool, seen = [], set()
    for k, o, txt in BLOCKS:
        for item in txt.replace("\n", " ").split(","):
            item = item.strip()
            if not item: continue
            n, r = item.rsplit(":", 1)
            if n in seen: continue
            seen.add(n)
            r = int(r)
            b = base(r)
            if o: b = max(b, .5)
            pool.append(dict(n=n, k=k, o=o, r=r, b=b))
    return pool


def order(pool, mq=14):
    """Marquee set first (shuffled), then role-based sets in random order, higher-rated before lower-rated."""
    ps = sorted(pool, key=lambda p: -p["r"])
    marquee, rest = ps[:mq], ps[mq:]
    random.shuffle(marquee)
    out = marquee[:]
    for group in ([p for p in rest if p["r"] >= 70], [p for p in rest if p["r"] < 70]):
        sets = [[p for p in group if p["k"] == k] for k in "BLAW"]
        random.shuffle(sets)
        for s in sets:
            random.shuffle(s)
            out += s
    return out


# Fan-favourite big names, in priority order. They always play (as many as fit: small auctions take the first ones).
FAMOUS = ["MS Dhoni", "Suresh Raina", "Dale Steyn", "Virender Sehwag", "Sachin Tendulkar", "Shane Warne", "Yuvraj Singh",
 "Gautam Gambhir", "Shikhar Dhawan", "Andre Russell", "Glenn Maxwell", "Sunil Narine", "Kieron Pollard", "Dwayne Bravo",
 "Shane Watson", "Ravichandran Ashwin", "Harbhajan Singh", "Yuzvendra Chahal", "Trent Boult", "Jofra Archer",
 "Josh Hazlewood", "Mohammed Siraj", "Bhuvneshwar Kumar", "Faf du Plessis", "David Warner", "Quinton de Kock",
 "Kane Williamson", "Steve Smith", "Mitchell Marsh", "Marcus Stoinis", "Liam Livingstone", "Sam Curran", "Ben Stokes",
 "Tilak Varma", "Rinku Singh", "Abhishek Sharma", "Axar Patel", "Varun Chakravarthy", "Rajat Patidar", "Phil Salt",
 "Mustafizur Rahman", "Wanindu Hasaranga", "Zaheer Khan", "Ashish Nehra", "Brendon McCullum", "Kumar Sangakkara",
 "Kevin Pietersen", "Michael Hussey", "Matthew Hayden", "Jacques Kallis", "Imran Tahir", "Dinesh Karthik",
 "Robin Uthappa", "Ambati Rayudu", "Rahul Dravid", "Sourav Ganguly", "Andrew Symonds", "Brett Lee", "Morne Morkel",
 "Washington Sundar", "Shivam Dube", "Deepak Chahar", "T Natarajan", "Prasidh Krishna", "Harshit Rana", "Noor Ahmad",
 "Matheesha Pathirana", "Tim David", "Shimron Hetmyer", "David Miller", "Aiden Markram", "Harry Brook",
 "Devdutt Padikkal", "Ishan Kishan", "Jitesh Sharma", "Dhruv Jurel", "Riyan Parag", "Mitchell Johnson",
 "Chris Morris", "Jason Roy", "Eoin Morgan", "Yusuf Pathan", "Irfan Pathan", "Ricky Ponting", "Glenn McGrath"]


def pick(pool, n, mq, max_ov=.38, cap=.6):
    """Top `mq` by rating + famous names always play (up to `cap` of the auction); the rest is a random sample
    with a realistic overseas share."""
    ps = sorted(pool, key=lambda p: -p["r"])
    g = ps[:mq]
    have = {p["n"] for p in g}
    by = {p["n"]: p for p in pool}
    for nm in FAMOUS:
        if len(g) >= int(cap * n): break
        if nm in by and nm not in have:
            g.append(by[nm]); have.add(nm)
    rest = [p for p in pool if p["n"] not in have]
    ov = [p for p in rest if p["o"]]
    ind = [p for p in rest if not p["o"]]
    room = n - len(g)
    want_ov = min(len(ov), max(0, round(max_ov * n) - sum(p["o"] for p in g)), room)
    take_in = min(len(ind), room - want_ov)
    take_ov = min(len(ov), room - take_in)
    return g + random.sample(ind, take_in) + random.sample(ov, take_ov)

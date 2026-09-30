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

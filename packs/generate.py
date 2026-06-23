# -*- coding: utf-8 -*-
"""
Erzeugt jede Woche frische Pakete (Rezepte, Tagesplan, Training).
- Rotation per ISO-Kalenderwoche -> jede Woche andere Auswahl.
- Liest optional packs/likes.json (von Andriys Favoriten-Export gepflegt):
  { "boost_meals":[...], "drop_meals":[...], "boost_ex":[...], "drop_ex":[...] }
  -> Gelikte werden bevorzugt, Disgelikte fliegen raus.
Läuft lokal und in GitHub Actions (.github/workflows/weekly-packs.yml).
"""
import json, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/"
WEEK = datetime.date.today().isocalendar()[1]   # 1..53 -> Rotations-Offset

def R(name, tags, ing, steps): return {"name": name, "tags": tags, "ing": ing, "steps": steps}
def o(name, a, b, kcal): return {"name": name, "a": a, "b": b, "kcal": kcal}
def EX(name, scheme, en, idn): return {"name": name, "scheme": scheme, "en": en,
                                       "img": BASE+idn+"/0.jpg", "img2": BASE+idn+"/1.jpg"}

# ---------------------------------------------------------------- Rezept-Bibliothek
ALL = [
 R("Skyr-Beeren-Bowl",["frühstück","süß","high-protein"],["Skyr 400 g","TK-Beeren 200 g","Nüsse 40 g","Honig 2 TL"],["Beeren auftauen.","Skyr in Schalen geben, Beeren darauf.","Mit Nüssen und Honig toppen."]),
 R("Rührei mit Tomaten & Käse",["frühstück","high-protein","schnell"],["Eier 5","Tomaten 2","Reibekäse 70 g","Butter","Salz, Pfeffer"],["Eier verquirlen, salzen.","In Butter stocken lassen.","Tomaten und Käse unterheben, kurz schmelzen lassen."]),
 R("Overnight Oats",["frühstück","meal-prep"],["Haferflocken 100 g","Skyr 350 g","Milch 100 ml","TK-Beeren 150 g","Honig 2 TL"],["Hafer, Skyr und Milch verrühren.","Über Nacht kühlen.","Mit Beeren und Honig toppen."]),
 R("Cottage-Cheese-Brot",["frühstück","high-protein","schnell"],["Vollkornbrot 3 Scheiben","Cottage Cheese 250 g","Gurke 1/2","Salz, Pfeffer"],["Brot mit Cottage Cheese bestreichen.","Gurke darauflegen.","Würzen."]),
 R("Griechischer Joghurt mit Nüssen & Honig",["frühstück","süß","high-protein"],["Griechischer Joghurt 400 g","Nüsse 40 g","Honig 2 TL"],["Joghurt in Schalen geben.","Nüsse und Honig darüber."]),
 R("Käse-Schinken-Omelett",["frühstück","high-protein","schnell"],["Eier 5","Reibekäse 70 g","Schinken 80 g","Butter"],["Eier verquirlen, salzen.","In Butter gießen, leicht stocken lassen.","Schinken und Käse auf eine Hälfte, zusammenklappen."]),
 R("Protein-Pancakes",["frühstück","high-protein","süß"],["Haferflocken 60 g","Eier 2","Topfen 150 g","Banane 1","Backpulver 1 TL"],["Alles zu einem Teig pürieren.","Kleine Pancakes mit wenig Öl goldbraun backen.","Mit Beeren oder Honig servieren."]),
 R("Vollkornbrot mit Frischkäse & Räucherlachs",["frühstück","high-protein","fisch"],["Vollkornbrot 3 Scheiben","Frischkäse 80 g","Räucherlachs 130 g","Zitrone","Dill"],["Brot mit Frischkäse bestreichen.","Räucherlachs darauflegen.","Mit Zitrone und Dill verfeinern."]),
 R("Hähnchen-Reis-Bowl",["mittag","high-protein","meal-prep"],["Hähnchenbrust 350 g","Reis 150 g","Brokkoli oder TK-Gemüse 250 g","Sojasauce 2 EL","Olivenöl"],["Reis kochen.","Hähnchen würfeln und braten.","Gemüse kurz mitbraten.","Mit Sojasauce und Reis anrichten."]),
 R("Großer griechischer Salat mit Hähnchen",["mittag","salat","high-protein"],["Hähnchenbrust 300 g","Gurke 1","Tomaten 3","Paprika 1","Rote Zwiebel 1/2","Oliven 60 g","Feta 120 g","Olivenöl 2 EL","Oregano"],["Hähnchen würzen und braten.","Gemüse schneiden, mit Oliven mischen.","Mit Öl und Oregano anmachen.","Feta und Hähnchen darüber geben."]),
 R("Putenwrap (Vollkorn)",["mittag","high-protein","schnell"],["Vollkorn-Wraps 3","Putenbrust 300 g","Blattsalat","Tomate 1","Joghurt-Dip 4 EL"],["Pute in Streifen braten.","Wraps mit Dip bestreichen.","Salat, Tomate und Pute einfüllen.","Einrollen und halbieren."]),
 R("Thunfisch-Couscous-Salat",["mittag","meal-prep","fisch"],["Couscous 150 g","Thunfisch 2 Dosen","Gurke 1/2","Tomaten 2","Zitrone 1/2","Olivenöl 2 EL","Petersilie"],["Couscous quellen lassen.","Thunfisch und Gemüse untermischen.","Mit Zitrone und Öl abschmecken."]),
 R("Chicken-Caesar-Salat",["mittag","salat","high-protein"],["Hähnchenbrust 300 g","Römersalat 1","Parmesan 40 g","Caesar-Dressing 4 EL","Vollkorn-Croutons"],["Hähnchen braten, in Streifen schneiden.","Salat mit Dressing mischen.","Mit Hähnchen, Parmesan und Croutons toppen."]),
 R("Bulgur-Salat mit Feta",["mittag","vegetarisch","meal-prep"],["Bulgur 150 g","Feta 120 g","Gurke 1","Tomaten 2","Petersilie","Zitrone","Olivenöl 2 EL"],["Bulgur kochen, abkühlen lassen.","Gurke, Tomaten, Petersilie untermischen.","Mit Zitrone und Öl abschmecken, Feta darüber."]),
 R("Putengeschnetzeltes mit Reis",["mittag","high-protein","schnell"],["Putenbrust 500 g","Reis 160 g","Champignons 200 g","Zwiebel 1","Crème fraîche 100 g","Senf 1 TL"],["Reis kochen.","Pute anbraten, herausnehmen.","Zwiebel + Champignons braten, mit Crème fraîche und Senf zur Sauce.","Pute zurück, mit Reis servieren."]),
 R("Apfel + Nüsse",["snack","schnell"],["Apfel 2","Nüsse 50 g"],["Apfel in Spalten schneiden.","Mit einer Handvoll Nüssen genießen."]),
 R("Käsewürfel + Gemüsesticks",["snack","schnell"],["Käse 100 g","Gurke, Paprika oder Karotte"],["Käse würfeln.","Gemüse in Sticks schneiden.","Zusammen snacken."]),
 R("Hüttenkäse mit Obst",["snack","high-protein","süß"],["Hüttenkäse 300 g","Obst (Beeren, Apfel oder Banane)"],["Hüttenkäse in Schalen geben.","Mit klein geschnittenem Obst toppen."]),
 R("Schoko-Quark-Mousse",["dessert","süß","high-protein"],["Topfen 300 g","Kakao 2 EL","Honig oder Ahornsirup 2 TL","Zartbitterschokolade 70 % 15 g"],["Topfen mit Kakao und Honig cremig rühren.","In Gläser füllen.","Mit gehobelter Zartbitterschokolade bestreuen."]),
 R("Bananen-Nicecream (Schoko)",["dessert","süß","schnell"],["Gefrorene Banane 2","Kakao 1 EL","Schuss Milch"],["Bananen in Scheiben einfrieren.","Mit Kakao und etwas Milch cremig pürieren.","Sofort wie Softeis genießen."]),
 R("Protein-Brownies",["dessert","süß","high-protein"],["Haferflocken 80 g","Kakao 4 EL","Banane 2","Ei 1","Zartbitterschokolade 70 % 30 g","Backpulver 1 TL"],["Hafer fein mahlen, alles verrühren.","Teig in kleine Form streichen.","Bei 180 °C 18 Min backen, in Stücke schneiden."]),
 R("Hafer-Bananen-Kekse",["dessert","süß","schnell"],["Reife Banane 2","Haferflocken 120 g","Zartbitterschokolade 70 % 30 g"],["Banane zerdrücken, mit Hafer und Schoko mischen.","Häufchen aufs Blech setzen.","Bei 180 °C 15 Min backen."]),
 R("Chia-Schoko-Pudding",["dessert","süß","meal-prep"],["Chiasamen 40 g","Milch 250 ml","Kakao 1 EL","Banane 1 oder Honig 1 TL"],["Chia, Milch, Kakao und Süße verrühren.","Über Nacht quellen lassen.","Mit Beeren toppen."]),
 R("Dattel-Kakao-Energy-Balls",["dessert","süß","meal-prep"],["Datteln 150 g","Haferflocken 80 g","Kakao 2 EL","Nüsse 40 g"],["Alles im Mixer zerkleinern.","Kleine Kugeln rollen.","Kalt stellen."]),
 R("Joghurt-Beeren-Schoko-Bark",["dessert","süß","high-protein"],["Skyr 300 g","TK-Beeren 80 g","Zartbitterschokolade 70 % 20 g","Honig 1 TL"],["Skyr mit Honig glatt rühren, auf Backpapier streichen.","Mit Beeren und Schoko-Splittern bestreuen.","Einfrieren, in Stücke brechen."]),
 R("Puten-Reis-Pfanne mit Paprika",["abend","schnell","high-protein","vorkochen"],["Putenbrust 800 g","Reis (roh) 320 g","Paprika 3","Zwiebel 2","Sojasauce 4 EL","Olivenöl 2 EL"],["Reis kochen.","Pute würfeln, scharf anbraten, herausnehmen.","Paprika und Zwiebel braten.","Pute zurück, mit Sojasauce ablöschen, mit Reis mischen.","Vorkochen: Hälfte für Tag 2 kühlen."]),
 R("Chili con Carne mit Reis",["abend","eisen","high-protein","vorkochen"],["Faschiertes (Rind) 600 g","Kidneybohnen 1 Dose (400 g)","Mais 1 Dose (300 g)","Stückige Tomaten 2 Dosen","Zwiebel 2","Knoblauch 2 Zehen","Reis (roh) 320 g","Kreuzkümmel 1 TL","Paprikapulver 1 TL"],["Zwiebel + Knoblauch anbraten, Faschiertes mitbraten.","Gewürze mitrösten.","Tomaten, Bohnen und Mais dazu, 20 Min köcheln.","Mit Reis servieren. Hälfte für Tag 2 kühlen."]),
 R("Nudelauflauf mit Pute & Käse",["abend","high-protein","käse","vorkochen"],["Putenbrust 600 g","Vollkornnudeln 400 g","Passata 700 g","Zwiebel 1","Knoblauch 2 Zehen","Reibekäse 200 g","Olivenöl 2 EL"],["Nudeln al dente kochen.","Pute mit Zwiebel + Knoblauch anbraten, Passata dazu.","Nudeln + Sauce in Auflaufform, Käse darüber.","Bei 200 °C 20 Min backen. Hälfte für Tag 2."]),
 R("Lachs mit Brokkoli & Zitrone",["abend","fisch","schnell","omega-3"],["Lachsfilet 2 Stück","Brokkoli (TK) 400 g","Zitrone 1","Olivenöl 1 EL"],["Ofen auf 200 °C.","Lachs mit Öl, Salz und Zitrone aufs Blech.","Brokkoli dazu, 15–18 Min backen."]),
 R("Hähnchen-Souvlaki mit griechischem Salat",["abend","high-protein","salat"],["Hähnchenbrust 400 g","Gurke 1","Tomaten 3","Rote Zwiebel 1/2","Oliven 50 g","Feta 100 g","Olivenöl 2 EL","Oregano 1 TL"],["Hähnchen marinieren und braten.","Salat schneiden, mit Oliven mischen.","Mit Öl beträufeln, Feta darüber.","Hähnchen dazu."]),
 R("Shakshuka mit Feta",["abend","vegetarisch","high-protein","eisen"],["Eier 4","Passata 400 g","Paprika 1","Zwiebel 1","Feta 100 g","Kreuzkümmel 1 TL"],["Zwiebel + Paprika anbraten.","Passata + Kreuzkümmel, 8 Min köcheln.","Eier hineingeben, stocken lassen.","Feta darüber."]),
 R("Garnelen-Knoblauch-Pfanne mit Couscous",["abend","fisch","schnell"],["Garnelen 300 g","Couscous 150 g","Knoblauch 2 Zehen","Zitrone 1/2","Olivenöl 2 EL","Petersilie"],["Couscous quellen lassen.","Garnelen mit Knoblauch braten.","Mit Zitrone und Petersilie auf Couscous servieren."]),
 R("Spaghetti Bolognese",["abend","high-protein","eisen"],["Vollkorn-Spaghetti 250 g","Faschiertes (Rind) 500 g","Passata 700 g","Zwiebel 1","Knoblauch 2 Zehen","Karotte 1","Parmesan 40 g"],["Zwiebel, Knoblauch, Karotte hacken und anbraten.","Faschiertes mitbraten.","Passata dazu, 15–20 Min köcheln.","Spaghetti kochen, mit Sauce und Parmesan servieren."]),
 R("Hähnchen-Fajitas",["abend","high-protein"],["Hähnchenbrust 500 g","Vollkorn-Tortillas 6","Paprika 2","Zwiebel 1","Fajita-Gewürz","Sauerrahm 100 g"],["Hähnchen mit Paprika und Zwiebel anbraten.","Mit Fajita-Gewürz würzen.","Tortillas füllen, mit Sauerrahm servieren."]),
 R("Schweinefilet mit Ofengemüse",["abend","high-protein"],["Schweinefilet 500 g","Kartoffeln 500 g","Paprika 2","Zucchini 1","Olivenöl 2 EL","Rosmarin"],["Ofen 200 °C. Gemüse und Kartoffeln 25 Min backen.","Schweinefilet anbraten, 12–15 Min mit in den Ofen.","In Scheiben mit Ofengemüse servieren."]),
 R("Gefüllte Paprika mit Faschiertem",["abend","high-protein","eisen"],["Paprika 4","Faschiertes (Rind) 500 g","Reis 100 g","Passata 400 g","Zwiebel 1","Reibekäse 80 g"],["Reis vorkochen. Paprika halbieren.","Faschiertes mit Zwiebel anbraten, mit Reis mischen.","Paprika füllen, Passata angießen, Käse darüber.","Bei 190 °C 30 Min backen."]),
]

# --------------------------------------------------------------- Tagesplan-Pools
BREAKFAST=[
 o("Skyr-Beeren-Bowl","150 g Skyr, 80 g Beeren, 15 g Nüsse","250 g Skyr, 120 g Beeren, 25 g Nüsse","~300 / ~470"),
 o("Rührei mit Tomaten & Käse","2 Eier, 30 g Käse, Tomate","3 Eier, 40 g Käse, 1 Scheibe Brot","~300 / ~480"),
 o("Overnight Oats","40 g Hafer, 150 g Skyr, Beeren","60 g Hafer, 200 g Skyr, Beeren, Nüsse","~300 / ~470"),
 o("Cottage-Cheese-Brot","1 Scheibe, 100 g Cottage Cheese","2 Scheiben, 150 g Cottage Cheese","~280 / ~470"),
 o("Griechischer Joghurt mit Nüssen & Honig","150 g, 15 g Nüsse, 1 TL Honig","250 g, 25 g Nüsse, 1 TL Honig","~290 / ~460"),
 o("Käse-Schinken-Omelett","2 Eier, 30 g Käse, Schinken","3 Eier, 40 g Käse, Schinken","~310 / ~480"),
 o("Protein-Pancakes","2 Stück","3–4 Stück","~320 / ~480"),
 o("Vollkornbrot mit Frischkäse & Räucherlachs","1 Scheibe, 50 g Lachs","2 Scheiben, 80 g Lachs","~300 / ~470"),
]
LUNCH=[
 o("Hähnchen-Reis-Bowl","350 g","500 g","~450 / ~650"),
 o("Großer griechischer Salat mit Hähnchen","120 g Hähnchen + Salat","180 g + Salat + Brot","~440 / ~650"),
 o("Putenwrap (Vollkorn)","1 Wrap","2 Wraps","~430 / ~660"),
 o("Thunfisch-Couscous-Salat","120 g Couscous","180 g Couscous","~450 / ~650"),
 o("Chicken-Caesar-Salat","120 g Hähnchen + Salat","180 g + Croutons","~440 / ~660"),
 o("Bulgur-Salat mit Feta","1 Schüssel","1,5 Schüsseln","~440 / ~650"),
 o("Putengeschnetzeltes mit Reis","300 g","450 g","~450 / ~660"),
 o("Reste vom Vortag","0,8 Portion (aufwärmen)","1,2 Portion (aufwärmen)","~450 / ~650"),
]
SNACK=[
 o("Schoko-Quark-Mousse","150 g (halbe Portion)","ganze Portion + Schoko","~210 / ~300"),
 o("Bananen-Nicecream (Schoko)","1 Banane","2 Bananen","~170 / ~290"),
 o("Protein-Brownies","1 Stück","2 Stück","~180 / ~320"),
 o("Hafer-Bananen-Kekse","2 Kekse","3–4 Kekse","~170 / ~300"),
 o("Chia-Schoko-Pudding","1 Glas","1 großes Glas","~200 / ~300"),
 o("Dattel-Kakao-Energy-Balls","2 Bällchen","3 Bällchen","~180 / ~300"),
 o("Joghurt-Beeren-Schoko-Bark","1 Portion","1,5 Portionen","~160 / ~280"),
 o("Hüttenkäse mit Obst","150 g + Obst","200 g + Obst","~180 / ~280"),
 o("Apfel + Nüsse","1 Apfel, 20 g Nüsse","1 Apfel, 30 g Nüsse","~190 / ~280"),
 o("Käsewürfel + Gemüsesticks","40 g Käse","60 g Käse","~180 / ~270"),
]
DINNER=[
 o("Puten-Reis-Pfanne mit Paprika","0,8 Portion","1,2 Portion","~500 / ~650"),
 o("Chili con Carne mit Reis","0,8 Portion","1,2 Portion","~520 / ~670"),
 o("Nudelauflauf mit Pute & Käse","0,8 Portion","1,2 Portion","~520 / ~680"),
 o("Lachs mit Brokkoli & Zitrone","1 Filet + Brokkoli","1,5 Filets + Reis","~480 / ~650"),
 o("Hähnchen-Souvlaki mit griechischem Salat","120 g + Salat","180 g + Reis","~480 / ~650"),
 o("Shakshuka mit Feta","2 Eier + Brot","3 Eier + Brot","~470 / ~640"),
 o("Garnelen-Knoblauch-Pfanne mit Couscous","120 g Couscous","180 g","~470 / ~650"),
 o("Spaghetti Bolognese","100 g Nudeln + Sauce","150 g + Sauce","~520 / ~680"),
 o("Hähnchen-Fajitas","2 Fajitas","3 Fajitas","~500 / ~680"),
 o("Schweinefilet mit Ofengemüse","120 g + Gemüse","180 g + Kartoffeln","~480 / ~660"),
 o("Gefüllte Paprika mit Faschiertem","1 Paprika","2 Paprika","~490 / ~670"),
]

# --------------------------------------------------------------- Training
GYM_A = [
 EX("Beinpresse","3 × 10–12","Leg Press (Machine)","Leg_Press"),
 EX("Brustpresse (Maschine)","3 × 10–12","Chest Press (Machine)","Leverage_Chest_Press"),
 EX("Latzug","3 × 10–12","Lat Pulldown","Wide-Grip_Lat_Pulldown"),
 EX("Schulterpresse (Maschine)","3 × 10","Shoulder Press (Machine)","Leverage_Shoulder_Press"),
 EX("Plank","3 × 20–30 s","Plank","Plank"),
]
GYM_B = [
 EX("Beinpresse","3 × 10–12","Leg Press (Machine)","Leg_Press"),
 EX("Beinbeuger (Maschine)","3 × 12","Leg Curl (Machine)","Lying_Leg_Curls"),
 EX("Rudern (Maschine)","3 × 10–12","Seated Row (Machine)","Seated_Cable_Rows"),
 EX("Bizeps-Curls (Maschine)","3 × 12","Machine Bicep Curl","Machine_Bicep_Curl"),
 EX("Trizeps-Drücken (Kabel)","3 × 12","Triceps Pushdown","Triceps_Pushdown"),
]
HOME_POOL = [
 EX("Crunches","3 × 15","Crunches","Crunches"),
 EX("Beinheben (liegend)","3 × 12","Lying Leg Raise","Flat_Bench_Lying_Leg_Raise"),
 EX("Plank","3 × 20–30 s","Plank","Plank"),
 EX("Mountain Climbers","3 × 20","Mountain Climbers","Mountain_Climbers"),
 EX("Bicycle-Crunch","3 × 20","Bicycle Crunch","Air_Bike"),
 EX("Russian Twist","3 × 20","Russian Twist","Russian_Twist"),
 EX("Seitlicher Plank","2 × 20 s je Seite","Side Plank","Side_Bridge"),
 EX("Käfer (Dead Bug)","3 × 10 je Seite","Dead Bug","Dead_Bug"),
 EX("Flutter Kicks","3 × 20","Flutter Kicks","Flutter_Kicks"),
 EX("Sit-Ups","3 × 12","Sit-Up","Sit-Up"),
]

DAYS=["Mo","Di","Mi","Do","Fr","Sa","So"]

def load_likes():
    p=os.path.join(HERE,"likes.json")
    if os.path.exists(p):
        try: return json.load(open(p,encoding="utf-8"))
        except Exception: return {}
    return {}

def apply_prefs(pool, boost, drop, keyname="name"):
    drop=set(x.lower() for x in drop)
    kept=[x for x in pool if x[keyname].lower() not in drop]
    boost=[x.lower() for x in boost]
    kept.sort(key=lambda x: 0 if x[keyname].lower() in boost else 1)
    return kept or pool   # nie ganz leer

def rot(pool, day_idx, k=4):
    n=len(pool); s=(WEEK*7 + day_idx*3) % n
    return [pool[(s+j)%n] for j in range(min(k,n))]

def main():
    likes=load_likes()
    bm=likes.get("boost_meals",[]); dm=likes.get("drop_meals",[])
    bx=likes.get("boost_ex",[]);    dx=likes.get("drop_ex",[])
    BF=apply_prefs(BREAKFAST,bm,dm); LU=apply_prefs(LUNCH,bm,dm)
    SN=apply_prefs(SNACK,bm,dm);     DI=apply_prefs(DINNER,bm,dm)
    home=apply_prefs(HOME_POOL,bx,dx)
    dayplan={}
    for i,d in enumerate(DAYS):
        dayplan[d]={"F":rot(BF,i),"M":rot(LU,i),"S":rot(SN,i),"A":rot(DI,i)}
    # Home-Bauch rotiert wöchentlich aus dem Pool; Gym bleibt stabil (Progression)
    hs=(WEEK*4)%len(home)
    homeA=[home[(hs+j)%len(home)] for j in range(4)]
    homeB=[home[(hs+4+j)%len(home)] for j in range(4)]
    training={"program":{
        "A":{"label":"Gym 1 · Ganzkörper","ex":GYM_A},
        "B":{"label":"Gym 2 · Ganzkörper","ex":GYM_B},
        "C":{"label":"Zuhause · Bauch A","ex":homeA},
        "D":{"label":"Zuhause · Bauch B","ex":homeB},
    }}
    # Coverage-Sicherung
    have=set(r["name"].lower() for r in ALL)
    names=set(opt["name"] for d in DAYS for sl in ("F","M","S","A") for opt in dayplan[d][sl])
    missing=[n for n in names if n!="Reste vom Vortag" and n.lower() not in have]
    assert not missing, "Gericht ohne Rezept: "+repr(missing)
    json.dump({"replaceMeals":True,"meals":ALL}, open(os.path.join(HERE,"rezepte.json"),"w",encoding="utf-8"), ensure_ascii=False)
    json.dump({"dayplan":dayplan}, open(os.path.join(HERE,"wochenplan.json"),"w",encoding="utf-8"), ensure_ascii=False)
    json.dump({"training":training}, open(os.path.join(HERE,"training.json"),"w",encoding="utf-8"), ensure_ascii=False)
    print("KW",WEEK,"- Pakete erzeugt. Rezepte:",len(ALL),"Home-Bauch A:",[e["name"] for e in homeA],"B:",[e["name"] for e in homeB])

if __name__=="__main__":
    main()

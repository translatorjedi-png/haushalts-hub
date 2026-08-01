# -*- coding: utf-8 -*-
"""
Erzeugt jede Woche frische Pakete (Rezepte, Tagesplan, Training).

Leitplanken (Stand August 2026, nach Andriys Rueckmeldung):
  * Energie vorne: Fruehstueck und Mittag sind die grossen Mahlzeiten,
    der Abend ist leicht und kohlenhydratarm.
      Anna   ~1450 kcal:  F 420 · M 480 · S 180 · A 370
      Andriy ~2050 kcal:  F 620 · M 700 · S 280 · A 450
  * Tagesenergie fuer Anna: Eisen + Vitamin C zusammen, Folsaeure, B12,
    Magnesium, Selen; Vollkorn statt Weissmehl, Protein in JEDER Mahlzeit.
    Alles auf Lebensmittel-Ebene - keine Medizin, keine Dosierungen.
  * Vielfalt: grosse Pools, Rotation per ISO-Kalenderwoche.
  * Training: pro Tag Muskelgruppen-SLOTS mit Alternativen -> die App
    rotiert selbst bei "Trainiert" durch; gelikte Uebungen bleiben stehen.

Liest optional packs/likes.json (aus Andriys Favoriten-Export):
  { "boost_meals":[...], "drop_meals":[...], "boost_ex":[...], "drop_ex":[...] }
Laeuft lokal und in GitHub Actions (.github/workflows/weekly-packs.yml).
"""
import json, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/"
WEEK = datetime.date.today().isocalendar()[1]   # 1..53 -> Rotations-Offset

def R(name, tags, ing, steps): return {"name": name, "tags": tags, "ing": ing, "steps": steps}
def o(name, a, b, kcal): return {"name": name, "a": a, "b": b, "kcal": kcal}
def EX(name, scheme, en, idn, lvl=1):
    """lvl 1 = Anfaenger: gefuehrte Maschine, Kabelzug oder einfache
    Koerpergewichtsuebung. lvl 2 = freie Gewichte / mehr Technik.
    Anna trainiert seit Mai 2026 -> die App zeigt standardmaessig nur lvl 1."""
    return {"name": name, "scheme": scheme, "en": en, "lvl": lvl,
            "img": BASE+idn+"/0.jpg", "img2": BASE+idn+"/1.jpg"}

VORKOCH = ("Fuer 2 Tage: einfach an beiden Tagen im Tagesplan waehlen - dann kauft "
           "die App automatisch die doppelte Menge ein. Doppelte Portion kochen, "
           "Haelfte kuehl stellen.")

# ================================================================= REZEPTE
# Alle Mengen = 1 Tag = 2 Portionen (Anna + Andriy zusammen).
# Zutaten-Format "Name Menge Einheit" -> die Einkaufsliste kann summieren.

FRUEHSTUECK = [
 R("Rührei mit Tomaten & Käse",["frühstück","high-protein","schnell"],
   ["Eier 5","Tomaten 2","Reibekäse 70 g","Vollkornbrot 3 Scheiben","Butter 15 g","Salz, Pfeffer"],
   ["Eier verquirlen, salzen.","In Butter langsam stocken lassen.","Tomatenwürfel und Käse unterheben.","Mit Vollkornbrot servieren - das Brot gehört dazu, es ist die Energie für den Vormittag."]),
 R("Käse-Schinken-Omelett mit Vollkornbrot",["frühstück","high-protein","schnell"],
   ["Eier 5","Reibekäse 70 g","Schinken 100 g","Vollkornbrot 3 Scheiben","Butter 15 g","Schnittlauch"],
   ["Eier verquirlen, salzen.","In Butter gießen, leicht stocken lassen.","Schinken und Käse auf eine Hälfte, zusammenklappen.","Mit Brot und Schnittlauch servieren."]),
 R("Spiegeleier auf Vollkorntoast mit Spinat",["frühstück","high-protein","eisen","energie"],
   ["Eier 4","Blattspinat 200 g","Vollkornbrot 4 Scheiben","Knoblauch 1 Zehe","Olivenöl 1 EL","Zitrone 1/2","Cherrytomaten 150 g"],
   ["Spinat mit Knoblauch in Öl zusammenfallen lassen, mit Zitrone abschmecken.","Eier als Spiegeleier braten.","Brot toasten, Spinat darauf, Ei obendrauf.","Cherrytomaten dazu - das Vitamin C hilft, das Eisen aus Spinat und Ei aufzunehmen."]),
 R("Haferbrei mit Apfel, Zimt & Nüssen",["frühstück","energie","meal-prep"],
   ["Haferflocken 120 g","Milch 400 ml","Apfel 2","Walnüsse 40 g","Zimt 1 TL","Honig 2 TL","Salz 1 Prise"],
   ["Hafer mit Milch und einer Prise Salz aufkochen, 5 Min quellen lassen.","Apfel würfeln, mit Zimt unterrühren.","Mit Nüssen und Honig toppen.","Hafer liefert langsame Kohlenhydrate + Magnesium - hält bis Mittag satt."]),
 R("Overnight Oats mit Beeren & Nüssen",["frühstück","meal-prep","energie"],
   ["Haferflocken 120 g","Skyr 350 g","Milch 150 ml","TK-Beeren 200 g","Nüsse 40 g","Honig 2 TL"],
   ["Hafer, Skyr und Milch verrühren.","Über Nacht kühlen.","Morgens mit Beeren, Nüssen und Honig toppen.", "Am Vorabend gleich die doppelte Menge ansetzen - dann steht das Frühstück auch morgen fertig da."]),
 R("Bircher Müsli mit Apfel & Nüssen",["frühstück","meal-prep","energie"],
   ["Haferflocken 110 g","Griechischer Joghurt 300 g","Milch 150 ml","Apfel 2","Haselnüsse 40 g","Rosinen 30 g","Zitrone 1/2"],
   ["Hafer mit Milch und Joghurt anrühren, über Nacht kühlen.","Apfel grob raspeln, mit Zitrone mischen, unterheben.","Mit Nüssen und Rosinen bestreuen."]),
 R("Protein-Pancakes mit Beeren",["frühstück","high-protein","süß"],
   ["Haferflocken 90 g","Eier 3","Topfen 200 g","Banane 1","Backpulver 1 TL","TK-Beeren 150 g","Öl 1 EL"],
   ["Alles außer Beeren zu einem Teig pürieren.","Kleine Pancakes mit wenig Öl goldbraun backen.","Beeren kurz erwärmen und darüber geben."]),
 R("Vollkornbrot mit Frischkäse & Räucherlachs",["frühstück","high-protein","fisch","omega-3"],
   ["Vollkornbrot 4 Scheiben","Frischkäse 100 g","Räucherlachs 150 g","Gurke 1/2","Zitrone 1/2","Dill"],
   ["Brot mit Frischkäse bestreichen.","Räucherlachs und Gurkenscheiben darauflegen.","Mit Zitrone und Dill verfeinern."]),
 R("Cottage-Cheese-Brot mit Ei",["frühstück","high-protein","schnell"],
   ["Vollkornbrot 3 Scheiben","Cottage Cheese 250 g","Eier 2","Gurke 1/2","Radieschen 5","Salz, Pfeffer"],
   ["Eier 7 Min kochen, schrecken, schälen.","Brot mit Cottage Cheese bestreichen.","Ei, Gurke und Radieschen darauf, würzen."]),
 R("Skyr-Beeren-Bowl mit Haferflocken",["frühstück","high-protein","süß"],
   ["Skyr 400 g","TK-Beeren 200 g","Haferflocken 60 g","Nüsse 40 g","Honig 2 TL"],
   ["Beeren auftauen lassen.","Skyr in Schalen geben, Hafer untermischen.","Beeren, Nüsse und Honig darüber."]),
 R("Griechischer Joghurt mit Nüssen, Honig & Hafer",["frühstück","süß","high-protein"],
   ["Griechischer Joghurt 400 g","Nüsse 50 g","Haferflocken 50 g","Honig 2 TL","Banane 1"],
   ["Joghurt in Schalen geben.","Hafer, Nüsse, Bananenscheiben und Honig darüber."]),
 R("Frühstücks-Burrito mit Ei & Bohnen",["frühstück","high-protein","eisen","energie"],
   ["Vollkorn-Tortillas 4","Eier 4","Kidneybohnen 1 Dose (400 g)","Reibekäse 60 g","Paprika 1","Zwiebel 1","Paprikapulver 1 TL"],
   ["Zwiebel und Paprika anbraten, Bohnen abspülen und dazu, würzen.","Eier verquirlen, dazugeben und stocken lassen.","Auf die Tortillas geben, Käse darüber, einrollen.","Bohnen + Paprika = Eisen mit Vitamin C, ein guter Start in einen langen Tag."]),
 R("Avocado-Ei-Brot",["frühstück","energie","schnell"],
   ["Vollkornbrot 4 Scheiben","Avocado 2","Eier 4","Zitrone 1/2","Cherrytomaten 150 g","Chiliflocken","Salz, Pfeffer"],
   ["Avocado mit Zitrone, Salz und Pfeffer zerdrücken.","Eier als Spiegeleier braten.","Brot toasten, Avocado darauf streichen, Ei obendrauf.","Tomaten und Chiliflocken dazu."]),
 R("Quinoa-Porridge mit Beeren",["frühstück","energie","eisen","meal-prep"],
   ["Quinoa 120 g","Milch 400 ml","TK-Beeren 200 g","Mandeln 40 g","Honig 2 TL","Zimt 1 TL"],
   ["Quinoa gut abspülen, mit Milch 15 Min weich köcheln.","Zimt unterrühren.","Mit Beeren, Mandeln und Honig servieren.","Quinoa bringt Eisen und Magnesium - die Beeren liefern das Vitamin C dazu."]),
 R("Pilz-Omelett mit Vollkornbrot",["frühstück","high-protein","schnell"],
   ["Eier 5","Champignons 200 g","Reibekäse 60 g","Vollkornbrot 3 Scheiben","Petersilie","Butter 15 g"],
   ["Champignons in Butter kräftig anbraten.","Eier darüber gießen, stocken lassen.","Käse darüber schmelzen, Petersilie und Brot dazu."]),
 R("Topfencreme mit Kürbiskernen & Vollkornbrot",["frühstück","high-protein","energie"],
   ["Topfen 350 g","Kürbiskerne 40 g","Vollkornbrot 3 Scheiben","Honig 2 TL","Banane 1","Zimt 1 TL"],
   ["Topfen mit Honig und Zimt cremig rühren.","Bananenscheiben unterheben.","Mit Kürbiskernen bestreuen, Brot dazu.","Kürbiskerne liefern Magnesium und Eisen."]),
]

MITTAG = [
 R("Hähnchen-Reis-Bowl",["mittag","high-protein","meal-prep"],
   ["Hähnchenbrust 400 g","Reis 180 g","Brokkoli 300 g","Karotte 1","Sojasauce 2 EL","Olivenöl 1 EL","Sesam 1 EL"],
   ["Reis kochen.","Hähnchen würfeln und scharf anbraten.","Brokkoli und Karotte kurz mitbraten.","Mit Sojasauce ablöschen, über den Reis geben, Sesam darüber.", VORKOCH]),
 R("Putengeschnetzeltes mit Reis",["mittag","high-protein","schnell"],
   ["Putenbrust 450 g","Reis 180 g","Champignons 250 g","Zwiebel 1","Crème fraîche 100 g","Senf 1 TL","Petersilie"],
   ["Reis kochen.","Pute anbraten, herausnehmen.","Zwiebel und Champignons braten, mit Crème fraîche und Senf zur Sauce rühren.","Pute zurück in die Pfanne, mit Reis servieren.", VORKOCH]),
 R("Spaghetti Bolognese",["mittag","high-protein","eisen","energie","vorkochen"],
   ["Vollkorn-Spaghetti 220 g","Faschiertes Rind 400 g","Passata 700 g","Zwiebel 1","Knoblauch 2 Zehen","Karotte 1","Sellerie 1 Stange","Parmesan 40 g","Olivenöl 1 EL"],
   ["Zwiebel, Knoblauch, Karotte und Sellerie fein hacken und anbraten.","Faschiertes mitbraten, bis es Farbe hat.","Passata dazu, 20-25 Min köcheln.","Spaghetti kochen, mit Sauce und Parmesan servieren.","Rindfleisch + Tomate = Eisen mit Vitamin C. Mittags gegessen trägt es durch den Nachmittag.", VORKOCH]),
 R("Nudelauflauf mit Pute & Käse",["mittag","high-protein","käse","vorkochen"],
   ["Putenbrust 350 g","Vollkornnudeln 220 g","Passata 400 g","Zwiebel 1","Knoblauch 1 Zehe","Reibekäse 100 g","Brokkoli 200 g","Olivenöl 1 EL"],
   ["Nudeln al dente kochen, Brokkoli die letzten 3 Min mitkochen.","Pute mit Zwiebel und Knoblauch anbraten, Passata dazu.","Alles in eine Auflaufform, Käse darüber.","Bei 200 °C 20 Min backen.", VORKOCH]),
 R("Chili con Carne mit Reis",["mittag","eisen","high-protein","energie","vorkochen"],
   ["Faschiertes Rind 350 g","Kidneybohnen 1 Dose (400 g)","Mais 1 Dose (150 g)","Stückige Tomaten 1 Dose (400 g)","Zwiebel 1","Knoblauch 2 Zehen","Paprika 1","Reis 170 g","Kreuzkümmel 1 TL","Paprikapulver 1 TL"],
   ["Zwiebel und Knoblauch anbraten, Faschiertes mitbraten.","Gewürze kurz mitrösten.","Tomaten, Bohnen, Mais und Paprika dazu, 20 Min köcheln.","Mit Reis servieren.","Doppelter Eisen-Treffer: Rind und Bohnen, dazu Paprika für das Vitamin C.", VORKOCH]),
 R("Linsen-Bolognese mit Vollkornnudeln",["mittag","vegetarisch","eisen","energie","vorkochen"],
   ["Rote Linsen 200 g","Vollkornnudeln 220 g","Passata 700 g","Zwiebel 1","Knoblauch 2 Zehen","Karotte 2","Parmesan 40 g","Olivenöl 1 EL","Oregano 1 TL"],
   ["Zwiebel, Knoblauch und Karotte anbraten.","Linsen und Passata dazu, 20 Min köcheln, bis die Linsen weich sind.","Nudeln kochen und untermischen.","Mit Parmesan servieren.","Linsen liefern Eisen und Folsäure, die Tomaten das Vitamin C dazu.", VORKOCH]),
 R("Putenwrap (Vollkorn)",["mittag","high-protein","schnell"],
   ["Vollkorn-Wraps 4","Putenbrust 350 g","Blattsalat 1","Tomaten 2","Paprika 1","Joghurt-Dip 5 EL","Reibekäse 50 g"],
   ["Pute in Streifen scharf anbraten.","Wraps mit Dip bestreichen.","Salat, Tomate, Paprika, Käse und Pute einfüllen.","Einrollen und halbieren."]),
 R("Thunfisch-Couscous-Salat",["mittag","meal-prep","fisch","schnell"],
   ["Couscous 180 g","Thunfisch 2 Dosen","Gurke 1","Tomaten 3","Paprika 1","Zitrone 1","Olivenöl 2 EL","Petersilie","Kichererbsen 1 Dose (400 g)"],
   ["Couscous mit kochendem Wasser übergießen und quellen lassen.","Thunfisch, Kichererbsen und Gemüse untermischen.","Mit Zitrone, Öl, Salz und Pfeffer abschmecken.", VORKOCH]),
 R("Großer griechischer Salat mit Hähnchen",["mittag","salat","high-protein"],
   ["Hähnchenbrust 350 g","Gurke 1","Tomaten 4","Paprika 1","Rote Zwiebel 1","Oliven 70 g","Feta 150 g","Olivenöl 3 EL","Oregano 1 TL","Vollkornbrot 2 Scheiben"],
   ["Hähnchen würzen und braten.","Gemüse grob schneiden, mit Oliven mischen.","Mit Öl und Oregano anmachen, Feta darüber bröseln.","Hähnchen und Brot dazu."]),
 R("Chicken-Caesar-Salat",["mittag","salat","high-protein"],
   ["Hähnchenbrust 350 g","Römersalat 2","Parmesan 50 g","Caesar-Dressing 5 EL","Vollkornbrot 3 Scheiben","Eier 2"],
   ["Hähnchen braten und in Streifen schneiden.","Brot würfeln und in der Pfanne rösten - fertige Croutons.","Eier 8 Min kochen und halbieren.","Salat mit Dressing mischen, alles darauf verteilen, Parmesan darüber."]),
 R("Bulgur-Salat mit Feta & Kichererbsen",["mittag","vegetarisch","meal-prep","eisen"],
   ["Bulgur 180 g","Kichererbsen 1 Dose (400 g)","Feta 150 g","Gurke 1","Tomaten 3","Petersilie","Zitrone 1","Olivenöl 3 EL"],
   ["Bulgur kochen und abkühlen lassen.","Kichererbsen abspülen, mit Gurke, Tomaten und Petersilie untermischen.","Mit Zitrone und Öl abschmecken, Feta darüber.", VORKOCH]),
 R("Rindfleisch-Reis-Pfanne mit Paprika",["mittag","eisen","high-protein","energie","schilddrüse"],
   ["Rindfleisch Streifen 350 g","Reis 180 g","Paprika 2","Zwiebel 1","Knoblauch 2 Zehen","Sojasauce 2 EL","Zitrone 1/2","Olivenöl 1 EL"],
   ["Reis kochen.","Rindfleisch scharf anbraten, herausnehmen.","Paprika und Zwiebel braten, Fleisch zurück.","Mit Sojasauce und einem Spritzer Zitrone abschmecken, mit Reis servieren.", VORKOCH]),
 R("Lachs-Kartoffel-Pfanne mit Spinat",["mittag","fisch","omega-3","eisen","energie"],
   ["Lachsfilet 350 g","Kartoffeln 500 g","Blattspinat 250 g","Knoblauch 2 Zehen","Zitrone 1","Olivenöl 2 EL","Dill"],
   ["Kartoffeln würfeln und 12 Min kochen, dann in der Pfanne knusprig braten.","Lachs würfeln und 4 Min mitbraten.","Spinat mit Knoblauch zusammenfallen lassen.","Mit Zitrone und Dill abschmecken."]),
 R("Hähnchen-Nudel-Pfanne mit Brokkoli",["mittag","high-protein","schnell"],
   ["Hähnchenbrust 400 g","Vollkornnudeln 220 g","Brokkoli 350 g","Knoblauch 2 Zehen","Frischkäse 100 g","Parmesan 40 g","Olivenöl 1 EL"],
   ["Nudeln kochen, Brokkoli die letzten 4 Min mitkochen.","Hähnchen in Streifen anbraten, Knoblauch dazu.","Frischkäse mit etwas Nudelwasser zur Sauce rühren.","Alles mischen, Parmesan darüber.", VORKOCH]),
 R("Quinoa-Bowl mit Hähnchen & Avocado",["mittag","energie","high-protein","eisen"],
   ["Quinoa 180 g","Hähnchenbrust 350 g","Avocado 1","Cherrytomaten 250 g","Gurke 1","Zitrone 1","Olivenöl 2 EL","Kürbiskerne 30 g"],
   ["Quinoa abspülen und 15 Min kochen.","Hähnchen würzen und braten.","Gemüse schneiden, alles in Schalen anrichten.","Mit Zitrone und Öl abschmecken, Kürbiskerne darüber."]),
 R("Süßkartoffel-Hähnchen-Blech mit Feta",["mittag","high-protein","energie"],
   ["Hähnchenbrust 400 g","Süßkartoffeln 600 g","Paprika 2","Rote Zwiebel 1","Feta 120 g","Olivenöl 2 EL","Paprikapulver 1 TL","Rosmarin"],
   ["Ofen auf 200 °C.","Süßkartoffeln und Gemüse würfeln, mit Öl und Gewürzen mischen, 20 Min backen.","Hähnchen dazulegen, weitere 15 Min backen.","Feta darüber bröseln.", VORKOCH]),
 R("Kichererbsen-Curry mit Reis",["mittag","vegetarisch","eisen","energie","vorkochen"],
   ["Kichererbsen 2 Dosen (800 g)","Reis 180 g","Kokosmilch 400 ml","Passata 200 g","Zwiebel 1","Knoblauch 2 Zehen","Currypulver 2 TL","Spinat 150 g","Zitrone 1/2"],
   ["Reis kochen.","Zwiebel und Knoblauch anbraten, Curry mitrösten.","Kichererbsen, Passata und Kokosmilch dazu, 15 Min köcheln.","Spinat unterheben, mit Zitrone abschmecken.", VORKOCH]),
 R("Hähnchen-Fajitas (Vollkorn)",["mittag","high-protein","schnell"],
   ["Hähnchenbrust 450 g","Vollkorn-Tortillas 6","Paprika 3","Zwiebel 1","Fajita-Gewürz 2 TL","Sauerrahm 100 g","Reibekäse 60 g","Limette 1"],
   ["Hähnchen in Streifen mit Paprika und Zwiebel anbraten.","Mit Fajita-Gewürz würzen, Limette darüber.","Tortillas füllen, Sauerrahm und Käse dazu."]),
 R("Gefüllte Paprika mit Faschiertem & Reis",["mittag","high-protein","eisen","vorkochen"],
   ["Paprika 4","Faschiertes Rind 450 g","Reis 120 g","Passata 400 g","Zwiebel 1","Knoblauch 1 Zehe","Reibekäse 80 g","Petersilie"],
   ["Reis vorkochen, Paprika halbieren und entkernen.","Faschiertes mit Zwiebel und Knoblauch anbraten, mit Reis mischen.","Paprika füllen, Passata angießen, Käse darüber.","Bei 190 °C 30 Min backen.", VORKOCH]),
 R("Reste vom Vortag",["mittag","schnell","meal-prep"],
   [],
   ["Die Portion vom Vortag aufwärmen.","Wenn wenig übrig ist: ein Ei, eine Handvoll Käse oder etwas Salat dazu."]),
]

SNACK = [
 R("Schoko-Quark-Mousse",["dessert","süß","high-protein"],
   ["Topfen 300 g","Kakao 2 EL","Honig 2 TL","Zartbitterschokolade 15 g (70 %)","Milch 3 EL"],
   ["Topfen mit Kakao, Milch und Honig cremig rühren.","In Gläser füllen.","Mit gehobelter Zartbitterschokolade bestreuen."]),
 R("Bananen-Nicecream (Schoko)",["dessert","süß","schnell"],
   ["Gefrorene Banane 3","Kakao 1 EL","Milch 4 EL","Erdnussmus 1 TL"],
   ["Bananen in Scheiben einfrieren (am Vortag).","Mit Kakao, Erdnussmus und etwas Milch cremig pürieren.","Sofort wie Softeis essen."]),
 R("Protein-Brownies",["dessert","süß","high-protein","meal-prep"],
   ["Haferflocken 80 g","Kakao 4 EL","Banane 2","Eier 1","Zartbitterschokolade 30 g (70 %)","Backpulver 1 TL","Topfen 100 g"],
   ["Hafer fein mahlen, alles verrühren.","Teig in eine kleine Form streichen.","Bei 180 °C 18 Min backen, abkühlen lassen, in Stücke schneiden."]),
 R("Hafer-Bananen-Kekse",["dessert","süß","schnell","meal-prep"],
   ["Reife Banane 2","Haferflocken 120 g","Zartbitterschokolade 30 g (70 %)","Zimt 1 TL"],
   ["Banane zerdrücken, mit Hafer, Zimt und gehackter Schokolade mischen.","Häufchen aufs Blech setzen.","Bei 180 °C 15 Min backen."]),
 R("Chia-Schoko-Pudding",["dessert","süß","meal-prep","energie"],
   ["Chiasamen 40 g","Milch 250 ml","Kakao 1 EL","Banane 1","TK-Beeren 80 g"],
   ["Chia, Milch, Kakao und zerdrückte Banane verrühren.","Über Nacht quellen lassen.","Mit Beeren toppen."]),
 R("Dattel-Kakao-Energy-Balls",["dessert","süß","meal-prep","energie"],
   ["Datteln 150 g","Haferflocken 80 g","Kakao 2 EL","Nüsse 40 g","Kokosraspeln 2 EL"],
   ["Alles im Mixer zerkleinern, bis eine klebrige Masse entsteht.","Kleine Kugeln rollen, in Kokosraspeln wenden.","Kalt stellen - hält eine Woche."]),
 R("Joghurt-Beeren-Schoko-Bark",["dessert","süß","high-protein","meal-prep"],
   ["Skyr 300 g","TK-Beeren 80 g","Zartbitterschokolade 20 g (70 %)","Honig 1 TL"],
   ["Skyr mit Honig glatt rühren und auf Backpapier streichen.","Mit Beeren und Schoko-Splittern bestreuen.","Einfrieren und in Stücke brechen."]),
 R("Protein-Schoko-Creme",["dessert","süß","high-protein","schnell"],
   ["Skyr 300 g","Kakao 2 EL","Erdnussmus 2 TL","Honig 2 TL","Zartbitterschokolade 10 g (70 %)"],
   ["Skyr mit Kakao, Erdnussmus und Honig glatt rühren.","In Gläser füllen, Schokoraspeln darüber.","Zehn Minuten kalt stellen - wird fester."]),
 R("Hüttenkäse mit Obst",["snack","high-protein","süß","schnell"],
   ["Hüttenkäse 300 g","Beeren 150 g","Banane 1","Honig 1 TL"],
   ["Hüttenkäse in Schalen geben.","Mit klein geschnittenem Obst und Honig toppen."]),
 R("Apfel + Nüsse",["snack","schnell"],
   ["Apfel 2","Nüsse 50 g"],
   ["Apfel in Spalten schneiden.","Mit einer Handvoll Nüsse essen."]),
 R("Käsewürfel + Gemüsesticks",["snack","schnell"],
   ["Käse 120 g","Gurke 1","Paprika 1","Karotte 2"],
   ["Käse würfeln.","Gemüse in Sticks schneiden.","Zusammen snacken."]),
 R("Skyr mit Beeren & Paranüssen",["snack","süß","high-protein","schilddrüse"],
   ["Skyr 300 g","TK-Beeren 100 g","Paranüsse 3","Honig 1 TL"],
   ["Skyr in Schalen geben.","Beeren und grob gehackte Paranüsse darüber.","Paranüsse liefern Selen - 2-3 Stück am Tag reichen völlig."]),
 R("Zimt-Apfel-Topfen",["dessert","süß","high-protein","schnell"],
   ["Topfen 300 g","Apfel 2","Zimt 1 TL","Honig 2 TL","Walnüsse 30 g"],
   ["Apfel würfeln und mit Zimt in der Pfanne 3 Min weich dünsten.","Topfen mit Honig cremig rühren.","Warme Apfelwürfel und Walnüsse darüber."]),
 R("Kürbiskern-Schoko-Riegel",["dessert","süß","meal-prep","eisen","energie"],
   ["Haferflocken 100 g","Kürbiskerne 60 g","Datteln 120 g","Kakao 2 EL","Erdnussmus 2 EL","Zartbitterschokolade 20 g (70 %)"],
   ["Datteln mit Erdnussmus im Mixer zerkleinern.","Hafer, Kürbiskerne und Kakao untermischen.","In eine kleine Form pressen, Schokolade darüber schmelzen.","Kalt stellen und in Riegel schneiden - Kürbiskerne bringen Eisen und Magnesium."]),
 R("Beeren-Skyr-Eis am Stiel",["dessert","süß","high-protein","meal-prep"],
   ["Skyr 350 g","TK-Beeren 200 g","Honig 2 TL","Vanille 1 Prise"],
   ["Beeren mit Skyr, Honig und Vanille pürieren.","In Eisformen füllen.","Über Nacht einfrieren."]),
 R("Erdnussbutter-Bananenbrot",["snack","süß","schnell","energie"],
   ["Vollkornbrot 2 Scheiben","Erdnussmus 3 EL","Banane 2","Zimt 1 TL"],
   ["Brot toasten und mit Erdnussmus bestreichen.","Bananenscheiben darauflegen, mit Zimt bestreuen."]),
]

# Abendessen: leicht und kohlenhydratarm - Eiweiss + viel Gemuese.
ABEND = [
 R("Lachs mit Brokkoli & Zitrone",["abend","fisch","schnell","omega-3","low-carb"],
   ["Lachsfilet 300 g","Brokkoli 500 g","Zitrone 1","Olivenöl 1 EL","Knoblauch 1 Zehe","Dill"],
   ["Ofen auf 200 °C.","Lachs mit Öl, Salz und Zitrone aufs Blech legen.","Brokkoli dazu, 15-18 Min backen.","Ohne Beilage - abends reicht Fisch mit viel Gemüse."]),
 R("Hähnchen-Souvlaki mit griechischem Salat",["abend","high-protein","salat","low-carb"],
   ["Hähnchenbrust 350 g","Gurke 1","Tomaten 3","Rote Zwiebel 1/2","Oliven 50 g","Feta 100 g","Olivenöl 2 EL","Oregano 1 TL","Zitrone 1/2"],
   ["Hähnchen mit Öl, Oregano und Zitrone marinieren, dann braten.","Salat schneiden, mit Oliven mischen.","Feta darüber bröseln, Hähnchen dazu."]),
 R("Shakshuka mit Feta",["abend","vegetarisch","high-protein","eisen","low-carb"],
   ["Eier 4","Passata 400 g","Paprika 2","Zwiebel 1","Feta 100 g","Kreuzkümmel 1 TL","Knoblauch 1 Zehe","Petersilie"],
   ["Zwiebel, Knoblauch und Paprika anbraten.","Passata und Kreuzkümmel dazu, 8 Min köcheln.","Eier hineinschlagen und stocken lassen.","Feta und Petersilie darüber."]),
 R("Garnelen-Knoblauch-Pfanne mit Zucchini",["abend","fisch","schnell","low-carb"],
   ["Garnelen 350 g","Zucchini 2","Cherrytomaten 250 g","Knoblauch 3 Zehen","Zitrone 1/2","Olivenöl 2 EL","Petersilie","Chiliflocken"],
   ["Zucchini in Streifen schneiden (Sparschäler) und kurz anbraten.","Garnelen mit Knoblauch und Chili 3 Min braten.","Tomaten dazu, mit Zitrone und Petersilie abschmecken."]),
 R("Puten-Paprika-Pfanne",["abend","high-protein","schnell","low-carb"],
   ["Putenbrust 400 g","Paprika 3","Zucchini 1","Zwiebel 1","Sojasauce 2 EL","Olivenöl 1 EL","Sesam 1 EL"],
   ["Pute würfeln und scharf anbraten, herausnehmen.","Paprika, Zucchini und Zwiebel braten.","Pute zurück, mit Sojasauce ablöschen, Sesam darüber.", VORKOCH]),
 R("Rindfleisch-Spinat-Pfanne",["abend","eisen","high-protein","schilddrüse","low-carb","energie"],
   ["Rindfleisch Streifen 300 g","Blattspinat 300 g","Champignons 200 g","Knoblauch 2 Zehen","Zitrone 1/2","Olivenöl 1 EL","Cherrytomaten 150 g"],
   ["Rindfleischstreifen scharf anbraten, herausnehmen.","Champignons braten, Knoblauch und Spinat kurz zusammenfallen lassen.","Fleisch zurück, Tomaten dazu, mit Zitronensaft abschmecken.","Zitrone und Tomate liefern das Vitamin C, das die Eisenaufnahme aus Fleisch und Spinat verbessert."]),
 R("Schweinefilet mit Ofengemüse",["abend","high-protein","low-carb"],
   ["Schweinefilet 400 g","Zucchini 2","Paprika 2","Karotten 3","Kartoffeln 250 g","Olivenöl 2 EL","Rosmarin","Knoblauch 2 Zehen"],
   ["Ofen 200 °C, Gemüse und Kartoffeln 25 Min backen.","Schweinefilet rundum anbraten, 12-15 Min mit in den Ofen.","In Scheiben schneiden und mit dem Gemüse servieren."]),
 R("Ofen-Lachs mit grünen Bohnen",["abend","fisch","omega-3","low-carb"],
   ["Lachsfilet 300 g","Grüne Bohnen 400 g","Cherrytomaten 200 g","Zitrone 1","Olivenöl 1 EL","Mandelblättchen 20 g"],
   ["Bohnen 6 Min blanchieren.","Lachs bei 200 °C 14 Min backen.","Bohnen mit Tomaten in Öl schwenken, Mandeln darüber, Lachs dazu."]),
 R("Hähnchen-Zucchini-Auflauf mit Käse",["abend","high-protein","low-carb","vorkochen"],
   ["Hähnchenbrust 400 g","Zucchini 3","Passata 300 g","Reibekäse 100 g","Zwiebel 1","Knoblauch 1 Zehe","Oregano 1 TL"],
   ["Hähnchen würfeln und anbraten, Zwiebel und Knoblauch dazu.","Zucchini in Scheiben mit Passata in die Form schichten.","Käse darüber, bei 200 °C 25 Min backen.", VORKOCH]),
 R("Putenmedaillons mit Champignonrahm & Bohnen",["abend","high-protein","low-carb"],
   ["Putenbrust 400 g","Champignons 300 g","Grüne Bohnen 350 g","Crème fraîche 80 g","Zwiebel 1","Senf 1 TL","Petersilie"],
   ["Pute in dicke Scheiben schneiden und braten, warm stellen.","Zwiebel und Champignons braten, mit Crème fraîche und Senf binden.","Bohnen dämpfen, alles zusammen anrichten."]),
 R("Kabeljau mit Tomaten-Zucchini-Gemüse",["abend","fisch","low-carb","schnell"],
   ["Kabeljaufilet 350 g","Zucchini 2","Cherrytomaten 300 g","Zwiebel 1","Knoblauch 2 Zehen","Olivenöl 2 EL","Zitrone 1/2","Thymian"],
   ["Zwiebel, Knoblauch und Zucchini anbraten, Tomaten dazu, 5 Min schmoren.","Fisch salzen, obenauf legen, Deckel drauf, 8-10 Min garen.","Mit Zitrone und Thymian abschmecken."]),
 R("Gemüse-Frittata mit Käse",["abend","vegetarisch","high-protein","low-carb","schnell"],
   ["Eier 6","Zucchini 1","Paprika 1","Cherrytomaten 200 g","Reibekäse 80 g","Zwiebel 1","Olivenöl 1 EL","Basilikum"],
   ["Gemüse klein schneiden und in der Pfanne anbraten.","Eier verquirlen, salzen, darüber gießen.","Käse darauf, Deckel drauf, bei kleiner Hitze 10 Min stocken lassen."]),
 R("Rinderstreifen-Salat mit Rucola & Parmesan",["abend","eisen","salat","low-carb","energie"],
   ["Rindfleisch Streifen 300 g","Rucola 150 g","Cherrytomaten 250 g","Parmesan 40 g","Zitrone 1","Olivenöl 2 EL","Pinienkerne 20 g","Rote Zwiebel 1/2"],
   ["Rindfleisch scharf und kurz anbraten, salzen.","Rucola mit Tomaten, Zwiebel, Zitrone und Öl anmachen.","Fleisch darauf, Parmesan und Pinienkerne darüber.","Zitrone nicht weglassen - sie holt das Eisen aus dem Fleisch."]),
 R("Hähnchenspieße mit Ofengemüse & Joghurt-Dip",["abend","high-protein","low-carb"],
   ["Hähnchenbrust 400 g","Paprika 2","Zucchini 1","Rote Zwiebel 1","Griechischer Joghurt 200 g","Knoblauch 1 Zehe","Zitrone 1/2","Paprikapulver 1 TL","Olivenöl 1 EL"],
   ["Hähnchen und Gemüse würfeln, auf Spieße stecken, würzen.","Bei 210 °C 20 Min backen (oder in der Pfanne).","Joghurt mit Knoblauch und Zitrone zum Dip rühren."]),
 R("Zucchini-Nudeln mit Hackfleisch-Tomatensauce",["abend","eisen","high-protein","low-carb"],
   ["Zucchini 4","Faschiertes Rind 300 g","Passata 400 g","Zwiebel 1","Knoblauch 2 Zehen","Parmesan 40 g","Olivenöl 1 EL","Basilikum"],
   ["Zucchini mit dem Sparschäler in Bänder schneiden.","Zwiebel, Knoblauch und Faschiertes anbraten, Passata dazu, 15 Min köcheln.","Zucchini nur 2 Min mitziehen lassen, Parmesan darüber."]),
 R("Blumenkohl-Käse-Auflauf mit Schinken",["abend","vegetarisch","low-carb","vorkochen"],
   ["Blumenkohl 800 g","Schinken 150 g","Reibekäse 120 g","Crème fraîche 100 g","Muskat 1 Prise","Eier 2"],
   ["Blumenkohl in Röschen 8 Min kochen.","Crème fraîche mit Eiern und Muskat verquirlen.","Blumenkohl und Schinken in die Form, Guss darüber, Käse obenauf.","Bei 200 °C 25 Min backen.", VORKOCH]),
 R("Thunfisch-Ei-Salat",["abend","fisch","high-protein","low-carb","schnell"],
   ["Thunfisch 2 Dosen","Eier 4","Blattsalat 1","Cherrytomaten 250 g","Gurke 1","Rote Zwiebel 1/2","Olivenöl 2 EL","Zitrone 1/2","Oliven 50 g"],
   ["Eier 8 Min kochen, schrecken, vierteln.","Salat und Gemüse schneiden, Thunfisch abtropfen lassen.","Alles mischen, mit Öl, Zitrone, Salz und Pfeffer abschmecken."]),
 R("Forelle aus dem Ofen mit Fenchel",["abend","fisch","omega-3","low-carb"],
   ["Forelle 2 Stück","Fenchel 2","Cherrytomaten 200 g","Zitrone 1","Olivenöl 2 EL","Knoblauch 2 Zehen","Petersilie"],
   ["Fenchel in Spalten schneiden, mit Öl und Knoblauch aufs Blech.","Forellen salzen, Zitronenscheiben hineinlegen, dazulegen.","Bei 200 °C 22 Min backen, Tomaten die letzten 8 Min dazu."]),
 R("Rindersteak mit Brokkoli & Kräuterbutter",["abend","eisen","high-protein","low-carb","energie"],
   ["Rindersteak 350 g","Brokkoli 500 g","Butter 30 g","Knoblauch 1 Zehe","Petersilie","Zitrone 1/2","Olivenöl 1 EL"],
   ["Steaks kräftig anbraten, je Seite 3-4 Min, dann ruhen lassen.","Brokkoli dämpfen.","Butter mit Knoblauch, Petersilie und Zitrone verrühren, auf Steak und Brokkoli geben."]),
 R("Omelett mit Spinat & Feta",["abend","vegetarisch","eisen","low-carb","schnell","energie"],
   ["Eier 6","Blattspinat 250 g","Feta 100 g","Knoblauch 1 Zehe","Cherrytomaten 200 g","Olivenöl 1 EL","Muskat 1 Prise"],
   ["Spinat mit Knoblauch zusammenfallen lassen, abtropfen.","Eier verquirlen, mit Spinat und Muskat mischen.","In der Pfanne stocken lassen, Feta und Tomaten darauf."]),
 R("Hähnchen-Curry mit Blumenkohlreis",["abend","high-protein","low-carb"],
   ["Hähnchenbrust 400 g","Blumenkohl 700 g","Kokosmilch 200 ml","Currypulver 2 TL","Zwiebel 1","Paprika 1","Ingwer 1 Stück","Koriander"],
   ["Blumenkohl grob raspeln und 5 Min in der Pfanne trocken anbraten - das ist der Reis-Ersatz.","Hähnchen mit Zwiebel, Ingwer und Curry anbraten.","Paprika und Kokosmilch dazu, 10 Min köcheln.","Über den Blumenkohlreis geben."]),
 R("Krautsalat mit Hähnchen (asiatisch)",["abend","salat","low-carb","schnell"],
   ["Hähnchenbrust 350 g","Weißkraut 500 g","Karotten 2","Frühlingszwiebel 2","Sojasauce 2 EL","Sesamöl 1 EL","Limette 1","Erdnüsse 30 g"],
   ["Hähnchen in Streifen braten.","Kraut und Karotten fein hobeln.","Mit Sojasauce, Sesamöl und Limette anmachen.","Hähnchen, Frühlingszwiebel und Erdnüsse darüber."]),
]

# ---- Nachschub (August 2026): mehr Auswahl, damit 5 Optionen je Mahlzeit
# ---- ohne Wiederholungen durch die Woche kommen.
FRUEHSTUECK += [
 R("Ei-Muffins mit Gemüse & Käse",["frühstück","high-protein","meal-prep"],
   ["Eier 6","Paprika 1","Zucchini 1","Reibekäse 80 g","Schinken 80 g","Vollkornbrot 2 Scheiben","Schnittlauch"],
   ["Ofen auf 180 °C, Muffinform einfetten.","Gemüse fein würfeln, mit verquirlten Eiern, Schinken und Käse mischen.","In die Form füllen, 20 Min backen.","Halten 3 Tage im Kühlschrank - gleich die doppelte Menge backen."]),
 R("Skyr-Porridge mit Kakao & Banane",["frühstück","high-protein","süß","schnell"],
   ["Haferflocken 110 g","Milch 350 ml","Skyr 250 g","Kakao 2 EL","Banane 2","Honig 2 TL","Nüsse 30 g"],
   ["Hafer mit Milch und Kakao aufkochen, 5 Min quellen lassen.","Vom Herd nehmen, Skyr unterrühren - so bleibt das Eiweiß cremig.","Mit Banane, Nüssen und Honig servieren."]),
 R("Käse-Tomaten-Toast mit Ei",["frühstück","high-protein","schnell"],
   ["Vollkornbrot 4 Scheiben","Reibekäse 100 g","Tomaten 3","Eier 3","Oregano 1 TL","Olivenöl 1 EL"],
   ["Brot mit Tomatenscheiben und Käse belegen.","Unter dem Grill 6 Min überbacken.","Eier dazu braten, Oregano darüber."]),
 R("Grießbrei mit Beeren & Mandeln",["frühstück","süß","schnell"],
   ["Grieß 100 g","Milch 500 ml","TK-Beeren 200 g","Mandeln 40 g","Honig 2 TL","Zimt 1 TL"],
   ["Milch aufkochen, Grieß einrühren, 3 Min quellen lassen.","Beeren kurz erwärmen.","Grießbrei mit Beeren, Mandeln und Honig servieren."]),
 R("Räucherforelle-Brot mit Ei",["frühstück","high-protein","fisch","omega-3"],
   ["Vollkornbrot 4 Scheiben","Räucherforelle 150 g","Eier 2","Frischkäse 80 g","Kren 1 TL","Zitrone 1/2","Dill"],
   ["Brot mit Frischkäse und etwas Kren bestreichen.","Forellenfilet darauf zupfen.","Eier hart kochen, in Scheiben darauflegen, mit Zitrone und Dill servieren."]),
 R("Erdnussbutter-Hafer-Bowl mit Apfel",["frühstück","energie","schnell"],
   ["Haferflocken 110 g","Milch 350 ml","Erdnussmus 3 EL","Apfel 2","Zimt 1 TL","Skyr 150 g"],
   ["Hafer mit Milch 5 Min kochen.","Erdnussmus einrühren.","Mit Apfelwürfeln, Zimt und einem Löffel Skyr servieren."]),
 R("Vollkorn-Porridge mit Birne & Walnüssen",["frühstück","energie","meal-prep"],
   ["Haferflocken 110 g","Milch 400 ml","Birne 2","Walnüsse 40 g","Honig 2 TL","Zimt 1 TL","Salz 1 Prise"],
   ["Hafer mit Milch und Salz aufkochen, quellen lassen.","Birne würfeln und kurz mitziehen lassen.","Mit Walnüssen und Honig servieren."]),
 R("Frühstücks-Jause mit Ei",["frühstück","high-protein","schnell"],
   ["Vollkornbrot 4 Scheiben","Schinken 120 g","Käse 100 g","Eier 3","Gurke 1","Tomaten 2","Butter 20 g"],
   ["Eier 7 Min kochen, schrecken, schälen.","Brot buttern, mit Schinken und Käse belegen.","Ei, Gurke und Tomate dazu anrichten."]),
]
MITTAG += [
 R("Hähnchen-Gyros mit Reis & Tzatziki",["mittag","high-protein","schnell"],
   ["Hähnchenbrust 400 g","Reis 180 g","Tzatziki 200 g","Paprika 2","Rote Zwiebel 1","Gyros-Gewürz 2 TL","Olivenöl 1 EL","Tomaten 2"],
   ["Hähnchen in Streifen mit Gyros-Gewürz marinieren.","Reis kochen.","Fleisch mit Paprika und Zwiebel scharf anbraten.","Mit Reis, Tomaten und Tzatziki servieren.", VORKOCH]),
 R("Lachs-Nudeln mit Spinat & Frischkäse",["mittag","fisch","omega-3","schnell"],
   ["Lachsfilet 350 g","Vollkornnudeln 220 g","Blattspinat 250 g","Frischkäse 120 g","Knoblauch 2 Zehen","Zitrone 1/2","Parmesan 30 g"],
   ["Nudeln kochen.","Lachs würfeln und 4 Min braten, herausnehmen.","Knoblauch und Spinat zusammenfallen lassen, Frischkäse mit etwas Nudelwasser zur Sauce rühren.","Nudeln und Lachs untermischen, mit Zitrone und Parmesan abschmecken."]),
 R("Linsensalat mit Feta & Ei",["mittag","vegetarisch","eisen","meal-prep","energie"],
   ["Berglinsen 200 g","Feta 150 g","Eier 4","Cherrytomaten 250 g","Gurke 1","Rote Zwiebel 1","Zitrone 1","Olivenöl 3 EL","Petersilie"],
   ["Linsen 20 Min kochen, abkühlen lassen.","Eier 8 Min kochen, vierteln.","Gemüse schneiden, alles mischen.","Mit reichlich Zitrone und Öl abschmecken - die Säure hilft, das Eisen aus den Linsen aufzunehmen.", VORKOCH]),
 R("Puten-Kartoffel-Blech mit Kräutern",["mittag","high-protein","vorkochen"],
   ["Putenbrust 400 g","Kartoffeln 600 g","Karotten 3","Zucchini 1","Olivenöl 2 EL","Rosmarin","Knoblauch 2 Zehen","Paprikapulver 1 TL"],
   ["Ofen 200 °C. Kartoffeln und Gemüse würfeln, mit Öl und Gewürzen mischen.","20 Min backen.","Pute in Stücken dazugeben, weitere 15 Min backen.", VORKOCH]),
 R("Reisnudel-Bowl mit Hähnchen & Erdnusssauce",["mittag","high-protein","schnell"],
   ["Hähnchenbrust 400 g","Reisnudeln 200 g","Karotten 2","Gurke 1","Frühlingszwiebel 2","Erdnussmus 3 EL","Sojasauce 2 EL","Limette 1","Erdnüsse 30 g"],
   ["Reisnudeln nach Packung garen, kalt abspülen.","Hähnchen in Streifen braten.","Erdnussmus mit Sojasauce, Limette und etwas Wasser zur Sauce rühren.","Alles mischen, Erdnüsse darüber."]),
 R("Faschierte Laibchen mit Kartoffelpüree",["mittag","eisen","high-protein","vorkochen"],
   ["Faschiertes Rind 450 g","Kartoffeln 700 g","Eier 1","Semmelbrösel 40 g","Zwiebel 1","Milch 100 ml","Butter 20 g","Petersilie","Senf 1 TL"],
   ["Kartoffeln kochen, mit Milch und Butter stampfen.","Faschiertes mit Ei, Bröseln, Zwiebel und Senf verkneten, Laibchen formen.","In der Pfanne je Seite 4-5 Min braten.","Mit Püree und Petersilie servieren.", VORKOCH]),
 R("Thunfisch-Nudel-Auflauf mit Erbsen",["mittag","fisch","vorkochen"],
   ["Vollkornnudeln 220 g","Thunfisch 2 Dosen","TK-Erbsen 200 g","Passata 400 g","Reibekäse 100 g","Zwiebel 1","Knoblauch 1 Zehe"],
   ["Nudeln al dente kochen.","Zwiebel und Knoblauch anbraten, Passata, Thunfisch und Erbsen dazu.","Mit den Nudeln in die Form, Käse darüber.","Bei 200 °C 20 Min backen.", VORKOCH]),
 R("Falafel-Bowl mit Couscous & Joghurt-Dip",["mittag","vegetarisch","eisen","schnell"],
   ["TK-Falafel 12 Stück","Couscous 180 g","Griechischer Joghurt 200 g","Gurke 1","Tomaten 3","Rote Zwiebel 1","Zitrone 1","Olivenöl 2 EL","Petersilie"],
   ["Falafel nach Packung im Ofen knusprig backen.","Couscous quellen lassen.","Joghurt mit Zitrone, Salz und Petersilie zum Dip rühren.","Alles in Schalen anrichten."]),
]
SNACK += [
 R("Topfen-Vanille-Creme mit Himbeeren",["dessert","süß","high-protein","schnell"],
   ["Topfen 300 g","TK-Himbeeren 150 g","Vanillezucker 1 Pkg","Honig 1 TL","Mandeln 20 g"],
   ["Topfen mit Vanillezucker und Honig cremig rühren.","Himbeeren auftauen und unterheben.","Mit gehobelten Mandeln bestreuen."]),
 R("Bananenbrot (Vollkorn)",["dessert","süß","meal-prep"],
   ["Vollkornmehl 180 g","Banane 3","Eier 2","Griechischer Joghurt 100 g","Walnüsse 50 g","Backpulver 1 TL","Zimt 1 TL","Honig 2 EL"],
   ["Bananen zerdrücken, mit Eiern, Joghurt und Honig verrühren.","Mehl, Backpulver, Zimt und Nüsse unterheben.","Bei 175 °C 40 Min backen, auskühlen lassen.","Hält eine Woche - eine Scheibe pro Snack."]),
 R("Schinken-Käse-Röllchen mit Gurke",["snack","high-protein","schnell"],
   ["Schinken 150 g","Frischkäse 100 g","Gurke 1","Paprika 1","Schnittlauch"],
   ["Schinkenscheiben mit Frischkäse bestreichen.","Gurken- und Paprikastreifen darauflegen, aufrollen.","Mit Schnittlauch bestreuen."]),
 R("Warme Zimt-Birne mit Topfen",["dessert","süß","high-protein","schnell"],
   ["Birne 2","Topfen 250 g","Zimt 1 TL","Honig 2 TL","Walnüsse 30 g"],
   ["Birne würfeln und mit Zimt 4 Min dünsten.","Topfen mit Honig cremig rühren.","Warme Birne und Walnüsse darüber."]),
 R("Gemüsesticks mit Hummus",["snack","schnell","eisen"],
   ["Hummus 200 g","Karotten 3","Gurke 1","Paprika 2","Zitrone 1/2"],
   ["Gemüse in Sticks schneiden.","Hummus mit einem Spritzer Zitrone verrühren.","Zusammen snacken - Kichererbsen liefern Eisen, die Paprika das Vitamin C dazu."]),
 R("Beeren-Skyr-Shake mit Hafer",["snack","süß","high-protein","schnell","energie"],
   ["Skyr 250 g","TK-Beeren 200 g","Haferflocken 40 g","Milch 200 ml","Honig 1 TL"],
   ["Alles im Mixer glatt pürieren.","In zwei Gläser füllen.","Wenn er zu dick ist: noch einen Schuss Milch dazu."]),
]
ABEND += [
 R("Puten-Gyros mit Krautsalat",["abend","high-protein","low-carb","schnell"],
   ["Putenbrust 400 g","Weißkraut 400 g","Karotten 2","Griechischer Joghurt 150 g","Gyros-Gewürz 2 TL","Zitrone 1","Olivenöl 2 EL","Knoblauch 1 Zehe"],
   ["Pute in Streifen mit Gyros-Gewürz marinieren und scharf braten.","Kraut und Karotten fein hobeln, mit Zitrone, Öl und Salz kräftig durchkneten.","Joghurt mit Knoblauch als Dip dazu."]),
 R("Zucchini-Lasagne mit Faschiertem",["abend","eisen","high-protein","low-carb","vorkochen"],
   ["Zucchini 4","Faschiertes Rind 350 g","Passata 400 g","Reibekäse 120 g","Frischkäse 100 g","Zwiebel 1","Knoblauch 2 Zehen","Oregano 1 TL"],
   ["Zucchini längs in dünne Platten schneiden.","Faschiertes mit Zwiebel und Knoblauch anbraten, Passata dazu, 15 Min köcheln.","Abwechselnd Zucchini und Sauce schichten, Frischkäse und Reibekäse obenauf.","Bei 200 °C 30 Min backen, 5 Min ruhen lassen.", VORKOCH]),
 R("Garnelen-Spinat-Pfanne",["abend","fisch","eisen","low-carb","schnell","energie"],
   ["Garnelen 350 g","Blattspinat 300 g","Cherrytomaten 250 g","Knoblauch 3 Zehen","Zitrone 1","Olivenöl 2 EL","Chiliflocken","Feta 80 g"],
   ["Knoblauch in Öl anschwitzen, Garnelen 3 Min braten, herausnehmen.","Spinat und Tomaten zusammenfallen lassen.","Garnelen zurück, mit Zitrone abschmecken, Feta darüber."]),
 R("Hähnchen-Pilz-Pfanne mit grünen Bohnen",["abend","high-protein","low-carb"],
   ["Hähnchenbrust 400 g","Champignons 300 g","Grüne Bohnen 400 g","Crème fraîche 80 g","Zwiebel 1","Knoblauch 1 Zehe","Thymian"],
   ["Bohnen 6 Min blanchieren.","Hähnchen in Stücken anbraten, herausnehmen.","Pilze und Zwiebel braten, mit Crème fraîche binden.","Alles zusammenführen, mit Thymian abschmecken."]),
 R("Rindfleisch-Brokkoli-Pfanne (asiatisch)",["abend","eisen","high-protein","low-carb","energie"],
   ["Rindfleisch Streifen 300 g","Brokkoli 500 g","Paprika 1","Knoblauch 2 Zehen","Ingwer 1 Stück","Sojasauce 2 EL","Sesamöl 1 EL","Limette 1","Sesam 1 EL"],
   ["Brokkoli 3 Min blanchieren.","Rindfleisch scharf anbraten, herausnehmen.","Knoblauch, Ingwer und Paprika braten, Brokkoli dazu.","Fleisch zurück, mit Sojasauce und Limette ablöschen, Sesam darüber."]),
 R("Ofengemüse mit Feta & Ei",["abend","vegetarisch","low-carb","schnell"],
   ["Zucchini 2","Paprika 2","Cherrytomaten 300 g","Rote Zwiebel 1","Feta 150 g","Eier 4","Olivenöl 2 EL","Oregano 1 TL"],
   ["Gemüse würfeln, mit Öl und Oregano bei 200 °C 25 Min backen.","Feta darüber bröseln, Mulden formen und die Eier hineinschlagen.","Weitere 8 Min backen, bis das Eiweiß gestockt ist."]),
 R("Hühnersuppe mit viel Gemüse",["abend","low-carb","vorkochen"],
   ["Hühnerbrust 350 g","Karotten 3","Lauch 1","Sellerie 1 Stange","Zucchini 1","Petersilie","Suppenwürze 1 TL","Ingwer 1 Stück"],
   ["Hühnerbrust in 1,5 l Wasser mit Ingwer 20 Min leise köcheln, herausnehmen und zerpflücken.","Gemüse klein schneiden und 10 Min in der Brühe garen.","Fleisch zurück, mit Suppenwürze und Petersilie abschmecken.", VORKOCH]),
 R("Gefüllte Zucchini mit Pute & Käse",["abend","high-protein","low-carb","vorkochen"],
   ["Zucchini 4","Putenbrust 350 g","Passata 300 g","Reibekäse 100 g","Zwiebel 1","Knoblauch 1 Zehe","Oregano 1 TL"],
   ["Zucchini halbieren und aushöhlen.","Pute klein würfeln, mit Zwiebel, Knoblauch und dem Zucchini-Inneren anbraten, Passata dazu.","Zucchini füllen, Käse darüber, bei 190 °C 25 Min backen.", VORKOCH]),
]

ALL = FRUEHSTUECK + MITTAG + SNACK + ABEND

# ============================================================ TAGESPLAN-POOLS
# Portionen pro Person: a = Anna (~1450 kcal/Tag), b = Andriy (~2050 kcal/Tag).
# Verteilung NEU: viel Energie am Vormittag, leichter Abend.
BREAKFAST=[
 o("Rührei mit Tomaten & Käse","2 Eier, 30 g Käse, 1 Scheibe Brot","3 Eier, 40 g Käse, 2 Scheiben Brot","~420 / ~620"),
 o("Käse-Schinken-Omelett mit Vollkornbrot","2 Eier, Schinken, 1 Scheibe Brot","3 Eier, Schinken, 2 Scheiben Brot","~420 / ~620"),
 o("Spiegeleier auf Vollkorntoast mit Spinat","2 Eier, 1,5 Scheiben, Spinat","2 Eier, 2,5 Scheiben, Spinat","~420 / ~610"),
 o("Haferbrei mit Apfel, Zimt & Nüssen","50 g Hafer, 1 Apfel, 15 g Nüsse","70 g Hafer, 1 Apfel, 25 g Nüsse","~420 / ~620"),
 o("Overnight Oats mit Beeren & Nüssen","50 g Hafer, 150 g Skyr, 15 g Nüsse","70 g Hafer, 200 g Skyr, 25 g Nüsse","~420 / ~620"),
 o("Bircher Müsli mit Apfel & Nüssen","45 g Hafer, 130 g Joghurt","65 g Hafer, 170 g Joghurt, extra Nüsse","~420 / ~620"),
 o("Protein-Pancakes mit Beeren","3 Stück + Beeren","5 Stück + Beeren","~420 / ~620"),
 o("Vollkornbrot mit Frischkäse & Räucherlachs","1,5 Scheiben, 60 g Lachs","2,5 Scheiben, 90 g Lachs","~420 / ~620"),
 o("Cottage-Cheese-Brot mit Ei","1 Scheibe, 100 g Cottage Cheese, 1 Ei","2 Scheiben, 150 g Cottage Cheese, 1 Ei","~410 / ~620"),
 o("Skyr-Beeren-Bowl mit Haferflocken","150 g Skyr, 25 g Hafer, Beeren","250 g Skyr, 35 g Hafer, Beeren, Nüsse","~420 / ~620"),
 o("Griechischer Joghurt mit Nüssen, Honig & Hafer","150 g Joghurt, 20 g Hafer","250 g Joghurt, 30 g Hafer, extra Nüsse","~420 / ~620"),
 o("Frühstücks-Burrito mit Ei & Bohnen","1 Tortilla","2 Tortillas","~430 / ~630"),
 o("Avocado-Ei-Brot","1,5 Scheiben, 1/2 Avocado, 2 Eier","2,5 Scheiben, 1 Avocado, 2 Eier","~430 / ~630"),
 o("Quinoa-Porridge mit Beeren","50 g Quinoa, Beeren, 15 g Mandeln","70 g Quinoa, Beeren, 25 g Mandeln","~420 / ~620"),
 o("Pilz-Omelett mit Vollkornbrot","2 Eier, Pilze, 1 Scheibe Brot","3 Eier, Pilze, 2 Scheiben Brot","~410 / ~610"),
 o("Topfencreme mit Kürbiskernen & Vollkornbrot","150 g Topfen, 1 Scheibe Brot","200 g Topfen, 2 Scheiben Brot","~420 / ~620"),
 o("Ei-Muffins mit Gemüse & Käse","2 Muffins + 1 Scheibe Brot","3 Muffins + 1,5 Scheiben Brot","~420 / ~620"),
 o("Skyr-Porridge mit Kakao & Banane","45 g Hafer, 100 g Skyr, 1 Banane","65 g Hafer, 150 g Skyr, 1 Banane","~420 / ~620"),
 o("Käse-Tomaten-Toast mit Ei","1,5 Scheiben, 1 Ei","2,5 Scheiben, 2 Eier","~420 / ~620"),
 o("Grießbrei mit Beeren & Mandeln","40 g Grieß, Beeren, 15 g Mandeln","60 g Grieß, Beeren, 25 g Mandeln","~410 / ~610"),
 o("Räucherforelle-Brot mit Ei","1,5 Scheiben, 60 g Forelle","2,5 Scheiben, 90 g Forelle","~420 / ~620"),
 o("Erdnussbutter-Hafer-Bowl mit Apfel","45 g Hafer, 1 EL Erdnussmus","65 g Hafer, 2 EL Erdnussmus","~430 / ~630"),
 o("Vollkorn-Porridge mit Birne & Walnüssen","45 g Hafer, 1 Birne, 15 g Nüsse","65 g Hafer, 1 Birne, 25 g Nüsse","~420 / ~620"),
 o("Frühstücks-Jause mit Ei","1,5 Scheiben, 1 Ei, Schinken & Käse","2,5 Scheiben, 2 Eier, Schinken & Käse","~420 / ~620"),
]
LUNCH=[
 o("Hähnchen-Reis-Bowl","0,85 Portion","1,15 Portion","~480 / ~700"),
 o("Putengeschnetzeltes mit Reis","0,85 Portion","1,15 Portion","~480 / ~700"),
 o("Spaghetti Bolognese","0,85 Portion","1,15 Portion","~490 / ~710"),
 o("Nudelauflauf mit Pute & Käse","0,85 Portion","1,15 Portion","~490 / ~710"),
 o("Chili con Carne mit Reis","0,85 Portion","1,15 Portion","~490 / ~700"),
 o("Linsen-Bolognese mit Vollkornnudeln","0,85 Portion","1,15 Portion","~480 / ~700"),
 o("Putenwrap (Vollkorn)","1,5 Wraps","2,5 Wraps","~480 / ~700"),
 o("Thunfisch-Couscous-Salat","0,85 Portion","1,15 Portion","~480 / ~700"),
 o("Großer griechischer Salat mit Hähnchen","150 g Hähnchen + Salat + 1 Scheibe Brot","200 g + Salat + 2 Scheiben","~480 / ~700"),
 o("Chicken-Caesar-Salat","150 g Hähnchen + Salat + Croutons","200 g + Salat + extra Croutons","~480 / ~700"),
 o("Bulgur-Salat mit Feta & Kichererbsen","0,85 Portion","1,15 Portion","~480 / ~700"),
 o("Rindfleisch-Reis-Pfanne mit Paprika","0,85 Portion","1,15 Portion","~480 / ~700"),
 o("Lachs-Kartoffel-Pfanne mit Spinat","0,85 Portion","1,15 Portion","~480 / ~700"),
 o("Hähnchen-Nudel-Pfanne mit Brokkoli","0,85 Portion","1,15 Portion","~490 / ~710"),
 o("Quinoa-Bowl mit Hähnchen & Avocado","0,85 Portion","1,15 Portion","~480 / ~700"),
 o("Süßkartoffel-Hähnchen-Blech mit Feta","0,85 Portion","1,15 Portion","~480 / ~700"),
 o("Kichererbsen-Curry mit Reis","0,85 Portion","1,15 Portion","~480 / ~700"),
 o("Hähnchen-Fajitas (Vollkorn)","2 Fajitas","3-4 Fajitas","~490 / ~710"),
 o("Gefüllte Paprika mit Faschiertem & Reis","1,5 Hälften","2,5 Hälften","~480 / ~700"),
 o("Reste vom Vortag","0,85 Portion aufwärmen","1,15 Portion aufwärmen","~480 / ~700"),
 o("Hähnchen-Gyros mit Reis & Tzatziki","0,85 Portion","1,15 Portion","~490 / ~710"),
 o("Lachs-Nudeln mit Spinat & Frischkäse","0,85 Portion","1,15 Portion","~490 / ~710"),
 o("Linsensalat mit Feta & Ei","0,85 Portion","1,15 Portion","~480 / ~700"),
 o("Puten-Kartoffel-Blech mit Kräutern","0,85 Portion","1,15 Portion","~480 / ~700"),
 o("Reisnudel-Bowl mit Hähnchen & Erdnusssauce","0,85 Portion","1,15 Portion","~490 / ~710"),
 o("Faschierte Laibchen mit Kartoffelpüree","2 Laibchen + Püree","3 Laibchen + Püree","~490 / ~710"),
 o("Thunfisch-Nudel-Auflauf mit Erbsen","0,85 Portion","1,15 Portion","~490 / ~710"),
 o("Falafel-Bowl mit Couscous & Joghurt-Dip","5 Falafel + Couscous","7 Falafel + Couscous","~480 / ~700"),
]
SNACKS=[
 o("Schoko-Quark-Mousse","1 Glas","1 großes Glas + Schoko","~180 / ~280"),
 o("Bananen-Nicecream (Schoko)","1 Banane","2 Bananen","~170 / ~280"),
 o("Protein-Brownies","1 Stück","2 Stück","~180 / ~290"),
 o("Hafer-Bananen-Kekse","2 Kekse","3-4 Kekse","~175 / ~285"),
 o("Chia-Schoko-Pudding","1 Glas","1 großes Glas","~180 / ~280"),
 o("Dattel-Kakao-Energy-Balls","2 Bällchen","3 Bällchen","~180 / ~280"),
 o("Joghurt-Beeren-Schoko-Bark","1 Portion","1,5 Portionen","~170 / ~275"),
 o("Protein-Schoko-Creme","1 Glas","1 großes Glas","~180 / ~285"),
 o("Hüttenkäse mit Obst","150 g + Obst","220 g + Obst","~180 / ~285"),
 o("Apfel + Nüsse","1 Apfel, 20 g Nüsse","1 Apfel, 30 g Nüsse","~180 / ~280"),
 o("Käsewürfel + Gemüsesticks","45 g Käse + Gemüse","70 g Käse + Gemüse","~180 / ~280"),
 o("Skyr mit Beeren & Paranüssen","150 g Skyr, 2 Paranüsse","220 g Skyr, 3 Paranüsse","~180 / ~285"),
 o("Zimt-Apfel-Topfen","1 Glas","1 großes Glas","~180 / ~280"),
 o("Kürbiskern-Schoko-Riegel","1 Riegel","1,5 Riegel","~185 / ~285"),
 o("Beeren-Skyr-Eis am Stiel","1 Stück","2 Stück","~170 / ~275"),
 o("Erdnussbutter-Bananenbrot","1/2 Scheibe + Banane","1 Scheibe + Banane","~180 / ~285"),
 o("Topfen-Vanille-Creme mit Himbeeren","1 Glas","1 großes Glas","~180 / ~280"),
 o("Bananenbrot (Vollkorn)","1 Scheibe","1,5 Scheiben","~185 / ~285"),
 o("Schinken-Käse-Röllchen mit Gurke","3 Röllchen","5 Röllchen","~180 / ~280"),
 o("Warme Zimt-Birne mit Topfen","1 Portion","1,5 Portionen","~180 / ~280"),
 o("Gemüsesticks mit Hummus","80 g Hummus + Gemüse","120 g Hummus + Gemüse","~180 / ~280"),
 o("Beeren-Skyr-Shake mit Hafer","1 Glas","1 großes Glas","~180 / ~285"),
]
DINNER=[
 o("Lachs mit Brokkoli & Zitrone","0,85 Portion","1,15 Portion","~370 / ~450"),
 o("Hähnchen-Souvlaki mit griechischem Salat","0,85 Portion","1,15 Portion","~370 / ~450"),
 o("Shakshuka mit Feta","2 Eier + Salat","2 Eier + Feta extra","~370 / ~450"),
 o("Garnelen-Knoblauch-Pfanne mit Zucchini","0,85 Portion","1,15 Portion","~360 / ~440"),
 o("Puten-Paprika-Pfanne","0,85 Portion","1,15 Portion","~370 / ~450"),
 o("Rindfleisch-Spinat-Pfanne","0,85 Portion","1,15 Portion","~370 / ~455"),
 o("Schweinefilet mit Ofengemüse","0,85 Portion","1,15 Portion","~380 / ~460"),
 o("Ofen-Lachs mit grünen Bohnen","0,85 Portion","1,15 Portion","~375 / ~455"),
 o("Hähnchen-Zucchini-Auflauf mit Käse","0,85 Portion","1,15 Portion","~375 / ~455"),
 o("Putenmedaillons mit Champignonrahm & Bohnen","0,85 Portion","1,15 Portion","~370 / ~450"),
 o("Kabeljau mit Tomaten-Zucchini-Gemüse","0,85 Portion","1,15 Portion","~355 / ~435"),
 o("Gemüse-Frittata mit Käse","0,85 Portion","1,15 Portion","~370 / ~450"),
 o("Rinderstreifen-Salat mit Rucola & Parmesan","0,85 Portion","1,15 Portion","~375 / ~455"),
 o("Hähnchenspieße mit Ofengemüse & Joghurt-Dip","0,85 Portion","1,15 Portion","~370 / ~450"),
 o("Zucchini-Nudeln mit Hackfleisch-Tomatensauce","0,85 Portion","1,15 Portion","~375 / ~455"),
 o("Blumenkohl-Käse-Auflauf mit Schinken","0,85 Portion","1,15 Portion","~380 / ~460"),
 o("Thunfisch-Ei-Salat","0,85 Portion","1,15 Portion","~360 / ~440"),
 o("Forelle aus dem Ofen mit Fenchel","0,85 Portion","1,15 Portion","~370 / ~450"),
 o("Rindersteak mit Brokkoli & Kräuterbutter","0,85 Portion","1,15 Portion","~380 / ~460"),
 o("Omelett mit Spinat & Feta","0,85 Portion","1,15 Portion","~365 / ~445"),
 o("Hähnchen-Curry mit Blumenkohlreis","0,85 Portion","1,15 Portion","~370 / ~450"),
 o("Krautsalat mit Hähnchen (asiatisch)","0,85 Portion","1,15 Portion","~360 / ~440"),
 o("Puten-Gyros mit Krautsalat","0,85 Portion","1,15 Portion","~370 / ~450"),
 o("Zucchini-Lasagne mit Faschiertem","0,85 Portion","1,15 Portion","~380 / ~460"),
 o("Garnelen-Spinat-Pfanne","0,85 Portion","1,15 Portion","~360 / ~440"),
 o("Hähnchen-Pilz-Pfanne mit grünen Bohnen","0,85 Portion","1,15 Portion","~370 / ~450"),
 o("Rindfleisch-Brokkoli-Pfanne (asiatisch)","0,85 Portion","1,15 Portion","~370 / ~455"),
 o("Ofengemüse mit Feta & Ei","0,85 Portion","1,15 Portion","~370 / ~450"),
 o("Hühnersuppe mit viel Gemüse","1 großer Teller","1,5 Teller + 1 Scheibe Brot","~350 / ~440"),
 o("Gefüllte Zucchini mit Pute & Käse","1,5 Hälften","2,5 Hälften","~370 / ~450"),
]

# ================================================================== TRAINING
# Pro Trainingstag: SLOTS nach Muskelgruppe, je Slot mehrere Alternativen.
# Die App rotiert bei "Trainiert" durch die Alternativen -> jedes Mal etwas
# Neues, aber die Struktur (Beine / Ziehen / Druecken / Schulter+Arme / Bauch)
# bleibt gleich. Gelikte Uebungen (Daumen hoch) bleiben stehen.
GYM_A_SLOTS = [
 [EX("Beinpresse","3 × 10–12","Leg Press","Leg_Press"),
  EX("Beinstrecker (Maschine)","3 × 12","Leg Extensions","Leg_Extensions"),
  EX("Kniebeuge (Maschine)","3 × 10–12","Machine Squat","Lying_Machine_Squat"),
  EX("Goblet-Kniebeuge","3 × 10","Goblet Squat","Goblet_Squat",2),
  EX("Ausfallschritte (Kurzhantel)","3 × 10 je Bein","Dumbbell Lunges","Dumbbell_Lunges",2)],
 [EX("Latzug","3 × 10–12","Wide-Grip Lat Pulldown","Wide-Grip_Lat_Pulldown"),
  EX("Latzug eng","3 × 10–12","Close-Grip Lat Pulldown","Close-Grip_Front_Lat_Pulldown"),
  EX("Latzug (Untergriff)","3 × 10–12","Underhand Cable Pulldown","Underhand_Cable_Pulldowns"),
  EX("Rudern (Kurzhantel)","3 × 10 je Arm","Bent Over Two-Dumbbell Row","Bent_Over_Two-Dumbbell_Row",2)],
 [EX("Brustpresse (Maschine)","3 × 10–12","Chest Press (Machine)","Leverage_Chest_Press"),
  EX("Butterfly (Maschine)","3 × 12","Butterfly","Butterfly"),
  EX("Kabel-Brustpresse","3 × 12","Cable Chest Press","Cable_Chest_Press"),
  EX("Kabel-Brustpresse (schräg)","3 × 12","Incline Cable Chest Press","Incline_Cable_Chest_Press"),
  EX("Kurzhantel-Bankdrücken","3 × 10","Dumbbell Bench Press","Dumbbell_Bench_Press",2)],
 [EX("Schulterpresse (Maschine)","3 × 10","Shoulder Press (Machine)","Leverage_Shoulder_Press"),
  EX("Schulterdrücken (Maschine)","3 × 10","Machine Military Press","Machine_Shoulder_Military_Press"),
  EX("Seitheben am Kabel","3 × 12 je Seite","Cable Seated Lateral Raise","Cable_Seated_Lateral_Raise"),
  EX("Seitheben (Kurzhantel)","3 × 12","Side Lateral Raise","Side_Lateral_Raise",2),
  EX("Kurzhantel-Schulterdrücken","3 × 10","Dumbbell Shoulder Press","Dumbbell_Shoulder_Press",2)],
 [EX("Plank","3 × 20–30 s","Plank","Plank"),
  EX("Bauchmaschine","3 × 12","Ab Crunch Machine","Ab_Crunch_Machine"),
  EX("Kabel-Crunch","3 × 12","Cable Crunch","Cable_Crunch")],
]
GYM_B_SLOTS = [
 [EX("Beinpresse","3 × 10–12","Leg Press","Leg_Press"),
  EX("Hüftheben (Brücke)","3 × 15","Butt Lift (Bridge)","Butt_Lift_Bridge"),
  EX("Kniebeuge (Körpergewicht)","3 × 15","Bodyweight Squat","Bodyweight_Squat"),
  EX("Step-Ups (Kurzhantel)","3 × 10 je Bein","Dumbbell Step Ups","Dumbbell_Step_Ups",2),
  EX("Rumänisches Kreuzheben","3 × 10","Romanian Deadlift","Romanian_Deadlift",2),
  EX("Hüftheben (Langhantel)","3 × 12","Barbell Glute Bridge","Barbell_Glute_Bridge",2)],
 [EX("Beinbeuger (Maschine)","3 × 12","Lying Leg Curls","Lying_Leg_Curls"),
  EX("Beinbeuger sitzend","3 × 12","Seated Leg Curl","Seated_Leg_Curl"),
  EX("Beinbeuger stehend","3 × 12 je Bein","Standing Leg Curl","Standing_Leg_Curl"),
  EX("Wadenheben (Beinpresse)","3 × 15","Calf Press","Calf_Press_On_The_Leg_Press_Machine"),
  EX("Wadenheben sitzend","3 × 15","Seated Calf Raise","Seated_Calf_Raise")],
 [EX("Rudern (Maschine)","3 × 10–12","Seated Cable Rows","Seated_Cable_Rows"),
  EX("Reverse Flys (Maschine)","3 × 12","Reverse Machine Flyes","Reverse_Machine_Flyes"),
  EX("Rückenstrecker","3 × 12","Back Extensions","Hyperextensions_Back_Extensions"),
  EX("Face Pulls","3 × 15","Face Pull","Face_Pull",2)],
 [EX("Bizeps-Curls (Maschine)","3 × 12","Machine Bicep Curl","Machine_Bicep_Curl"),
  EX("Bizeps-Curls (Scottbank)","3 × 12","Machine Preacher Curls","Machine_Preacher_Curls"),
  EX("Hammer-Curls am Kabel","3 × 12","Cable Hammer Curls","Cable_Hammer_Curls_-_Rope_Attachment"),
  EX("Hammer-Curls (Kurzhantel)","3 × 12","Hammer Curls","Hammer_Curls",2)],
 [EX("Trizeps-Drücken (Kabel)","3 × 12","Triceps Pushdown","Triceps_Pushdown"),
  EX("Trizeps-Seil","3 × 12","Triceps Pushdown - Rope","Triceps_Pushdown_-_Rope_Attachment"),
  EX("Trizeps-Maschine","3 × 12","Machine Triceps Extension","Machine_Triceps_Extension")],
]
HOME_SLOTS_A = [
 [EX("Crunches","3 × 15","Crunches","Crunches"),
  EX("Sit-Ups","3 × 12","Sit-Up","Sit-Up"),
  EX("Cross-Body-Crunch","3 × 12 je Seite","Cross-Body Crunch","Cross-Body_Crunch"),
  EX("Zehen antippen","3 × 15","Toe Touchers","Toe_Touchers")],
 [EX("Beinheben (liegend)","3 × 12","Lying Leg Raise","Flat_Bench_Lying_Leg_Raise"),
  EX("Umgekehrte Crunches","3 × 12","Reverse Crunch","Reverse_Crunch"),
  EX("Flutter Kicks","3 × 20","Flutter Kicks","Flutter_Kicks"),
  EX("Klappmesser","3 × 10","Jackknife Sit-Up","Jackknife_Sit-Up",2)],
 [EX("Plank","3 × 20–30 s","Plank","Plank"),
  EX("Seitlicher Plank","2 × 20 s je Seite","Side Bridge","Side_Bridge"),
  EX("Käfer (Dead Bug)","3 × 10 je Seite","Dead Bug","Dead_Bug")],
 [EX("Mountain Climbers","3 × 20","Mountain Climbers","Mountain_Climbers"),
  EX("Bicycle-Crunch","3 × 20","Air Bike","Air_Bike"),
  EX("Russian Twist","3 × 20","Russian Twist","Russian_Twist",2),
  EX("Fersen antippen","3 × 20","Alternate Heel Touchers","Alternate_Heel_Touchers")],
]
HOME_SLOTS_B = [
 [EX("Hüftheben (Brücke)","3 × 15","Butt Lift (Bridge)","Butt_Lift_Bridge"),
  EX("Beckenkippen-Brücke","3 × 12","Pelvic Tilt Into Bridge","Pelvic_Tilt_Into_Bridge",2),
  EX("Kniebeuge (Körpergewicht)","3 × 15","Bodyweight Squat","Bodyweight_Squat")],
 [EX("Superman","3 × 12","Superman","Superman"),
  EX("Käfer (Dead Bug)","3 × 10 je Seite","Dead Bug","Dead_Bug"),
  EX("Seitliches Beinheben","3 × 15 je Seite","Side Leg Raises","Side_Leg_Raises")],
 [EX("Seitlicher Plank","2 × 20 s je Seite","Side Bridge","Side_Bridge"),
  EX("Plank","3 × 25–35 s","Plank","Plank"),
  EX("Mountain Climbers","3 × 20","Mountain Climbers","Mountain_Climbers")],
 [EX("Russian Twist","3 × 20","Russian Twist","Russian_Twist",2),
  EX("Bicycle-Crunch","3 × 20","Air Bike","Air_Bike"),
  EX("Stehendes Zehen-Antippen","3 × 15","Standing Toe Touches","Standing_Toe_Touches"),
  EX("Umgekehrte Crunches","3 × 12","Reverse Crunch","Reverse_Crunch")],
]

DAYS=["Mo","Di","Mi","Do","Fr","Sa","So"]

def load_likes():
    p=os.path.join(HERE,"likes.json")
    if os.path.exists(p):
        try: return json.load(open(p,encoding="utf-8"))
        except Exception: return {}
    return {}

def drop_only(pool, drop):
    drop=set(x.lower() for x in drop)
    kept=[x for x in pool if x["name"].lower() not in drop]
    return kept or pool   # nie ganz leer

def week_options(pool, boost, k=5):
    """Optionen fuer alle 7 Tage auf einmal.

    Pro Tag: 2 gelikte Gerichte + Rest. Beide Stroeme laufen ueber einen
    durchlaufenden Cursor durch die Woche - dadurch wiederholt sich nichts
    unnoetig (frueher sprang die Auswahl in Zweierschritten und landete alle
    zwei Tage wieder auf demselben Paar). Der Fuell-Strom nutzt den GANZEN
    Pool, nicht nur die ungelikten - sonst ist er bei vielen Favoriten zu
    klein fuer 7 Tage.
    """
    bset=set(x.lower() for x in boost)
    boosted=[x for x in pool if x["name"].lower() in bset]
    nb=min(2, len(boosted), max(0,k-2))
    bcur=WEEK % len(boosted) if boosted else 0
    fcur=(WEEK*3) % len(pool)
    days=[]
    for _ in range(7):
        day=[]
        for _ in range(nb):
            day.append(boosted[bcur % len(boosted)]); bcur+=1
        guard=0
        while len(day)<k and guard<4*len(pool):
            c=pool[fcur % len(pool)]; fcur+=1; guard+=1
            if c not in day: day.append(c)
        days.append(day[:k])
    return days

def build_day(slots, drop_ex, boost_ex, rot, easy=True):
    """Aus den Slot-Alternativen die Startauswahl bauen - dieselbe Logik wie
    in der App: Disgelikte raus, im Anfaenger-Modus nur lvl 1, Gelikte fix."""
    dset=set(x.lower() for x in drop_ex); bset=set(x.lower() for x in boost_ex)
    out=[]
    for i,alts in enumerate(slots):
        ok=[e for e in alts if e["name"].lower() not in dset] or alts
        if easy:
            simple=[e for e in ok if e.get("lvl",1)<=1]
            if simple: ok=simple
        liked=[e for e in ok if e["name"].lower() in bset]
        src=liked if liked else ok
        out.append(src[(rot+i)%len(src)])
    return out

def clean_slots(slots, drop_ex):
    """Disgelikte Uebungen kommen gar nicht erst ins Paket."""
    dset=set(x.lower() for x in drop_ex)
    out=[]
    for alts in slots:
        keep=[e for e in alts if e["name"].lower() not in dset]
        out.append(keep or alts)
    return out

def firestore_safe(obj, path="", bad=None):
    """Firestore lehnt Arrays DIREKT in Arrays ab (DocumentReference.set()
    schlaegt fehl: 'Nested arrays are not supported'). Alles, was die App in
    das geteilte Dokument schreibt, muss diese Pruefung bestehen."""
    if bad is None: bad=[]
    if isinstance(obj, list):
        for i,v in enumerate(obj):
            if isinstance(v, list): bad.append(path+"["+str(i)+"]")
            else: firestore_safe(v, path+"["+str(i)+"]", bad)
    elif isinstance(obj, dict):
        for k,v in obj.items(): firestore_safe(v, path+"."+str(k), bad)
    return bad

def main():
    likes=load_likes()
    bm=likes.get("boost_meals",[]); dm=likes.get("drop_meals",[])
    bx=likes.get("boost_ex",[]);    dx=likes.get("drop_ex",[])
    BF=drop_only(BREAKFAST,dm); LU=drop_only(LUNCH,dm)
    SN=drop_only(SNACKS,dm);    DI=drop_only(DINNER,dm)
    wk={"F":week_options(BF,bm), "M":week_options(LU,bm),
        "S":week_options(SN,bm), "A":week_options(DI,bm)}
    dayplan={}
    for i,d in enumerate(DAYS):
        dayplan[d]={sl:wk[sl][i] for sl in ("F","M","S","A")}

    program={}
    for key,label,slots in (("A","Gym 1 · Ganzkörper",GYM_A_SLOTS),
                            ("B","Gym 2 · Ganzkörper",GYM_B_SLOTS),
                            ("C","Zuhause · Bauch A",HOME_SLOTS_A),
                            ("D","Zuhause · Bauch B",HOME_SLOTS_B)):
        cs=clean_slots(slots,dx)
        # WICHTIG: Firestore kann KEINE Arrays direkt in Arrays speichern.
        # Darum jede Variantenliste in ein Objekt packen: [{"alts":[...]}, ...]
        program[key]={"label":label,"rot":WEEK,
                      "ex":build_day(cs,dx,bx,WEEK),
                      "slots":[{"alts":a} for a in cs]}
    training={"program":program}

    # Coverage-Sicherung: jede Tagesplan-Option braucht ein Rezept.
    have=set(r["name"].lower() for r in ALL)
    names=set(opt["name"] for d in DAYS for sl in ("F","M","S","A") for opt in dayplan[d][sl])
    missing=[n for n in names if n.lower() not in have]
    assert not missing, "Gericht ohne Rezept: "+repr(missing)
    pool_names=set(x["name"].lower() for x in BREAKFAST+LUNCH+SNACKS+DINNER)
    orphan=[r["name"] for r in ALL if r["name"].lower() not in pool_names]
    assert not orphan, "Rezept ohne Tagesplan-Option: "+repr(orphan)
    # Jeder Platz braucht auch im Anfaenger-Modus noch Auswahl zum Tauschen.
    thin=[]
    for key,day in program.items():
        for i,s in enumerate(day["slots"]):
            easy=[e for e in s["alts"] if e.get("lvl",1)<=1]
            if len(easy)<2: thin.append(key+"/Platz "+str(i+1)+": "+str(len(easy))+" Anfaengerübung(en)")
    assert not thin, "Zu wenig Anfaenger-Alternativen: "+repr(thin)

    packs={"rezepte":{"replaceMeals":True,"meals":ALL},
           "wochenplan":{"dayplan":dayplan},
           "training":{"training":training}}
    for name,data in packs.items():
        nested=firestore_safe(data)
        assert not nested, "Verschachtelte Arrays in "+name+".json (Firestore lehnt das ab): "+repr(nested[:5])
        json.dump(data, open(os.path.join(HERE,name+".json"),"w",encoding="utf-8"), ensure_ascii=False)
    print("KW",WEEK,"- Pakete erzeugt.")
    print("  Rezepte:",len(ALL),
          "(F",len(FRUEHSTUECK),"/ M",len(MITTAG),"/ S",len(SNACK),"/ A",len(ABEND),")")
    print("  Verschiedene Gerichte in der Woche:",len(names))
    for k,v in program.items():
        print("  ",k,v["label"],"->",[e["name"] for e in v["ex"]])

if __name__=="__main__":
    main()

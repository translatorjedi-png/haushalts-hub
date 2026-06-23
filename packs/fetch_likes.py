# -*- coding: utf-8 -*-
"""
Liest Andriys/Annas Likes aus Firestore (Doc haushalt/shared) per Service-Account
und schreibt packs/likes.json fuer generate.py.
- Tagesplan-Auswahl (dayplan.prefs, Slug-Keys) -> bevorzugte Gerichte (boost_meals).
- Trainings-Likes (training.prefs, 1/-1) -> boost_ex / drop_ex.
Faellt sauber durch (exit 0), wenn kein Service-Account/Doc vorhanden ist
-> dann laeuft generate.py nur mit Rotation (ohne Favoriten).
Aufruf: python packs/fetch_likes.py <pfad-zur-service-account.json>
"""
import sys, os, json

def bail(msg):
    print(msg); sys.exit(0)

sa = sys.argv[1] if len(sys.argv) > 1 else "sa.json"
if not os.path.exists(sa):
    bail("Kein Service-Account-File ("+sa+") -> ohne Favoriten.")
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    bail("firebase-admin nicht installiert -> ohne Favoriten.")
try:
    firebase_admin.initialize_app(credentials.Certificate(sa))
    db = firestore.client()
    data = db.collection("haushalt").document("shared").get().to_dict() or {}
except Exception as e:
    bail("Firestore-Lesen fehlgeschlagen ("+str(e)+") -> ohne Favoriten.")

# --- Gerichte: dayplan.prefs (Slug) ueber die Optionen zu Namen aufloesen ---
dp = data.get("dayplan", {}) or {}
slug2name = {}
for day, slots in (dp.get("days", {}) or {}).items():
    if not isinstance(slots, dict):
        continue
    for sk, slot in slots.items():
        for opt in (slot or {}).get("opts", []) or []:
            if opt.get("key") and opt.get("name"):
                slug2name[opt["key"]] = opt["name"]
fp = dp.get("prefs", {}) or {}
boost_meals = [slug2name[k] for k, v in fp.items() if v and v > 0 and k in slug2name]

# --- Training: prefs sind nach kleingeschriebenem Namen gekeyt (1 / -1) ---
tp = (data.get("training", {}) or {}).get("prefs", {}) or {}
boost_ex = [k for k, v in tp.items() if v and v > 0]
drop_ex  = [k for k, v in tp.items() if v and v < 0]

likes = {
    "boost_meals": sorted(set(boost_meals)),
    "drop_meals": [],
    "boost_ex": sorted(set(boost_ex)),
    "drop_ex": sorted(set(drop_ex)),
}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(likes, open(os.path.join(here, "likes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("likes.json geschrieben:", json.dumps(likes, ensure_ascii=False))

import json, os
from datetime import datetime, timedelta

DATA_FILE = "grooming_data.json"
SERVICES = {"haircut": 60, "bath": 60}  # each bath and haircut is 1 hour
MAX_CHOICES = 10  # keeps the slot list short and customer-friendly

# converts time to AM/PM
def _fmt_ampm(hhmm: str) -> str:
    dt = datetime.strptime(hhmm, "%H:%M")
    return dt.strftime("%I:%M %p").lstrip("0")

# starting with 5 groomers with 8 hour shifts
DEFAULT_GROOMERS = [
    {"id": 1, "name": "Alex",   "work_start": "09:00", "work_end": "17:00"},
    {"id": 2, "name": "Riley",  "work_start": "09:00", "work_end": "17:00"},
    {"id": 3, "name": "Sam",    "work_start": "10:00", "work_end": "18:00"},
    {"id": 4, "name": "Jordan", "work_start": "08:00", "work_end": "16:00"},
    {"id": 5, "name": "Taylor", "work_start": "09:30", "work_end": "17:30"}
]

# since we are aiming for a more customer based app i only implemented 5 groomers without the ability to add more.
# storage
DEFAULT_DATA = {"groomers": DEFAULT_GROOMERS.copy(), "appointments": []}

# loads saved data, checks if file exist, if it does not it will create the file and input default groomer info
def save_db(db):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

def load_db():
    if not os.path.exists(DATA_FILE):
        save_db(DEFAULT_DATA)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)
    if not db.get("groomers"):
        db["groomers"] = DEFAULT_GROOMERS.copy()
        save_db(db)
    return db

# Helpers
def _dt(date, time):
    return datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

def _overlap(s1, e1, s2, e2):
    return s1 < e2 and s2 < e1

def _today():
    return datetime.now().strftime('%Y-%m-%d')

# prevents double booking
def can_book(groomer_id, date, start, end):
    db = load_db()
    new_s, new_e = _dt(date, start), _dt(date, end)
    for a in db["appointments"]:
        if a["groomer_id"] == groomer_id and a["date"] == date and a["status"] == "booked":
            s, e = _dt(a["date"], a["start"]), _dt(a["date"], a["end"])
            if _overlap(new_s, new_e, s, e):
                return False
    return True

# finds open slots for a groomer
def find_slots(groomer_id, date):
    db = load_db()
    g = next((x for x in db["groomers"] if x["id"] == groomer_id), None)
    if not g:
        return []
    day_start = _dt(date, g.get("work_start", "09:00"))
    day_end = _dt(date, g.get("work_end", "17:00"))
    existing = [
        (_dt(a["date"], a["start"]), _dt(a["date"], a["end"]))
        for a in db["appointments"]
        if a["groomer_id"] == groomer_id and a["date"] == date and a["status"] == "booked"
    ]
    step, block = timedelta(minutes=30), timedelta(minutes=60)
    out, cur = [], day_start
    while cur + block <= day_end:
        if all(not _overlap(cur, cur + block, s, e) for s, e in existing):
            out.append(f"{cur.strftime('%H:%M')}-{(cur + block).strftime('%H:%M')}")
        cur += step
    return out

# aggregates all open slots for today
def list_today_open_slots():
    db = load_db()
    date = _today()
    slots = []
    for g in db["groomers"]:
        for rng in find_slots(g["id"], date):
            start_raw, end_raw = rng.split('-')
            label = f"{g['name']} {_fmt_ampm(start_raw)}–{_fmt_ampm(end_raw)}"
            slots.append({
                "groomer_id": g["id"],
                "groomer_name": g["name"],
                "start_raw": start_raw,
                "end_raw": end_raw,
                "label": label
            })
    slots.sort(key=lambda x: x["start_raw"])
    total = len(slots)
    return slots[:MAX_CHOICES], total

# creates and saves an appointment
def book_appointment(pet_name, groomer_id, service, date, start):
    db = load_db()
    duration = SERVICES.get(service, 60)
    s_dt = _dt(date, start)
    e_dt = s_dt + timedelta(minutes=duration)
    end = e_dt.strftime('%H:%M')
    if not can_book(groomer_id, date, start, end):
        print("! Overlaps existing appointment")
        return
    appt = {
        "id": pet_name,
        "pet_id": pet_name,
        "groomer_id": groomer_id,
        "service": service,
        "date": date,
        "start": start,
        "end": end,
        "status": "booked"
    }
    db["appointments"].append(appt)
    save_db(db)
    start_disp, end_disp = _fmt_ampm(start), _fmt_ampm(end)
    gname = next((g["name"] for g in db["groomers"] if g["id"] == groomer_id), f"GID {groomer_id}")
    print(f"✓ Booked {service} for {pet_name} with {gname} at {start_disp}–{end_disp} today!")

# cancels appointment by pet name
def cancel_appointment(pet_name):
    db = load_db()
    for a in db["appointments"]:
        if a["pet_id"] == pet_name and a["status"] == "booked":
            a["status"] = "cancelled"
            save_db(db)
            print(f"✓ Cancelled {pet_name}'s appointment")
            return
    print("! No active appointment found for that pet name")

# gets and prints today's schedule
def get_today_schedule():
    db = load_db()
    today = _today()
    items = []
    for a in db["appointments"]:
        # Only include actively booked appointments (hide cancelled)
        if a.get("date") == today and a.get("status") == "booked":
            gname = next(
                (g["name"] for g in db["groomers"] if g["id"] == a["groomer_id"]),
                f"GID {a['groomer_id']}"
            )
            items.append({
                "start": a["start"],
                "end": a["end"],
                "start_disp": _fmt_ampm(a["start"]),
                "end_disp": _fmt_ampm(a["end"]),
                "groomer": gname,
                "pet": a.get("pet_id", ""),
                "service": a.get("service", "")
            })
    items.sort(key=lambda x: x["start"])
    return items

def show_today_schedule():
    items = get_today_schedule()
    today = _today()
    if not items:
        print(f"(no appointments today: {today})")
        return
    print(f"Today's schedule ({today}):")
    for i, it in enumerate(items, start=1):
        print(f" {i}) {it['start_disp']}–{it['end_disp']}  {it['groomer']}  {it['pet']}  {it['service']}")

# display menu
def menu():
    while True:
        print("""
==== Grooming Scheduler (Customer) ====
1) Book a 1-hour appointment (haircut/bath)
2) Show today's schedule
3) Cancel appointment (by pet name)
0) Exit
""")
        c = input("Choose: ").strip()
        if c == "1":
            service = input("Service (haircut/bath): ").strip().lower()
            if service not in SERVICES:
                print("! Invalid service"); continue
            today = _today()
            slots, total = list_today_open_slots()
            if not slots:
                print(f"(no available slots today: {today})"); continue
            print(f"Pick a slot for today ({today}):")
            for i, s in enumerate(slots, start=1):
                print(f" {i}) {s['label']}")
            if total > len(slots):
                print(f" ...and {total - len(slots)} more later today")
            try:
                pick = int(input("Choose #: ").strip())
                chosen = slots[pick - 1]
            except (ValueError, IndexError):
                print("! Invalid choice"); continue
            pet_name = input("Enter pet name: ").strip()
            book_appointment(pet_name, chosen['groomer_id'], service, today, chosen['start_raw'])
        elif c == "2":
            show_today_schedule()
        elif c == "3":
            pet_name = input("Enter pet name to cancel: ").strip()
            cancel_appointment(pet_name)
        elif c == "0":
            break
        else:
            print("! Invalid option")

if __name__ == "__main__":
    load_db()
    menu()

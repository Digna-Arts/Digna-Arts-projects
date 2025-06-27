import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import os

memory = {}
NOTIZ_ORDNER = "core_notizen"

# Stelle sicher, dass der Notiz-Ordner existiert
if not os.path.exists(NOTIZ_ORDNER):
    os.makedirs(NOTIZ_ORDNER)

def show_help():
    print("""
🧠 Core Assistent – Befehle
----------------------------
stopuhr                  : Stopuhr starten (Enter zum stoppen)
timer <sekunden>         : Timer stellen, z.B. timer 60
wecker <hh:mm>           : Wecker stellen, z.B. wecker 07:30
merke key = value        : Info merken, z.B. merke name = Jan
was ist <key>            : Gemerkte Info abrufen
notiz neue <name>        : Neue Notiz anlegen
notiz schreiben <name>   : Notiz bearbeiten (Terminal)
notiz lesen <name>       : Notiz anzeigen
notiz löschen <name>     : Notiz löschen
notiz liste              : Alle Notizen anzeigen
help                     : Diese Hilfe anzeigen
exit                     : Core beenden
""")

def popup_message(text):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Core Alarm", text)
    root.destroy()

def start_stopuhr():
    print("⏱️ Stopuhr gestartet. Drücke Enter zum Stoppen.")
    start = time.time()
    input()
    end = time.time()
    dauer = end - start
    print(f"⏱️ Gestoppte Zeit: {round(dauer, 2)} Sekunden")

def start_timer(sekunden):
    def countdown():
        print(f"⏳ Timer läuft für {sekunden} Sekunden...")
        time.sleep(sekunden)
        print("⏰ Zeit ist um!")
        popup_message("⏰ Timer fertig!")
    threading.Thread(target=countdown).start()

def start_wecker(uhrzeit):
    def alarm():
        print(f"🔔 Wecker gesetzt auf {uhrzeit}.")
        while True:
            jetzt = datetime.now().strftime("%H:%M")
            if jetzt == uhrzeit:
                print("🔔 WECKER! Es ist jetzt " + jetzt)
                popup_message(f"🔔 Wecker! Es ist jetzt {jetzt}")
                break
            time.sleep(10)
    threading.Thread(target=alarm).start()

def dateipfad(name):
    # sichere Dateiname + Pfad für Notiz
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip()
    return os.path.join(NOTIZ_ORDNER, f"{safe_name}.txt")

def notiz_neu(name):
    pfad = dateipfad(name)
    if os.path.exists(pfad):
        print(f"⚠️ Notiz '{name}' existiert schon.")
        return
    with open(pfad, "w", encoding="utf-8") as f:
        f.write("")  # leere Notiz
    print(f"✅ Notiz '{name}' angelegt.")

def notiz_lesen(name):
    pfad = dateipfad(name)
    if not os.path.exists(pfad):
        print(f"⚠️ Notiz '{name}' nicht gefunden.")
        return
    with open(pfad, "r", encoding="utf-8") as f:
        inhalt = f.read()
    print(f"--- Notiz '{name}': ---\n{inhalt}\n----------------------")

def notiz_schreiben(name):
    pfad = dateipfad(name)
    if not os.path.exists(pfad):
        print(f"⚠️ Notiz '{name}' nicht gefunden.")
        return
    print(f"✍️ Schreibe Notiz '{name}'. Tippe 'ENDE' in neuer Zeile zum Speichern.")
    inhalt = []
    while True:
        zeile = input()
        if zeile.strip().upper() == "ENDE":
            break
        inhalt.append(zeile)
    with open(pfad, "w", encoding="utf-8") as f:
        f.write("\n".join(inhalt))
    print(f"✅ Notiz '{name}' gespeichert.")

def notiz_loeschen(name):
    pfad = dateipfad(name)
    if not os.path.exists(pfad):
        print(f"⚠️ Notiz '{name}' nicht gefunden.")
        return
    os.remove(pfad)
    print(f"🗑️ Notiz '{name}' gelöscht.")

def notiz_liste():
    dateien = [f for f in os.listdir(NOTIZ_ORDNER) if f.endswith(".txt")]
    if not dateien:
        print("ℹ️ Keine Notizen gefunden.")
        return
    print("📒 Notizen:")
    for datei in dateien:
        print(" - " + datei[:-4])  # ohne .txt

def run_core():
    print("🧠 Willkommen bei Core – deinem persönlichen Assistenten!")
    print("Tipp 'help' für Hilfe. 'exit' beendet ihn.")

    while True:
        user_input = input("Du: ").strip()

        # alles klein für Befehle, Groß-/Kleinschreibung für Notiznamen behalten
        user_input_lower = user_input.lower()

        if user_input_lower == "exit":
            print("Core: Bis bald, Jan 😌")
            break

        if user_input_lower == "help":
            show_help()
            continue

        if user_input_lower == "stopuhr":
            start_stopuhr()
            continue

        if user_input_lower.startswith("timer "):
            try:
                sek = int(user_input_lower.split()[1])
                start_timer(sek)
            except:
                print("⚠️ Ungültige Sekundenzahl.")
            continue

        if user_input_lower.startswith("wecker "):
            try:
                uhrzeit = user_input_lower.split()[1]
                datetime.strptime(uhrzeit, "%H:%M")
                start_wecker(uhrzeit)
            except:
                print("⚠️ Format: wecker 07:30")
            continue

        if user_input_lower.startswith("merke "):
            parts = user_input[6:].split("=", 1)
            if len(parts) == 2:
                key, val = parts[0].strip(), parts[1].strip()
                memory[key] = val
                print(f"💾 Gespeichert: {key} = {val}")
            else:
                print("⚠️ Beispiel: merke name = Jan")
            continue

        if user_input_lower.startswith("was ist "):
            key = user_input[8:].strip()
            if key in memory:
                print(f"🔍 {key} = {memory[key]}")
            else:
                print("❓ Nicht gefunden. Nutze 'merke' zuerst.")
            continue

        # Notiz-Befehle
        if user_input_lower.startswith("notiz "):
            befehl = user_input_lower.split()
            if len(befehl) < 2:
                print("⚠️ Nutze: notiz neue/lesen/schreiben/löschen/liste ...")
                continue
            aktion = befehl[1]

            if aktion == "neue" and len(befehl) >= 3:
                name = user_input.split(" ", 2)[2]
                notiz_neu(name)
                continue
            elif aktion == "lesen" and len(befehl) >= 3:
                name = user_input.split(" ", 2)[2]
                notiz_lesen(name)
                continue
            elif aktion == "schreiben" and len(befehl) >= 3:
                name = user_input.split(" ", 2)[2]
                notiz_schreiben(name)
                continue
            elif aktion == "löschen" and len(befehl) >= 3:
                name = user_input.split(" ", 2)[2]
                notiz_loeschen(name)
                continue
            elif aktion == "liste":
                notiz_liste()
                continue
            else:
                print("⚠️ Unbekannte Notiz-Aktion oder Name fehlt.")
                continue

        print("Core: Das habe ich noch nicht gelernt. Tippe help für Hilfe")

if __name__ == "__main__":
    run_core()

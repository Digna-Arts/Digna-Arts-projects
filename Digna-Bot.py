import re
import os

def show_help():
    print("""
Core - Hilfe Übersicht:

- help                  : Diese Hilfe anzeigen
- exit                  : Core beenden
- was ist <Matheaufgabe>: Rechenaufgabe auswerten (z.B. was ist 1+1?)
- merke key = value     : Eine Info merken (z.B. merke name = Jan)
- was ist <key>         : Gespeicherte Info abfragen
- öffne <dateipfad>     : Text- oder Code-Datei öffnen und anzeigen
- notiere <dateiname>   : Notiz schreiben und speichern (folgt Eingabe)
- variable              : Erklärung zu Variablen in Python
- funktion              : Erklärung zu Funktionen in Python
- liste                 : Erklärung zu Listen in Python
- klasse / objekt       : Erklärung zu Klassen in Python
- schleife              : Erklärung zu Schleifen in Python
""")

def read_file(filepath):
    if not os.path.isfile(filepath):
        print("Core: Datei nicht gefunden.")
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"--- Inhalt von {filepath} ---\n")
        print(content)
        print(f"\n--- Ende von {filepath} ---")
    except Exception as e:
        print(f"Core: Fehler beim Lesen der Datei: {e}")

def write_note(filename):
    print(f"Core: Schreib jetzt deine Notiz. Beende mit einer leeren Zeile.")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    content = "\n".join(lines)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Core: Notiz in '{filename}' gespeichert.")
    except Exception as e:
        print(f"Core: Fehler beim Speichern: {e}")

def coding_assistant():
    print("Core - Dein Coding Assistent (Terminal)")
    print("Tippe 'help' für Befehle. 'exit' beendet Core.\n")

    memory = {}

    while True:
        user_input = input("Du: ").strip()

        if user_input.lower() == "exit":
            print("Core: Bis zum nächsten Mal!")
            break

        if user_input.lower() == "help":
            show_help()
            continue

        # Merke Info
        if user_input.lower().startswith("merke "):
            key_val = user_input[6:].split("=", 1)
            if len(key_val) == 2:
                key, val = key_val[0].strip(), key_val[1].strip()
                memory[key] = val
                print(f"Core: Gelernt: {key} = {val}")
            else:
                print("Core: Schreib so: merke name = Jan")
            continue

        # Abfrage gemerkter Info
        if user_input.lower().startswith("was ist "):
            key = user_input[8:].strip()
            if key in memory:
                print(f"Core: {key} ist {memory[key]}")
                continue

            # Matheaufgabe erkennen und auswerten
            mathe_match = re.match(r"was ist ([\d\+\-\*\/\(\)\.\s]+)\??", user_input.lower())
            if mathe_match:
                expr = mathe_match.group(1)
                try:
                    allowed_chars = "0123456789+-*/(). "
                    if all(c in allowed_chars for c in expr):
                        result = eval(expr)
                        print(f"Core: Das Ergebnis ist {result}")
                    else:
                        print("Core: Ungültige Zeichen in der Rechnung.")
                except Exception:
                    print("Core: Fehler bei der Berechnung.")
                continue

            print("Core: Das weiß ich nicht. Merk es mir doch mit 'merke'.")
            continue

        # Datei öffnen
        if user_input.lower().startswith("öffne "):
            filepath = user_input[6:].strip()
            read_file(filepath)
            continue

        # Notiz schreiben und speichern
        if user_input.lower().startswith("notiere "):
            filename = user_input[8:].strip()
            if not filename:
                print("Core: Gib bitte einen Dateinamen an, z.B. notiere notiz.txt")
                continue
            write_note(filename)
            continue

        # Programmier-Erklärungen
        lcase = user_input.lower()
        if "variable" in lcase:
            print("Core: Variablen in Python definierst du so:\n  x = 5\n  name = 'Jan'\nSie sind dynamisch typisiert.")
            continue
        if "funktion" in lcase:
            print("Core: Funktionen definierst du so:\n  def meine_funktion(param):\n    print(param)\n\nSie helfen dir, Code besser zu strukturieren.")
            continue
        if "liste" in lcase:
            print("Core: Listen sind geordnete Sammlungen:\n  meine_liste = [1, 2, 3, 'Text']\nZugriff z.B.: meine_liste[0]")
            continue
        if "klasse" in lcase or "objekt" in lcase:
            print("Core: Klassen definieren Objekte:\n  class Auto:\n    def __init__(self, farbe):\n      self.farbe = farbe\n\n  mein_auto = Auto('rot')")
            continue
        if "schleife" in lcase:
            print("Core: Schleifen erlauben Wiederholungen:\n  for i in range(5):\n    print(i)\n  while schleifen laufen solange Bedingung wahr ist.")
            continue

        print("Core: Sorry, das weiß ich noch nicht. Frag mich was zum Programmieren!")

if __name__ == "__main__":
    coding_assistant()

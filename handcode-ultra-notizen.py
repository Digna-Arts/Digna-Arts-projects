import random
import string
import json
import base64
import os
import hashlib

def generate_dynamic_key(text):
    chars = set(text.lower())
    key = {}
    used = set()

    for c in chars:
        while True:
            code = ''.join(random.choices(string.ascii_lowercase, k=5))
            if code not in used:
                key[c] = code
                used.add(code)
                break
    return key

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def encrypt(text, password):
    text = text.lower()
    key = generate_dynamic_key(text)
    encrypted = ''.join(key.get(c, c) for c in text)
    key_json = json.dumps(key)
    key_b64 = base64.b64encode(key_json.encode()).decode()
    pw_hash = hash_password(password)
    # Speichere Passwort-Hash und Schlüssel zusammen mit verschlüsseltem Text
    return pw_hash + '|' + key_b64 + '|' + encrypted

def decrypt(data, password):
    try:
        pw_hash_stored, key_b64, encrypted = data.split('|', 2)
        pw_hash_input = hash_password(password)
        if pw_hash_stored != pw_hash_input:
            return "[Falsches Passwort]"
        key_json = base64.b64decode(key_b64.encode()).decode()
        key = json.loads(key_json)
        reverse_key = {v: k for k, v in key.items()}
        decrypted = ''
        for i in range(0, len(encrypted), 5):
            chunk = encrypted[i:i+5]
            decrypted += reverse_key.get(chunk, '?')
        return decrypted
    except Exception as e:
        return f"[Fehler beim Entschlüsseln] {e}"

def save_note(filename, content, password):
    encrypted = encrypt(content, password)
    with open(filename, "w") as f:
        f.write(encrypted)
    print(f"✅ Notiz gespeichert in '{filename}'.")

def load_note(filename, password):
    if not os.path.exists(filename):
        print("❌ Datei nicht gefunden.")
        return
    with open(filename, "r") as f:
        data = f.read()
    print("\n🔓 Entschlüsselte Notiz:\n")
    print(decrypt(data, password))

if __name__ == "__main__":
    while True:
        print("\n📝 Kryptonotizblock mit Passwortschutz")
        print("1. Neue Notiz schreiben")
        print("2. Notiz lesen")
        print("3. Beenden")
        wahl = input("Auswahl: ")
        
        if wahl == '1':
            text = input("Notiz eingeben:\n> ")
            datei = input("Dateiname (z.B. notiz.txt): ")
            pw = input("Passwort zum Verschlüsseln: ")
            save_note(datei, text, pw)
        elif wahl == '2':
            datei = input("Dateiname (z.B. notiz.txt): ")
            pw = input("Passwort zum Entschlüsseln: ")
            load_note(datei, pw)
        elif wahl == '3':
            break
        else:
            print("Ungültige Eingabe.")

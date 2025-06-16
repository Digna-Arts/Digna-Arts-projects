import random
import string
import json
import base64

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

def encrypt(text):
    text = text.lower()
    key = generate_dynamic_key(text)
    encrypted = ''.join(key.get(c, c) for c in text)

    # Schlüssel als JSON und dann base64 codieren
    key_json = json.dumps(key)
    key_b64 = base64.b64encode(key_json.encode()).decode()

    return key_b64 + '|' + encrypted  # Schlüssel + '|' + codierter Text

def decrypt(data):
    try:
        key_b64, encrypted = data.split('|', 1)
        key_json = base64.b64decode(key_b64.encode()).decode()
        key = json.loads(key_json)
    except Exception as e:
        return f"Fehler beim Parsen des Schlüssels: {e}"

    reverse_key = {v: k for k, v in key.items()}

    decrypted = ''
    for i in range(0, len(encrypted), 5):
        chunk = encrypted[i:i+5]
        decrypted += reverse_key.get(chunk, '?')
    return decrypted

if __name__ == "__main__":
    while True:
        mode = input("\n(e) Verschlüsseln | (d) Entschlüsseln | (exit): ").lower()
        if mode == 'exit':
            break
        elif mode == 'e':
            text = input("Text eingeben: ")
            print("\n🔒 Ergebnis:\n" + encrypt(text))
        elif mode == 'd':
            data = input("Verschlüsselten Text inkl. Schlüssel eingeben: ")
            print("\n🔓 Entschlüsselt:\n" + decrypt(data))
        else:
            print("Ungültige Eingabe.")

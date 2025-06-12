def binary_to_text(binary_str):
    try:
        chars = binary_str.strip().split()
        return ''.join(chr(int(b, 2)) for b in chars)
    except ValueError:
        return "⚠️ Ungültige Eingabe! Stelle sicher, dass du nur 8-Bit-Binärwerte (z. B. 01000001) eingibst, getrennt durch Leerzeichen."

def main():
    print("🔢 ➜ 💬 Binär-zu-Text-Decoder")

    user_input = input("Binär code:")
    result = binary_to_text(user_input)

    print("\nErkannter Text:")
    print(result)

    save = input("\nMöchtest du das Ergebnis als Datei speichern? (j/n): ").lower()
    if save == 'j':
        with open("text_output.txt", "w", encoding="utf-8") as f:
            f.write(result)
        print("💾 Gespeichert als 'text_output.txt'.")

if __name__ == "__main__":
    main()

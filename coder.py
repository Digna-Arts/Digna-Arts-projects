def text_to_binary(text):
    return ' '.join(format(ord(char), '08b') for char in text)

def main():
    print("💬 ➜ 🔢 Text-zu-Binär-Converter")
    user_input = input("Gib deinen Text ein: ")
    binary_result = text_to_binary(user_input)

    print("\nBinär-Code:")
    print(binary_result)

    save = input("\nMöchtest du das Ergebnis als Datei speichern? (j/n): ").lower()
    if save == 'j':
        with open("binary_output.txt", "w", encoding="utf-8") as f:
            f.write(binary_result)
        print("💾 Gespeichert als 'binary_output.txt'.")

if __name__ == "__main__":
    main()

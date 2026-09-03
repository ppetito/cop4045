def caesar_cipher(text, shift):
    """Encrypt text by shifting its alphabetic characters.

    Args:
        text: The string to encrypt.
        shift: The number of alphabet positions to shift each letter.

    Returns:
        The encrypted string, with original letter casing and non-alphabetic
        characters preserved.
    """
    encrypted_text = ""

    for character in text:
        if "A" <= character <= "Z":
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            index = alphabet.index(character)
            encrypted_text += alphabet[(index + shift) % len(alphabet)]
        elif "a" <= character <= "z":
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            index = alphabet.index(character)
            encrypted_text += alphabet[(index + shift) % len(alphabet)]
        else:
            encrypted_text += character

    return encrypted_text


def caesar_decipher(ciphertext, shift):
    """Decrypt Caesar cipher text using the original shift amount.

    Args:
        ciphertext: The encrypted string to decrypt.
        shift: The number of alphabet positions used during encryption.

    Returns:
        The original plaintext string.
    """
    return caesar_cipher(ciphertext, -shift)


def letter_frequency(text):
    """Count occurrences of each alphabet letter in text.

    Args:
        text: The string whose letters will be counted.

    Returns:
        A dictionary mapping every lowercase letter from 'a' to 'z' to its
        count, ignoring case and non-alphabetic characters.
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    frequencies = {}

    for letter in alphabet:
        frequencies[letter] = 0

    for character in text.lower():
        if character in alphabet:
            frequencies[character] += 1

    return frequencies


def main():
    """Run a menu-driven Caesar cipher terminal program.
    The program lets users encrypt a message, decrypt a message, or quit.
    """
    while True:
        print("\nCaesar Cipher Menu")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            message = input("Enter a message to encrypt: ")
            try:
                shift = int(input("Enter the shift value: "))
            except ValueError:
                print("Please enter a whole number for the shift value.")
                continue

            print("Ciphered text:", caesar_cipher(message, shift))
            print("Letter frequency of the original message:")
            frequencies = letter_frequency(message)
            for letter in "abcdefghijklmnopqrstuvwxyz":
                print(letter + ":", frequencies[letter])
        elif choice == "2":
            ciphertext = input("Enter a message to decrypt: ")
            try:
                shift = int(input("Enter the shift value: "))
            except ValueError:
                print("Please enter a whole number for the shift value.")
                continue

            print("Deciphered text:", caesar_decipher(ciphertext, shift))
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()

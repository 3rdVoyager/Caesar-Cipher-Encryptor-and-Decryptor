print("Welcome to CaesarCracker! This program allows you to encrypt and decrypt messages using the Caesar cipher. It also includes a feature to attempt to decrypt messages with an unknown shift by trying all possible shifts and checking for plausibility based on common words and letter patterns.")

# Function to get user input for mode, message, and shift
def get_input():
    start=input("Type 'c' to start a new session, 'i' to see instructions, or 'q' to quit: ")
    # Handle user input for starting, instructions, or quitting the program
    if start.lower() == 'q':
        print("Goodbye!")
        print("Created by Joshua Cheng.")
        print("Program exited.")
        exit()
    elif start.lower() == 'i':
        print()
        print("Instructions:")
        print("1. Choose to encrypt or decrypt.")
        print("2. Enter a message.")
        print("3. Enter a shift value (1-25).")
        print("4. When decrypting, if the shift is unknown, enter 0.")
        return get_input()
    elif start.lower() == 'c':
        mode = input("Would you like to encrypt or decrypt? (e/d): ").lower()
        if mode not in ['e', 'd']:
            print("Invalid choice. Please choose 'e' for encrypt or 'd' for decrypt.")
            return get_input()
        message = input("Enter a message: ")
        if mode == 'd':
            shift = int(input("Enter shift (1-25). If shift is unknown, enter 0: "))
        else:
            shift = int(input("Enter shift (1-25): "))
        if shift < 0 or shift > 25:
            print("Invalid shift. Please enter a shift between 1 and 25.")
            return get_input()
        return mode, message, shift
    else:
        print("Invalid input. Please try again.")
        return get_input()

# Function to perform Caesar cipher encryption or decryption based on the mode
def caesar(text, shift, mode):
    result = ""
    # Loop through each character in the input text
    for char in text:
        # Check if the character is an alphabetic character
        if char.isalpha():
            base = ord("a") if char.islower() else ord("A")

            # Encrypt or decrypt the character based on the mode
            if mode == 'e':
                result += chr((ord(char) - base + shift) % 26 + base)
            elif mode == 'd':
                if shift == 0:
                    # If shift is unknown, try all possible shifts and print the results
                    force_decrypt(text)
                    return
                else:
                    result += chr((ord(char) - base - shift) % 26 + base)
        
        # If the character is not alphabetic, add it to the result without changing it
        else:
            result += char
    # Print the resulting encrypted or decrypted message
    print("Result:", result)
    print("Would you like to continue?")
 
def force_decrypt(text):
    found=False
    print("Attempting to force decrypt the message with all possible shifts.")
    print("The most plausible decryptions will be displayed below:")
    print()
    for shift in range(1, 26):
        decrypted_message = ""
        for char in text:
            if char.isalpha():
                base = ord("a") if char.islower() else ord("A")
                decrypted_message += chr((ord(char) - base - shift) % 26 + base)
            else:
                decrypted_message += char
        if check_plausibility(decrypted_message):
            print(f"Shift of {shift}: {decrypted_message}")
            found=True
    if found == False:
        print("No plausible decryptions found. Message may be too short to filter reliably.")
        if input("Would you like to see all possible decryptions? (y/n): ").lower() == 'y':
            for shift in range(1, 26):
                decrypted_message = ""
                for char in text:
                    if char.isalpha():
                        base = ord("a") if char.islower() else ord("A")
                        decrypted_message += chr((ord(char) - base - shift) % 26 + base)
                    else:
                        decrypted_message += char
                print(f"Shift of {shift}: {decrypted_message}")
            print("Would you like to continue?")
            get_input()
        else:
            get_input()


def check_plausibility(decrypted_message):
    # This function checks for common words or patterns in the decrypted message
    common_words = ["the", "and", "is", "in", "it", "you", "that"]
    for word in common_words:
        if word in decrypted_message.lower():
            return True
    letters = [char for char in decrypted_message if char.isalpha()]
    # Check for a reasonable number of vowels in a row (not more than 3)
    vowel_run = 0
    for v in letters:
        if v in 'aeiou':
            vowel_run += 1
            if vowel_run > 3:
                return False
        else:
            vowel_run = 0
    # Check for a reasonable number of consonants in a row (not more than 5)
    consonant_run = 0
    for c in letters:
        if c not in 'aeiou':
            consonant_run += 1
            if consonant_run > 5:
                return False
        else:
            consonant_run = 0
    return True


# Main loop to continuously get user input and perform encryption/decryption until the user decides to quit
while True:
    mode, message, shift = get_input()
    caesar(message, shift, mode)

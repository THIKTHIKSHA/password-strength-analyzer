import re
import random
import string
import hashlib
import json
import os

# File to store password history
HISTORY_FILE = "password_history.json"

# Common weak passwords list
COMMON_PASSWORDS = [
    "123456", "password", "123456789", "12345",
    "12345678", "qwerty", "abc123", "password1"
]

# Load password history
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# Save password history
def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

# Hash password for secure storage
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Check password strength
def check_strength(password):
    score = 0
    feedback = []

    # Length check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    # Digits
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers.")

    # Special characters
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add special characters.")

    # Common password check
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("Password is too common.")
        score = 0

    return score, feedback

# Suggest strong password
def suggest_password(length=12):
    all_chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(all_chars) for _ in range(length))

# Check reuse
def is_reused(password, history):
    hashed = hash_password(password)
    return hashed in history

# Main function
def main():
    history = load_history()

    password = input("Enter your password: ")

    # Check reuse
    if is_reused(password, history):
        print("\n❌ You have already used this password before!")
        return

    score, feedback = check_strength(password)

    print("\nPassword Strength Analysis:")
    print("--------------------------")

    if score <= 2:
        print("🔴 Weak Password")
    elif score == 3 or score == 4:
        print("🟡 Moderate Password")
    else:
        print("🟢 Strong Password")

    # Show feedback
    if feedback:
        print("\nSuggestions:")
        for f in feedback:
            print("-", f)

    # Suggest new password if weak
    if score <= 2:
        print("\n💡 Suggested Strong Password:", suggest_password())

    # Save password
    history.append(hash_password(password))
    save_history(history)

    print("\n✅ Password stored securely (hashed).")

# Run program
if __name__ == "__main__":
    main()
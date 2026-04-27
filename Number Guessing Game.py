import random

def play_game():
    print("\n🎯 Welcome to Number Guessing Game")

    # Difficulty levels
    print("\nSelect Difficulty Level:")
    print("1. Easy (1 to 50)")
    print("2. Medium (1 to 100)")
    print("3. Hard (1 to 200)")

    choice = input("Enter choice (1/2/3): ")

    if choice == "1":
        low, high = 1, 50
    elif choice == "2":
        low, high = 1, 100
    elif choice == "3":
        low, high = 1, 200
    else:
        print("Invalid choice, defaulting to Medium")
        low, high = 1, 100

    number = random.randint(low, high)
    attempts = 0

    print(f"\nGuess a number between {low} and {high}")

    while True:
        guess = int(input("Enter your guess: "))
        attempts += 1

        if guess < number:
            print("📉 Too low!")
        elif guess > number:
            print("📈 Too high!")
        else:
            print(f"🎉 Correct! You guessed it in {attempts} attempts.")
            return attempts  # return attempts for best score tracking


# Main loop for replay and best score
best_score = None

while True:
    attempts = play_game()

    if best_score is None or attempts < best_score:
        best_score = attempts
        print(f"🏆 New Best Score: {best_score} attempts!")
    else:
        print(f"⭐ Best Score so far: {best_score} attempts")

    replay = input("\nDo you want to play again? (yes/no): ").lower()
    if replay != "yes":
        print("Thanks for playing! 👋")
        break
import random


def main():
    secret = random.randint(1, 100)
    attempts = 0
    print("Guess the secret number between 1 and 100.")
    while True:
        guess = input("Enter your guess: ")
        attempts += 1
        if not guess.isdigit():
            print("Please enter a valid integer.")
            continue
        guess = int(guess)
        if guess < secret:
            print("Too low!")
        elif guess > secret:
            print("Too high!")
        else:
            print(f"Correct! You guessed it in {attempts} attempts.")
            break


if __name__ == "__main__":
    main()

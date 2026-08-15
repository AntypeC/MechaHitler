import random

words = ["python", "computer", "hangman", "coding", "banana"]
word = random.choice(words)

guessed_letters = []
wrong_guesses = 0
max_wrong = 6

while wrong_guesses < max_wrong:
    display = ""

    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "

    print("\nWord:", display)
    print("Wrong guesses:", wrong_guesses, "/", max_wrong)

    if "_" not in display:
        print("You win!")
        break

    guess = input("Guess a letter: ").lower()

    if len(guess) != 1 or not guess.isalpha():
        print("Please enter one letter.")
        continue

    if guess in guessed_letters:
        print("You already guessed that letter.")
        continue

    guessed_letters.append(guess)

    if guess not in word:
        wrong_guesses += 1
        print("Wrong guess!")

else:
    print("\nYou lose!")
    print("The word was:", word)
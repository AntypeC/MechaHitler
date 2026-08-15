import random

guess_count = 10
words = ["hello", "python", "energy", "apple", "screw", "you"]
selected_word = random.choice(words)
letter = ""

display = ""

for i in range(len(selected_word)):
    display += "_"

print(f"Word: {" ".join(display)}")

while display != selected_word and guess_count != 0:
    print(f"Guesses remaining: " + str(guess_count))
    while True:
        letter = input(f"Guess a letter: ").lower()
        if letter in list(display):
            print("You already guessed this letter, try again.")
        else:
            break

    count = 0
    for elem in list(selected_word):
        if letter == elem:
            new_display = display[:count] + letter + display[count+1:]
            display = new_display
        count += 1
    print("Word:", " ".join(display))
    guess_count -= 1

if display == selected_word:
    print("You win!")
else:
    print("You lost!")
    print(f"The word was {selected_word}.")

import random

# import torch
# from transformers import AutoModelForSequenceClassification, AutoTokenizer

# # Load the pre-trained model and tokenizer
# model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
# tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# # Prepare your input data (e.g., text samples)
# input_ids = ...
# attention_masks = ...

# # Run inference on the LLM model
# outputs = model(input_ids, attention_mask=attention_masks)

# print(outputs)

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


# dog_food = 3
# cat_food = 2
# parrot_food = 1
# total_food = dog_food + cat_food + parrot_food
# total_food = total_food * 7
# message = "total food needed per week is: " + str(total_food) + " kilograms."
# message_2 = "thats enough "+str(dog_food)+" "+str(cat_food)+", and" + str(parrot_food) + "!"
# print(message)
# print(message_2)
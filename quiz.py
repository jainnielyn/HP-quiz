import requests, json
import random
import time
import config

def check_answer(q, maximum):
    while True:
        answer = input(q)
        try:
            answer = int(answer)
            if answer <= 0 or answer > maximum:
                print(f"That is invalid. Please enter a number between 1 and {maximum}.")
                print("")
                continue
            break
        except:
            print("That is invalid. Please enter a number greater than 0.")
            print("")
            continue
    return int(answer)

def print_options(correct, options):
    q_options = random.sample(options,3)

    # If by some coincidence, the correct answer is in the random options, draw another 3
    while correct in q_options:
        q_options = random.sample(options,3)

    q_options.append(correct)
    random.shuffle(q_options)

    # Print options
    for n,o in enumerate(q_options):
        print(f"{n+1}. {o}")

    # Return integer of correct option
    return q_options.index(correct)+1

response = requests.get(f"https://www.potterapi.com/v1/spells?key={config.api_key}")
spells = response.json()

# Ask user how many questions they want
tot_questions = check_answer("How many questions do you want to get tested on (1-150)? ", maximum=150)
num_correct = 0

questions = random.sample(spells, tot_questions)
options = random.sample(spells, tot_questions*4)
options = [o['spell'] for o in options]

for i in range(tot_questions):
    print("Question number", i+1)
    print(f"Which {questions[i]['type'].lower()} {questions[i]['effect']}?")

    # print options
    correct = questions[i]['spell']
    correct_choice = print_options(correct, options)

    # get answer input
    answer = check_answer("Answer: ", maximum=4)

    # if correct, say correct. count.
    if answer==correct_choice:
        print("Correct! Dumbledore would be proud.")
        num_correct += 1

    # if wrong, say wrong, correct answer is... then continue
    else:
        print(f"Your enemies snicker at you. The answer is {correct}.")

    print("===")
    time.sleep(2)

# At end of loop, congratulations, you answered X out of X questions!
print(f"Well... young witch/wizard, you answered {num_correct} of {tot_questions} \
correctly. {num_correct*2} points to you!")

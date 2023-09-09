"""Contains functions related to the card selection."""
import random


def get_rand_cards(limit, civ):
    """Randomly selects."""
    ages = [1, 2, 3, 4]
    db = []
    curr_age_n = {k: 0 for k in ages}

    while len(db) < limit:
        age_choice = random.choice(ages)
        while True:
            card_choice = random.randint(1, civ[age_choice])
            if (age_choice, card_choice) not in db:
                db.append((age_choice, card_choice))
                curr_age_n[age_choice] += 1
                print(f"Age {age_choice}, Card {card_choice}")
                break
    print("Cards: " + str(len(db)))
    return sorted(db, key=lambda x:x[0])
"""Contains functions related to the card selection."""
import random


def get_rand_cards(limit, civ, age_limit=None):
    """Randomly selects."""
    ages = [1, 2, 3, 4]
    if age_limit != None:
        allowed_ages = ages[:age_limit]
        if age_limit == 2:
            limit = 20
        if age_limit == 1:
            limit = 10
    else:
        allowed_ages = ages
    db = []
    curr_age_n = {k: 0 for k in allowed_ages}

    while len(db) < limit:
        age_choice = random.choice(allowed_ages)
        while True:
            card_choice = random.randint(1, civ[age_choice])
            if curr_age_n[age_choice] == 10:
                break
            if ((age_choice, card_choice) not in db):
                db.append((age_choice, card_choice))
                curr_age_n[age_choice] += 1
                print(f"Age {age_choice}, Card {card_choice}")
                break
    print("Cards: " + str(len(db)))
    return sorted(db, key=lambda x:(x[0], x[1]))
import os
import random 
from food_map import create_food_maps
from code_generation import create_code_mutations
from probability import with_probability
x = None
y = None
food_map = None
health = None
total_moves = None
brain_size = None # A mutation uses more energy per move if it has a large brain size (which is the number of lines of code it has)
verbose = False

def main():
    global x
    global y
    global health
    global total_moves
    global food_map
    global brain_size
    number_of_tests = 50
    code_mutations = create_code_mutations(100)
    food_maps = create_food_maps(50)
    results = [] # Contains tuples of each mutation along with how long mutation survived
    for code_mutation in code_mutations:
        total_moves = 0
        if verbose:
            print "Testing a new code mutation across 10 food maps:"
        current_mutation = convert_code_from_list_to_string(code_mutation)
        brain_size = len(code_mutation)
        if verbose:
            print "Testing code mutation against a new food map:"
        for _ in range(number_of_tests):
            x = 50
            y = 50
            health = 100
            food_map = random.choice(food_maps)
            while health > 0:
                exec current_mutation
                update_everything()
                if verbose:
                    print "Health: " + str(health)
        results.append((current_mutation, (total_moves / number_of_tests),len(code_mutation)) ) # Takes the average survival time
    sorted(results, key=lambda result: result[1], reverse=True) #Rank the best average survival times
    print "The top mutation was as follows: \n" + results[0][0] + "\n\nWhich on average survived for " + str(results[0][1]) + " units of time and had a brain size of " + str(results[0][2]) + " lines of code."


def convert_code_from_list_to_string(input_code):
    output_code = ""
    for line in input_code:
        output_code = output_code + os.linesep + line
    return output_code


def update_everything():
    global total_moves
    global health
    total_moves += 1
    health -= calculate_energy_required_to_maintain_brain() # loses 0.1 to 2.1 health per move
    if food_map[x][y] > 0:
        eat = min(food_map[x][y], 10)
        health += eat
        food_map[x][y] -= eat
    if verbose:
        print "Position = [" + str(x) + "," + str(y) + "], health = " + str(health) 

def calculate_energy_required_to_maintain_brain():
    minimum_loss = 1
    energy_loss = (4*(brain_size / 100))
    return minimum_loss+energy_loss


def up():
    global y
    y -= 1
    y = max(y, 0)
    update_everything()


def right():
    global x
    x += 1
    x = min(x, 99)
    update_everything()


def down():
    global y
    y += 1
    y = min(y, 99)
    update_everything()


def left():
    global x
    x -= 1
    x = max(x, 0)
    update_everything()


def stay():
    update_everything()

def on_food_square():
    return food_map[x][y] > 0

if __name__ == '__main__':
    main()
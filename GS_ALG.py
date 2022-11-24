"""
    Script Name: GS_ALG.java
    Description: This is script that simulates a basic implementation of the 
                 Gale-Shapley Algorithm that solves the stable matching problem,
                 specically the marriage problem between a group of
                 men and women. This script randomly generates two groups
                 of men and women of random sizes and finds a stable matching.
    Date: November 23rd, 2022
    Author: Kasonde Besa
"""
"""
Modules
"""
from random import randint as rnd
from random import choice as ch
from copy import deepcopy as dpc

"""
This function generates temporary lists of men and women that will eventually be dictionaries with preference lists.
"""
# (list) ->  (list)
def generateNames(MALE_NAMES,FEMALE_NAMES):
    # Select groups to try to match
    group_size = rnd(3,12)
    temp_men = []
    temp_women = []
    
    # Chosen names
    chosen_names = set()

    # Populate the groups of men and women to use
    for num in range(group_size):
        # Check to ensure that names are not chosen more than once
        while True:
            chosen_male_name = ch(MALE_NAMES)
            chosen_female_name = ch(FEMALE_NAMES)
            if chosen_male_name in chosen_names or chosen_female_name in chosen_names:
                continue
            else:
                # Keep track of chosen names
                chosen_names.add(chosen_female_name)
                chosen_names.add(chosen_male_name)
                break
        # Add names to the temporary lists
        temp_women.append(chosen_female_name)
        temp_men.append(chosen_male_name)
    return temp_men, temp_women

"""
This function generates two groups' preference lists for suitors, namely men and women from a list of males and females
"""
# (void) -> (list)
def generatePreferenceLists(temp_men,temp_women):
    # Dictionaries with preference lists for each person
    men, women = {},{}

    size = len(temp_men)

    # Populate men dictionary
    for man in temp_men:
        # Current preference list
        temp_list = []

        # Copy the women list for choosing
        women_copied = dpc(temp_women)

        for i in range(size):
            woman = ch(women_copied)
            temp_list.append(woman)
            women_copied.remove(woman)
        men[man] = temp_list

    # Populate men dictionary
    for woman in temp_women:
        # Current preference list
        temp_list = []

        # Copy the women list for choosing
        men_copied = dpc(temp_men)

        for i in range(size):
            man = ch(men_copied)
            temp_list.append(man)
            men_copied.remove(man)
        women[woman] = temp_list

    return [men,women]

"""
Coordinates the creation of groups and their respective preference lists
"""
# (void) -> (list)
def generateNamesAndPreferences():
    # Options to choose from for people to try to match
    MALE_NAMES = ["Liam", "Noah", "Oliver", "Elijah", "James", "William", "Benjamin", "Lucas","Henry","Theodore", "Jack", "Levi", "Alexander", "Jackson", "Mateo", "Daniel", "Michael", "Mason", "Sebastian", "Ethan", "Logan", "Owen", "Samuel", "Jacob", "Asher"]
    FEMALE_NAMES = ["Olivia", "Emma", "Charlotte", "Amelia", "Ava", "Sophia", "Isabella", "Mia", "Evelyn", "Harper", "Luna", "Camila", "Gianna", "Elizabeth", "Eleanor", "Ella", "Abigail", "Sofia", "Avery", "Scarlett", "Emily", "Aria", "Penelope", "Chloe", "Layla"]

    # Choose names
    temp_men, temp_women = generateNames(MALE_NAMES,FEMALE_NAMES)

    # Make preference lists
    men, women = generatePreferenceLists(temp_men,temp_women)
    
    return [men,women]

"""
This uses the gale-shapley algorithm to return a stable matching given groups of men and women
and the preference list.
"""
# (list) -> (list)
def gsAlgorithm(men,women):
    # Stable matching of the two groups involved
    stable_matching = set()
    
    # Helps keep track of engaged women and men
    engaged_women = {}   
    engaged_men = {}
    # Men do the choosing until none of them is free
    while len(men)!= 0:
        # Pick a man from the Dictionary of men
        man = list(men.keys())[0]
        lady_man_prefers = men[man][0]
        man_preference_list = men[man]

        # Man and lady he likes most right now get engaged if she isn't already
        if lady_man_prefers not in engaged_women:
            # Lady gets engaged
            engaged_women [lady_man_prefers] = man

            # We save the engagement temporarily
            stable_matching.add((man,lady_man_prefers))
            
            # We remove lady from current man's list because he has asked her once and make him engaged
            man_preference_list.remove(lady_man_prefers)
            engaged_men [man] = man_preference_list

            # Man is no longer free for now
            del men[man]
        
        # If the lady the man likes is already engaged
        else:
            # Find out the fiance to the lady current man prefers
            fiance_to_lady = engaged_women[lady_man_prefers]
            # Get fiance and man's positions in the lady's list
            fiance_rank = women[lady_man_prefers].index(fiance_to_lady)
            man_rank = women[lady_man_prefers].index(man)
            
            # Man ranks higher than fiance
            if man_rank < fiance_rank:

                # Add fiance back to list of single men and remove him from engaged men group
                men[fiance_to_lady] = engaged_men[fiance_to_lady]
                del engaged_men[fiance_to_lady]

                # Break previous  engagement and make new engagement
                man_preference_list.remove(lady_man_prefers)
                engaged_men[man] = man_preference_list
                engaged_women[lady_man_prefers] = man
                del men[man]
                stable_matching.remove((fiance_to_lady,lady_man_prefers))
                stable_matching.add((man,lady_man_prefers))
            else:
                # Remove lady from man's least because she rejected him
                man_preference_list.remove(lady_man_prefers)
                men[man] = man_preference_list

    return stable_matching

"""
This function prints out the preference lists for each person involved.
"""
# (dict) -> (dict)
def printPreferenceLists(men,women):
    # Print men's preference lists
    print("MEN'S PREFERENCE LISTS ARE LISTED BELOW:")
    for man in men.keys():
        print(man + ": " + str(men[man]))

    # Print women's preference lists
    print("\nWOMEN'S PREFERENCE LISTS ARE LISTED BELOW:")
    for woman in women.keys():
        print(woman + ": " + str(women[woman]))

""" 
This function prints out the stable matching that the Gale-Shapley Algorithm finds.
"""
# (list) -> (void)
def printStableMatching(stable_matching):
    print("\nHere's the result of the gales shapley algorithm:\n")
    for pair in stable_matching:
        print(pair[0] + " marries " + pair[1])

"""
Main Function to control functionality of G-S Algorithm.
"""
# (void) -> (void)
def main():

    # Dictionaries of men, women and their preference lists
    men, women = generateNamesAndPreferences()
    
    # Display the preference lists
    printPreferenceLists(men,women)

    # Generate the stable matching and display it
    stable_matching = gsAlgorithm(men,women)
    
    # Print out stable matching
    printStableMatching(stable_matching)

"""
Entry point into the script.
"""
if __name__ =="__main__":
    main()
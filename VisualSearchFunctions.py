'''
Let's start simple, with the randomiser.
Actually that's so simple that python already has functions for it
From the random module: shuffle(). The only thing we could want to do, is give an option to
shuffle a larger nbag.

So we have a randomiser by loading in the random module and using shuffle()

Let's start by writing out an example config for the VST

Pop-out: color yes 10%, letter yes 10%
trial number: 200
block size: 20
distractor amounts: 4, 10, 20

Target should always be the same and explained in instructions
Target should not always be present

'''

import random
import matplotlib.pyplot as plt
import numpy as np

# Probably going to use tkinter for GUI creation
# And keyboard for dealing with keyboard things, unless tkinter already knows how to do that

# This takes the condition, target presence, and amount of distractors
# Then it generates a plot with the stimuli placed randomly at non-overlapping coordinates
# Condition will be named for which condition it is, target is 1 for present 0 for absent
# Currently, this function is fully functional! At least, it seems to be, from limited testing

# Conditions are: ColPopOut, ShapePopOut, Conjunction
# Target is always a red X

# Note: stimulusnum has to be a minimum of 4, implement checks for this!
def GenerateStimulus(condition = "ColPopOut", target = 1, stimulusnum = 20):
    coordspace = [(x, y) for x in range(100) for y in range(100)]
    coordslist = random.sample(coordspace, k = stimulusnum)
    if target == 1:
        targetcoords = coordslist[0]
        coordslist = coordslist[1:]


    plt.figure(figsize = (10,10))
    plt.axis([-5, 105, -5, 105])
    if condition == "ColPopOut":
        BlackO = coordslist[:len(coordslist)//2]
        BlackOx, BlackOy = zip(*BlackO)
        plt.plot(BlackOx, BlackOy, "ko")
        BlackX = coordslist[len(coordslist)//2:]
        BlackXx, BlackXy = zip(*BlackX)
        plt.plot(BlackXx, BlackXy, "kx")

    elif condition == "ShapePopOut":
        BlackO = coordslist[:len(coordslist)//2]
        BlackOx, BlackOy = zip(*BlackO)
        plt.plot(BlackOx, BlackOy, "ko")
        RedO = coordslist[len(coordslist)//2:]
        RedOx, RedOy = zip(*RedO)
        plt.plot(RedOx, RedOy, "ro")

    elif condition == "Conjunction":
        BlackO = coordslist[:len(coordslist)//3]
        BlackOx, BlackOy = zip(*BlackO)
        plt.plot(BlackOx, BlackOy, "ko")
        RedO = coordslist[len(coordslist)//3:len(coordslist)//3 * 2]
        RedOx, RedOy = zip(*RedO)
        plt.plot(RedOx, RedOy, "ro")
        BlackX = coordslist[len(coordslist)//3 * 2:]
        BlackXx, BlackXy = zip(*BlackX)
        plt.plot(BlackXx, BlackXy, "kx")

    else:
        print("Error: Invalid Condition")
        # Really there should be proper error handling, but for now this will suffice

    if target == 1:
        plt.plot(targetcoords[0], targetcoords[1], "rx")
    plt.style.use('_mpl-gallery-nogrid')
    plt.show()


# Now let's make the function to determine the order of trials

# For this function, trialnum refers to the number of trials in the whole experiment
# ColPopOutPercent refers to the % of trials that are a colour popout,
# Same for ShapePopOutPercent and shape popouts.
# TargetPercent refers to how often a target must be present
# StimulusNums refers to the amount of different trial types for the number of stimuli
# This expects a vector such as (4, 10, 20)
# It should return something with a condition, target 1/0, and stimulusnum for each trial
def TrialOrder(trialnum, ColPopOutPercent, ShapePopOutPercent, TargetPercent, StimulusNums):
    # what you try to generate here is first a vector with the conditions in amount by weight
    # so for 10% colpopout and 10% shapepopout you would have a vector with 8x conjunction
    # 1x colpopout, and 1x shapepopout
    # And it will be limited to increments of 10% because it's hard to balance everything
    # otherwise

    #Then the targetpercent: honestly might just leave this as a set 50%
    # Or otherwise very limited options?
    # Eihter way you have to create multiple of the vectors, for 50% you'd have a vector as
    # before with .TargetPresent in it, and one with .TargetAbsent in it
    # (the . is to make use of strsplit functions, the idea here is that you create
    # conditions like ColPopOut.TargetPresent.20)

    # Same process for splitting to stimulusnums, and definitely no filling in percentages
    # there, balancing gets harder and harder the more you ask for

    # After all this is done, you have 10 * 2 * 3 = 60 conditions in a "bag"
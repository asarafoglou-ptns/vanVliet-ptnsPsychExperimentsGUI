import tkinter as tk
import random
import matplotlib.pyplot as plt
import time
from PIL import Image, ImageTk
import io


RunningExperiment = False
trial_info = []

def RunVST():
    # Here we first want to handle the explanation screen, wait for user input
    # (for this, input() works, because we will just instruct the participant to press enter to
    # continue) and then set a flag that the experiment is currently running for the keypress
    # handler to use and respond to

    # For now though, just set a flag, mostly
    trials = int(NumEntry.get())
    global trial_info
    trial_info = TrialOrder(trials, 10, 10, 50, [4,10,20])

    global RunningExperiment
    RunningExperiment = "VST"


def GoToConfigCreation():
    # First clear the current screen
    for widget in frame.winfo_children():
        widget.pack_forget()
    
    # Then start creating the configcreation screen
    StandardText = tk.Label(master = frame,
                            text = "Selected Experiment: Visual Search Task \n Settings:")
    StandardText.pack()
    TrialNum = tk.Label(master = frame,
                        text = "Number of trials:")
    #NumEntry = tk.Entry(master = frame)
    # This inserts a value for the entry, necessary for presets
    #NumEntry.insert(0, 20)
    # Without specifying, they will simply go to the top. But if you specify LEFT and RIGHT they will sit next to each other
    TrialNum.pack(side = tk.LEFT)
    NumEntry.pack(side = tk.RIGHT)

    StartExperiment = tk.Button(master = frame,
                                text = "Start Experiment",
                                width = 25,
                                height = 5,
                                bg = "white",
                                command = RunVST)
    StartExperiment.pack(side = tk.RIGHT)
    # tk.filedialog.askdirectory() for determining where to save things
    # There's more fields and buttons, those need to be added


window = tk.Tk()
frame = tk.Frame()
frame.pack()
openingtext = tk.Label(master = frame,
                       text = "Welcome to the Psychology Experiment GUI \n Please start by selecting an experiment from the following",
                       width = "50",
                       height = "5")
openingtext.pack()

exp1button = tk.Button(master = frame,
    text = "Visual Search Task",
    width = 25,
    height = 5,
    bg = "white",
    command = GoToConfigCreation
)
exp1button.pack()

NumEntry = tk.Entry(master = frame)
NumEntry.insert(0, 20)

t = 0
t2 = 0
counter = 0

def ExperimentPress(event):
    print(event.keysym)
    global counter
    if event.keysym == "Escape":
        window.destroy()
        exit()
    elif counter > 20:
        window.destroy()
        exit()
    elif RunningExperiment == "VST":
        if event.keysym == "j" or event.keysym == "n":
            global t2
            global t

            t2 = time.time() - t
            print(t2)
            img = GenerateStimulus()
            test = ImageTk.PhotoImage(img)
            StimulusImage = tk.Label(image = test)
            StimulusImage.image = test
            StimulusImage.place(x=0, y=0)

            t = time.time()
            print(t)
            counter = counter + 1


# A similar function would go to the current settings screen, and then finally there's a function
# that goes to the experiment


# For this function, trialnum refers to the number of trials in the whole experiment
# ColPopOutPercent refers to the % of trials that are a colour popout,
# Same for ShapePopOutPercent and shape popouts.
# TargetPercent refers to how often a target must be present
# StimulusNums refers to the amount of different trial types for the number of stimuli
# This expects a vector such as (4, 10, 20)
# It should return something with a condition, target 1/0, and stimulusnum for each trial


def TrialOrder(trialnum, ColPopOutPercent, ShapePopOutPercent, TargetPercent, StimulusNums):
    # For the sake of testing and having something that at least works, this function will
    # not use balanced randomisation in its first version.
    # If balanced randomisation is later implemented, it will likely use nbag randomisation
    # This involves generating trials in batches containing each possible trial type with the
    # respective weights as number of times a condition is present and then using
    # random.shuffle() to make these appear in a random order

    # Initialise an empty list, and determine % conjunction based on the other percentages
    trials_info = []
    ConjPercent = 100 - ColPopOutPercent - ShapePopOutPercent

    for i in range(trialnum):
        # random.choices allows using weights to make some conditions more common than others
        # while random.choice assumes equal weights
        # here these functions are used to generate the information about the current trial
        condition = random.choices(["Conjunction", "ColPopOut", "ShapePopOut"],
                                   weights = [ConjPercent, ColPopOutPercent, ShapePopOutPercent])
        stimuli_num = random.choice(StimulusNums)
        target = random.choices([1, 0], weights = [TargetPercent, 100 - TargetPercent])

        # The trial information is then put in a dict, and appended to the trials_info list
        current_trial = {
            "trial_num": i,
            "trial_type": condition,
            "stimuli_num": stimuli_num,
            "target": target
        }
        trials_info.append(current_trial)

    # When all trials have their randomly generated conditions, we return a list of dicts
    return trials_info

# This takes the condition, target presence, and amount of distractors
# Then it generates a plot with the stimuli placed randomly at non-overlapping coordinates
# Condition will be named for which condition it is, target is 1 for present 0 for absent
# Currently, this function is fully functional! At least, it seems to be, from limited testing

# Conditions are: ColPopOut, ShapePopOut, Conjunction
# Target is always a red X

# Note: stimulusnum has to be a minimum of 4, implement checks for this!
# Also note: when implementing this in the GUI, it might not be with matplotlib
# Or it will be converting matplotlib into an image or something else along those lines
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
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    plt.close(fig)
    return img


window.bind("<KeyPress>", ExperimentPress)
window.mainloop()


# As for other functions needed:

def SaveResult():
    return NotImplemented

def OpenConfig():
    return NotImplemented

def SaveConfig():
    return NotImplemented
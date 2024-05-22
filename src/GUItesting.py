import tkinter as tk
import random
import matplotlib.pyplot as plt
import time
from PIL import Image, ImageTk
import io


RunningExperiment = False
trial_info = []

def RunVST():
    '''
    Internal function called on when starting the VST experiment
    In its curent version, all it does is set some global variables to be used by other functions

    The current plan for it is to make it also provide instructions to the participant and
    resize the window (probably to fullscreen)
    '''
    # Use TrialOrder to globally prepare randomised trials
    trials = int(NumEntry.get())
    global trial_info
    trial_info = TrialOrder(trials, 10, 10, 50, [4,10,20])
    
    # Set a flag that the VST experiment is running
    global RunningExperiment
    RunningExperiment = "VST"

root = tk.Tk()
frame1 = tk.Frame()
frame2 = tk.Frame()
frame1.pack(side = tk.LEFT)
frame2.pack(side = tk.RIGHT)

test1 = tk.Label(master = frame1,
                 text = "should be left")
test3 = tk.Label(master = frame1,
                 text = "should be under and left")
test2 = tk.Entry(master = frame2)
test2.insert(0,"top")
test4 = tk.Entry(master = frame2)
test4.insert(0,"bottom")

test1.pack()
test2.pack()
test3.pack()
test4.pack()


def GoToConfigCreation():
    '''
    This function can be called by any button that is meant to lead the user to the configuration
    screen (also referred to as Settings) for an experiment. It removes the current active widgets
    and places those needed for the configuration, with pre-existing values based on a preset
    or matching the changes already made. It will also contain buttons to continue or go back.

    In its current state, the only available option is the number of trials and the only
    available button is to start the experiment.
    '''
    # First clear the current screen, using forget() rather than destroy so the information
    # in the fillable fields stays accessible
    for widget in frame.winfo_children():
        widget.pack_forget()
    
    # Then start creating the configcreation screen
    StandardText = tk.Label(master = frame,
                            text = "Selected Experiment: Visual Search Task \n Settings:")
    StandardText.pack()
    TrialNum = tk.Label(master = frame,
                        text = "Number of trials:")
                        #\n Block size: \n Percentage Colour Pop-Out: \n Percentage Shape Pop-Out: \n Target Percent: \n Possible Stimulus Amounts:")
    BlockNum = tk.Label(master = frame,
                        text = "Block size:")

    #NumEntry = tk.Entry(master = frame)
    # This inserts a value for the entry, necessary for presets
    #NumEntry.insert(0, 20)
    # Without specifying, they will simply go to the top. But if you specify LEFT and RIGHT they will sit next to each other
    TrialNum.pack(side = tk.LEFT)
    NumEntry.pack()
    BlockNum.pack()
    BlockEntry.pack()
    ColPopOutEntry.pack()
    ShapePopOutEntry.pack()
    TargetEntry.pack()
    StimAmountEntry.pack()

    frame2.pack()
    StartExperiment = tk.Button(master = frame2,
                                text = "Start Experiment",
                                width = 25,
                                height = 5,
                                bg = "white",
                                command = RunVST)
    StartExperiment.pack(side = tk.RIGHT)
    # tk.filedialog.askdirectory() for determining where to save things
    # There's more fields and buttons, those need to be added

'''
These, and other loose declarations, need to become part of a function such as InitialiseGUI(), to define later
'''
window = tk.Tk()
frame = tk.Frame()
frame2 = tk.Frame()
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

BlockEntry = tk.Entry(master = frame)
BlockEntry.insert(0,5)

ColPopOutEntry = tk.Entry(master = frame)
ColPopOutEntry.insert(0,20)

ShapePopOutEntry = tk.Entry(master = frame)
ShapePopOutEntry.insert(0,20)

TargetEntry = tk.Entry(master = frame)
TargetEntry.insert(0,50)

StimAmountEntry = tk.Entry(master = frame)
StimAmountEntry.insert(0, "[4, 10, 20]")

t = 0
t2 = 0
counter = 0

def ExperimentPress(event):
    '''
    Function for internal use. This determines how to handle keypresses, whether that's by closing the program (esc)
    or timing the response and showing the next stimulus (j or n).
    This will be expanded on, but it essentially provides a way to close the program and a way to run the actual experiment.
    Currently prints responses and timings, rather than saving them.
    '''
    print(event.keysym)

    # global counter is used to determine where in the experiment you are, and if it should end
    global counter

    # esc should always be possible to use to exit the program
    if event.keysym == "Escape":
        window.destroy()
        exit()

    # condition to determine whether to continue
    elif counter > 20:
        window.destroy()
        exit()

    # this is where the experiment actions are performed
    elif RunningExperiment == "VST":
        if event.keysym == "j" or event.keysym == "n":
            global t2
            global t

            # t2 determines how long it's been since the previous stimulus was shown
            t2 = time.time() - t
            print(t2)

            # generate and place image
            img = GenerateStimulus()
            test = ImageTk.PhotoImage(img)
            StimulusImage = tk.Label(image = test)
            StimulusImage.image = test
            StimulusImage.place(x=0, y=0)

            # adjust t to start timing for the next response 
            t = time.time()
            print(t)

            # increment
            counter = counter + 1




def TrialOrder(trialnum, ColPopOutPercent, ShapePopOutPercent, TargetPercent, StimulusNums):
    '''
    Function mainly intended for internal use, but can be used on its own.
    This generates randomised trials based on the provided information.

    trialnum: int, number of trials wanted
    ColPopOutPercent: int, percentage of trials that should be a colour pop-out condition, i.e. 20 for 20%
    ShapePopOutPercent: int, percentage of trials that should be a shape pop-out condition, i.e. 20 for 20%
    TargetPercent: int, percentage of trials that should include a target, i.e. 50 for 50%
    StimulusNums: vector of ints, i.e. [4, 10, 20], determines how many stimuli could be present in a trial, equal weighting assumed

    Currently the function does not perform balanced randomisation, this may be changed to n-bag randomisation later.

    Returns: dict with trial_num (int), trial_type (str from Conjunction, ColPopOut, ShapePopOut),
    stimuli_num (int from provided vector in StimulusNums), target (int, 0 or 1)
    '''

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
    '''
    Takes a condition, whether a target is present, and the stimulusnum to generate an image of randomly placed non-overlapping
    x's and o's.

    condition: str, ColPopOut, ShapePopOut, or Conjunction
    target: int, 1 for present, 0 for absent
    stimulusnum: int, must be higher than 4

    Returns: image object
    '''

    # this generates a space for stimuli to be placed (possibly move this to a different initialiser
    # to see if that improves running time) 
    coordspace = [(x, y) for x in range(100) for y in range(100)]
    # from this, take a random sample (this does not repeat, so overlap does not happen)
    coordslist = random.sample(coordspace, k = stimulusnum)

    # only if there is a target, take out one from the list for the target
    if target == 1:
        targetcoords = coordslist[0]
        coordslist = coordslist[1:]

    plt.figure(figsize = (5,5))
    plt.axis([-5, 105, -5, 105])

    # subset coordinates for ColPopOut distractors
    if condition == "ColPopOut":
        BlackO = coordslist[:len(coordslist)//2]
        BlackOx, BlackOy = zip(*BlackO)
        plt.plot(BlackOx, BlackOy, "ko")
        BlackX = coordslist[len(coordslist)//2:]
        BlackXx, BlackXy = zip(*BlackX)
        plt.plot(BlackXx, BlackXy, "kx")

    # subset coordinates for ShapePopOut distractors
    elif condition == "ShapePopOut":
        BlackO = coordslist[:len(coordslist)//2]
        BlackOx, BlackOy = zip(*BlackO)
        plt.plot(BlackOx, BlackOy, "ko")
        RedO = coordslist[len(coordslist)//2:]
        RedOx, RedOy = zip(*RedO)
        plt.plot(RedOx, RedOy, "ro")

    # subset coordinates for conjunction distractors
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

    # convert to fig object, and then to img object
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

import tkinter as tk
from tkinter import filedialog
import random
import matplotlib.pyplot as plt
import time
from PIL import Image, ImageTk
import io
import json
from pandas import DataFrame


# Initialising functions

def InitVars():

    '''
    This is called by InitGUI() to set global variables and flags that are needed
    Takes no inputs and returns no values
    '''

    global RunningExperiment
    # This is set to True when the VST starts, and used by the function that handles keypresses
    RunningExperiment = False

    global InstructionScreen
    InstructionScreen = False

    # These are created to ensure python does not get confused by them not existing yet
    global trial_info
    trial_info = []

    global t
    global t2
    global counter
    global blockcounter
    global StimulusImage
    t = 0
    t2 = 0
    counter = 0
    blockcounter = 0
    StimulusImage = 0

    global settings
    settings = ["Total trials:", "Block size:", "Percentage colour pop-out:",
                "Percentage shape pop-out:", "Percentage target present:",
                "Possible stimulus amounts:", "Seed (optional):"]
    
    # One of the most important global variables that are initialised, the config
    # This contains the default settings for the task, and this variable is edited when the
    # settings are changed.
    global config
    config = {
        "Experiment Type": "VST",
        "Total Trials": 200,
        "Block size": 20,
        "ColPopOutPercent": 10,
        "ShapePopOutPercent": 10,
        "TargetPercent": 50,
        "Possible Stimulus Amounts": "4, 10, 20",
        "Seed": None,
        "Study ID": "test_run",
        "Participant ID": "001",
        "SaveFilePath": 'C:/Documents/Research/VST_test'
    }

#InitVars()


def InitGUI():
    
    '''
    Initialises the GUI. It calls on InitVars() to initialise global variables needed, creates a
    window, binds KeyPress events to the function handling user input, turns on the main loop,
    and creates the welcome screen.
    '''

    # Currently commented out due to testing, in the package version this will be called by InitGUI()
    InitVars()

    global root
    root = tk.Tk()
    global frame
    frame = tk.Frame()
    frame.pack()
    
    WelcomeScreen()

    root.bind("<KeyPress>", ExperimentPress)
    root.mainloop()


# GUI screens

def WelcomeScreen():
    for widget in frame.winfo_children():
        widget.destroy()
    openingtext = tk.Label(master = frame,
                           text = "Welcome to the Psychology Experiment GUI \n Please start by selecting an experiment from the following",
                           width = "50",
                           height = "5")
    openingtext.pack()

    # This buttom uses GoToConfigCreation() to lead the user to the settings for the VST experiment
    exp1button = tk.Button(master = frame,
        text = "Visual Search Task",
        width = 25,
        height = 5,
        bg = "white",
        command = GoToConfigCreation
    )
    exp1button.pack()

    # This button uses GoToWCSTConfig(), a currently unimplemented function. This means it does nothing
    exp2button = tk.Button(master = frame,
                           text = "Wisconsin Card Sorting Task\n(Not Implemented)",
                           width = 25,
                           height = 5,
                           bg = "white",
                           command = GoToWCSTConfig)
    exp2button.pack()

def InitSettings():
    '''
    This is called by GoToConfigCreation(), it populates the window with frames, labels, and entry boxes.
    The result is a fairly standard screen with labels matching entry boxes to tell you which setting each
    entry is connected to. The entry boxes are initialised based on the config initialised in InitVars().
    There are also buttons linked to commands to go back to the welcome screen, continue to the next,
    save/load configs [not implemented], and choose a directory to save results to.
    '''

    # Creating frames to make it possible to place each label, entry, and button, where it's wanted
    topframe = tk.Frame(master = frame)
    topframe.pack()

    MiddleFrame = tk.Frame(master = frame)
    MiddleFrame.pack()
    frame1 = tk.Frame(master = MiddleFrame)
    frame2 = tk.Frame(master = MiddleFrame)
    frame1.pack(side = tk.LEFT)
    frame2.pack(side = tk.RIGHT)

    
    # The following code is all manually writing which labels and entries to create and packing them
    # There is probably a more efficient way to do this, but I did not manage to find it
    # The entries are also created as global variables, to make it possible to get user input
    # out of them in different functions
    StandardText = tk.Label(master = topframe,
                            text = "Selected Experiment: Visual Search Task \n Settings:")
    StandardText.pack()

    TrialLabel = tk.Label(master = frame1, text = settings[0])

    global TrialEntry
    TrialEntry = tk.Entry(master = frame2)
    TrialEntry.insert(0, config['Total Trials'])

    BlockLabel = tk.Label(master = frame1, text = settings[1])

    global BlockEntry
    BlockEntry = tk.Entry(master = frame2)
    BlockEntry.insert(0, config['Block size'])

    ColPopLabel = tk.Label(master = frame1, text = settings[2])

    global ColPopEntry
    ColPopEntry = tk.Entry(master = frame2)
    ColPopEntry.insert(0, config['ColPopOutPercent'])

    ShapePopLabel = tk.Label(master = frame1, text = settings[3])

    global ShapePopEntry
    ShapePopEntry = tk.Entry(master = frame2)
    ShapePopEntry.insert(0, config['ShapePopOutPercent'])

    TargetLabel = tk.Label(master = frame1, text = settings[4])

    global TargetEntry
    TargetEntry = tk.Entry(master = frame2)
    TargetEntry.insert(0, config['TargetPercent'])

    StimLabel = tk.Label(master = frame1, text = settings[5])

    global StimEntry
    StimEntry = tk.Entry(master = frame2)
    StimEntry.insert(0, config['Possible Stimulus Amounts'])

    SeedLabel = tk.Label(master = frame1, text = settings[6])
    global SeedEntry
    SeedEntry = tk.Entry(master = frame2)

    if config["Seed"] != None:
        SeedEntry.insert(0, config["Seed"])

    for widget in frame1.winfo_children():
        widget.pack()

    for widget in frame2.winfo_children():
        widget.pack()

    StudyFrame = tk.Frame(master = frame)
    StudyFrame.pack()

    StudyLabel = tk.Label(master = StudyFrame, text = "Required study information: \n")
    StudyLabel.pack()

    StudyLabels = tk.Frame(master = StudyFrame)
    StudyEntries = tk.Frame(master = StudyFrame)

    StudyLabels.pack(side = tk.LEFT)
    StudyEntries.pack(side = tk.RIGHT)

    StudyID = tk.Label(master = StudyLabels, text = "Study ID:")
    StudyID.pack()

    global StudyIDEntry
    StudyIDEntry = tk.Entry(master = StudyEntries)
    StudyIDEntry.insert(0, config['Study ID'])
    StudyIDEntry.pack()

    ParticipantID = tk.Label(master = StudyLabels, text = "Participant ID:")
    ParticipantID.pack()

    global ParticipantIDEntry
    ParticipantIDEntry = tk.Entry(master = StudyEntries)
    ParticipantIDEntry.insert(0, config['Participant ID'])
    ParticipantIDEntry.pack()

    FileLabel = tk.Label(master = StudyLabels, text = "Choose where to save the results:")
    FileLabel.pack()

    global FileEntry
    FileEntry = tk.Entry(master = StudyEntries, width = 30)
    FileEntry.insert(0, config['SaveFilePath'])
    FileEntry.pack(side = tk.LEFT)

    # Calls on GetDirectory() to prompt the user to select a directory to save files to
    # and then adjusts the entry box next to it to match the chosen directory (if one was chosen)
    FileButton = tk.Button(master = StudyEntries, text = "...", command = GetDirectory)
    FileButton.pack(side = tk.RIGHT)

    bottomframe = tk.Frame(master = frame)
    bottomframe.pack()

    # Returns to the welcome screen
    ReturnButton = tk.Button(master = bottomframe,
                             text = "Back",
                             width = 25,
                             height = 5,
                             bg = "white",
                             command = WelcomeScreen)
    ReturnButton.pack(side = tk.LEFT)

    # Save the config
    SaveConfigButton = tk.Button(master = bottomframe,
                                 text = "Save config",
                                 bg = "white",
                                 command = SaveConfig)
    SaveConfigButton.pack(side = tk.RIGHT)

    OpenConfigButton = tk.Button(master = bottomframe,
                                 text = "Open config",
                                 bg = "white",
                                 command = OpenConfig)
    OpenConfigButton.pack(side = tk.RIGHT)

    # Linked to a command to start the experiment
    StartExperiment = tk.Button(master = bottomframe,
                                text = "Continue",
                                width = 25,
                                height = 5,
                                bg = "white",
                                command = RunVST)
    StartExperiment.pack(side = tk.RIGHT)



# Button functions

def GoToWCSTConfig():
    # Possibility for future development
    NotImplemented


def GetDirectory():
    '''
    Internal function that prompts the user to select where they want results to be saved to
    adjusts the entry box to match this
    '''
    global FileEntry
    filepath = filedialog.askdirectory()
    
    if len(filepath) > 0:
        FileEntry.delete(0, 'end')
    FileEntry.insert(0, filepath)


def GoToConfigCreation():
    '''
    Destroys the widgets in the current window and then calls on InitSettings() to create the
    widgets that make the settings screen instead
    '''

    # First clear the current screen
    for widget in frame.winfo_children():
        widget.destroy()

    # Then use the init to load the wanted screen
    InitSettings()

def OpenConfig():
    
    '''
    Function called on by the "load config" button, prompts the user to select a config file to open
    and use for the experiment. It also changes the entry boxes to match the new config
    '''

    # First open the file
    newconfig = filedialog.askopenfilename(defaultextension=".json", filetypes =(("json file", "*.json"),))
    file = open(newconfig)
    global config
    config = json.load(file)
    file.close()

    UpdateEntries()

def SaveConfig():
    
    '''
    Function called on by the "save config" button, prompts the user to select where and with what name
    to save their config file. Then it uses this to save the config as a .json
    '''

    # First update the config to make sure the correct values are saved
    UpdateConfig()

    global config
    # First do the dialog and collect the filename from it
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes =(("json file", "*.json"),))

    # Check to see if the user filled in anything at all before writing to a json file
    if len(filename) > 0:
        with open(filename, 'w') as file:
            json.dump(config, file)




# Experiment functions

def RunVST():
    '''
    Internal function called on when starting the VST experiment
    In its curent version, all it does is set some global variables to be used by other functions

    The current plan for it is to make it also provide instructions to the participant and
    resize the window (probably to fullscreen)
    '''

    # Updates the config to match the entry boxes
    UpdateConfig()

    stimulusstrs = config["Possible Stimulus Amounts"]
    stimulusstrs = stimulusstrs.split(", ")
    stimulusnums = []
    for i in stimulusstrs:
        stimulusnums.append(int(i))

    global randomised_trials
    randomised_trials = TrialOrder(config["Total Trials"],
                                   config["ColPopOutPercent"],
                                   config["ShapePopOutPercent"],
                                   config["TargetPercent"],
                                   stimulusnums,
                                   config["Seed"])
    
    # Clear out widgets, honestly maybe even by just destroying the window entirely for good measure
    # Then creating a new one that gets set to fullscreen with instructions and no close button
    global frame
    for widget in frame.winfo_children():
        widget.destroy()

    root.attributes("-fullscreen", True)
    InstructionLabel = tk.Label(master = frame,
                                text = "Welcome to the Visual Search Task\n You will be shown images with crosses and circles, in red and black.\n Your task is to determine if there is a red X in the image. \n If there is a red X press \"y\", if there is no red x press \"n\" \n After a number of images, there will be a short break.\n \n Please press enter to start the task",
                                font = ("Arial", 25))
    InstructionLabel.pack()

    global InstructionScreen
    InstructionScreen = True
    # Set a flag that the VST experiment is running
    global RunningExperiment
    RunningExperiment = "VST"


def ExperimentPress(event):
    '''
    Function for internal use. This determines how to handle keypresses, whether that's by closing the program (esc)
    or timing the response and showing the next stimulus (j or n).
    This will be expanded on, but it essentially provides a way to close the program and a way to run the actual experiment.
    Currently prints responses and timings, rather than saving them.
    '''
    #print(event.keysym)

    # global counter is used to determine where in the experiment you are, and if it should end
    global counter

    # global blockcounter is made for determining whether a pause between blocks should be created
    global blockcounter

    # the config is referred to for certain checks
    global config

    global randomised_trials

    # esc should always be possible to use to exit the program
    if event.keysym == "Escape":
        root.destroy()
        exit()

    # condition to determine whether to continue
    elif counter >= config["Total Trials"]:
        
        # Save data, create exit screen [to do]
        SaveResult()
        root.destroy()
        exit()

    # this is where the experiment actions are performed
    elif RunningExperiment == "VST":
        
        if counter % config["Block size"] == 0 and counter / config["Block size"] < blockcounter:
            # Create the pause screen for the block
            global StimulusImage
            StimulusImage.destroy()

        elif event.keysym == "y" or event.keysym == "n" or event.keysym == "Y" or event.keysym == "N":
            global t2
            global t

            # t2 determines how long it's been since the previous stimulus was shown
            t2 = time.time() - t
            

            # generate and place image
            condition = randomised_trials[counter]["trial_type"]
            target = randomised_trials[counter]["target"]
            stimulusnum = randomised_trials[counter]["stimuli_num"]
            
            img = GenerateStimulus(condition = condition, target = target, stimulusnum = stimulusnum)
            test = ImageTk.PhotoImage(img)

            StimulusImage = tk.Label(image = test)
            StimulusImage.image = test
            StimulusImage.place(x=0, y=0)

            # adjust t to start timing for the next response 
            t = time.time()
            
            randomised_trials[counter]["reaction_time"] = t2
            randomised_trials[counter]["response"] = event.keysym

            # increment
            counter = counter + 1



def TrialOrder(trialnum, ColPopOutPercent, ShapePopOutPercent, TargetPercent, StimulusNums, Seed):
    '''
    Function mainly intended for internal use, but can be used on its own.
    This generates randomised trials based on the provided information.

    trialnum: int, number of trials wanted
    ColPopOutPercent: int, percentage of trials that should be a colour pop-out condition, i.e. 20 for 20%
    ShapePopOutPercent: int, percentage of trials that should be a shape pop-out condition, i.e. 20 for 20%
    TargetPercent: int, percentage of trials that should include a target, i.e. 50 for 50%
    StimulusNums: vector of ints, i.e. [4, 10, 20], determines how many stimuli could be present in a trial, equal weighting assumed
    Seed: int, used as a seed for the random order of trials. Only use for replicability

    Currently the function does not perform balanced randomisation, this may be changed to n-bag randomisation later.

    Returns: dict with trial_num (int), trial_type (str from Conjunction, ColPopOut, ShapePopOut),
    stimuli_num (int from provided vector in StimulusNums), target (int, 0 or 1)
    '''

    if Seed != None:
        random.seed(Seed)
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
            "trial_type": condition[0],
            "stimuli_num": stimuli_num,
            "target": target[0],
            "reaction_time": None,
            "response": None
        }
        trials_info.append(current_trial)

    # When all trials have their randomly generated conditions, we return a list of dicts
    return trials_info

def GenerateStimulus(condition = "ColPopOut", target = 1, stimulusnum = 10):
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
    coordspace = [(x, y) for x in range(50) for y in range(50)]
    # from this, take a random sample (this does not repeat, so overlap does not happen)
    coordslist = random.sample(coordspace, k = stimulusnum)

    # only if there is a target, take out one from the list for the target
    if target == 1:
        targetcoords = coordslist[0]
        coordslist = coordslist[1:]

    plt.figure(figsize = (7,7))
    plt.axis([-5, 55, -5, 55])

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


def SaveResult():
    global randomised_trials
    df = DataFrame(randomised_trials)

    global config
    filename = config["SaveFilePath"] + "/" + "VSTresult" + config["Study ID"] + config["Participant ID"] + ".csv"
    df.to_csv(filename)


# General functions

def UpdateConfig():
    '''
    Updates the config variable based on the entry boxes
    '''
    global config
    config["Total Trials"] = int(TrialEntry.get())
    config["Block size"] = int(BlockEntry.get())
    config["ColPopOutPercent"] = int(ColPopEntry.get())
    config["ShapePopOutPercent"] = int(ShapePopEntry.get())
    config["TargetPercent"] = int(TargetEntry.get())
    config["Possible Stimulus Amounts"] = StimEntry.get()
    if len(SeedEntry.get()) > 0:
        config["Seed"] = int(SeedEntry.get())
    config["Study ID"] = StudyIDEntry.get()
    config["Participant ID"] = ParticipantIDEntry.get()
    config["SaveFilePath"] = FileEntry.get()


def UpdateEntries():

    '''
    Function called on to update the entry boxes when a config is loaded in
    '''

    global TrialEntry
    TrialEntry.delete(0, 'end')
    TrialEntry.insert(0, config["Total Trials"])

    global BlockEntry
    BlockEntry.delete(0, 'end')
    BlockEntry.insert(0, config["Block size"])

    global ColPopEntry
    ColPopEntry.delete(0, 'end')
    ColPopEntry.insert(0, config["ColPopOutPercent"])

    global ShapePopEntry
    ShapePopEntry.delete(0, 'end')
    ShapePopEntry.insert(0, config["ShapePopOutPercent"])

    global TargetEntry
    TargetEntry.delete(0, 'end')
    TargetEntry.insert(0, config["TargetPercent"])

    global StimEntry
    StimEntry.delete(0, 'end')
    StimEntry.insert(0, config["Possible Stimulus Amounts"])

    global SeedEntry
    SeedEntry.delete(0, 'end')
    if config["Seed"] != None:
        SeedEntry.insert(0, config["Seed"])

    global StudyIDEntry
    StudyIDEntry.delete(0, 'end')
    StudyIDEntry.insert(0, config["Study ID"])

    global ParticipantIDEntry
    ParticipantIDEntry.delete(0, 'end')
    ParticipantIDEntry.insert(0, config["Participant ID"])

    global FileEntry
    FileEntry.delete(0, 'end')
    FileEntry.insert(0, config["SaveFilePath"])
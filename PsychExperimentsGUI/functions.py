import tkinter as tk
from tkinter import filedialog
import random
import matplotlib.pyplot as plt
import time
from PIL import Image, ImageTk
import io
import json
from pandas import DataFrame


# Initialising functions --------------------------------------------------------------

def InitVars():

    '''
    This is called by InitGUI() to set global variables and flags that are needed
    Takes no inputs and returns no values
    '''

    # Flags to determine how the GUI should respond to user input
    global RunningExperiment
    RunningExperiment = False

    global InstructionScreen
    InstructionScreen = False

    global BlockScreen
    BlockScreen = False

    global FinishedExperiment
    FinishedExperiment = False

    global FullScreen
    FullScreen = False

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

    # In the current version, the VST experiment is assumed because that is the only experiment
    # that has been implemented yet
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



def InitGUI():
    
    '''
    Initialises the GUI. This calls on InitVars to initialise global variables, creates the window,
    creates the welcome screen, and ensures keypresses are bound to the window.
    Takes no inputs and returns no values
    '''

    # initialise global variables
    InitVars()

    # create initial window and frame
    global root
    root = tk.Tk()

    # this is the master frame, every frame and widget used is a child or grandchild of this
    # By setting expand = True, its children will be responsive to vertical changes of window size
    global frame
    frame = tk.Frame()
    frame.pack(expand = True)
    
    # call to create the first screen
    WelcomeScreen()

    # bind keypresses and start main loop
    root.bind("<KeyPress>", ExperimentPress)
    root.mainloop()


# GUI screens ----------------------------------------------------------------------------

def WelcomeScreen():

    '''
    Function used by other GUI functions, destroys any currently present widgets or frames except
    the master frame. Then it creates the widgets of the welcome screen and packs them.
    Takes no inputs and returns no values
    '''

    # Destroy everything except master frame
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
    entry is connected to. The entry boxes have values based on the config initialised in InitVars().
    There are also buttons linked to commands to go back to the welcome screen, continue to the next,
    save/load configs, and choose a directory to save results to.
    Takes no inputs and returns no values
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

    # packing the frames in a loop
    for widget in frame1.winfo_children():
        widget.pack()

    for widget in frame2.winfo_children():
        widget.pack()

    # frame for study related information
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
    # which then adjusts the entry box next to it to match the chosen directory (if one was chosen)
    FileButton = tk.Button(master = StudyEntries, text = "...", command = GetDirectory)
    FileButton.pack(side = tk.RIGHT)

    configframe = tk.Frame(master = frame)
    configframe.pack()

    # Save the config
    SaveConfigButton = tk.Button(master = configframe,
                                 text = "Save config",
                                 bg = "white",
                                 command = SaveConfig)
    SaveConfigButton.pack(side = tk.RIGHT)

    # Load the config
    OpenConfigButton = tk.Button(master = configframe,
                                 text = "Open config",
                                 bg = "white",
                                 command = OpenConfig)
    OpenConfigButton.pack(side = tk.RIGHT)

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

    # Continues to a screen with a summary of the current settings
    StartExperiment = tk.Button(master = bottomframe,
                                text = "Continue",
                                width = 25,
                                height = 5,
                                bg = "white",
                                command = GoToSettingsCheck)
    StartExperiment.pack(side = tk.RIGHT)

def SettingsCheck():

    '''
    Internal GUI function that creates a screen showing the user their current settings before
    they continue to the experiment. There is a button to go back to adjust their settings and
    a button to start the experiment.
    Takes no inputs, returns no values
    '''

    # Destroy any existing widgets and frames except the master frame
    for widget in frame.winfo_children():
        widget.destroy()

    global config

    # Uses the config to generate strings for each of the settings
    exptype = "Experiment Type: " + config["Experiment Type"]
    trialnum = "Total Trials: " + str(config["Total Trials"])
    blocksize = "Block Size: " + str(config["Block size"])
    ColPercent = "Percentage Colour Pop-Out: " + str(config["ColPopOutPercent"])
    ShapePercent = "Percentage Shape Pop-Out: " + str(config["ShapePopOutPercent"])
    TargetPercent = "Percentage Target: " + str(config["TargetPercent"])
    StimAmounts = "Possible Stimulus Amounts: " + config["Possible Stimulus Amounts"]
    if config["Seed"] != None:
        Seed = "Seed: " + str(config["Seed"])
    else:
        Seed = "Seed: None"
    StudyID = "Study ID: " + config["Study ID"]
    ParticipantID = "Participant ID: " + config["Participant ID"]
    SaveFilePath = "Location to save results to: " + config["SaveFilePath"]

    # Combines strings generated above so they can be placed in one label together
    SettingsText = exptype + "\n" + trialnum + "\n" + blocksize + "\n" + ColPercent + "\n" + ShapePercent + "\n" + TargetPercent + "\n" + StimAmounts + "\n" + Seed + "\n" + StudyID + "\n" + ParticipantID + "\n" + SaveFilePath

    SettingsLabel = tk.Label(master = frame, text = SettingsText)
    SettingsLabel.pack()

    # Back to config screen
    buttonframe = tk.Frame(master = frame)
    buttonframe.pack()
    ReturnConfig = tk.Button(master = buttonframe,
                             text = "Change Settings",
                             width = 25,
                             height = 5,
                             bg = "white",
                             command = GoToConfigCreation)
    ReturnConfig.pack(side = tk.LEFT)

    # Start experiment
    StartExperiment = tk.Button(master = buttonframe,
                                text = "Start Experiment",
                                width = 25,
                                height = 5,
                                bg = "white",
                                command = RunVST)
    StartExperiment.pack(side = tk.RIGHT)

def ShowBlockScreen():

    '''
    Used by GUI functions to clear the screen and show the block instruction
    Takes no inputs, returns no values
    '''

    # Clear stimulus
    global StimulusImage
    StimulusImage.destroy()

    # Show instruction
    InstructionLabel = tk.Label(master = frame,
                                text = "This is a small break between blocks \n Press Enter when you are ready to continue",
                                font = ("Arial", 25))
    InstructionLabel.pack()

def EndExperiment():

    '''
    Used by GUI functions to show the final end screen instructions
    Takes no inputs, returns no values
    '''

    InstructionLabel = tk.Label(master = frame,
                                text = "This is the end of the experiment \n Thank you for your participation \n Press Enter to exit",
                                font = ("Arial", 25))
    InstructionLabel.pack()

def ResultsScreen():

    '''
    Used by GUI functions to clear the screen and show that the results have been saved, and
    a button to return to the welcome screen.
    Takes no inputs, returns no values
    '''

    # Clear screen
    for widget in frame.winfo_children():
        widget.destroy()

    SavedText = tk.Label(master = frame,
                         text = "Your results have been saved!")
    SavedText.pack()

    # Return to welcome screen
    StartScreenButton = tk.Button(master = frame,
                                  text = "Return to start",
                                  width = 25,
                                  height = 5,
                                  bg = "white",
                                  command = WelcomeScreen)
    StartScreenButton.pack()


# Button functions ----------------------------------------------------------------------

def GoToWCSTConfig():
    # Possibility for future development
    NotImplemented


def GetDirectory():
    '''
    Internal function that prompts the user to select where they want results to be saved to,
    adjusts the entry box to match this
    Takes no inputs, returns no values
    '''

    global FileEntry
    # Prompt user with file selection screen
    filepath = filedialog.askdirectory()
    
    # Checks if the user has selected anything before deleting the previously set path
    if len(filepath) > 0:
        FileEntry.delete(0, 'end')
    
    # Inserts the selected path (or nothing, if nothing was selected)
    FileEntry.insert(0, filepath)


def GoToConfigCreation():
    '''
    Destroys the widgets in the current window and then calls on InitSettings() to create the
    widgets that make the settings screen instead
    Takes no inputs, returns no values
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
    Takes no inputs, returns no values
    '''

    # Prompt user to select a file to open
    newconfig = filedialog.askopenfilename(defaultextension=".json", filetypes =(("json file", "*.json"),))
    file = open(newconfig)
    global config
    # sets the loaded config as the config to use going forward
    config = json.load(file)
    file.close()

    # Update the entry boxes to match the new config
    UpdateEntries()

def SaveConfig():
    
    '''
    Function called on by the "save config" button, prompts the user to select where and with what name
    to save their config file. Then it uses this to save the config as a .json
    Takes no inputs, returns no values
    '''

    # First update the config to make sure the correct values are saved
    UpdateConfig()

    global config
    # Prompt user for filename to save with
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes =(("json file", "*.json"),))

    # Check to see if the user filled in anything before writing to a json file
    if len(filename) > 0:
        with open(filename, 'w') as file:
            json.dump(config, file)


def GoToSettingsCheck():

    '''
    Function attached to a button, which triggers required updates before calling on a function to create the
    SettingsCheck screen (where a user can check if their settings are what they wanted, before continuing)
    Takes no inputs, returns no values
    '''

    # update the config
    UpdateConfig()

    # Then make the new screen
    SettingsCheck()

# Experiment functions

def RunVST():
    '''
    Used when running the Visual Search Task experiment, this uses the config to generate a trial
    order for the experiment. Then it clears the screen, resizes to fullscreen, shows the instructions,
    and sets global flags to match the state of the experiment.
    Takes no inputs, returns no values
    '''

    # Convert the stimulus amounts (a string, due to taking it from the entry widget) into a list of integers
    stimulusstrs = config["Possible Stimulus Amounts"]
    stimulusstrs = stimulusstrs.split(", ")
    stimulusnums = []
    for i in stimulusstrs:
        stimulusnums.append(int(i))

    # Use the config settings as arguments for TrialOrder, which returns a list of dicts with
    # information about the generated trials and space to fill in participant responses
    global randomised_trials
    randomised_trials = TrialOrder(config["Total Trials"],
                                   config["ColPopOutPercent"],
                                   config["ShapePopOutPercent"],
                                   config["TargetPercent"],
                                   stimulusnums,
                                   config["Seed"])
    
    # Clear screen
    global frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Resize to fullscreen, and set a flag that FullScreen is True
    root.attributes("-fullscreen", True)
    global FullScreen
    FullScreen = True

    # Instructions
    InstructionLabel = tk.Label(master = frame,
                                text = "Welcome to the Visual Search Task\n You will be shown images with crosses and circles, in red and black.\n Your task is to determine if there is a red X in the image. \n If there is a red X press \"y\", if there is no red x press \"n\" \n After a number of images, there will be a short break.\n \n Please press enter to start the task",
                                font = ("Arial", 25))
    InstructionLabel.pack()

    # Relevant flags about the experiment's state
    global InstructionScreen
    InstructionScreen = True

    global RunningExperiment
    RunningExperiment = "VST"

    global FinishedExperiment
    FinishedExperiment = False


def ExperimentPress(event):

    '''
    Function that handles KeyPress events, responding to user input.

    Responses:

    Escape while in fullscreen closes the window without saving
    On an instruction screen or block screen, pressing enter continues to a stimulus presentation
    While a stimulus is presented, 'y' or 'n' is taken as a response to the stimulus, responses are logged,
    and the program decides what to show next
    Takes KeyPress events as input, returns no values
    '''

    # global counter is used to determine where in the experiment you are, and if it should end
    global counter

    # global blockcounter is made for determining whether a pause between blocks should be created
    global blockcounter

    # various values and flags that need to be used within this function
    global config
    global randomised_trials
    global InstructionScreen
    global StimulusImage
    global t
    global t2
    global RunningExperiment
    global FinishedExperiment
    global BlockScreen
    global FullScreen

    # While in fullscreen, there is no button to close the program but it should always be
    # possible to close the program. There is no confirmation and nothing is saved
    if event.keysym == "Escape" and FullScreen == True:

        # Close the GUI
        root.destroy()
        # Stop the Python script
        exit()

    # Is the VST experiment running?
    elif RunningExperiment == "VST":

        # Is the current screen the instruction screen?
        if InstructionScreen == True:

            # When the user presses enter
            if event.keysym == "Return":

                # Clear the window
                for widget in frame.winfo_children():
                    widget.destroy()

                # Set flag that there is no instruction screen
                InstructionScreen = False

                # Use information from generated trials
                condition = randomised_trials[counter]["trial_type"]
                target = randomised_trials[counter]["target"]
                stimulusnum = randomised_trials[counter]["stimuli_num"]
                
                # Create image
                img = GenerateStimulus(condition = condition, target = target, stimulusnum = stimulusnum)
                test = ImageTk.PhotoImage(img)

                # Place image in the center of the screen
                StimulusImage = tk.Label(image = test)
                StimulusImage.image = test
                StimulusImage.place(x=root.winfo_width() // 2, y=root.winfo_height() // 2, anchor = "center")

                # Start timer for participant response
                t = time.time()

        # Is the current screen a break between blocks?        
        elif BlockScreen == True:

            # When the user presses enter
            if event.keysym == "Return":

                # Clear the window
                for widget in frame.winfo_children():
                    widget.destroy()
                BlockScreen = False

                # Use information from generated trials
                condition = randomised_trials[counter]["trial_type"]
                target = randomised_trials[counter]["target"]
                stimulusnum = randomised_trials[counter]["stimuli_num"]
                
                # Create image
                img = GenerateStimulus(condition = condition, target = target, stimulusnum = stimulusnum)
                test = ImageTk.PhotoImage(img)

                # Place image in the center of the screen
                StimulusImage = tk.Label(image = test)
                StimulusImage.image = test
                StimulusImage.place(x=root.winfo_width() // 2, y=root.winfo_height() // 2, anchor = "center")

                # Start timer for participant response
                t = time.time()

        # A stimulus must be visible due to ruling out other states of the GUI
        # Check if the user gave a response
        elif event.keysym == "y" or event.keysym == "n" or event.keysym == "Y" or event.keysym == "N":

            # t2 determines how long it's been since the stimulus was shown
            t2 = time.time() - t

            # Save response
            randomised_trials[counter]["reaction_time"] = t2
            randomised_trials[counter]["response"] = event.keysym

            # increment counter
            counter = counter + 1

            # Get rid of current image
            StimulusImage.destroy()
            
            # Is the experiment complete?
            if counter >= config["Total Trials"]:
        
                # Save data
                SaveResult()

                # Set flags
                RunningExperiment = False
                FinishedExperiment = True

                # Go to end screen
                EndExperiment()

            # Should the next screen be a break between blocks?
            elif counter % config["Block size"] == 0 and counter / config["Block size"] > blockcounter:
                
                # Set flag
                BlockScreen = True

                # This counter is used to ensure the pause between blocks does not get stuck when the
                # counter for the trials doesn't go up
                blockcounter = blockcounter + 1

                # Create the screen for the pause between blocks
                ShowBlockScreen()

            # The next screen should not be an ending or break, so it must be a stimulus
            else:

                # generate and place image
                condition = randomised_trials[counter]["trial_type"]
                target = randomised_trials[counter]["target"]
                stimulusnum = randomised_trials[counter]["stimuli_num"]
                
                img = GenerateStimulus(condition = condition, target = target, stimulusnum = stimulusnum)
                test = ImageTk.PhotoImage(img)

                StimulusImage = tk.Label(image = test)
                StimulusImage.image = test
                StimulusImage.place(x=root.winfo_width() // 2, y=root.winfo_height() // 2, anchor = "center")

                # adjust t to start timing for the next response 
                t = time.time()

    # Experiment is finished, user pressed enter as instructed
    elif FinishedExperiment == True and event.keysym == "Return":

        # Turn fullscreen off
        root.attributes("-fullscreen", False)
        FullScreen = False

        # Leave the state where this elif can be met
        FinishedExperiment = False

        # Go to the screen that tells the user their results were saved
        ResultsScreen()


def TrialOrder(trialnum, ColPopOutPercent, ShapePopOutPercent, TargetPercent, StimulusNums, Seed):
    '''
    Generates randomised trials based on provided arguments. Not callable as user

    trialnum: int, number of trials wanted
    ColPopOutPercent: int, percentage of trials that should be a colour pop-out condition, i.e. 20 for 20%
    ShapePopOutPercent: int, percentage of trials that should be a shape pop-out condition, i.e. 20 for 20%
    TargetPercent: int, percentage of trials that should include a target, i.e. 50 for 50%
    StimulusNums: vector of ints, i.e. [4, 10, 20], determines how many stimuli could be present in a trial, equal weighting assumed
    Seed: int, used as a seed for the random order of trials. Use for replicability

    WARNING: this is unbalanced randomisation, there may be many trials of one type in a row when that would not
    be expected based on intuition about the odds. There is also no guarantee that in i.e. 200 trials at 10%
    ColPopOutPercent there will be 20 trials with a ColPopout condition.

    Returns: list of dicts with trial_num: (int), trial_type: (str from Conjunction, ColPopOut, ShapePopOut),
    stimuli_num: (int from provided vector in StimulusNums), target: (int, 0 or 1)
    '''

    # Check if there is a seed, and if there is, use it
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

    # When all trials have their randomly generated conditions, return a list of dicts
    return trials_info

def GenerateStimulus(condition = "ColPopOut", target = 1, stimulusnum = 10):
    '''
    Takes a condition, whether a target is present, and the stimulusnum to generate an image of randomly placed non-overlapping
    x's and o's.
    Used by the GUI, not callable by users

    condition: str, ColPopOut, ShapePopOut, or Conjunction
    target: int, 1 for present, 0 for absent
    stimulusnum: int, must be higher than 4

    Returns: image object
    '''

    # this generates a space for stimuli to be placed
    coordspace = [(x, y) for x in range(50) for y in range(50)]
    # from this, take a random sample (this does not repeat, so overlap does not happen)
    coordslist = random.sample(coordspace, k = stimulusnum)

    # only if there is a target, take out one from the list for the target
    if target == 1:
        targetcoords = coordslist[0]
        coordslist = coordslist[1:]

    # Create a plot and set the axes
    plt.figure(figsize = (7,7))
    plt.axis([-5, 55, -5, 55])

    # subset coordinates for ColPopOut distractors
    if condition == "ColPopOut":

        # Select first half of coordinates
        BlackO = coordslist[:len(coordslist)//2]
        # split into x and y coordinates, and place
        BlackOx, BlackOy = zip(*BlackO)
        plt.plot(BlackOx, BlackOy, "ko")

        # Select second half of coordinates
        BlackX = coordslist[len(coordslist)//2:]
        # split into x and y coordinates, and place
        BlackXx, BlackXy = zip(*BlackX)
        plt.plot(BlackXx, BlackXy, "kx")

    # subset coordinates for ShapePopOut distractors
    elif condition == "ShapePopOut":

        # Select first half of coordinates
        BlackO = coordslist[:len(coordslist)//2]
        # split into x and y coordinates, and place
        BlackOx, BlackOy = zip(*BlackO)
        plt.plot(BlackOx, BlackOy, "ko")

        # Select second half of coordinates
        RedO = coordslist[len(coordslist)//2:]
        # split into x and y coordinates, and place
        RedOx, RedOy = zip(*RedO)
        plt.plot(RedOx, RedOy, "ro")

    # subset coordinates for conjunction distractors
    elif condition == "Conjunction":

        # Select first third
        BlackO = coordslist[:len(coordslist)//3]
        # split into x and y coordinates, and place
        BlackOx, BlackOy = zip(*BlackO)
        plt.plot(BlackOx, BlackOy, "ko")
        
        # Select second third
        RedO = coordslist[len(coordslist)//3:len(coordslist)//3 * 2]
        # split into x and y coordinates, and place
        RedOx, RedOy = zip(*RedO)
        plt.plot(RedOx, RedOy, "ro")

        # Select final third
        BlackX = coordslist[len(coordslist)//3 * 2:]
        # split into x and y coordinates, and place
        BlackXx, BlackXy = zip(*BlackX)
        plt.plot(BlackXx, BlackXy, "kx")

    # If none of the conditions apply
    else:
        print("Error: Invalid Condition")

    # If there is a target, place it
    if target == 1:
        plt.plot(targetcoords[0], targetcoords[1], "rx")

    # Style that places the least amount of grid to distract the participant
    plt.style.use('_mpl-gallery-nogrid')

    # convert to fig object, and then to img object
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)

    # Close the fig object, or else python will eventually take issue with having 50 of them open
    plt.close(fig)

    return img


def SaveResult():

    '''
    Saves the results in a previously selected directory
    Takes no inputs, returns no values
    '''

    # Turn the list of dicts that kept track of trials and user responses into a dataframe
    global randomised_trials
    df = DataFrame(randomised_trials)

    # Use the config to tell where to save it and how to name it based on study ID and participant ID
    global config
    filename = config["SaveFilePath"] + "/" + "VSTresult" + config["Study ID"] + config["Participant ID"] + ".csv"
    # Saved with the sep set as ; because this plays nice with Dutch excel settings
    df.to_csv(filename, sep = ";")


# General functions ---------------------------------------------------------------------------------------

def UpdateConfig():

    '''
    Updates the config variable based on the entry boxes
    Takes no inputs, returns no values
    '''

    # For each part of the config with an entry box, use .get() while converting to the right type where needed
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
    Takes no inputs, returns no values
    '''

    # For each Entry box, load it in globally, delete the current values in it, and insert the value from the config
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



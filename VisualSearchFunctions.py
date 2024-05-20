
# This document has had the functions moved to GUItesting
# This is now treated as a sort of sketch for what will be needed

'''
To Do:

- Config handling
- GUI handling
    - Different screens
    - Filling in config!
    - Showing trials of the experiment in the GUI
    - Responding to user input during trials
- Saving experiment data
'''

# So what does the config look like? It would probably be a dict a bit like this:
'''
config = {
    "Experiment Type": "VST",
    "Total Trials": 200,
    "Block size": 20,
    "ColPopOutPercent": 10,
    "ShapePopOutPercent": 10,
    "TargetPercent": 50,
    "Possible Stimulus Amounts": [4, 10, 20],
    "Seed": None,
    "Study ID": "test_run",
    "Participant ID": "001",
    "SaveFilePath": "C:\Documents\Research\VST_test"
}

'''

'''
So what exactly does the keylogger need to do? What does the experiment look like?
The experiment starts, the participant sees a screen (GUI) with an explanation for how to
continue, they press the button (listener for keyboard). Actually looking into it, it looks
like tkinter can also handle this actually so the keyboard module is not actually needed.
tkinter treats keypresses as an event, so now it's a matter of deciding what happens when a
keypress event occurs!

When a keypress occurs:

is it esc? -> open window asking if you want to close the program, including a warning
for possible unsaved progress.

is it another special character? -> possibly ignore

is the experiment running? -> if not, do nothing! buttons and fields handle everything needed
are you on the introduction? -> define specific behaviour here for the introduction

are you on a trial? -> save the keypress, elapsed time, and prep next trial

something like:

if trial_shown == True:
    response_time = time.time() - start_time
    dict$response_time[i] = response_time
    dict$keypress[i] = event.char
'''

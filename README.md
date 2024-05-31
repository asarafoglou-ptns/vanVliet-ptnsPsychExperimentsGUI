# PsychExperimentsGUI
This package provides a simple GUI that is capable of running a Visual Search Task. The task has a default configuration, but the user canchange several experimental values values such as the percentage of the time that the target is present, or the amount of distractors. They can also save their own preferred settings and load these in again for future experiments. The results of the Visual Search Task will be saved in a folder specified in the configuration.

There are plans to implement a Wisconsin Card Sorting Task in the future, this is currently not implemented beyond showing a button on the welcome screen.

## Installation
To install the package from GitHub, run the following in a command prompt terminal:

``py -m pip install "PsychExperimentsGUI @ git+https://github.com/asarafoglou-ptns/vanVliet-ptnsPsychExperimentsGUI"``

## Scenario:

### Purpose
Scenario that describes the use of the GUI to run a psychological experiment and save results.

### Individual
Researcher A, PhD student at UvA

### Equipment
A computer able to run python scripts, tested on Windows 10, effectiveness on other operating systems unknown.
Package dependencies: pillow, matplotlib, and pandas.

### Description
1. Researcher A installs the package from the terminal, imports the package, and uses InitGUI() to start the GUI
2. Researcher A selects the experiment type Visual Search Task
3. This is the first time researcher A uses this GUI, so they look at the default settings, add a study ID, participant ID, choose a directory to save to, and adjust the distractor amounts from ``4, 10, 20`` to just ``10, 20``. The other settings match what they want already.
4. They click "save config" and a file explorer window opens where they navigate to their experiment folder, and name their config "expconfig".
5. They click to go to the next page, and are shown their current settings. They notice that the block size is actually not what they want, so they click “back”.
6.	Back on the configuration screen, they change the block size to 10, save the config again (overwriting the old one), then click “next” to go back to the screen that shows the current settings.
8.	After checking that the settings are right this time, they continue to the experiment and the GUI changes to a fullscreen view of the explanation for the participant.
9.	The researcher now shows the screen to the participant, as well as providing the relevant controls (keyboard).
10.	The participant follows the instructions to complete the experiment, during this keypresses are logged and timed by the program.
11.	When the experiment completes, a final button press closes the experiment view and results are automatically saved as a csv, named for the study, experiment type, and participant.
12.	The researcher closes the program, and navigates to the folder where the csv file was saved. They can now use this data for analysis.
13.	When the researcher starts another experiment later, after selecting the Visual Search Task they click "load config", navigate to their experiment folder, click on the config they saved before, and are shown the settings they wanted. All they have to do now is adjust the participant ID, and run the experiment.

## Flowchart

## Example application and how to use the UI
After installing the package, the following lines need to be used in a Python terminal or script:
``import PsychExperimentsGUI``
``PsychExperimentsGUI.InitGUI()``

This will open the following screen:

![afbeelding](https://github.com/asarafoglou-ptns/vanVliet-ptnsPsychExperimentsGUI/assets/157616983/4a220769-cccb-44c9-85cc-924cafce5661)

As the Wisconsin Card Sorting Task is not implemented, click on Visual Search Task.
This leads to the following screen:

![afbeelding](https://github.com/asarafoglou-ptns/vanVliet-ptnsPsychExperimentsGUI/assets/157616983/3f3fe1d2-5338-4726-96f5-372b09d28b30)

Here you can change experimental parameters by editing values in the red box (highlighted below). Only use numbers for this, and for "Possible stimulus amounts" separate numbers with a comma and space as in the default setting. Do not set a possible stimulus amount lower than 4. The percentages for colour pop-out and shape pop-out should not add up to more than 100.

![afbeelding](https://github.com/asarafoglou-ptns/vanVliet-ptnsPsychExperimentsGUI/assets/157616983/f50dc1d1-a495-4565-832b-23b56a4527ec)


In the green highlighted box you have to fill in the informaton needed to save the results. For study ID and participant ID you can fill in anything that helps you identify what study the results were for, and from which participant they came. The bottom row is to decide where the results should be saved, on the right is a button with ``...`` which can be clicked to open a window that lets you navigate to the folder you want to use.

After this, if you want to be able to reuse these settings easily later, you can click "Save config" in the blue box. This opens a window where you can navigate to the folder you want to save to, and write a name for the file. Later on if you want to load these settings in again for your next experiment, you click "Open config" in the blue box, navigate back to this folder, and open the file you saved.

From this screen, clicking "Back" brings you to the previous screen, while clicking "Continue" brings you to a screen where you can see a summary of your settings.

![afbeelding](https://github.com/asarafoglou-ptns/vanVliet-ptnsPsychExperimentsGUI/assets/157616983/090c241a-5d7c-4aca-91cb-51d10d803c64)

Here you can check your settings one last time. If you notice something that should be different, you can go back with "Change Settings". If everything is as you want it to be, you can click "Start Experiment".

After this, the window goes to fullscreen mode and the following instructions are shown:

![afbeelding](https://github.com/asarafoglou-ptns/vanVliet-ptnsPsychExperimentsGUI/assets/157616983/3041f638-86ce-47dd-bb95-33ba4c85dc34)

(Note: the mouse is still visible in fullscreen, it is best to move this into the right side of the screen to avoid it distracting the participant)

From this point onwards, there is no button visible to close the window with. However, it is possible to exit out of the program by pressing ``Esc``. **WARNING:** doing this will close the program immediately, without asking for confirmation and without saving results.

At this point the participant should be shown the screen and offered the keyboard. When they press enter, the first stimulus is shown. For example:

![afbeelding](https://github.com/asarafoglou-ptns/vanVliet-ptnsPsychExperimentsGUI/assets/157616983/2014af19-ef3c-478f-95be-774723ec6151)

(Note: the stimuli may take up a larger or smaller portion of the screen, depending on the screen's size. For the first stimulus the numbers on the axes are visible as well, this is not true for later stimuli.)

Above you can see an example of a conjunction task, with the target absent. This has distractors both for colour (red) and shape (x).

For a shape pop-out trial, only colour distractors are present:

![afbeelding](https://github.com/asarafoglou-ptns/vanVliet-ptnsPsychExperimentsGUI/assets/157616983/08319bd6-a40d-4fbc-9cc2-2517da8318e7)


For a colour pop-out trial, only shape distractors are present:

![afbeelding](https://github.com/asarafoglou-ptns/vanVliet-ptnsPsychExperimentsGUI/assets/157616983/d4094e7c-90b0-4b0a-9001-8be875b12b08)

After a number of trials specified in the Block size setting, the following screen will be shown:

![afbeelding](https://github.com/asarafoglou-ptns/vanVliet-ptnsPsychExperimentsGUI/assets/157616983/ff520645-4713-4eb7-8aa7-95d1b36645b2)

After the participant presses enter, they are again shown stimuli. Once all trials are completed, their results are saved and they will be shown the ending screen:

![afbeelding](https://github.com/asarafoglou-ptns/vanVliet-ptnsPsychExperimentsGUI/assets/157616983/ccf33b34-2b82-42eb-ae74-1ebae1d07655)

Pressing enter here will lead to the following screen:

![afbeelding](https://github.com/asarafoglou-ptns/vanVliet-ptnsPsychExperimentsGUI/assets/157616983/e5786b65-0658-433c-af9b-24f6b64e50a5)

The program can now be closed or you can click the button to go back to the experiment selection screen

![afbeelding](https://github.com/asarafoglou-ptns/vanVliet-ptnsPsychExperimentsGUI/assets/157616983/6026a0d3-9b57-4268-85cb-b318ee2e1856)

The result of this is a .csv file, which has the following structure:

[add image after fixing bug]

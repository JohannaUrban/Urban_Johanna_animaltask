import csv
from random import randint

from psychopy import core, event, visual
from psychopy.hardware import keyboard
from psychopy.gui import Dlg

import random

#-----------------------------------------------------------------------------
#Testing version vs.  Full experiment
#------------------------------------------------------------------------------
testing= True 

if testing:
    trial_number=5     
else:
    trial_number=72    

#-------------------------------------------------------------------------------
#Participant ID
#-------------------------------------------------------------------------------
ID = Dlg(title='ID')
ID.addField(label='participant_ID')
ID.show()
participant_id = ID.data[0]

print("Participant ID: ", participant_id)


#------------------------------------------------------------------------------
#Instructions
#------------------------------------------------------------------------------

# Create a window to display the task
win = visual.Window([1000, 600], color='black')

# Welcome and instructions screen
instruction_text = """Welcome to the animal performance task!

Instructions

In this task, you will be presented 4 different animals: 
    dog, frog, duck, and cat.
    
You will see one animal, then a blank screen, and then another animal. Then you will be asked to choose a key.

(Press space to continue)"""
instructions = visual.TextStim(win, text=instruction_text, wrapWidth=700, color = 'red', units='pix')
instructions.draw()
win.flip()
event.waitKeys(keyList=['space'])

instruction_text = """
Instructions

Your task is to help the dog tell the cat that it's feeding time. 
So, when the dog is presented followed by a cat, press 'F' for food.

But the cat is thirsty, too! 
You also need to help the duck tell the cat that it's time to drink.
So, when the duck is presented followed by a cat, press 'D' for drink.

For all other animal combinations, press 'X' for no food or drink.

Wait for the prompt before pressing a key.

(Press space to continue)"""
instructions = visual.TextStim(win, text=instruction_text, wrapWidth=700, units='pix')
instructions.draw()
win.flip()
event.waitKeys(keyList=['space'])

instruction_text = """
Instructions

Respond as quickly and accurately as you can. Performance feedback will be provided after each trial.

If you want to quit the test, you need to press q as soon as you are asked to press a key. 

Get ready: Put your fingers on the X, D, F response buttons.

(Press space to get started)"""
instructions = visual.TextStim(win, text=instruction_text, wrapWidth=700, units='pix')
instructions.draw()
win.flip()
event.waitKeys(keyList=['space'])

#-------------------------------------------------------------------------------
#Trial details
#-------------------------------------------------------------------------------

# Define the possible combinations of animals that will be presented
combinations = [] 
for i in range (18): 
    combinations.append (('Duck', 'Cat'))    #  -> D
    combinations.append (('Dog', 'Cat'))     #  -> F  
for i in range (4):
    combinations.append (('Cat', 'Dog'))     #  -> X
    combinations.append (('Dog', 'Frog'))    #  -> X 
    combinations.append (('Frog', 'Dog'))    #  -> X
    combinations.append (('Cat', 'Frog'))    #  -> X
    combinations.append (('Frog', 'Cat'))    #  -> X
    combinations.append (('Dog', 'Duck'))    #  -> X
    combinations.append (('Duck', 'Dog'))    #  -> X
    combinations.append (('Cat', 'Duck'))    #  -> X
    combinations.append (('Frog', 'Duck'))   #  -> X
    combinations.append (('Duck', 'Frog'))   #  -> X

# Create a keyboard object to record the participant's keypresses
kb = keyboard.Keyboard()
keys = kb.getKeys()

# Keep track of the number of trials
attemp_count = 0

# Initalize list to store results for savings as csv later
file_output = []
file_output.append('Evaluation of your animal performance test;')
file_output.append('participant_id; attemp count; key; correct/incorrect; reaction time (ms) ;animal 1; animal 2;')

# Initalize variables for average reaction time and number of correct answers
avg_reaction_time = 0
good_attemps_count  = 0

# Randomize list
random.shuffle(combinations)
    
# Loop showing animal combinations
counter=-1 
while 'escape' not in keys and attemp_count <trial_number:
  
    # Increase number of trial 
    attemp_count = attemp_count + 1
    print('Attemp #' + str(attemp_count))
    
    #List counter
    counter=counter+1
    
    #Choose stimulus
    animal_1 = combinations[counter][0]
    animal_2 = combinations[counter][1]
    
    # Display first animal for 500 ms
    animal_stim = visual.ImageStim(win, size=[0.6, 0.9], image=animal_1 + '.png')
    animal_stim.draw()
    win.flip()
    core.wait(0.5)

    # Blank delay for 1300ms 
    win.flip()		
    core.wait(1.3)
    
    # Display second animal for 500 ms
    animal_stim = visual.ImageStim(win, size=[0.6, 0.9], image=animal_2 + '.png')
    animal_stim.draw()
    win.flip()
    core.wait(0.5)
    
    # Ask to choose a key
    instruction_key = visual.TextStim(win, text='Choose a key now.')
    instruction_key.draw()
    win.flip()
    
#-------------------------------------------------------------------------------
#Recording of responses
#-------------------------------------------------------------------------------
    
    Clock = core.Clock()
    keys = event.waitKeys(keyList=['x', 'f', 'd', 'q'], timeStamped = Clock)

    # Check correctness of responses
    correctUserInput = 'false'
    if keys:
        reaction_time = keys[0][1]
        if keys[0][0] == 'd':
            if combinations[counter] == ('Duck', 'Cat'):
                correctUserInput = 'correct'
        if keys[0][0] == 'f': 
            if combinations[counter] == ('Dog', 'Cat'):
                correctUserInput = 'correct'
        if keys[0][0] == 'x':
            if combinations[counter] not in [('Duck', 'Cat'), ('Dog', 'Cat')]:
                correctUserInput = 'correct'
        if keys[0][0] == 'q':
            win.close()
            core.quit()
    else:
        reaction_time = 0

#-------------------------------------------------------------------------------
# Immediate feedback
#-------------------------------------------------------------------------------
    # Generate feedback after each trial
    if keys:
        if correctUserInput == 'correct':
            feedback_stim = visual.TextStim(win, text="Well done! Your answer was " + correctUserInput + ". Your reaction time was " + str(round(reaction_time,2)) + " ms.")
        else:
            feedback_stim = visual.TextStim(win, text="Sorry, your answer was " + correctUserInput +".")
    
    # Display feedback screen
    feedback_stim.draw()
    win.flip()
    core.wait(3)

    # Update reaction time and number of correct answers
    avg_reaction_time = avg_reaction_time + reaction_time
    if correctUserInput == 'correct':
        good_attemps_count = good_attemps_count + 1
        
#-------------------------------------------------------------------------------
# Save Output in a file
#-------------------------------------------------------------------------------
    # Add data to file output
    feedbackToFile = participant_id + ";" + "#" + str(attemp_count) + ";" + str(keys[0][0]) + ";" + correctUserInput + ";" + str(reaction_time)  + ";" + str(animal_1) + ";" + str(animal_2) 
    file_output.append(feedbackToFile)

file_output.append(' ')
file_output.append('Testresults')

#After all trials are completed, calculate the average reaction time and accurate cells in percents
str_reaction_time = avg_reaction_time / attemp_count
str_accurate_calls = good_attemps_count * 100 / attemp_count
file_output.append('average reaction time (ms);' + str(str_reaction_time))
file_output.append('accurate calls (percent);' + str(str_accurate_calls))

# Writing result to disk
print('--- Writing result file ---')
with open("animal-test-result.csv", "w") as file:
    writer = csv.writer(file)
    for s in file_output:
        writer.writerow([s])

#-------------------------------------------------------------------------------
# Results and end screen
#-------------------------------------------------------------------------------
# Show final results
feedback_text="""
Your test-results have been saved as an excel file.

Your average reaction-time was: """ + str(round(str_reaction_time,2)) +""" ms. 

You percentage of accurate calls was: """ + str(round(str_accurate_calls,2)) + """ 

(press space to continue)"""

feedback_screen = visual.TextStim(win, text=feedback_text, wrapWidth=700, units='pix')  
feedback_screen.draw()
win.flip()
event.waitKeys(keyList=['space'])

# End screen
end_text=""" 
Thank you for your participation! 

The window will close automatically.
"""
end_screen = visual.TextStim(win, text=end_text, wrapWidth=700, color='red', units='pix')
end_screen.draw()
win.flip()
core.wait(3)

# Close window
win.close()
core.quit()
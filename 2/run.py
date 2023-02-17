from models import *
from time import sleep

states = StateModel( 8, 8) # 448 = 128 states
loc = Localizer( states)
tMat = loc.get_transition_model()
sVecs = loc.get_observation_model()

# count how many times the sensed position is the same as the true position
correct = 0
total = 0
total_manhattan = 0

def sensedIsCorrect(trueR, trueC, sensedR, sensedC):
    global total
    total += 1
    return trueR == sensedR and trueC == sensedC

for i in range(0, 100):
    sensed, trueR, trueC, trueH, sensedR, sensedC, guessedR, guessedC, error, f = loc.update()
    if sensedIsCorrect(trueR, trueC, sensedR, sensedC):
        correct += 1


    print("Sensed: ", sensed, "True: ", trueR, trueC, trueH, "Sensed: ", sensedR, sensedC, "Guessed: ", guessedR, guessedC, "Error: ", error)

print("Correct: ", loc.get_correct(), "Avg Manhattan: ", loc.get_avg_manhattan(), "Correct Sensed", correct/total)
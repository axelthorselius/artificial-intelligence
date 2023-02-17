
import random
import numpy as np

from models import TransitionModel,ObservationModel,StateModel

#
# Add your Robot Simulator here
#
class RobotSim:
    def __init__(self, tm, sm, om):
        self.__tm = tm
        self.__sm = sm
        self.__om = om

        print("RobotSim init")
    
    def move_robot(self, ts):
        probs = self.__tm.get_T()
        next_state = np.random.choice(self.__sm.get_num_of_states(), p=probs[ts])
        return next_state

    def sense(self, ts):
        reading = self.__sm.state_to_reading(ts)
        probs = self.__om.get_o_reading(reading)
        probs = np.diag(probs)
        
        nbr_states = self.__sm.get_num_of_states()
        none_prob = self.__om.get_o_reading_state(None, ts)

        if random.random() < none_prob:
            return None
        
        probs = probs / np.sum(probs)
        sense = np.random.choice(nbr_states, p=probs)
        sense = self.__sm.state_to_reading(sense)
        return sense
        
class HMMFilter:
    def __init__(self, sm, om):
        self.__sm = sm
        self.__om = om
        
        print("HMMFilter init")
    
    def forward_filter(self, sense, Tt, f):
        o = self.__om.get_o_reading(sense)
        f = np.dot(o, np.dot(Tt, f))
        best = self.__sm.state_to_position(np.argmax(f))
        return f/np.sum(f), best
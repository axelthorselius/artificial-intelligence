
import random
import numpy as np

from models import TransitionModel,ObservationModel,StateModel

#
# Add your Robot Simulator here
#
class RobotSim:
    def __init__(self, tm, sm):
        self.__tm = tm
        self.__sm = sm

        print("RobotSim init")
    
    def __available_headings(self, row, col) -> list:
        # 0 = south
        # 1 = east
        # 2 = north
        # 3 = west
        headings = []
        num_rows, num_cols, _ = self.__sm.get_grid_dimensions()
        # row cant be > num_rows so no redundancy needed
        if row > 0:
            headings.append(2)
        if col > 0:
            headings.append(3)
        if row < num_rows - 1:
            headings.append(0)
        if col < num_cols - 1:
            headings.append(1)
        return headings
    
    def __new_pos_from_heading(self, heading, row, col):
        # current_row, current_col= self.__sm.state_to_position(self.__trueState)
        if heading == 0:
            row += 1
        if heading == 1:
            col += 1
        if heading == 2:
            row -= 1
        if heading == 3:
            col -= 1
        return row, col
            
    # return the next state 
    def move_robot(self, ts) -> int:
        row, col = self.__sm.state_to_position(ts)
        available_headings = self.__available_headings(row, col)
        prob_list = []
        for h in available_headings:
            new_row, new_col = self.__new_pos_from_heading(h, row, col)
            next_state = self.__sm.pose_to_state(new_row, new_col, h)
            prob = self.__tm.get_T_ij(ts, next_state)
            prob_list.append(prob)
        heading = random.choices(available_headings, weights=prob_list, k=1)[0]
        new_row, new_col = self.__new_pos_from_heading(heading, row, col)
        next_state = self.__sm.pose_to_state(new_row, new_col, heading)
        return next_state
    
    def simulated_sensor_reading(self, ts) -> int:
        # # p = prob
        # # w = wall
        # # nw = no wall
        # # s = same heading
        # # ns = not same heading
        # p_s_nw = 0.7
        # p_ns_nw = 0.3
        # p_s_w = 0.0
        # p_ns_w = 1.0
        p_L = 0.1
        p_n_Ls = 0.05
        p_n_Ls2 = 0.025
        # p_none = 1 # for now. 'nothing' prob will be decreased
        
        row, col = self.__sm.state_to_position(ts)
        num_rows, num_cols, _ = self.__sm.get_grid_dimensions()

        # for row_i in [-1, 1]:
        #     for col_i in [-1, 1]:

        pos_list = []
        prob_list = []
        for row_i in range (-2, 2):
            for col_i in range (-2, 2):
                # real (actual) row and col
                r_row = row + row_i
                r_col = col + col_i
                if r_row > 0 and r_row < num_rows - 1 and r_col > 0 and r_col < num_cols -1:
                    pos_list.append((r_row, r_col))
                    # secondary surrounding fields
                    if abs(row_i) == 2 or abs(col_i) == 2:
                        prob_list.append(p_n_Ls2)
                        # p_none -= p_n_Ls2
                    # true loc
                    elif row_i == 0 and col_i == 0:
                        prob_list.append(p_L)
                        # p_none -= p_L
                    # surrounding fields
                    else:
                        prob_list.append(p_n_Ls)
                        # p_none -= p_n_Ls
        pos_list.append(None)
        prob_list.append(1 - sum(prob_list))
        choice = random.choices(pos_list, weights=prob_list, k=1)[0]
        if (choice != None):
            new_row, new_col = choice
            # does heading matter?
            # sim_state = self.__sm.pose_to_state(new_row, new_col, 0)
            sim_reading = self.__sm.position_to_reading(new_row, new_col)
            return sim_reading
        
        return None
                    

#
# Add your Filtering approach here (or within the Localiser, that is your choice!)
#
class HMMFilter:
    def __init__(self, sm, om):
        self.__sm = sm
        self.__om = om
        
        print("HMMFilter init")
    
    def forward_filter(self, sense, Tt, f):
        o = self.__om.get_o_reading(sense)
        f = np.dot(o, np.dot(Tt, f))
        # print('f')
        # print(f)
        # print('f/np.sum(f)')
        # print(f/np.sum(f))
        # print('np.sum(f)')
        # print(np.sum(f))
        # print('len(f)')
        # print(len(f))
        # print('np.argmax(f)')
        # print(np.argmax(f))
        best = self.__sm.state_to_position(np.argmax(f)) # Why state and not reading?
        return f/np.sum(f), best
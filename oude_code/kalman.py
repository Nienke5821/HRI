import numpy as np

class KalmanFilter():
    def __init__(self):
        self.A = np.eye(2)
        self.C = np.eye(2)


        ###
        # self.x = [left
                #   right]

class Disturbances(object):
    def __init__(self):
        self.flag = True

    def update_disturbances(self):
        if self.flag:
            print('dist')

    def get_disturbance_torque(self):
        return 0
import time


class Datetime:

    def __init__(self, cooldown: int):
        self.cooldown = cooldown
        self.first_date = int(time.time())
        self.second_date = self.first_date + self.cooldown

    def get_delta_time(self):
        return self.second_date - int(time.time())

    def reset_cd(self):
        self.__init__(cooldown=self.cooldown)

    def check(self):
        return time.time() >= self.second_date






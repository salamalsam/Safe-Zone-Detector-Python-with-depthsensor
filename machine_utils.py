class Machine:
    def __init__(self):
        self.is_on = False
        self.is_turning = False
        self.turning_speed = None

    def turn_on(self):
        if self.is_on:
            print("Machine is already on.")
        else:
            self.is_on = True
            print("Machine turned on.")

    def turn_off(self):
        if not self.is_on:
            print("Machine is already off.")
        else:
            self.is_on = False
            self.is_turning = False
            self.turning_speed = None
            print("Machine turned off.")

    def status(self):
        if self.is_on:
            status_msg = "Machine is on."
            if self.is_turning:
                status_msg += f" Turning speed: {self.turning_speed}."
            print(status_msg)
        else:
            print("Machine is off.")

    def turn_slow(self):
        if not self.is_on:
            print("Cannot turn. Machine is off.")
        else:
            self.is_turning = True
            self.turning_speed = "slow"
            print("Machine is turning slow.")

    def turn_fast(self):
        if not self.is_on:
            print("Cannot turn. Machine is off.")
        else:
            self.is_turning = True
            self.turning_speed = "fast"
            print("Machine is turning fast.")

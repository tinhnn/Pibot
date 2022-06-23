
from Adafruit_MotorHAT import Adafruit_MotorHAT

class MotorController:
    MOTOR_LEFT  = 1
    MOTOR_RIGHT = 2
    def __init__(self) -> None:
        # open Adafruit MotorHAT driver
        self.driver = Adafruit_MotorHAT(i2c_bus=1)
        # get motor objects from driver
        self.motors = {
            self.MOTOR_LEFT : self.driver.getMotor(self.MOTOR_LEFT),
            self.MOTOR_RIGHT : self.driver.getMotor(self.MOTOR_RIGHT)
        }
        
        self.pwm_channels = {
            self.MOTOR_LEFT : (1, 0),
            self.MOTOR_RIGHT : (2, 3)
        }

    def set_speed(self, mot_l_spd, mot_r_spd):
        self._set_pwm(self.MOTOR_LEFT, mot_l_spd)
        self._set_pwm(self.MOTOR_LEFT, mot_r_spd)
        pass

    def motor_stop(self):
        self.set_speed(0, 0)
        pass

    def __set_pwm(self, mot_id, vel):
        pwm = int(min(max((abs(vel)) * self.max_pwm, 0), self.max_pwm))
        self.motors[mot_id].setSpeed(pwm)

        # set the motor direction
        ina, inb = self.pwm_channels[mot_id]
        
        if vel > 0:
            self.motors[mot_id].run(Adafruit_MotorHAT.FORWARD)
            self.driver._pwm.setPWM(ina, 0, pwm * 16)
            self.driver._pwm.setPWM(inb, 0, 0)
        elif vel < 0:
            self.motors[mot_id].run(Adafruit_MotorHAT.BACKWARD)
            self.driver._pwm.setPWM(ina, 0, 0)
            self.driver._pwm.setPWM(inb, 0, pwm * 16)
        else:
            self.motors[mot_id].run(Adafruit_MotorHAT.RELEASE)
            self.driver._pwm.setPWM(ina, 0, 0)
            self.driver._pwm.setPWM(inb, 0, 0)
        pass

# end of file

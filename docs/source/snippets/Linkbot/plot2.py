import linkbot3 as linkbot

class MotorPlot():
    def __init__(self):
        self.angles = []
        self.times = []

    def cb(self, angle, timestamp):
        print('cb', angle, timestamp)
        self.angles.append(angle)
        self.times.append(timestamp)

l = linkbot.Linkbot('7944')
l.motors.reset()
l.motors.move([0,0,0], relative=False)
myplot = MotorPlot()
l.motors[0].set_event_handler(myplot.cb)
l.motors[0].set_controller(linkbot.peripherals.Motor.Controller.SMOOTH)
l.motors[0].set_accel(30)
l.motors[0].set_decel(30)
l.motors[0].move(360)
print('Plotting...')
linkbot.plot(myplot.times, myplot.angles)

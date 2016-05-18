import linkbot3 as linkbot
from matplotlib import pyplot

class MotorPlot():
    def __init__(self):
        self.angles = []
        self.times = []

    def cb(self, angle, timestamp):
        print('cb', angle, timestamp)
        self.angles.append(angle)
        self.times.append(timestamp)

l = linkbot.Linkbot('XJLL')
myplot = MotorPlot()
l.motors[2].set_event_handler(myplot.cb)
l.motors[2].move(900)
print('Plotting...')
pyplot.plot(myplot.times, myplot.angles)
pyplot.show()
input()

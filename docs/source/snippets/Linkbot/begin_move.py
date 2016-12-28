import linkbot3 as linkbot
import time


robot = linkbot.Linkbot("ZRG6")
robot.motors[0].begin_move()
robot.motors[2].begin_move()
time.sleep(1)
robot.motors[0].begin_move(forward=False)
robot.motors[2].begin_move(forward=False)
time.sleep(1)
robot.motors[0].begin_move(forward=False)
robot.motors[2].begin_move()
time.sleep(1)
robot.motors[0].begin_move()
robot.motors[2].begin_move(forward=False)
time.sleep(1)
robot.motors.stop()

import math
from objects import *

def defaultPD(agent, c, local,):
    turn = math.atan2(local[1],local[0])
    up =  agent.me.matrix.dot(Vector3(0,0,agent.me.location[2]))
    target = [math.atan2(up[1],up[2]), math.atan2(local[2],local[0]), turn]
    c.steer = steerPD(turn, 0)
    c.yaw = steerPD(target[2],-agent.me.rvel[2]/5)
    c.pitch = steerPD(target[1],agent.me.rvel[1]/5)
    c.roll = steerPD(target[0],agent.me.rvel[0]/5)
    return target

def flip(agent,c,local):
    #assumes controller will handle recovery
    pitch = -sign(local[0])
    if not agent.me.airborn:
        c.jump = True
        agent.sinceJump = 0
    if agent.sinceJump <= 0.05:
        c.jump = True
        c.pitch = pitch
    elif agent.sinceJump > 0.05 and agent.sinceJump <= 0.1:
        c.jump = False
        c.pitch = pitch
    elif agent.sinceJump > 0.1 and agent.sinceJump <= 0.13:
        c.jump = True
        c.pitch = pitch
        c.roll = 0
        c.yaw = 0
        
def steerPD(angle,rate):
    final = ((35*(angle+rate))**3)/10
    return cap(final,-1,1)

def throttle(target_speed, agent_speed, direction = 1):
    final = ((abs(target_speed) - abs(agent_speed))/100) * direction
    if final > 1.5:
        boost = True
    else:
        boost = False
    if final > 0 and target_speed > 1400:
        final = 1
    return cap(final,-1,1),boost

def radius(v):
    return 139.059 + (0.1539 * v) + (0.0001267716565 * v * v)

def side(x):
    if x <= 0:
        return -1
    return 1

def sign(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1
    
def cap(x, low, high):
    if x < low:
        return low
    elif x > high:
        return high
    else:
        return x

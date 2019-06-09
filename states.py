from objects import *
from utils import *

class atba():
    def __init__(self):
        self.expired = False
    def execute(self, agent):
        target = agent.ball.location
        targetV = 1410
        return driver(agent, target, targetV)

class shot():
    def __init__(self):
        self.expired = False
    def execute(self, agent):
        goal = Vector3(0, 5100 * -side(agent.team), 93)
        direction = (goal - agent.ball.location).normalize()
        distance = (agent.me.location - agent.ball.location).flatten().magnitude()/2
        target = agent.ball.location - (direction * distance)
        targetV = 2300
        return driver(agent, target, targetV)
def driver(agent, target, targetV):
    local = agent.me.matrix.dot(target - agent.me.location)
    localV = agent.me.matrix.dot(agent.me.velocity)
    r = radius(localV[0])
    slowdown = (Vector3(0,sign(local[1])*(r+40) ,0) - local.flatten()).magnitude()/cap(r*1.5, 1, 1200)
    targetV = cap(slowdown * targetV, 0, targetV) 
    defaultPD(agent, agent.c, local)
    agent.c.throttle, agent.c.boost = throttle(targetV, localV[0])
    return agent.c

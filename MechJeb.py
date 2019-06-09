import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from objects import *
from states import *


class MechJeb(BaseAgent):

    def initialize_agent(self):
        self.c = SimpleControllerState()
        self.me = carObject(self.index)
        self.ball = ballObject()
        self.teammates = []
        self.opponents = []

        self.states = [atba(), shot()]
        self.state = self.states[1]
        self.time = 0.0
        self.sinceJump = 0.0

    def refresh(self):
        self.c.__init__()
        

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        self.refresh()
        self.preprocess(packet)
        return self.state.execute(self)
        

    def preprocess(self, packet):
        elapsed = packet.game_info.seconds_elapsed-self.time
        self.sinceJump += elapsed
        self.time = packet.game_info.seconds_elapsed
        self.ball.update(packet.game_ball)
        for i in range(packet.num_cars):
            car = packet.game_cars[i]
            if i == self.index:
                self.me.update(car)
            elif car.team == self.team:
                flag = True
                for teammate in self.teammates:
                    if i == teammate.index:
                        teammate.update(car)
                        flag = False
                if flag:
                    self.teammates.append(carObject(i,car))
            else:
                flag = True
                for opponent in self.opponents:
                    if i == opponent.index:
                        opponent.update(car)
                        flag = False
                if flag:
                    self.opponents.append(carObject(i,car))


"""
Simulation of Air Ambulance Requirements
Uses basic Monte Carlo simulation techniques to derive statistical
analysis of air ambulance requirements.

IS590PR

Simran Sanjiv Wig - swig2@illinois.edu
Srijith Srinath - ssrina2@illinois.edu
Vinu Prasad Bhambore - vpb2@illinois.edu

"""

from random import choice, randint
import pandas as pd

class Helicopter:

    all_helicopter = []         # automatically track all helicopters

    def __init__(self, name=None, empty_weight=None, max_speed=None, max_distance=None, max_no_people=None):
        Helicopter.all_helicopter.append(self)

        self.name = name
        self.empty_weight = empty_weight
        self.max_speed = max_speed
        self.max_distance = max_distance
        self.max_no_people = max_no_people

    def caluclate_time(self, heli):

        weather = set_weather(heli)

        if weather == "Winter":
            x = 1
        elif weather == "Rainy":
            y = 2
        else:
            z = 1


class condition:

    def __init__(self):

    def set_weather_tendency(self, t: tuple):
        if t is None:
            self.weather_tendency = (1, 1, 1)
        else:
            self.weather_tendency = t

        s, w, r = self.weather_tendency
        self.randmax = s + w + r

    def set_weather(self):
        n = randint(1, self.randmax)
        if n <= self.weather_tendency[0]:
            return 'Winter'
        elif n <= self.weather_tendency[0] + self.weather_tendency[1]:
            return 'Rainy'
        else:
            return 'Summer'


if __name__ == "__main__":

    helicopter_df = pd.read_csv("Helicopter.csv")
    condition_df = pd.read_csv("Condition.csv")

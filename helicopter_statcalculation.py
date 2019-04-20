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


class Helicopter:

    helicopter_count = 0        # Initialize count of all helicopters
    all_helicopter = []         # automatically track all helicopters

    def __init__(self, name=None, weather_tendency=None):
        Helicopter.helicopter_count += 1
        Helicopter.all_helicopter.append(self)

        if name is None:
            self.name = 'Helicopter {:02}'.format(Helicopter.helicopter_count)
        else:
            self.name = name

        self.weather_tendency = None
        self.randmax = None
        self.set_weather_tendency(weather_tendency)

        self.wins = 0

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

    def caluclate_time(self, heli):

        weather = set_weather(heli)

        if weather == "Winter":
            x = 1
        elif weather == "Rainy":
            y = 2
        else:
            z = 1


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

    @staticmethod
    def get_weather_co_ef(w):
        if w == "Summer":
            return 0.96
        elif w == "Winter":
            return 1
        else:
            return 0.92

    @staticmethod
    def get_alt_co_ef(a):

        if a < 10000:
            return 1

        else:
            return (100 - ((a - 10000)/1000)/100

    @staticmethod
    def caluclate_time(heli, condition_obj):

        distance = condition.distance
        max_speed = heli.max_speed
        weather = condition.weather
        no_of_ppl = condition.number_of_people
        altitude = condition.altitude
        wind_speed = condition.wind_speed
        wind_direction = condition.wind_direction
        heli_direction = condition.heli_direction

        weather_co_ef = get_weather_co_ef(weather)

        no_of_ppl_co_ef = (100 - no_of_ppl)/100

        alt_co_ef = get_alt_co_ef(altitude)

        direction_offset = get_relation_between_directions(wind_direction,heli_direction)



class condition:

    def __init__(self, weather_tendency=None, distance=None, number_of_people=None, altitude=None, wind_speed=None):
        self.distance = distance
        self.number_of_people = number_of_people
        self.altitude = altitude
        self.wind_speed = wind_speed


        self.tendency = None
        self.randmax = None
        self.set_weather_tendency(weather_tendency)


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
            return 'Summer'
        elif n <= self.weather_tendency[0] + self.weather_tendency[1]:
            return 'Winter'
        else:
            return 'Rainy'

    def get_distance(self, max_distance):
        if max_distance is None:
            self.distance = randint(1, 400)
        else:
            self.distance = randint(1, max_distance)
        return self.distance

    def get_number_of_people(self, max_number_of_people):
        if max_number_of_people is None:
            self.number_of_people = randint(1, 13)
        else:
            self.number_of_people = randint(1, max_number_of_people)
        return self.number_of_people

    def get_altitude(self, min_altitude, max_altitude):
        if min_altitude is None:
            self.altitude = randint(1000, max_altitude)
        elif max_altitude is None:
            self.altitude = randint(min_altitude, 25000)
        else:
            self.altitude = randint(min_altitude, max_altitude)
        return self.altitude

    def get_wind_speed(self, wind_speed):
        if wind_speed is None:
            self.wind_speed = randint(1, 25)
        else:
            self.wind_speed = randint(1, max_speed)
        return self.wind_speed


if __name__ == "__main__":

    helicopter_df = pd.read_csv("Helicopter.csv")
    condition_df = pd.read_csv("Conditions_file.csv")


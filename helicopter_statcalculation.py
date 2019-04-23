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
    all_helicopters = []  # automatically track all helicopters

    def __init__(self, name=None, empty_weight=None, max_speed=None, max_distance=None, max_no_people=None):
        Helicopter.all_helicopters.append(self)

        self.name = name
        self.empty_weight = empty_weight
        self.max_speed = max_speed
        self.max_distance = max_distance
        self.max_no_people = max_no_people
        self.win_count = 0

    def record_play(self):
        self.win_count += 1

    @staticmethod
    def get_weather_co_ef(w):
        if w == "Summer":
            return 0.05
        elif w == "Winter":
            return 0
        else:
            return 0.1

    @staticmethod
    def get_alt_co_ef(a):
        if a < 10000:
            return 0
        else:
            return ((a - 10000) / 1000) / 100

    @staticmethod
    def get_relation_between_directions(wd, hd):
        if wd == hd:
            return 15
        elif (wd == 'N' and hd == 'S') or (wd == 'S' and hd == 'N') or (wd == 'E' and hd == 'W') or (
                wd == 'W' and hd == 'E'):
            return -25
        else:
            return -5

    @staticmethod
    def caluclate_time(heli, condition_obj):

        distance = condition_obj.distance
        max_speed = heli.max_speed
        weather = condition_obj.weather
        no_of_ppl = condition_obj.number_of_people
        altitude = condition_obj.altitude
        wind_speed = condition_obj.wind_speed
        wind_direction = condition_obj.wind_direction
        heli_direction = condition_obj.helicopter_direction

        weather_co_ef = heli.get_weather_co_ef(weather) * heli.max_speed

        no_of_ppl_co_ef = heli.max_speed * (2 * no_of_ppl) / 100

        alt_co_ef = heli.get_alt_co_ef(altitude) * heli.max_speed

        direction_offset = heli.get_relation_between_directions(wind_direction, heli_direction)
        wind_speed_co_ef = ((direction_offset * wind_speed / 100)/ (heli.empty_weight / 15000)) * 2

        speed = max_speed - no_of_ppl_co_ef - alt_co_ef - weather_co_ef + wind_speed_co_ef

        time = distance / speed

        return time

    @staticmethod
    def get_winner_heli(time_dict):

        print(sorted(time_dict.items()))
        winner = sorted(time_dict.items()[0][0], reverse=True)
        return winner

    def reset_values(self):

        self.win_count = 0


class Condition:

    all_conditions = []

    def __init__(self, weather_tendency=None):
        Condition.all_conditions.append(self)

        self.distance = None
        self.number_of_people = None
        self.altitude = None
        self.wind_speed = None
        self.wind_direction = None
        self.helicopter_direction = None
        self.weather = None

        self.tendency = None
        self.randmax = None
        self.set_weather_tendency(weather_tendency)

    def set_weather_tendency(self, t: tuple):
        if t is None:
            self.weather_tendency = (1, 1, 1)
        else:
            self.weather_tendency = t

        s, w, r = self.weather_tendency
        s = int(s)
        w = int(w)
        r = int(r)
        self.randmax = s + w + r

    def get_weather(self):
        n = randint(1, self.randmax)
        if n <= int(self.weather_tendency[0]):
            self.weather = 'Summer'
        elif n <= int(self.weather_tendency[0]) + int(self.weather_tendency[1]):
            self.weather = 'Winter'
        else:
            self.weather = 'Rainy'

    def get_distance(self, max_distance):
        if max_distance is None:
            self.distance = randint(1, 400)
        else:
            self.distance = randint(1, max_distance)

    def get_number_of_people(self, max_number_of_people):
        if max_number_of_people is None:
            self.number_of_people = randint(1, 10)
        else:
            self.number_of_people = randint(1, max_number_of_people)

    def get_altitude(self, min_altitude, max_altitude):
        if min_altitude is None and max_altitude is None:
            self.altitude = randint(1000, 25000)
        elif min_altitude is None:
            self.altitude = randint(1000, max_altitude)
        elif max_altitude is None:
            self.altitude = randint(min_altitude, 25000)
        else:
            self.altitude = randint(min_altitude, max_altitude)

    def get_wind_speed(self, max_wind_speed):
        if max_wind_speed is None:
            self.wind_speed = randint(1, 25)
        else:
            self.wind_speed = randint(1, max_wind_speed)

    def get_wind_direction(self):
        directions = ['N', 'S', 'W', 'E']
        d = randint(0, 3)
        self.wind_direction = directions[d]

    def get_helicopter_direction(self):
        directions = ['N', 'S', 'W', 'E']
        d = randint(0, 3)
        self.helicopter_direction = directions[d]

    def get_values_conditions(self, max_distance, max_number_of_people, min_altitude, max_altitude, wind_speed):
        self.get_distance(max_distance)
        self.get_number_of_people(max_number_of_people)
        self.get_altitude(min_altitude, max_altitude)
        self.get_wind_speed(wind_speed)

        self.get_wind_direction()
        self.get_helicopter_direction()
        self.get_weather()


if __name__ == "__main__":

    helicopter_df = pd.read_csv("Input_Helicopter_new.csv")
    condition_df = pd.read_csv("Conditions_file.csv")

    for h in range(0,len(helicopter_df)):
        Helicopter(helicopter_df.iloc[h]['Name'], helicopter_df.iloc[h]['Empty_Weight(lbs)'],
                   helicopter_df.iloc[h]['Max_Speed(mph)'],
                   helicopter_df.iloc[h]['Max_Distance(miles)'], helicopter_df.iloc[h]['Max_no_of_people'])

    for c in range(len(condition_df)):
        tendency = tuple(condition_df.iloc[c]['Weather_Tendency'].split('-'))
        Condition(tendency)

    while True:

        no_of_iters = int(input("\nPlease enter the number of simulations to be run: "))

        if no_of_iters == 0:
            break

        for conds in Condition.all_conditions:
            i = 0
            for iters in range(no_of_iters):

                conds.get_values_conditions(condition_df.iloc[i]['Distance'], condition_df.iloc[i]['Number_of_People'],
                                            condition_df.iloc[i]['MinAltitude'], condition_df.iloc[i]['MaxAltitude'],
                                            condition_df.iloc[i]['Wind_Speed'])
                heli_time_dict = {}
                for heli in Helicopter.all_helicopters:
                    time = Helicopter.caluclate_time(heli, conds)
                    heli_time_dict[heli.name] = time

                sorted_heli_dict = sorted(heli_time_dict.items(), key=lambda x: x[1])
                winner_heli = sorted_heli_dict[0][0]

                for heli in Helicopter.all_helicopters:
                    if heli.name == winner_heli:
                        heli.record_play()

            for heli in Helicopter.all_helicopters:
                print(heli.name, heli.win_count)

            i += 1

        for heli in Helicopter.all_helicopters:

            heli.reset_values()



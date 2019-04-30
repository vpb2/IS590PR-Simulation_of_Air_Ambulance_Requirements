"""
Simulation of Air Ambulance Requirements
Uses basic Monte Carlo simulation techniques to derive statistical
analysis of air ambulance requirements.

IS590PR

Simran Sanjiv Wig - swig2@illinois.edu
Srijith Srinath - ssrina2@illinois.edu
Vinu Prasad Bhambore - vpb2@illinois.edu

"""

from random import randint
import pandas as pd

class Helicopter:

    all_helicopters = []  # automatically track all helicopters

    def __init__(self, name=None, empty_weight=None, max_speed=None, max_distance=None, max_no_people=None):
        '''
        initializes all the parameters for the class helicopter
        :param name: Name of the helicopter
        :param empty_weight: Empty weight of the helicopter
        :param max_speed: Maximum speed the helicopter can traverse at
        :param max_distance: Maximmum distance the helicopter can cover
        :param max_no_people: Maximum number of people the helicopter can carry
        '''

        Helicopter.all_helicopters.append(self)

        self.name = name
        self.empty_weight = empty_weight
        self.max_speed = max_speed
        self.max_distance = max_distance
        self.max_no_people = max_no_people
        self.win_count = 0

    def record_play(self):
        '''
        Increases the win count to keep a track of the wins of every helicopter
        '''
        self.win_count += 1

    @staticmethod
    def get_weather_co_ef(w):
        '''
        Calculates the weather coefficient for every weather to be used in  speed calculation
        :param w: Indicates the weather which can be summer, rainy or winter
        :return: Returns the weather coefficient used in speed calculation depending on the weather
        '''
        if w == "Summer":
            return 0.05
        elif w == "Winter":
            return 0
        else:
            return 0.1

    @staticmethod
    def get_alt_co_ef(a):
        '''
        Calculates the altitude coefficient for every helicopter
        :param a: Indicates the altitude of the helicopter
        :return: Returns the altitude coefficient used in speed calculation depending on the value of the altitude
        '''
        if a < 10000:
            return 0
        else:
            return ((a - 10000) / 1000) / 100

    @staticmethod
    def get_relation_between_directions(wd, hd):
        '''
        Checks for the relationship between the speed of the helicopter and speed of thw wind
        :param wd: Indicates the direction of wind
        :param hd: Indicates the direction of the helicopter
        :return: Returns the direction coefficient depending on the wind and the helicopter direction
        '''
        if wd == hd:
            return 15
        elif (wd == 'N' and hd == 'S') or (wd == 'S' and hd == 'N') or (wd == 'E' and hd == 'W') or (
                wd == 'W' and hd == 'E'):
            return -25
        else:
            return -5

    @staticmethod
    def caluclate_time(heli, condition_obj):
        '''
        Calculates the time taken by the helicopter
        :param heli: Instance of the class helicopter
        :param condition_obj: Condition object from the conditions file
        :return: Returns the time taken by the helicopter using speed and distance
        '''

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
        wind_speed_co_ef = ((direction_offset * wind_speed / 100)/ (heli.empty_weight / 18000)) * 2

        speed = max_speed - no_of_ppl_co_ef - alt_co_ef - weather_co_ef + wind_speed_co_ef

        time = distance / speed

        return time

    @staticmethod
    def get_winner_heli(time_dict):
        '''
        Finding the helicopter which won the most number of times by sorting the time dictionary
        :param time_dict: Indicates the time values calculated from the calculate time function
        :return: returns the winner which is the fastest performing helicopter
        '''

        print(sorted(time_dict.items()))
        winner = sorted(time_dict.items()[0][0], reverse=True)
        return winner

    def reset_values(self):
        '''
        Resets the value of the win count variable to zero
        '''
        self.win_count = 0

    def print_values(self, no_of_iters):
        '''
        Prints the name of the helicopter and their win count and win percentage respectively
        :param no_of_iters: indicates the number of iterations or simulations the user wants to perform
        '''
        win_percentage = self.win_count/no_of_iters
        print("%25s %10s %15s" % (self.name, self.win_count, round(win_percentage*100, 2)))


class Condition:

    all_conditions = []

    def __init__(self, weather_tendency=None):
        '''
        :param weather_tendency: indicates the tendency of every weather
        '''
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
        '''
        Generates the inidividual tendencies of the weather
        :param t: tuple which indicates the weather tendency

        '''
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
        '''
        Indicates the actual weather whether it is summer, rainy or winter
        '''
        n = randint(1, self.randmax)
        if n <= int(self.weather_tendency[0]):
            self.weather = 'Summer'
        elif n <= int(self.weather_tendency[0]) + int(self.weather_tendency[1]):
            self.weather = 'Winter'
        else:
            self.weather = 'Rainy'

    def get_distance(self, max_distance):
        '''
        Randomly generates distance in the range of maximum distance
        :param max_distance: maximum distance from the conditions file
        '''
        if max_distance is None:
            self.distance = randint(1, 400)
        else:
            self.distance = randint(1, max_distance)

    def get_number_of_people(self, max_number_of_people):
        '''
        Randomly generates integer for maximum number of people
        :param max_number_of_people: maximum number of people from the conditions file

        '''
        if max_number_of_people is None:
            self.number_of_people = randint(1, 10)
        else:
            self.number_of_people = randint(1, max_number_of_people)

    def get_altitude(self, min_altitude, max_altitude):
        '''
        Randomly generates an integer for altitude between the minimum and maximum altitude
        :param min_altitude: minimum altitude at which the helicopter is required to fly from the conditions file
        :param max_altitude: maximum altitude at which the helicopter is required to fly from the conditions file

        '''
        if min_altitude is None and max_altitude is None:
            self.altitude = randint(1000, 25000)
        elif min_altitude is None:
            self.altitude = randint(1000, max_altitude)
        elif max_altitude is None:
            self.altitude = randint(min_altitude, 25000)
        else:
            self.altitude = randint(min_altitude, max_altitude)

    def get_wind_speed(self, max_wind_speed):
        '''
        Randomly generates an integer for wind speed
        :param max_wind_speed: maximum wind speed from the conditions file
        '''
        if max_wind_speed is None:
            self.wind_speed = randint(1, 25)
        else:
            self.wind_speed = randint(1, max_wind_speed)

    def get_wind_direction(self):
        '''
        Randomly genertaes the wind direction
        '''
        directions = ['N', 'S', 'W', 'E']
        d = randint(0, 3)
        self.wind_direction = directions[d]

    def get_helicopter_direction(self):
        '''
        Randomly generates the helicopter direction
        '''
        directions = ['N', 'S', 'W', 'E']
        d = randint(0, 3)
        self.helicopter_direction = directions[d]

    def get_values_conditions(self, max_distance, max_number_of_people, min_altitude, max_altitude, wind_speed):
        '''
        Creates objects of each of the randomly generated function above
        :param max_distance: maximum distance of the helicopter
        :param max_number_of_people: maximum number of people that a helicopter can carry
        :param min_altitude: minimum altitude at which the helicopter can fly
        :param max_altitude: maximum altitude at which the helicopter can fly
        :param wind_speed: wind speed of the helicopter
        '''
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

        i = 0
        for conds in Condition.all_conditions:
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

            print("\nThe condition looks as follows - ")
            print("Weather Tendency - ", condition_df.iloc[i]["Weather_Tendency"], ", Max distance - ",
                  condition_df.iloc[i]['Distance'], ", Max number of people - ",
                  condition_df.iloc[i]['Number_of_People'], ", Minimum Altitude of location - ",
                  condition_df.iloc[i]['MinAltitude'], ", Maximum Altitude of location - ",
                  condition_df.iloc[i]['MaxAltitude'], ", Max Wind Speed of location - ",
                  condition_df.iloc[i]['Wind_Speed'])

            print("\nThe helicopter statistics are - ")
            print("--------------------------------------------------------")
            print("%25s %10s %15s %%" % ("Name", "Wins", "Win Percentage"))
            print("--------------------------------------------------------")
            for heli in Helicopter.all_helicopters:
                heli.print_values(no_of_iters)

            print("--------------------------------------------------------")

            for heli in Helicopter.all_helicopters:
                heli.reset_values()

            i += 1






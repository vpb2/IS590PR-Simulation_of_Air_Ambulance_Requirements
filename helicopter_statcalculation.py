"""
Simulation of Air Ambulance Requirements
Uses basic Monte Carlo simulation technique to gauge
the optimal performing helicopter to cater air ambulance requirements.

IS590PR by Professor John Weible

Simran Sanjiv Wig - swig2@illinois.edu
Srijith Srinath - ssrina2@illinois.edu
Vinu Prasad Bhambore - vpb2@illinois.edu

"""

from random import randint
import pandas as pd
import math

class Helicopter:

    '''
    >>> h1 = Helicopter("Kamov KA-52", 10000, 180, 450, 20)
    >>> h1.record_play()
    >>> h1.reset_values()
    >>> h1.win_count = 20
    >>> h1.print_values(100)
                  Kamov KA-52         20            20.0

    '''

    all_helicopters = []  # Tracks all helicopters

    def __init__(self, name=None, empty_weight=None, max_speed=None, max_distance=None, max_no_people=None):
        '''
        Initializes all the parameters for the class helicopter
        :param name: Name of the helicopter
        :param empty_weight: Empty weight of the helicopter
        :param max_speed: Maximum speed the helicopter can traverse at
        :param max_distance: Maximmum distance the helicopter can cover in one full tank of fuel
        :param max_no_people: Maximum number of people the helicopter can carry in one trip
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
        Calculates the weather coefficient for every weather to be used in speed calculation
        :param w: Indicates the tendency of weather which can be summer, rainy or winter
        :return: Returns the weather coefficient used in speed calculation depending on the weather

        >>> h1 = Helicopter("Kamov KA-52", 10000, 180, 450, 20)
        >>> h1.get_weather_co_ef("Summer")
        0.05
        >>> h1.get_weather_co_ef("Winter")
        0
        >>> h1.get_weather_co_ef("Rainy")
        0.1
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

        >>> h1 = Helicopter("Kamov KA-52", 10000, 180, 450, 20)
        >>> h1.get_alt_co_ef(8000)
        0
        >>> h1.get_alt_co_ef(15000)
        0.05

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

        >>> h1 = Helicopter("Kamov KA-52", 10000, 180, 450, 20)
        >>> h1.get_relation_between_directions('N', 'N')
        15
        >>> h1.get_relation_between_directions('E', 'W')
        -25
        >>> h1.get_relation_between_directions('N', 'W')
        -5
        '''

        if wd == hd:
            return 15
        elif (wd == 'N' and hd == 'S') or (wd == 'S' and hd == 'N') or (wd == 'E' and hd == 'W') or (
                wd == 'W' and hd == 'E'):
            return -25
        else:
            return -5

    @staticmethod
    def get_no_of_trips(heli_no_of_ppl, cond_max_no_of_ppl):
        '''
        Calculates the number of trips that the helicopter has to take to complete the rescue mission
        :param heli_no_of_ppl: Maximum number of people that the helicopter can carry at once
        :param cond_max_no_of_ppl: Maximum number of people that are involved in any emergency situation,
        this value comes from the conditions file
        :return: returns the number of trips that the helicopter will have to take

        >>> h1 = Helicopter("Kamov KA-52", 10000, 180, 450, 20)
        >>> h1.get_no_of_trips(20, 50)
        3
        '''

        trips = math.ceil(cond_max_no_of_ppl / heli_no_of_ppl)

        return trips

    @staticmethod
    def caluclate_time(heli, condition_obj):
        '''
        Calculates the time taken by the helicopter to complete the trip
        :param heli: Instance of the class helicopter
        :param condition_obj: Condition object from the conditions file
        :return: Returns the time taken by the helicopter using speed and distance

        >>> h1 = Helicopter("Kamov KA-52", 10000, 180, 450, 20)
        >>> c1 = Condition(('1', '1', '1'))
        >>> c1.distance = 300
        >>> c1.number_of_people = 25
        >>> c1.altitude = 15000
        >>> c1.wind_speed = 15
        >>> c1.wind_direction = 'N'
        >>> c1.helicopter_direction = 'S'
        >>> c1.weather = "Summer"
        >>> we1 = h1.get_weather_co_ef("Summer") * h1.max_speed
        >>> nop1 = h1.max_speed * (2 * c1.number_of_people) / 100
        >>> a1 = h1.get_alt_co_ef(c1.altitude) * h1.max_speed
        >>> do1 = h1.get_relation_between_directions(c1.wind_direction,c1.helicopter_direction)
        >>> ws1 = ((do1 * c1.wind_speed / 100) / (h1.empty_weight / 18000)) * 2
        >>> s1 = h1.max_speed - nop1 - a1 - we1 + ws1
        >>> t1 = c1.distance / s1
        >>> tr1 = h1.get_no_of_trips(h1.max_no_people, 25)
        >>> h1.caluclate_time(h1,c1)
        10.256410256410257
        '''

        distance = condition_obj.distance
        max_speed = heli.max_speed
        weather = condition_obj.weather
        cond_max_no_of_ppl = condition_obj.number_of_people
        altitude = condition_obj.altitude
        wind_speed = condition_obj.wind_speed
        wind_direction = condition_obj.wind_direction
        heli_direction = condition_obj.helicopter_direction

        # Calculates how speed of helicopter is affected due to weather
        weather_co_ef = heli.get_weather_co_ef(weather) * heli.max_speed

        # Calculates how speed of helicopter is affected due to number of people in it at the time
        no_of_ppl_co_ef = heli.max_speed * (2 * cond_max_no_of_ppl) / 100

        # Calculates how speed of helicopter is affected by altitude
        alt_co_ef = heli.get_alt_co_ef(altitude) * heli.max_speed

        # Calculates the relationship between direction of wind and direction of helicopter
        direction_offset = heli.get_relation_between_directions(wind_direction, heli_direction)
        # Calculates how these two directions are contributing to the helicopter speed
        wind_speed_co_ef = ((direction_offset * wind_speed / 100) / (heli.empty_weight / 18000)) * 2

        # Calculates the final speed of the helicopter at given conditions
        speed = max_speed - no_of_ppl_co_ef - alt_co_ef - weather_co_ef + wind_speed_co_ef

        # Calculates time taken by the helicopter
        time = distance / speed

        # Calculates the number of trips the helicopter has to take to complete the rescue mission
        trips = heli.get_no_of_trips(heli.max_no_people, cond_max_no_of_ppl)

        if trips == 1:
            return time
        else:
            return trips * time

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
        Generates the individual tendencies of the weather
        :param t: tuple which indicates the weather tendency for Summer, Winter and Rainy

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
        Indicates the actual weather if it is summer, rainy or winter
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
        :param min_altitude: minimum altitude at which the helicopter can fly from the conditions file
        :param max_altitude: maximum altitude at which the helicopter can fly from the conditions file

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

    #Input files: 1. Helicopter and 2. Conditions
    #Loading the input files into DataFrames
    helicopter_df = pd.read_csv("Input_Helicopter_new.csv")
    condition_df = pd.read_csv("Conditions_file.csv")

    #Creating Helicopter objects from Helicopter Dataframe
    for h in range(0,len(helicopter_df)):
        Helicopter(helicopter_df.iloc[h]['Name'], helicopter_df.iloc[h]['Empty_Weight(lbs)'],
                   helicopter_df.iloc[h]['Max_Speed(mph)'],
                   helicopter_df.iloc[h]['Max_Distance(miles)'], helicopter_df.iloc[h]['Max_no_of_people'])

    #Setting the weather Tendency for the simulation to follow
    for c in range(len(condition_df)):
        tendency = tuple(condition_df.iloc[c]['Weather_Tendency'].split('-'))
        Condition(tendency)

    while True:

        no_of_iters = int(input("\nPlease enter the number of simulations to be run: "))

        if no_of_iters <= 0:
            print("You cannot have 0 or negative iterations!!!")
            break

        i = 0
        for conds in Condition.all_conditions:
            for iters in range(no_of_iters):

                #Get a condition object
                conds.get_values_conditions(condition_df.iloc[i]['Distance'], condition_df.iloc[i]['Number_of_People'],
                                            condition_df.iloc[i]['MinAltitude'], condition_df.iloc[i]['MaxAltitude'],
                                            condition_df.iloc[i]['Wind_Speed'])

                #Dictionary to store the time taken at every iteration
                heli_time_dict = {}
                for heli in Helicopter.all_helicopters:
                    time = Helicopter.caluclate_time(heli, conds)
                    heli_time_dict[heli.name] = time

                #Sorting the dictionary to get the winner
                sorted_heli_dict = sorted(heli_time_dict.items(), key=lambda x: x[1])
                winner_heli = sorted_heli_dict[0][0]

                #Increasing the win count for the winner helicopter
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
            print("---------------------------------------------------------")
            print("%25s %10s %15s %%" % ("Name", "Wins", "Win Percentage"))
            print("---------------------------------------------------------")
            for heli in Helicopter.all_helicopters:
                heli.print_values(no_of_iters)

            print("---------------------------------------------------------")

            #Reset all values before starting the next condition
            for heli in Helicopter.all_helicopters:
                heli.reset_values()

            i += 1

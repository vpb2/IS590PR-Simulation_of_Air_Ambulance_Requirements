# Final_Project
# Title: Monte Carlo Simulation of Air Ambulance Requirements

Team Members:
Simran Wig(swig2), Srijith Srinath(ssrina2), Vinu Prasad Bhambore(vpb2)

# Introduction:
An air ambulance is a specially outfitted helicopter or fixed-wing aircraft that transports injured or sick people in a medical emergency or over distances or terrain impractical for a conventional ground ambulance. Helicopters can be used for air transportation during emergency to move patients to healthcare facilities from the scene of an emergency. The objective of the project is to understand how weather conditions affect a helicopter’s performance and recommend the best suited helicopter for a healthcare facility or a given rescue scenario. 

# Scenarios:
Given the weather conditions, the range of the helicopter and the maximum speed the helicopter can traverse at, we are considering the following scenarios:
1. If a buyer(hospital) wants to buy a helicopter, the system can help in recommending the best model of the helicopter to buy given their requirements.
2. In an emergency situation, given a hospital has different types of helicopters, the system will recommend the optimal performing one.

# Hypotheses:
1. Given certain weather conditions, the fastest helicopter will always be the optimal performing one.
2. Higher occupancy helicopters are always better than lower occupancy helicopters.

# Instructions regarding input file:
Our program takes input as a csv file which has 5 columns namely: Name, Empty_Weight(lbs), Max_Speed(mph), Max_Distance(miles), Max_no_of_people
Name: Name and Model of the helicopter
Empty_Weight(lbs): Empty weight of the helicopter
Max_Speed(mph): Maximum speed of the helicopter in miles per hour
Max_Distance(miles): Maximum distance the helicopter can traverse in one fuel of tank
Max_no_of_people: Maximum occupancy of the helicopter

# Results:
1. The first hypotheses was proved wrong according to our simulation that given any weather condition, the fastest helicopter is not the optimal performing helicopter. In different weather conditions, the performance of the helicopter enhances or degrades depending upon the weather condition. In rainy condition, the moisture in the air is the most compared to summer and winter and thus it affects the speed of the helicopter and the fastest helicopter is not always the fastest helicopter.
2. According to our simulation, the second hypotheses proves true in all the given conditions. Higher occupancy helicopters are better than lower occupancy helicopter since, higher occupancy helicopters will have to take comparatively less number of trips to rescue more number of people.


# Limitations and Future Work:
Our system considers only the weather condition, altitude, number of people and x while recommending the optimal performing helicopter.
Certain helicopter parameters like the climb rate or the horse power of the helicopter, is not being taken into consideration while suggesting the optimal performing helicopter.
The system is designed to respond to one emergency situation and does not cater to multiple emergency requests.
The system can be an useful implementation for recommending the air ambulance best suited for a hospital by including more factors which would affect the performance of the helicopter.

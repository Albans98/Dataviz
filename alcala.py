# -*- coding: utf-8 -*-
# -*- Author : Alban STEFF -*-


# -*- Import libraries -*-

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import statistics
import seaborn as sns

# -*- Import files in pandas Dataframe -*-

eec = pd.read_csv("eec.csv")
weather = pd.read_csv("weather.csv")
wifi = pd.read_csv("wifi_visits.csv")

val = eec.groupby(by = 'sensor').sum()
print(val)




# -*- Convert ISO time into datetime -*-

weather['time'] = pd.to_datetime(weather['time'])
weather = weather.sort_values(by='time', ascending = True, ignore_index = True)

wifi['operating_date'] = pd.to_datetime(wifi['operating_date'])
wifi = wifi.sort_values(by='operating_date', ascending = True, ignore_index = True)

eec['local_time'] = pd.to_datetime(eec['local_time'])
eec = eec.sort_values(by='local_time', ascending = True, ignore_index = True)

# -*- Check data -*-

print(weather['time'].head())

print("Data shape EEC : ", eec.shape)
print("Data shape Weather : ", weather.shape)
print("Data shape Wifi : ", wifi.shape)
print("\nEEC informations : \n\n")
print(eec.info())
print("\nWeather informations : \n\n")
print(weather.info())
print("\nWifi informations : \n\n")
print(wifi.info())


# -*- To check data very fast on a plot -*-

wifi.plot()
eec.plot()
plt.show()



# -*- Set plots parameters -*-

plt.style.use('fivethirtyeight')


plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 12
plt.rcParams['lines.linewidth'] = 3




# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* PROBLEM 1 -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*




# -*- Wifi visits -*-

# Daily
plt.figure(1, figsize = (14, 6))
plt.plot(wifi['visits'], linewidth = 1.5, linestyle = ':', marker = 'o', color = '#00e699')
plt.title('Daily Wifi visits (October 2018 - October 2019)')
plt.xlabel('Day number')
plt.ylabel('Visits')
plt.show()

# Weekly
weeks_list = []
for i in range(0, wifi['visits'].size - 1, 7):
  week_sum = 0
  for j in range(i, i + 7):
    week_sum += wifi['visits'][j]
  weeks_list.append(week_sum)

plt.figure(2, figsize = (10, 6))
plt.plot(weeks_list, color = '#00e699')
plt.title('Weekly Wifi visits (October 2018 - October 2019)')
plt.xlabel('Week number')
plt.ylabel('Visits')
plt.show()

# Monthly
i = 0
months_list = []
while i < wifi['operating_date'].size:
  current_month = wifi['operating_date'][i].month
  month = wifi['operating_date'][i + 1].month
  sum_visits = wifi['visits'][i]
  while(month == current_month):
    i += 1
    sum_visits += wifi['visits'][i]
    if(i < wifi['operating_date'].size - 1):
      month = wifi['operating_date'][i + 1].month
    else:
      month = 13
  months_list.append(sum_visits)
  i += 1

plt.figure(3, figsize = (10, 6))
plt.plot(months_list, color = '#00e699')
plt.title('Monthly Wifi visits (October 2018 - October 2019)')
plt.xlabel('Month number')
plt.ylabel('Visits')
plt.show()

# Distribution of visits over the days of the week (Monday to Sunday)
days = {'Monday' : [], 'Tuesday' : [], 'Wednesday' : [], 'Thursday' : [], 'Friday' : [], 'Saturday' : [], 'Sunday' : []}

for i in range(0, wifi['visits'].size - 1, 7):
  days['Monday'].append(wifi['visits'][i])
  days['Tuesday'].append(wifi['visits'][i + 1])
  days['Wednesday'].append(wifi['visits'][i + 2])
  days['Thursday'].append(wifi['visits'][i + 3])
  days['Friday'].append(wifi['visits'][i + 4])
  days['Saturday'].append(wifi['visits'][i + 5])
  days['Sunday'].append(wifi['visits'][i + 6])

# Last item
days['Monday'].append(wifi['visits'][364])

a = 4
for keys, values in days.items():
  plt.figure(a, figsize = (10, 6))
  a += 1
  plt.plot(values, color = '#00e699')
  plt.title(keys + ' Wifi visits (October 2018 - October 2019)')
  plt.xlabel('Week number')
  plt.ylabel('Visits')
  plt.show()

# Mean of wifi visits each day of the week

days_mean = []
for keys in days:
  days_mean.append(statistics.mean(days[keys]))

x = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

plt.figure(11, figsize = (10, 6))
plt.bar(x, days_mean, color = '#00e699')
plt.title('Mean of wifi visits each day (October 2018 - October 2019)')
plt.xlabel('Day of the week')
plt.ylabel('Visits')
plt.show()


# -*- Energy consumption -*-

# Daily energy consumption
i = 0
days_list = []
while i < eec['local_time'].size:
  current_day = eec['local_time'][i].day
  day = eec['local_time'][i + 1].day
  sum_consumption = eec['energy_consumed'][i]
  while(day == current_day):
    i += 1
    sum_consumption += eec['energy_consumed'][i]
    if(i < eec['local_time'].size - 1):
      day = eec['local_time'][i + 1].day
    else:
      day = -1
  days_list.append(sum_consumption)
  i += 1

plt.figure(12, figsize = (14, 6))
plt.plot(days_list, linewidth = 1.5, linestyle = ':', marker = 'o', color = '#00e699')
plt.title('Daily energy consumption (October 2018 - October 2019)')
plt.xlabel('Day number')
plt.ylabel('Energy consumption (mWh)')
plt.show()

#  Distribution of the energy consumption over the days of the week (Monday to Sunday)
days = [0 for i in range(7)]

for i in range(0, eec['local_time'].size):
  if(eec['local_time'][i].weekday() == 0):
    days[0] += eec['energy_consumed'][i]
  if(eec['local_time'][i].weekday() == 1):
    days[1] += eec['energy_consumed'][i]
  if(eec['local_time'][i].weekday() == 2):
    days[2] += eec['energy_consumed'][i]
  if(eec['local_time'][i].weekday() == 3):
    days[3] += eec['energy_consumed'][i]
  if(eec['local_time'][i].weekday() == 4):
    days[4] += eec['energy_consumed'][i]
  if(eec['local_time'][i].weekday() == 5):
    days[5] += eec['energy_consumed'][i]
  if(eec['local_time'][i].weekday() == 6):
    days[6] += eec['energy_consumed'][i]


x = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

plt.figure(13, figsize = (10, 6))
plt.bar(x, days, color = '#00e699')
plt.title('Energy consumed each day (October 2018 - October 2019)')
plt.xlabel('Day of the week')
plt.ylabel('Energy consumed (mWh)')
plt.show()


# Distribution of the energy consumption over the hours of the day (0 to 23)
hours = [0 for i in range(24)]
for i in range(0, eec['local_time'].size):
  hours[eec['local_time'][i].hour] += eec['energy_consumed'][i]


x = [i for i in range(24)]

plt.figure(14, figsize = (10, 6))
plt.bar(x, hours, color = '#00e699')
plt.title('Energy consumed each hour (October 2018 - October 2019)')
plt.xlabel('Hour of the day')
plt.ylabel('Energy consumed (mWh)')
plt.show()


#  Distribution of the energy consumption over the days of the week and hours of the day
days = {'Monday' : [0 for i in range(24)], 'Tuesday' : [0 for i in range(24)], 'Wednesday' : [0 for i in range(24)], 'Thursday' : [0 for i in range(24)], 'Friday' : [0 for i in range(24)], 'Saturday' : [0 for i in range(24)], 'Sunday' : [0 for i in range(24)]}

for i in range(0, eec['local_time'].size):
  if(eec['local_time'][i].weekday() == 0):
    days['Monday'][eec['local_time'][i].hour] += eec['energy_consumed'][i]
  if(eec['local_time'][i].weekday() == 1):
    days['Tuesday'][eec['local_time'][i].hour] += eec['energy_consumed'][i]
  if(eec['local_time'][i].weekday() == 2):
    days['Wednesday'][eec['local_time'][i].hour] += eec['energy_consumed'][i]
  if(eec['local_time'][i].weekday() == 3):
    days['Thursday'][eec['local_time'][i].hour] += eec['energy_consumed'][i]
  if(eec['local_time'][i].weekday() == 4):
    days['Friday'][eec['local_time'][i].hour] += eec['energy_consumed'][i]
  if(eec['local_time'][i].weekday() == 5):
    days['Saturday'][eec['local_time'][i].hour] += eec['energy_consumed'][i]
  if(eec['local_time'][i].weekday() == 6):
    days['Sunday'][eec['local_time'][i].hour] += eec['energy_consumed'][i]


a = 15
x = [i for i in range(24)]
for keys, values in days.items():
  plt.figure(a, figsize = (10, 6))
  a += 1
  plt.bar(x, values, color = '#00e699')
  plt.title(keys + ' energy consumption each hour (October 2018 - October 2019)')
  plt.xlabel('Hours')
  plt.ylabel('Energy consumption (mWh')
  plt.show()



# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* PROBLEM 2 -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*




# Heating/cooling degree days


hdd = {'date' : [], 'degree' : []} # heating degree days values
cdd = {'date' : [], 'degree' : []} # cooling degree days

temp_data = {'date' : [], 'temperature' : []}

i = 0
while i < weather['time'].size - 1:
	current_day = weather['time'][i].day
	temp = weather['temperature'][i]
	count = 1
	if(i < weather['time'].size - 1):
		while(current_day == weather['time'][i + 1].day):
  			if(i < weather['time'].size - 2):
  				i += 1
  			else:
  				current_day = -1
  			count += 1
  			temp += weather['temperature'][i]
		temp /= count
		temp_data['date'].append(weather['time'][i])
		temp_data['temperature'].append(temp)
		if(temp >= 18):
			cdd['degree'].append(max(temp - 18, 0))
			cdd['date'].append(weather['time'][i])
		if(temp < 18):
			hdd['degree'].append(max(18 - temp, 0))
			hdd['date'].append(weather['time'][i])
	i += 1


plt.figure(22, figsize = (10, 6))
plt.plot(hdd['degree'], color = '#00e699')
plt.title('Daily HDD (October 2018 - October 2019)')
plt.xlabel('Days')
plt.ylabel('HDD')
plt.show()

plt.figure(23, figsize = (10, 6))
plt.plot(cdd['degree'], color = '#00e699')
plt.title('Daily CDD (October 2018 - October 2019)')
plt.xlabel('Days')
plt.ylabel('CDD')
plt.show()




# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* PROBLEM 3 -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*


# Seasons temperature variation
plt.figure(24, figsize = (16, 6))
plt.scatter(weather['time'], weather['temperature'], color = '#00e699')
plt.title('Temperature variation each season (October 2018 - October 2019)')
plt.xlabel('Seasons')
plt.ylabel('Temperature')
plt.show()


# Daily energy consumption of HVAC and elevator
def energy_consumption(sensor):
	i = 0
	days_dict = {'date' : [], 'consumption' : []}
	while i < eec['local_time'].size:
		if(eec['sensor'][i] == sensor):
			current_day = eec['local_time'][i].day
			day = eec['local_time'][i + 1].day
			sum_consumption = eec['energy_consumed'][i]
			while(day == current_day):
				i += 1
				if(eec['sensor'][i] == sensor):
		  			sum_consumption += eec['energy_consumed'][i]
				if(i < eec['local_time'].size - 1):
		  			day = eec['local_time'][i + 1].day
				else:
		  			day = -1
			days_dict['date'].append(eec['local_time'][i])
			days_dict['consumption'].append(sum_consumption)
		i += 1
	return days_dict

# HVAC energy consumption and visits
hvac = energy_consumption('hvac-eec-meter')

sum_hvac = 0
for i in range(0, len(hvac['consumption'])):
	sum_hvac += hvac['consumption'][i]
print(sum_hvac)

plt.figure(25, figsize = (10, 6))

# Create the fit line
z = np.polyfit(wifi['visits'], hvac['consumption'], 1) # Fit the polynomial data
p = np.poly1d(z) # Create the right function for the fitted data
plt.plot(wifi['visits'] , p(wifi['visits']),"r")

plt.scatter(wifi['visits'], hvac['consumption'], color = '#00e699')
plt.title('HVAC consumption and visits (October 2018 - October 2019)')
plt.xlabel('Visits')
plt.ylabel('HVAC energy consumption')
plt.show()

# Elevator energy consumption and visits
elevator = energy_consumption('elevator-eec-meter')

sum_elevator = 0
for i in range(0, len(elevator['consumption'])):
	sum_elevator += elevator['consumption'][i]
print(sum_elevator)

plt.figure(26, figsize = (10, 6))
plt.scatter(wifi['visits'], elevator['consumption'], color = '#00e699')
plt.title('Elevator consumption and visits (October 2018 - October 2019)')
plt.xlabel('Visits')
plt.ylabel('Elevator energy consumption')
plt.show()

# HVAC and elevator energy consumption
plt.figure(27, figsize = (10, 6))

# Create the fit line
z = np.polyfit(elevator['consumption'], hvac['consumption'], 1) # Fit the polynomial data
p = np.poly1d(z) # Create the right function for the fitted data
plt.plot(elevator['consumption'] , p(elevator['consumption']),"r-")

plt.scatter(elevator['consumption'], hvac['consumption'], color = '#00e699')
plt.title(' Elevator and HVAC energy consumption (October 2018 - October 2019)')
plt.xlabel('Elevator energy consumption')
plt.ylabel('HVAC energy consumption')
plt.show()


# HVAC consumption and temperature

dico = {'date' : [], 'temperature' : [], 'hvac_consumption' : []}

for i in range(0, len(hvac['date'])):
	for j in range(0, len(temp_data['date'])):
		if(hvac['date'][i].day == temp_data['date'][j].day):
  			if(hvac['date'][i].month == temp_data['date'][j].month):
  				if(hvac['date'][i].year == temp_data['date'][j].year):
  					if(hvac['date'][i].weekday() != 5 and hvac['date'][i].weekday() != 6):
		  				date = str(hvac['date'][i].year) + '-' + str(hvac['date'][i].month) + '-' + str(hvac['date'][i].day)
		  				dico['date'].append(date)
		  				dico['hvac_consumption'].append(hvac['consumption'][i])
		  				dico['temperature'].append(temp_data['temperature'][j])

dataframe = pd.DataFrame(dico)

plt.figure(28, figsize = (12, 7))
days = [i for i in range(261)]
plt.scatter(dataframe['temperature'], dataframe['hvac_consumption'], c = days, cmap = 'plasma')
plt.colorbar(ticks = [50, 100, 150, 200, 250]).set_ticklabels(['Fall', 'Winter', 'Spring', 'Summer', 'Fall'])
plt.title(' Temperature and HVAC energy consumption (October 2018 - October 2019)')
plt.xlabel('Temperature')
plt.ylabel('HVAC energy consumption')
plt.show()

# Energy consumption and HDD/CDD

# HDD

hdd_hvac = {'date' : [], 'hdd' : [], 'hvac_consumption' : [], 'visits' : []}

for i in range(0, len(hvac['date'])):
	for j in range(0, len(hdd['date'])):
		for k in range(0, wifi['visits'].size):
			if(hvac['date'][i].day == hdd['date'][j].day and hvac['date'][i].day == wifi['operating_date'][k].day):
	  			if(hvac['date'][i].month == hdd['date'][j].month and hvac['date'][i].month == wifi['operating_date'][k].month):
	  				if(hvac['date'][i].year == hdd['date'][j].year  and hvac['date'][i].year == wifi['operating_date'][k].year):
	  					if(hvac['date'][i].weekday() != 5 and hvac['date'][i].weekday() != 6):
			  				date = str(hvac['date'][i].year) + '-' + str(hvac['date'][i].month) + '-' + str(hvac['date'][i].day)
			  				hdd_hvac['date'].append(date)
			  				hdd_hvac['hvac_consumption'].append(hvac['consumption'][i])
			  				hdd_hvac['hdd'].append(hdd['degree'][j])
			  				hdd_hvac['visits'].append(wifi['visits'][k])

data = pd.DataFrame(hdd_hvac)

plt.figure(29, figsize = (12, 7))
scatter_hdd = plt.scatter(data['hdd'], data['hvac_consumption'], s = data['visits'], color = '#00e699')
plt.title(' HDD and HVAC energy consumption (October 2018 - October 2019)')
plt.xlabel('HDD')
plt.ylabel('HVAC energy consumption')
handles, labels = scatter_hdd.legend_elements(prop = "sizes", alpha = 0.6, color = '#00e699')
plt.legend(handles, labels, loc = "upper left", title = "Wifi visits")
plt.show()

# CDD

cdd_hvac = {'date' : [], 'cdd' : [], 'hvac_consumption' : [], 'visits' : []}

for i in range(0, len(hvac['date'])):
	for j in range(0, len(cdd['date'])):
		for k in range(0, wifi['visits'].size):
			if(hvac['date'][i].day == cdd['date'][j].day and hvac['date'][i].day == wifi['operating_date'][k].day):
	  			if(hvac['date'][i].month == cdd['date'][j].month and hvac['date'][i].month == wifi['operating_date'][k].month):
	  				if(hvac['date'][i].year == cdd['date'][j].year  and hvac['date'][i].year == wifi['operating_date'][k].year):
	  					if(hvac['date'][i].weekday() != 5 and hvac['date'][i].weekday() != 6):
			  				date = str(hvac['date'][i].year) + '-' + str(hvac['date'][i].month) + '-' + str(hvac['date'][i].day)
			  				cdd_hvac['date'].append(date)
			  				cdd_hvac['hvac_consumption'].append(hvac['consumption'][i])
			  				cdd_hvac['cdd'].append(cdd['degree'][j])
			  				cdd_hvac['visits'].append(wifi['visits'][k])

data2 = pd.DataFrame(cdd_hvac)

plt.figure(30, figsize = (10, 6))
scatter_cdd = plt.scatter(data2['cdd'], data2['hvac_consumption'], s = data2['visits'], color = '#00e699')
plt.title(' CDD and HVAC energy consumption (October 2018 - October 2019)')
plt.xlabel('CDD')
plt.ylabel('HVAC energy consumption')
handles, labels = scatter_cdd.legend_elements(prop = "sizes", alpha = 0.6, color = '#00e699')
plt.legend(handles, labels, loc = "upper left", title = "Wifi visits")
plt.show()




# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* PROBLEM 4 -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*



# Is the data provided sufficient to start optimizing the energy consumption of the HVAC system and thermal comfort ?
# Suggest possible actions to undertake in order to reduce the energy consumption of the HVAC system while 
# maintaining or improving thermal comfort.
#
# Graphs show a strong correlation between degree days and HVAC energy consumption.
# Graphs show a strong correlation between outside temperature and HVAC energy consumption.
# The building must be heated or cooled depending on degree days values.
# By heating or cooling the building appropriately with degree days, we can improve thermal confort and save energy.
# We also have a lot of energy consumption during weekends, while almost nobody is there.
# Restructuring (sliding doors/walls) of the building depending on the season ?

#  What other variables should be measured in order to realize this goal ?
#
# Number of persons inside the building at every moment (use detection sensors)
# Potential computers in use (may be measured with the number of wifi connections) or anything dealing with Joule heating effect
# For thermal confort, the average age of the persons inside may have an impact (Old VS young)






# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* PROBLEM 5 -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*



# To what extent can elevator data alone be used to estimate the number of times people entered the building over a given day ?
#
# By looking at weekend or night values : the elevator, when not in use, consume 200.000 mWh approximately.
# First, we can subtract 200.000 * 24 mW for one day.
#
# https://www.connectionselevator.com/interesting-facts-you-might-not-know-about-elevators/
# "The average user takes 4 trips in an elevator daily."
# Then, we can divide by 4 the energy consumption.
#
# The number we now have can be used as a proportion of people inside the building, to compare with other days.
# If on a monday we get 1.800.000 as final number and on a friday 900.000, we have 2 times more people on monday than friday.
# To have the exact number, we need to know some data :
#								- energy used when the elevator is waiting
#								- energy used when the elevator travels through levels up or down (no weight inside)
#								- energy used to carry one person through levels up or down (elevator weight excluded)




# Is it possible to estimate the number of times people entered the building over a given hour using available data ?
#
# Yes, we need to get the number of visits for the day and the energy consumed for the day.
#
# Energy consumed at a given hour = (energy consumed during this hour / energy consumed for the day) * number of visits for the day

# Let's have an example :

energy_for_one_day = elevator['consumption'][0]
energy_at_this_hour = eec['energy_consumed'][16]
visits_for_one_day = wifi['visits'][0]
persons_inside = int((energy_at_this_hour / energy_for_one_day) * visits_for_one_day)
date = str(eec['local_time'][16].year) + "-" + str(eec['local_time'][16].month) + "-" + str(eec['local_time'][16].day)
print("Persons inside on the : " + date + " at " + str(eec['local_time'][16].hour) + "H : " + str(persons_inside))


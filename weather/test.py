#!/usr/bin/python
##########################
#  channon@hawk.iit.edu  #
##########################

import pywapi

delta = pywapi.get_weather_from_noaa('KORD')['wind_mph']
echo =  pywapi.get_weather_from_noaa('KORD')['temp_c']
print delta
print echo

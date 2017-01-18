# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 17:51:10 2016

@author: vismay
"""
import rebound
from astropy.time import Time
'''
This is a initialized sim with the planets and Sun in their positions at the 
launch time of Voyager 1, as taken from the JPL Horizons Database.
'''

def Tconvert(time):
    t = Time(time, format='jd', scale='tt', out_subfmt='date_hm')
    return t.iso

def init(time, name):
    start_date = Tconvert(time)  # put in in the form required by Horizons ephemeris
    sim = rebound.Simulation()
    sim.units = ('yr2pi', 'AU', 'Msun')
    sim.add("Sun", date=start_date)
    sim.add("Mercury", date=start_date)
    sim.add("Venus",date=start_date)
    sim.add("399", date=start_date)
    sim.add("Mars", date=start_date)
    sim.add("Jupiter", date=start_date)
    sim.add("Saturn", date=start_date)
    sim.add("Uranus", date=start_date)
    sim.add("Neptune", date=start_date)
    sim.add("Pluto", date=start_date)
    sim.add("-31", date=start_date, m=3.629e-28) # this is Voyager 1, mass ref: http://nssdc.gsfc.nasa.gov/planetary/voyager.html
    sim.save("start{}.bin".format(name))
    
    

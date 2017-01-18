"""
Created on Mon Jan 16 17:45:17 2017

@author: vismay
"""
import rebound 
import numpy as np
from matplotlib import pyplot as plt
import initialize


def get_day(jd, base_date):
    ''' get_day(float, float) --> float
    
    Tells you how many days from the start of the simulation a particular time is.
    Inputs are in Julian days, output is days from start of simulation.
    '''
    return jd - base_date
 
data_file = 'total_data.txt'
time_data = np.loadtxt(data_file, dtype='float', delimiter = ',', unpack=True, usecols=[0])
voy_final = np.loadtxt(data_file, dtype='float', delimiter = ',', skiprows=len(time_data)-1, unpack=True, usecols=[2,3,4])
times = np.arange(0., len(time_data)-1, 1.)
####---------------------------------------------------------------------------                                 
##   If running for the first time, setup the simulation, else comment this out
####---------------------------------------------------------------------------

# This creates a new simulation binary file called 'start___.bin' where ___ is the string argument to the init call.
# The simulation takes in data from HORIZONS ephemris at the time passed in as the first argument to the init call.
# The simulation is set to start at time t=0 and consists of a particle array, which has the following indices 
# 0=Sun, 1=Mercury, 2=Venus, 3=Earth, 4=Mars, 5=Jupiter, 6=Saturn, 7=Uranus, 8=Neptune, 9=Pluto, 10=Voyager 1 Sim

#print "Setting up simulation"
#initialize.init(float(time_data[0]), 'new')  

####---------------------------------------------------------------------------

# Now load the initial state of the simulation
sim = rebound.Simulation.from_file("startnew.bin")
# Ensure sim parameters are what we want, set up particle array
sim.integrator = "ias15" # IAS15 is the default integrator, so we actually don't need this line
sim.move_to_com()        # We always move to the center of momentum frame before an integration
ps = sim.particles       # ps is now an array of pointers and will change as the simulation runs
sim.t = 0 

# Now add kicks as needed; form is ([x-kick, y-kick, z-kick]), units of au/(year*2pi)
kicks = [] 
kicks.append([5.84564348e-04,-1.76732930e-05, -2.27558408e-04]) # @ before Jupiter
kicks.append([ 0.0006733192550000267, -2.7904549999985262e-05, -0.0020817132012]) # to get simulated probe to match Voyager 1 @ Jupiter
kicks.append([-4.39985253, 2.98410966, 0.09549758]) # @ before Saturn
kicks.append([4.479490862093, 3.169782377682, -0.2318683151419]) # to get simulated probe to match Voyager 1 @ Saturn
kicks.append([0.292789,  -0.1093,  0.4]) # kick needed @ some point after saturn

# Add in the times at which the kicks should take place, in Julian days
kick_t = []
kick_t.append(get_day(2443397.5973599595, time_data[0])) # @ before Jupiter
kick_t.append(get_day(2443930.5720933327, time_data[0])) # @ Jupiter
kick_t.append(get_day(2443937.4743615612, time_data[0])) # @ before Saturn
kick_t.append(get_day(2444009.8291733307, time_data[0])) # @ Saturn
kick_t.append(get_day(2444018.6247764258, time_data[0])) # Post Saturn

def integrate(time_array, kick_times, kick_array):
    '''integrate(numpy array, numpy array, numpy array) --> sim.status, numpy array
    
    This function integrates the simiulation to the last time value provided in time_array.
    At each step, it checks to see whether it is at (or has exceeded) the time of the 
    velocity change. If so, it adds a velocity specified in kick_array to the probe
    (ps[10]). It then removes that time and the velocity from the respective arrays.
    '''
    k_out = []
    step = 0 # this will be incremented everytime a velocity change occurs
    progress = 0 # this exists just to give a sense of progress
    for time in time_array:
        if (len(kick_times) == 0):
            sim.integrate(time)
            progress += 1
            if progress % 1000 == 0:
                print "Now on day {}".format(progress)
        elif time < kick_times[0]:
            sim.integrate(time)
        else:
            print 'step = {}'.format(step)
            step += 1 
            ax, ay, az = ps[10].vx, ps[10].vy, ps[10].vz
            sim.integrate(time)
            ps[10].vx += kick_array[0][0]
            ps[10].vy += kick_array[0][1]
            ps[10].vz += kick_array[0][2]
            ax = ps[10].vx - ax
            ay = ps[10].vy - ay
            az = ps[10].vz - az
            k_out.append([kick_times[0], [ax, ay, az]])  
            # instead of removing the elements, just redefine the arrays to avoid index out of range errors
            kick_times = kick_times[1:]
            kick_array = kick_array[1:]
    # distance at end of sim needs to be implemented 
    #dist = np.sqrt((ps[10].x-voy_final[0])**2 + (ps[10].y-voy_final[1])**2 + (ps[10].z-voy_final[2])**2)# * 1.496e+8 to make it in km
    return sim.status(), k_out#, dist
    
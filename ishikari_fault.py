# READ IN FAULT
# This file is mostly used for testing instead of running everything in maketopo.py
# It reads in a fault geometry and subfaults and there is an option for a "mini test" where
# you output moment and magnitdue, and the dtopography event is also tested

from clawpack.geoclaw import dtopotools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from copy import copy
from clawpack.visclaw import animation_tools
import os
from IPython.display import HTML


# set up environment variables
# os.environ['CLAW'] = '/Users/emiddleton/Documents/python/clawpack/clawpack_src/clawpack'
# os.environ['FC'] = 'gfortran'

try:
    CLAW = os.environ['CLAW']
except:
    raise Exception("*** Must first set CLAW enviornment variable")


# file directory
dir = os.path.join(CLAW, 'geoclaw/examples/hokkaido/')

# Files in directory read in
# Fault geometry is a 2D array with columns as described below
# fault No., centroid(lon,lat,z[km]), node1(lon,lat,z[km]), node2(lon,lat,z[km]), 
# node3(lon,lat,z[km]) , mean vertex length(km) , area(km^2) , strike(deg) , dip(deg)
#fault_geometry_file = os.path.join(dir + 'ishikari_fault.csv') 
fault_geometry_file = os.path.join(dir + 'tok_coords.csv')
#rupture_file = os.path.join(dir + 'ishikari_rupture.csv') #rupture information, currently only strike slip and dip slip for each subfault
rupture_file = os.path.join(dir + 'rupt_param.csv')

# ishikari = np.loadtxt(fault_geometry_file, delimiter=",", skiprows=1) #path, comma separated values, first row is a header
# ishikari[:,[3,6,9,12]] = 1e3*abs(ishikari[:,[3,6,9,12]]) #array slicing accesses depth element, changing it to be positive meters instead of negative km
# rupture_parameters = np.loadtxt(rupture_file, delimiter=",")

# fault0 = dtopotools.Fault() #create object
# fault0.subfaults = [] #initialize empty list

# nsubfaults = ishikari.shape[0]

# # read in the data for each subfault
# for j in range(nsubfaults):
#     subfault0 = dtopotools.SubFault() #create new object
#     node1 = ishikari[j,4:7].tolist() #lon,lat,depth of the first node in each triangle
#     node2 = ishikari[j,7:10].tolist()
#     node3 = ishikari[j,10:13].tolist()
#     node_list = [node1,node2,node3]
#     subfault0.slip = rupture_parameters[j,1] #all dip slip
#     subfault0.rake = 90 #all the same
#     subfault0.set_corners(node_list,projection_zone='10')
#     fault0.subfaults.append(subfault0)

ishikari = np.loadtxt(fault_geometry_file, delimiter=",", skiprows=1) #path, comma separated values, first row is a header
# ishikari[:,[3,6,9,12]] = 1e3*abs(ishikari[:,[3,6,9,12]]) #array slicing accesses depth element, changing it to be positive meters
ishikari[:,[2,5,8]] = 1e3*abs(ishikari[:,[2,5,8]]) #array slicing accesses depth element, changing it to be positive meters

fault0 = dtopotools.Fault() #create object
fault0.subfaults = [] #initialize empty list

nsubfaults = ishikari.shape[0]

for j in range(nsubfaults):
    subfault0 = dtopotools.SubFault() #create new object
    node1 = ishikari[j,0:3].tolist() #lon,lat,depth of the first node in each triangle
    node2 = ishikari[j,3:6].tolist()
    node3 = ishikari[j,6:9].tolist()
    node_list = [node1,node2,node3]
    subfault0.set_corners(node_list,projection_zone='10')
    fault0.subfaults.append(subfault0)

# # mini test to see if the fault has been read in correctly
# print("The seismic moment is %g N-m" % fault0.Mo())
# print("The Moment magnitude is %g" % fault0.Mw())
# print("  (Assuming the rigidity mu of all subfaults is the default value %g Pa)"\
#       % fault0.subfaults[0].mu)

#Dtopography testing

xlower = 141
xupper = 145
ylower = 41
yupper = 42.5

# dtopo parameters:
points_per_degree = 60  # 1 minute resolution
dx = 1./points_per_degree
mx = int((xupper - xlower)/dx + 1)
xupper = xlower + (mx-1)*dx
my = int((yupper - ylower)/dx + 1)
yupper = ylower + (my-1)*dx

x = np.linspace(xlower,xupper,mx)
y = np.linspace(ylower,yupper,my)

dtopo = fault0.create_dtopography(x,y,times=[1.], verbose=False)
dtopo_fname = ('/Users/anitamiddleton/Documents/python/clawpack/clawpack_src/clawpack/geoclaw/examples/hokkaido/ishikari.tt3')
dtopo.write(dtopo_fname, dtopo_type=3)

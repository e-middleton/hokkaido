#This file reads in the fault geometry file given and outputs a 3D perspective as well as top down plane image
#It doesn't do anything special, it just makes sure that everything is read in as expected and the fault
#doesn't appear to have errors

from clawpack.geoclaw import dtopotools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from copy import copy
from clawpack.visclaw import animation_tools
import os
from IPython.display import HTML

os.environ['CLAW'] = '/Users/anitamiddleton/Documents/python/clawpack/clawpack_src/clawpack'
os.environ['FC'] = 'gfortran'

try:
    CLAW = os.environ['CLAW']
except:
    raise Exception("*** Must first set CLAW enviornment variable")

#file directory
dir = os.path.join(CLAW, 'geoclaw/examples/hokkaido/')

fault_geometry_file = os.path.join(dir + 'ishikari_fault.csv')
ishikari = np.loadtxt(fault_geometry_file, delimiter=",", skiprows=1) #path, comma separated values, first row is a header
ishikari[:,[3,6,9,12]] = 1e3*abs(ishikari[:,[3,6,9,12]]) #array slicing accesses depth element, changing it to be positive meters

fault0 = dtopotools.Fault() #create object
fault0.subfaults = [] #initialize empty list

nsubfaults = ishikari.shape[0]

for j in range(nsubfaults):
	subfault0 = dtopotools.SubFault() #create new object
	node1 = ishikari[j,4:7].tolist() #lon,lat,depth of the first node in each triangle
	node2 = ishikari[j,7:10].tolist()
	node3 = ishikari[j,10:13].tolist()
	node_list = [node1,node2,node3]
	subfault0.set_corners(node_list,projection_zone='10')
	fault0.subfaults.append(subfault0)

#copied from CSZ_example.ipynb
fig = plt.figure(figsize=(15,10))
#ax = fig.add_subplot(121, projection='3d')
ax = fig.add_axes([.05,.05,.65,.9], projection='3d')
for s in fault0.subfaults:
    c = s.corners #list of 3 nodes
    c.append(c[0]) #does this close a loop or something?
    c = np.array(c)
    ax.plot(c[:,0],c[:,1],-c[:,2]/1000.,color='b') #depth is negative and km (m/1000)
ax.view_init(10,60)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Depth (km)')
ax.set_title('Triangular subfaults')

#ax = fig.add_subplot(122)
ax = fig.add_axes([.75,.05,.2,.9])
for s in fault0.subfaults:
    c = s.corners
    c.append(c[0])
    c = np.array(c)
    ax.plot(c[:,0],c[:,1], 'b')
ax.set_aspect(1./np.cos(45*np.pi/180.))
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Plan view')
plt.show()

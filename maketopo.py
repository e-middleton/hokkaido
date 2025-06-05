"""
Create topo and dtopo files needed for this project:
    modified from the maketopo file for the chile2010 example
    etopo10min120W60W60S0S.asc        download from GeoClaw topo repository
    dtopo_usgs100227.tt3              create using Okada model 
Prior to Clawpack 5.2.1, the fault parameters we specified in a .cfg file,
but now they are explicit below.
    
Call functions with makeplots==True to create plots of topo, slip, and dtopo.
"""

from __future__ import absolute_import
from __future__ import print_function
import os
import numpy as np

import clawpack.clawutil.data

# set up environment variables
os.environ['CLAW'] = '/Users/anitamiddleton/Documents/python/clawpack/clawpack_src/clawpack'
os.environ['FC'] = 'gfortran'

try:
    CLAW = os.environ['CLAW']
except:
    raise Exception("*** Must first set CLAW enviornment variable")

# Scratch directory for storing topo and dtopo files:
dir = os.path.join(CLAW, 'geoclaw/examples/hokkaido')

def get_topo(makeplots=True):
    """
    Retrieve the topo file from the GeoClaw repository.
    """
    from clawpack.geoclaw import topotools

    # topography file
    topo_fname = 'gebco_2024_n47.0_s34.5_w135.0_e152.0.asc'
    # put the header in the correct formatting and write the file for topotype3
    topotools.swapheader(topo_fname, 'hokkaido.tt3') 
    topo_fname = 'hokkaido.tt3'

    topo_path = os.path.join(dir, topo_fname)
    topo = topotools.Topography(topo_path, topo_type=3)
    print("The extent of the data in longitude and latitude: ")
    print(topo.extent)

    if makeplots:
        from matplotlib import pyplot as plt
        topo.plot()
        fname = 'hokkaido.png'
        plt.savefig(fname)
        print("Created ",fname)


    
def make_dtopo(makeplots=True):
    """
    Create dtopo data file for deformation of sea floor due to earthquake.
    Uses the Okada model with fault parameters and mesh specified below.
    """
    from clawpack.geoclaw import dtopotools
    import numpy

    dtopo_fname = os.path.join(dir, "ishikari.tt3")

    # Specify subfault parameters 

    #Files in directory read in
    fault_geometry_file = os.path.join(dir, 'ishikari_fault.csv')
    rupture_file = os.path.join(dir, 'ishikari_rupture2.csv')

    ishikari = np.loadtxt(fault_geometry_file, delimiter=",", skiprows=1) #path, comma separated values, first row is a header
    ishikari[:,[3,6,9,12]] = 1e3*abs(ishikari[:,[3,6,9,12]]) #array slicing accesses depth element, changing it to be positive meters
    rupture_parameters = np.loadtxt(rupture_file, delimiter=",")

    fault0 = dtopotools.Fault() #create object
    fault0.subfaults = [] #initialize empty list

    nsubfaults = ishikari.shape[0]

    for j in range(nsubfaults):
        subfault0 = dtopotools.SubFault() #create new object
        node1 = ishikari[j,4:7].tolist() #lon,lat,depth of the first node in each triangle
        node2 = ishikari[j,7:10].tolist()
        node3 = ishikari[j,10:13].tolist()
        node_list = [node1,node2,node3]
        subfault0.slip = rupture_parameters[j,1] #all dip slip
        subfault0.rake = 90 #all the same
        subfault0.set_corners(node_list,projection_zone='10')
        fault0.subfaults.append(subfault0)


    if os.path.exists(dtopo_fname):
        print("*** Not regenerating dtopo file (already exists): %s" \
                    % dtopo_fname)
    else:
        print("Using Okada model to create dtopo file")
        
        # specify extent of seafloor deformation (?)
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
        dtopo.write(dtopo_fname, dtopo_type=3)
        
    if makeplots:
        from matplotlib import pyplot as plt
        if fault0.dtopo is None:
            # read in the pre-existing file:
            print("Reading in dtopo file...")
            dtopo = dtopotools.DTopography()
            dtopo.read(dtopo_fname, dtopo_type=3)
            x = dtopo.x
            y = dtopo.y
        plt.figure(figsize=(12,7))
        ax1 = plt.subplot(121)
        ax2 = plt.subplot(122)
        fault0.plot_subfaults(axes=ax1,slip_color=True)
        ax1.set_xlim(x.min(),x.max())
        ax1.set_ylim(y.min(),y.max())
        dtopo.plot_dZ_colors(1.,axes=ax2)
        fname = os.path.splitext(os.path.split(dtopo_fname)[-1])[0] + '.png'
        plt.savefig(fname)
        print("Created ",fname)


if __name__=='__main__':
    get_topo(False)
    make_dtopo(False)

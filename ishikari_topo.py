from __future__ import print_function
from clawpack.geoclaw import topotools
import matplotlib.pyplot as plt
import os
CLAW = os.environ['CLAW']

dir = os.path.join(CLAW, 'geoclaw/examples/hokkaido')
topo_path = os.path.join(dir, 'tok_topo.tt3')
topo = topotools.Topography()
topo.read(topo_path, topo_type=3)

print("The extent of the data in longitude and latitude: ")
print(topo.extent)

print("topo.delta = ",topo.delta)
print("15 arcseconds is 1/240  degree = %8.6f degree" % (1./240.))

topo2 = topo.crop(filter_region=None, coarsen=16)
topo2_path = os.path.join(dir, 'tok_topo_coarse.tt3')
topo2.write(topo2_path, topo_type=3)

print("The original grid was of shape %s, topo2 has shape %s" % (topo.Z.shape,topo2.Z.shape))
print("topo2.delta = ",topo2.delta)
print("4 arc minutes is 1/15 degree = %8.6f degree" % (1./15.))

# filter_region = (141, 146, 41, 44)
# topo3 = topo.crop(filter_region)
# topo3.Z.shape
# topo3_path = ('/Users/anitamiddleton/Documents/python/clawpack/clawpack_src/clawpack/geoclaw/examples/hokkaido/hokkaido_cropped.tt3')
# topo3.write(topo3_path, topo_type=3)

figure = plt.figure(figsize=(12,6))
ax1 = figure.add_subplot(121)
topo.plot(axes=ax1)
ax1.set_title('Original')
ax2 = figure.add_subplot(122)
topo2.plot(axes=ax2)
ax2.set_title('Coarse')
plt.show()

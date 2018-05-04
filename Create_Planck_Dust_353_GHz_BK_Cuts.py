import numpy as np
import healpy as hp
import pysm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pickle as pk
from optparse import OptionParser
from Map_Cutter import MapCutter

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", default = 'Planck_dust_cuts_353GHz.pk',
                  help="output file")

parser.add_option("-d", "--dust_map_loc",
                   dest="dust_loc", default='/global/homes/k/kmaylor/cori/Planck_Foreground_maps/COM_CompMap_Dust-GNILC-F353_2048_R2.00.fits',
                  help="path to dust map")


options,args = parser.parse_args()

MP = MapCutter(options.dust_loc)
MP.convert_map_units(353)

delta_lon = 40.
delta_lat = 30.
step = 10.
map_cuts = []

for i,lon in enumerate(np.arange(-180,180+step-delta_lon,step)):
    for j,lat in enumerate(np.arange(-90,90+step-delta_lat,step)):
        map_cuts.append(MP.cut_map([lon,lon+delta_lon],[lat,lat+delta_lat],2./60))
    pk.dump(map_cuts,open(options.filename,'a+'), protocol = -1)
    map_cuts = []
    print('Batch %d out of %s completed' %(i+1,(360.+step-delta_lon)/step))

import numpy as np
import healpy as hp
import pysm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pickle as pk
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", default = 'Planck_dust_cuts_353GHz.pk',
                  help="output file")

parser.add_option("-d", "--dust_map_loc",
                   dest="dust_loc", default='/global/homes/k/kmaylor/cori/Planck_Foreground_maps/COM_CompMap_Dust-GNILC-F353_2048_R2.00.fits',
                  help="path to dust map")


options,args = parser.parse_args()

sf=pysm.common.convert_units("MJysr","uK_CMB",353)

dust_map=hp.read_map(options.dust_loc)*sf
npix = dust_map.shape[-1]
nside = hp.npix2nside(npix)
dust_val = lambda theta,phi: dust_map[hp.ang2pix(nside,theta,phi,lonlat=True)]

delta_lon = 40
delta_lat = 30
step = 10
map_cuts = []

for i,lon in enumerate(np.arange(-180,180+step-delta_lon,step)):
    for j,lat in enumerate(np.arange(-90,90+step-delta_lat,step)):
        theta = np.arange(lon,lon+delta_lon,2./60)
        phi = np.arange(lat,lat+delta_lat,2./60)
        Theta,Phi = np.meshgrid(theta,phi)
        map_cuts.append(dust_val(Theta.ravel(),Phi.ravel()).reshape((len(phi),len(theta))))
    pk.dump(map_cuts,open(options.filename,'a+'), protocol = -1)
    map_cuts = []
    print('Batch %d out of %s completed' %(i+1,(360+step-delta_lon)/10.))

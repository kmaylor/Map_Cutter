import numpy as np
import healpy as hp
import pysm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pickle as pk
from optparse import OptionParser
from Map_Cutter import MapCutter
import h5py

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", default = 'Planck_dust_cuts_353GHz.pk',
                  help="output file")

parser.add_option("-d", "--dust_map_loc",
                   dest="dust_loc", default='COM_CompMap_Dust-GNILC-F353_2048_R2.00.fits',
                  help="path to dust map")


options,args = parser.parse_args()

MP = MapCutter(options.dust_loc)
sf=pysm.common.convert_units("MJysr","uK_CMB",353)


delta_theta = 20./180*np.pi
step = 5./180*np.pi
galactic_cut = [80./180*np.pi,110./180*np.pi]
map_cuts = []

def phi_f(phi_0,theta_ra,f):
    """
    Find the phi_1 that give f percent of the sky for given theta_0,1 and phi_0.
    """
    return phi_0 - 4*np.pi*f/(-np.cos(theta_ra[0])+np.cos(theta_ra[1]))

for i,phi_0 in enumerate(np.arange(0,2*np.pi,step)):
#for i,phi_0 in enumerate(np.arange(0,20./180*np.pi,step)):
    for j,theta_0 in enumerate(np.arange(0,np.pi+step-delta_theta,step)):
        theta_1 = theta_0+delta_theta
        if (theta_0>=galactic_cut[0] and theta_0<=galactic_cut[0]) or (theta_1>=galactic_cut[0] and theta_1<=galactic_cut[0]): 
            pass
        else:
            phi_1=phi_f(phi_0,[theta_0,theta_1],0.01)
            map_cuts.append(MP.cut_map([phi_0,phi_1],[theta_0,theta_1],900)*sf)
    with h5py.File('Planck_dust_cuts_353GHz.h5', 'a') as hf:
        hf.create_dataset(str(i), data=map_cuts)
    #pk.dump(map_cuts,open(options.filename,'ab'), protocol = -1)
    map_cuts = []
    print('Batch %d out of %s completed' %(i+1,(2*np.pi)/step))

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


step = 5
galactic_cut = 20
map_cuts = []
log_means = []
log_vars = []
count=0
lat_range = list(range(-90,-galactic_cut,step))+list(range(galactic_cut+step,90,step))
for j,theta in enumerate(lat_range):
    lon_range = np.arange(0,360,step/np.cos(theta/180*np.pi))
    for i,phi in enumerate(lon_range):
        map_cut = MP.cut_map([phi,theta])*sf
        map_cuts.append(map_cut)
        with h5py.File('Planck_dust_cuts_353GHz.h5', 'a') as hf:
            hf.create_dataset(str(count), data=map_cut)
        count+=1
    log_means.append(np.mean(np.log(map_cuts)))
    log_vars.append(np.var(np.log(map_cuts)))
    map_cuts = []
    print('Batch %d out of %s completed' %(j+1,len(lat_range)))
log_mean = np.mean(log_means)
log_var = np.mean(log_vars)

print('Create norm-log maps')
with h5py.File('Planck_dust_cuts_353GHz.h5', 'r') as hfr:
    with h5py.File('Planck_dust_cuts_353GHz_norm_log.h5', 'w') as hfw:
        for i in np.arange(len(hfr.keys())):
            log_maps=np.log(np.array(hfr.get(str(i))))
            hfw.create_dataset(str(i),data=(log_maps-log_mean)/np.sqrt(log_var))
            
    
#for i,phi_0 in enumerate(np.arange(0,2*np.pi,step)):
#for i,phi_0 in enumerate(np.arange(0,20./180*np.pi,step)):
#    for j,theta_0 in enumerate(np.arange(10/180*np.pi,np.pi+step-delta_theta-10/180*np.pi,step)):
#        theta_1 = theta_0+delta_theta
#        if (theta_0>=galactic_cut[0] and theta_0<=galactic_cut[0]) or (theta_1>=galactic_cut[0] and theta_1<=galactic_cut[0]): 
#            pass
#        else:
#            phi_1=phi_f(phi_0,[theta_0,theta_1],0.01)
#            map_cut = MP.cut_map([phi_0,phi_1],[theta_0,theta_1],900)*sf
#            map_cuts.append(map_cut)
#    log_mean += np.mean(np.log(map_cuts))*step/(2*np.pi)
#    log_var += np.var(np.log(map_cuts))*step/(2*np.pi)
#    with h5py.File('Planck_dust_cuts_353GHz.h5', 'a') as hf:
#        hf.create_dataset(str(i), data=map_cuts)
#    #pk.dump(map_cuts,open(options.filename,'ab'), protocol = -1)
#    map_cuts = []
#    print('Batch %d out of %s completed' %(i+1,(2*np.pi)/step))
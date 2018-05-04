import numpy as np

import healpy as hp
import pysm
from pysm.nominal import models
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 

import pickle as pk
from Map_cutter import MapCutter

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", default = 'training_maps_dust_cmb_nu_30_270_d5c1.pk',
                  help="write report to FILE", metavar="FILE")
parser.add_option("-t", "--maptype",
                   dest="map_type", default=['T','Q','U'],
                  help="choose if you want T Q and or U")
parser.add_option("-n", "--nu",
                   dest="nu", default=[30,40,85,95,150,220,270],
                  help="frequencies to simulate")
parser.add_option("-s", "--seeds",
                   dest="seeds", default=1000,
                  help="number of maps to generate")
parser.add_option("-d", "--nside",
                   dest="nside", default=512,
                  help="healpix map resolution")
parser.add_option("-o", "--longitude",
                   dest="longitude", default=[-55,55],
                  help="longitude of cut")
parser.add_option("-a", "--latitude",
                   dest="latitude", default=[-70,-30],
                  help="latitude of cut")
parser.add_option("-r", "--save_rate",
                   dest="save_rate", default=10,
                  help="save after this number of realizations generated")

args,_ = parser.parse_args()
map_type = args.map_type
nu = args.nu
nside= args.nside
seeds = int(args.seeds)
save_rate = int(args.save_rate)
lonra=args.longitude
latra=args.latitude

def map_dic():
    return {'cmb':[],'dust':[],'total':[]}


maps = dict(zip(map_type,[map_dic() for i in map_type]))
sf=pysm.common.convert_units("uK_RJ","uK_CMB",nu)


for s,seed in enumerate(np.random.randint(0,10000,seeds)):
    c_config = models('c1', nside)
    c_config[0]['cmb_seed']=seed
    d_config = models("d5", nside)
    d_config[0]['draw_uval_seed']=seed
    sky_config = {'dust':d_config,'cmb':c_config}
    sky = pysm.Sky(sky_config)
    cmb_all_nu = sky.cmb(nu)
    dust_all_nu = sky.dust(nu)

    
    for x,m in enumerate(map_type):
        cmb_cube = []
        dust_cube = []
        total_cube = []
        for i,n in enumerate(nu):
            cmb = MapCutter(cmb_all_nu[i,x,:]).cut_map(lonra,latra,2./60)*sf[i]
            cmb_cube.append(cmb)
            dust = MapCutter(dust_all_nu[i,x,:]).cut_map(lonra,latra,2./60)*sf[i]
            dust_cube.append(dust)
            total_cube.append(cmb+dust)
        maps[m]['cmb'].append(np.array(cmb_cube))
        maps[m]['dust'].append(np.array(dust_cube))
        maps[m]['total'].append(np.array(total_cube))

    if s%save_rate == 0:
        pk.dump(maps,open(args.filename,'a+'))
        maps = dict(zip(map_type,[map_dic() for i in map_type]))
        print('%d out of %s completed' %(s+1,seeds))
        
    
           
        

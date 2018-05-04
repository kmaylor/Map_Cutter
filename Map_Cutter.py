from numpy import 
from hp import ang2pix, read_map, npix2nside
from pysm.common import convert_units

import pickle as pk

class MapCutter(object):
    """
    Map Cutter object: instantiate with a path to a map and use methods to convert units and produce cuts from desired map regions.
    """
    __init__(self,map_path):
        self.map = read_map(map_path)
        self.npix = self.map.shape[-1]
        self.nside = npix2nside(self.npix)
        
    def map_val(self,theta,phi):
        """
        Returns the value of the map at a given theta and phi in degrees.
        """
        return self.map[ang2pix(self.nside,theta,phi,lonlat=True)]
    
    def convert_map_units(freq, units = ["MJysr","uk_CMB"])
        """
        Converts the map from units[0] to ujits[1] at the given frequency
        """
        self.map*=convert_units(*units,freq)
        
    def cut_map(self, lonra, latra, res, out_put_file = None):
        """
        Returns map cut from desired region from the given longitudinal and latitudinal ranges (assuming small engough for flat sky limit)"
        """

        self.thetas = np.arange(lonra[0],lonra[1],res)
        self.phis = np.arange(latra[0],latra[1],res)
        Theta,Phi = np.meshgrid(self.theta,self.phi)
        map_cut = map_val(Theta.ravel(),Phi.ravel()).reshape((len(self.phis),len(self.thetas)))
        return map_cut
    
        if out_put_file != None:
            pk.dump(map_cut,open(out_put_file,'wb'), protocol = -1)
    

from healpy import get_interp_val, read_map, npix2nside
from pickle import dump
from numpy import arange, meshgrid
from pysm.common import convert_units

class MapCutter(object):
    """
    Map Cutter object: instantiate with a healpix map and use methods to convert units and produce cuts from desired map regions.
    """
    def __init__(self, map_to_cut):
        if isinstance(map_to_cut,str):
            self.map = read_map(map_to_cut)
        else:
            self.map = map_to_cut
        self.npix = self.map.shape[-1]
        self.nside = npix2nside(self.npix)
        
    def map_val(self, theta, phi):
        """
        Returns the value of the map at a given theta and phi in degrees.
        """
        return get_interp_val(self.map,theta,phi,lonlat=True)]
        
    def cut_map(self, lonra, latra, res, out_put_file = None):
        """
        Returns map cut from desired region from the given longitudinal and latitudinal ranges (assuming small engough for flat sky limit)"
        """

        self.thetas = arange(lonra[0],lonra[1],res)
        self.phis = arange(latra[0],latra[1],res)
        Theta,Phi = meshgrid(self.thetas,self.phis)
        map_cut = self.map_val(Theta.ravel(),Phi.ravel()).reshape((len(self.phis),len(self.thetas)))
        return map_cut
    
        if out_put_file != None:
            dump(map_cut,open(out_put_file,'wb'), protocol = -1)
    

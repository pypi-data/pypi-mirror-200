import sys, os

a_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,a_path + "/thinmam")

def state(solname,opt='all'):
    mod = __import__(solname)
    clas = getattr(mod,'solid')
    return clas(opt)

class solidframe(object):
        
    def rhomass(self):
        return self._rhomass
    def cpmass(self):
        return self._cpmass
    def conductivity(self):
        return self._conductivity
    def youngs_modulus(self):
        return self._youngs_modulus
    def poissons_ratio(self):
        return self._poissons_ratio

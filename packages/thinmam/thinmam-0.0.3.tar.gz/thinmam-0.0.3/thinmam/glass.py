from solidframe import solidframe

class solid(solidframe):
    def __init__(self,opt='all'): #properties are classified as thermophysical and mechanical properties. Depending on the component where it is assigned, the corresponding properties are alone loaded into the object.
        self.opt = opt
        if opt == 'ther' or opt == 'all':
            self._rhomass = 2500. 
            self._cpmass = 0. #800. #for faster SS convergence pending
            self._conductivity = 10. #1. increased to 10. to increase SS attainment speed pending
        if opt == 'mech' or opt == 'all':
            pass
            # self._youngs_modulus=1.E11
            # self._poissons_ratio=0.26
        
# -*- encoding: utf-8 -*-
#import sys
#sys.path.append('./modulos')
#from modulos.Ifta_Wyrowski import IftaWyrowski

from modulos.principal import funcionprincipal

#x = iftaWyrowski()
#x.iniciaralgooritmo()
ALLOWED_EXTENSIONS = set(['pgm', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


obj = {}
obj['ruta'] = "C:\\Users\\Lenovo\\Documents\\Tesis\\www\\Software\\holoeasy\\images\\3.jpg"
obj['tailleimg'] = 322
obj['pixelmargin'] = 4
obj['tipoimg']='file'
obj['phase'] = 'phaheur'
obj['phaseinitial'] = 'bandelimitee'
obj['iterODD'] = 200
obj['code'] = 'codedur'
obj['MASIRdes'] = 0.8
obj['control_banda'] = 0.01
obj['controlbande'] = 0.01
obj['diffphase'] = 1.335
obj['tipoilum'] = 'carre'
obj['nivel'] = 4
obj['PRs'] = 1
obj['PRb'] = 0
obj['DPRA'] = 1
obj['DPLRA'] = 0
obj['DPE'] = 0
obj['iteraccion'] = 20
obj['tailleobject'] = 322
obj['taillesignal'] = 644
obj['tailleholo'] = 322
obj['cuantificar'] = 'SI'

funcionprincipal(obj)

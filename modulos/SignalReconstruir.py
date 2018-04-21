# -*- coding: utf-8 -*-
import cv2
import numpy as np

#Construccion numérica del objeto
class SignalReconstruir(object):
    """docstring for SignalReconstruir"""
    def __init__(self):
        super(SignalReconstruir, self).__init__()
        
    def procesar(self,ruta,pixelmargin):
        img = cv2.imread(ruta,0).astype(float)
        Nimg = max(img.shape)  # tamano del objeto    [0]
        Nimgx,Nimgy = img.shape[1],img.shape[0]
        marg = pixelmargin
        Nobjx,Nobjy = Nimgx + 2*marg,Nimgy + 2*marg

        Nobj = max(Nobjx,Nobjy)
        if Nobj % 2 == 1:#Espo porque la imagen no cuadra con los procesos siguientes
            Nobj = Nobj + 1
        r1x,r1y = marg,marg
        r2x,r2y = r1x+(Nimgx),r1y+(Nimgy)
        fo = np.zeros((Nobj,Nobj))
        fo[r1y:r2y,r1x:r2x]=np.sqrt(img**2)

        return img,fo,Nimg,Nimgx,Nimgy,Nobj,Nobjx,Nobjy,r1x,r2x,r1y,r2y
        
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
#from skimage.filters.rank import entropy
from Excepciones import EntradaError
from funciones import f_sincinterp2v1,f_sincinterp2v2,f_OIDWYopt,f_pavr, f_OIDBhup, f_ODDWYopt, f_nsd
from math import pi

class Difusor(object):
    """docstring for Difusor"""
    def __init__(self, phase,phaseinitial):
        super(Difusor, self).__init__()
        self._phase = phase
        self._phaseinitial = phaseinitial
        self.s1 = 0
        self.s2 = 0
        self._optimiserODD = 0
    
    @property
    def controlbande(self):
        return self._controlbande

    @controlbande.setter
    def controlbande(self, value):
        self._controlbande = value

    @property
    def diffphase(self):
        return self._diffphase

    @diffphase.setter
    def diffphase(self, value):
        self._diffphase = value

    @property
    def iterODD(self):
        return self._iterODD

    @iterODD.setter
    def iterODD(self, value):
        self._iterODD = value

    @property
    def optimiserODD(self):
        return self._optimiserODD

    @optimiserODD.setter
    def optimiserODD(self, value):
        self._optimiserODD = value


    def calculerOID(self,Nobj):
        #obtener los datos corresppondientes
        phase = self._phase
        nobanlim=self._phaseinitial #---escoger fase no banda-limitada
        No=np.floor(Nobj/2)
        
        if phase=='phasealea' and nobanlim=='pasbandelimite':  #--calcular fase aleatoria no banda-limitada
            PH = 2*pi*np.random.rand(Nobj,Nobj)-pi# #---calcular fase aleatoria
            di = np.exp(1j*PH)# #---difusor con fase aleatoria banda-limitada
            DI = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(di)))*Nobj
            MASIR = np.amax(np.absolute(DI)**2)/np.mean(np.absolute(DI)**2)##--medida de la suavidad
            ffsin = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(DI)))/No
        if nobanlim=='bandelimitee': #---fase aleatoria de banda-limitada
            if phase == 'phasealea':
                PH = 2*pi*np.random.rand(No,No)-pi
                PH = np.exp(1j*PH)
                if Nobj%2==1: #--si el tamano del objeto es impar xoxox o xoxox
                    PH,self.s1,self.s2 = f_sincinterp2v1(PH,'i')
                else:        
                    PH,self.s1,self.s2 = f_sincinterp2v2(PH,'i')##---si es par xoxox o xoxo
                PH=np.angle(PH)
            if phase=='phaheur': #---metodo heuristico
                pho = self.diffphase
                PH,MASIRo = f_OIDBhup(int(No),pho)
                PH = np.exp(1j*PH)
                if Nobj%2==1:
                    PH,self.s1,self.s2 = f_sincinterp2v1(PH,'i')
                else:
                    PH,self.s1,self.s2 = f_sincinterp2v2(PH,'i')
                PH = np.angle(PH)
            if phase == 'phaspher': #----fase esferica
                R = self.controlbande
                N=2*No
                x=np.arange(-float(N)/2,float(N)/2)/N
                y=x
                X, Y = np.meshgrid(x,y)
                PH = 2*pi*R*(np.absolute(X)**2 + np.absolute(Y)**2)
                self.s1 = N/2-No/2
                self.s2 = self.s1+No
            if phase == 'phawyr': #----metodo Wyrowski
                PH,MASIR,self.s1,self.s2=f_OIDWYopt(Nobj,100,0.7)
            di = np.exp(1j*PH) #--difusor con fase aleatoria banda-limitada
            DI = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(di)))*Nobj
            MASIR = np.amax(np.absolute(DI[self.s1:self.s2,self.s1:self.s2])**2)/np.mean(np.absolute(DI[self.s1:self.s2,self.s1:self.s2])**2)
            MASK=np.zeros((DI.shape[0],DI.shape[0]))
            MASK[self.s1:self.s2,self.s1:self.s2]=1
            ffsin = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(DI*MASK)))/No
        return PH,MASIR,ffsin,DI


    def optimizerODD(self,fo,OID,MASIRdes,s1, s2, r1, r2):
        phase = self._phase
        nobanlim=self._phaseinitial
        if phase == 'phasealea' and nobanlim=='pasbandelimite':
            raise EntradaError('fait-vous directement le calcul hologramme analogue')
        PAVRdes, PHo = MASIRdes, OID
        N = np.shape(fo)[0]
        val = self.optimiserODD
        if val==0:
            phase_ODD = PHo
            fdo = np.absolute(fo)*np.exp(1j*phase_ODD)
            FD = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(fdo)))*N
            PAVRfinal = f_pavr(FD,1,N)
            ff = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(FD)))/N
            DSdif = f_nsd(ff,r1,r2)
        else:
            #cont = self.iterODD
            cont = 200
            dos  = np.exp(1j*PHo)
            phase_ODD,amp_ODD,Sf = f_ODDWYopt(fo,dos,s1,s2,PAVRdes,cont)
            fdo = np.absolute(fo)*np.exp(1j*phase_ODD)
            FD = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(fdo)))*N
            MASK=np.zeros((FD.shape[0],FD.shape[0]))
            MASK[s1:s2,s1:s2]=1
            ff = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(FD*MASK)))/N
            PAVRfinal = f_pavr(FD,s1,s2)
            DSdif = f_nsd(ff,r1,r2)
        return DSdif, PAVRfinal, phase_ODD, FD
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
#from skimage.filters.rank import entropy
from Excepciones import EntradaError
from funciones import f_nmse, f_snr, f_efficiency, f_uniformity, f_zeronoise, f_nsd, f_laplacianregularity
from math import pi

class Cuantificar(object):
    """docstring for Cuantificar"""

    def __init__(self, ILUM,tailleimg,taillesignal,pixelmargin,MASKholo):
        super(Cuantificar, self).__init__()
        self.B = np.array([0.3,0.5,0.6,0.7,0.75,0.8,0.85,0.9,0.95,1])
        self.ILUM = ILUM
        self.taillesignal = taillesignal
        self.pixelmargin = pixelmargin
        self.tailleimg = tailleimg
        self.MASKholo = MASKholo
        self.DPRA, self.PRs, self.PRb, self.DPLR, self.DPE = 1,1,0,0,0
        self._iterquantization = 20
        self._niveles = 4
        self.CODEDOUX = 'codedoux'

    @property
    def DPRA(self):
        return self.G

    @DPRA.setter
    def DPRA(self, value):
        self.G = value

    @property
    def PRs(self):
        return self.T

    @PRs.setter
    def PRs(self, value):
        self.T = value
    @property
    def PRb(self):
        return self.An

    @PRb.setter
    def PRb(self, value):
        self.An = value

    @property
    def DPLRA(self):
        # Do something if you want
        return self.Ad

    @DPLRA.setter
    def DPLRA(self, value):
        self.Ad = value

    @property
    def DPE(self):
        return self.Ent

    @DPE.setter
    def DPE(self, value):
        self.Ent = value
    
    @property
    def CODEDOUX(self):
        return self.codedoux

    @CODEDOUX.setter
    def CODEDOUX(self, value):
        self.codedoux = value
    
    @property
    def iterquantization(self):
        return self._iterquantization

    @iterquantization.setter
    def iterquantization(self, value):
        self._iterquantization = value + 10

    @property
    def NIVELES(self):
        return self._niveles

    @NIVELES.setter
    def NIVELES(self, value):
        self._niveles = value

    def calculer(self,fon,Go,go,M, p1, p2, q1, q2):
        NIVELES, ILUM = self.NIVELES, self.ILUM
        margen = self.pixelmargin
        R = self.tailleimg/2
        b1=p1+margen
        b2 = p2-margen
        ee, k, m, iterq = 1, 0, 1, self.iterquantization
        iterpasq = np.round(iterq*np.sort(self.B)[::-1])
        self.COURBE_EQ = np.zeros((1,max(self.B.shape)*iterq))#%zeros(1,ZE*iterpasq);
        self.COURBE_EDQ, self.COURBE_RSBQ, self.CUQ = self.COURBE_EQ, self.COURBE_EQ, self.COURBE_EQ
        DELTAFASE = 2*pi/NIVELES
        while ee < max(self.B.shape):
            k = k+1
            Gj = np.angle(Go)
            A = self.Ent*(self.entropySignal(Gj+pi)-pi)
            Gj2 = A+Gj + pi
            E = self.B[ee]
            for z in range(NIVELES):
                KK = (Gj2>(z-.5*E)*DELTAFASE) & (Gj2<=(z+0.5*E)*DELTAFASE)
                Gj2[KK] = z*DELTAFASE

            if self.CODEDOUX=='codedoux':
                Q_Gj = self.B[ee]*np.exp(1j*(Gj2-pi))*self.MASKholo+ (1-self.B[ee]*Go)
                Q_Gj1 = Q_Gj*ILUM #abs(Go).*exp(1i*(Gj));
            else:
                Q_Gj = np.exp(1j*(Gj2-pi))*self.MASKholo
                Q_Gj1 =Q_Gj*ILUM
            gj = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(Q_Gj1)))/M
            ##---ver reconst
            ##------------------
            Bj = np.sqrt(sum(sum(np.absolute(gj[p1:p2,p1:p2])**2))/sum(sum(np.absolute(fon)**2)))#bien + phase spherique
            foj = fon
            FILTER = f_laplacianregularity(np.absolute(gj),1,p1,p2)
            #FILTER = self.entropySignal(abs(gj(p1:p2,p1:p2)));
            if self.G==0 and self.T==1:
                Cj = sum(sum(np.absolute(Bj*fon)*abs(gj[p1:p2,p1:p2])))/sum(sum(np.absolute(Bj*fon)**2))
                #---libertad de escala wirowsky
                gj2 = (1-self.T*self.An)*gj
                #division por cero
                gj2[p1:p2,p1:p2] = Cj*foj*np.exp(1j*np.angle(gj[p1:p2,p1:p2]))+self.T*self.Ad*FILTER*np.exp(1j*np.angle(gj[p1:p2,p1:p2]))
            else:
                #Division por cero
                ARPD = (2*self.G/pi)*np.arctan((np.absolute(gj[p1:p2,p1:p2])-Bj*foj)/(Bj*foj))+self.G-1
                gj2 = (1-self.T*self.An)*gj
                gj2[p1:p2,p1:p2] = self.T*foj*np.exp(1j*np.angle(gj[p1:p2,p1:p2]))+ (1-self.T-self.T*ARPD)*gj[p1:p2,p1:p2]+self.T*self.Ad*FILTER*np.exp(1j*np.angle(gj[p1:p2,p1:p2]))
            Go = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(gj2)))*M
            
            if k == iterpasq[ee]:
                ee = ee+1
                k = 0
            self.EQ = f_nmse(go,gj,int(p1),int(p2))
            self.RSBQ = f_snr(go,gj,int(p1),int(p2))
            self.EDQ = f_efficiency(gj,int(b1),int(b2))
            self.UQ = f_uniformity(gj,int(b1),int(b2))
            self.ZNQ = f_zeronoise(gj,int(p1),int(p2),int(b1),int(b2))
            self.SDQ = f_nsd(gj,int(p1),int(p2))
            self.COURBE_EQ[0][m]=self.EQ
            self.COURBE_EDQ[0][m]=self.EDQ
            self.COURBE_RSBQ[0][m]=self.RSBQ
            self.CUQ[0][m] = self.UQ
            m=m+1
        ee, k, m = 1, 0, 1
        iterpasq2 = 5*np.ones((1,max(self.B.shape)))
        self.COURBE_EQ = np.zeros((1,max(np.shape(self.B))*iterq))
        self.COURBE_EDQ, self.COURBE_RSBQ, self.CUQ = self.COURBE_EQ, self.COURBE_EQ, self.COURBE_EQ
        DELTAFASE = 2*pi/NIVELES
        while ee < max(np.shape(self.B)):
            k = k+1
            #--operador U
            Gj = np.angle(Go)
            #--cuantizacion iterativa
            #KK = 0;
            A = self.Ent*(self.entropySignal(Gj+pi)-pi)
            Gj2 = A+Gj + pi
            E = self.B[ee]
            for z in range(NIVELES):
                KK = (Gj2>(z-.5*E)*DELTAFASE) & (Gj2<=(z+0.5*E)*DELTAFASE)
                Gj2[KK] = z*DELTAFASE
            Q_Gj = np.exp(1j*(Gj2-pi))*self.MASKholo
            Q_Gj1 =Q_Gj*ILUM
            gj = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(Q_Gj1)))/M
            #---ver reconst
            Bj = np.sqrt(sum(sum(np.absolute(gj[p1:p2,p1:p2])**2))/sum(sum(np.absolute(fon)**2)))#bien + phase spherique
            Cj = sum(sum(np.absolute(Bj*fon)*np.absolute(gj[p1:p2,p1:p2])))/sum(sum(np.absolute(Bj*fon)**2))#---libertad de escala wirowsky
            gj2 = (1-self.An)*gj
            gj2[p1:p2,p1:p2] = Cj*fon*np.exp(1j*np.angle(gj[p1:p2,p1:p2]))
            EA = f_nmse(go,gj,int(p1),int(p2))
            RSBA = f_snr(go,gj,int(p1),int(p2))
            EDA = f_efficiency(gj,int(b1),int(b2))
            Go = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(gj2)))*M
            if k == iterpasq2[0][ee]:
                ee = ee+1
                k = 0
            self.EQ = f_nmse(go,gj,int(p1),int(p2))
            self.RSBQ = f_snr(go,gj,int(p1),int(p2))
            self.EDQ = f_efficiency(gj,int(b1),int(b2))
            self.UQ = f_uniformity(gj,int(b1),int(b2))
            self.ZNQ = f_zeronoise(gj,int(p1),int(p2),int(b1),int(b2))
            self.SDQ = f_nsd(gj,int(p1),int(p2))
            #error
            self.COURBE_EQ[0][m]=self.EQ
            self.COURBE_EDQ[0][m]=self.EDQ
            self.COURBE_RSBQ[0][m]=self.RSBQ
            self.UQ = f_uniformity(gj,int(b1),int(b2))
            self.CUQ[0][m] = self.UQ
            m=m+1
        #--holo efectivo y su TF
        holoef = Q_Gj[q1:q2,q1:q2]*ILUM[q1:q2,q1:q2]
        recholoef = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(holoef)))/M
        self.EQ = f_nmse(go,gj,int(p1),int(p2))
        self.RSBQ = f_snr(go,gj,int(p1),int(p2))
        self.EDQ = f_efficiency(gj,int(b1),int(b2))
        #if ['tipoimg']=='circle':
        #    UQ = f_uniformitycircle(gj,R,p1,p2)
        #else:
        self.UQ = f_uniformity(gj,int(b1),int(b2))
        self.ZNQ = f_zeronoise(gj,int(p1),int(p2),int(b1),int(b2))
        self.SDQ = f_nsd(gj,int(p1),int(p2))
        return recholoef,Q_Gj,Gj,gj,holoef
        

    def entropySignal(self, signal):
        '''
        function returns entropy of a signal
        signal must be a 1-D numpy array
        '''
        imhist,bins = np.histogram(signal.flatten(),256,density=False)
        pdf = imhist.astype(float) / signal.size
        pdf[pdf == 0] = 1
        e = -sum(pdf*np.log2(pdf))
        return e

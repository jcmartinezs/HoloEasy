#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

#from skimage.measure import shannon_entropy
from skimage.morphology import disk
#from skimage.filters.rank import entropy
from Excepciones import EntradaError
from funciones import f_nmse, f_snr, f_efficiency,f_laplacianregularity
from math import pi


class Analogique(object):
    """docstring for Analogique"""
    def __init__(self, ILUM,iteropt,tailleimg,taillesignal,tailleholo,pixelmargin):
        super(Analogique, self).__init__()
        self.ILUM = ILUM
        #self.iteropt = iteropt
        self.iteropt = 50
        self.taillesignal = taillesignal
        self.tailleholo = tailleholo
        self.pixelmargin = pixelmargin
        self.tailleimg = tailleimg
        self.DPRA, self.PRs, self.PRb, self.DPLR, self.DPE = 1,1,0,0,0
        self.codedoux = ''

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

        
    def optimiser(self,_optimiser,fo, ODD,r1,r2,lissage2):
        PHo, ILUM, M, H, margen, iteropt, K = ODD, self.ILUM, self.taillesignal, self.tailleholo, self.pixelmargin, self.iteropt, lissage2
        R = self.tailleimg/2
        Nodd = PHo.shape[0]
        if M == Nodd:
            M,p1,p2 = Nodd,r1,r2
            PHo = PHo[p1:p2,p1:p2]
            fo = fo[p1:p2,p1:p2]
            TMP2 = M%2
        else:
            TMP1 = Nodd%2
            TMP2 = M%2
            if TMP1==1:
                p1 = (M-TMP2)/2-(Nodd-TMP1)/2
            else:
                p1 = (M-TMP2)/2-(Nodd)/2+1
            p2 = p1+Nodd
        #---coordonnes fenetre hologrammeopt
        TMP3 = H%2
        q1 = (M-TMP2)/2-(H-TMP3)/2
        q2 = q1+H
        #clear TMP1 TMP2 TMP3
        #--coodenadas zero noise dentro del plano senal
        b1 = p1 + margen
        b2 = p2 - margen
        #---normalizar energia en la ventana de acuerdo al tamano holograma
        Co = np.sqrt(H**2/sum(sum(np.absolute(fo)**2)))
        fon=Co*fo
        go = np.zeros((M,M),dtype=complex)
        go[p1:p2,p1:p2] = fon*np.exp(1j*PHo)
        if _optimiser==1:
            
            goi = go
            Gj = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(goi)))*M
            PAVRdes= K*np.amax(abs(Gj[q1:q2,q1:q2])**2)/np.mean(np.absolute(Gj[q1:q2,q1:q2])**2)
            for cont in range(iteropt):
                ABS_wind = np.absolute(Gj[q1:q2,q1:q2])
                PH_wind = np.angle(Gj[q1:q2,q1:q2])
                FD_clip = np.sqrt(PAVRdes*np.mean(ABS_wind**2))
                X, Y = np.nonzero(ABS_wind>FD_clip)
                ABS_wind[X,Y]=FD_clip
                U_Gj =np.zeros((M,M),dtype=complex)
                U_Gj[q1:q2,q1:q2]=ABS_wind*np.exp(1j*PH_wind)
                #===================
                U_Gj = ILUM*U_Gj#---haciendo lissage + gauss
                gj = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(U_Gj)))/M
                gj2 = np.zeros((M,M),dtype=complex)
                Bj = np.sqrt(sum(sum(np.absolute(gj[p1:p2,p1:p2])**2))/sum(sum(np.absolute(fon)**2)))#bien + phase spherique
                foj = Bj*fon
                #complex
                gj2[p1:p2,p1:p2] = foj*np.exp(1j*np.angle(gj[p1:p2,p1:p2]))
                #------------------------
                goi =gj2
                Gj = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(goi)))*M
                PAVRf= np.amax(np.absolute(Gj[q1:q2,q1:q2])**2)/np.mean(np.absolute(Gj[q1:q2,q1:q2])**2)
            go = np.zeros((M,M),dtype=complex)
            #complex
            go[p1:p2,p1:p2] = fon*np.exp(1j*np.angle(gj[p1:p2,p1:p2]))
        Gj = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(go)))*M
        return fon,go,p1,p2,q1,q2,b1,b2,Gj,go



    def calculer(self,obj,fon,go,iteranalog,p1, p2, q1, q2, b1, b2):
        iteranalog = iteranalog + 10
        M = self.taillesignal
        R = self.tailleimg/2
        ILUM = self.ILUM
        MASKholo = np.zeros((M,M))
        MASKholo[q1:q2,q1:q2]=1
        B = np.array([0.3,0.5,0.6,0.7,0.75,0.8,0.85,0.9,0.95,1,1])
        iterpas = iteranalog*np.ones((B.size,B.size))
        iterpas = np.reshape(iterpas,-1)
        self.CEA = np.zeros((2*B.size*iteranalog))
        self.CEDA = self.CEA
        self.CRSBA = self.CEA
        self.CUa = self.CEA
        goi = go
        m = 0
        for k in range(B.size):
            cont=0
            while cont < iterpas[k]:
                Gj = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(goi)))*M
                A = self.Ent*(self.entropySignal(np.angle(Gj)+pi)-pi)
                if self.CODEDOUX=='codedoux':
                    U_Gj = B[k]*np.exp(1j*(A+np.angle(Gj)))*MASKholo+ (1-B[k])*Gj
                    U_Gj1=U_Gj*ILUM
                else:
                    U_Gj = np.exp(1j*(A+np.angle(Gj)))*MASKholo
                    U_Gj1=U_Gj*ILUM
                gj = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(U_Gj1)))/M
                Bj = np.sqrt(sum(sum(np.absolute(gj[p1:p2,p1:p2])**2))/sum(sum(np.absolute(fon)**2)))
                FILTER1 = f_laplacianregularity(np.absolute(gj),1,p1,p2)
                if self.G==0 and self.T==1:
                    Cj = sum(sum(np.absolute(Bj*fon)*np.absolute(gj[p1:p2,p1:p2])))/sum(sum(np.absolute(Bj*fon)**2))#libertad de escala wirowsky
                    gj2 = (1-self.T*self.An)*gj
                    gj2[p1:p2,p1:p2] = Cj*fon*np.exp(1j*np.angle(gj[p1:p2,p1:p2]))+self.T*self.Ad*FILTER1*np.exp(1j*np.angle(gj[p1:p2,p1:p2]))
                else:
                    ARPD = (2*self.G/pi)*np.arctan((np.absolute(gj[p1:p2,p1:p2])-Bj*fon)/(Bj*fon))+self.G-1
                    gj2 = (1-self.T*self.An)*gj
                    gj2[p1:p2,p1:p2] = self.T*fon*np.exp(1j*np.angle(gj[p1:p2,p1:p2]))+ (1-self.T-self.T*ARPD)*gj[p1:p2,p1:p2]+self.T*self.Ad*FILTER1*np.exp(1j*np.angle(gj[p1:p2,p1:p2]))
                self.EA = f_nmse(np.absolute(go),gj,int(p1),int(p2))
                self.RSBA = f_snr(go,gj,int(p1),int(p2))
                self.EDA = f_efficiency(gj,int(b1),int(b2))
                self.CEA[m] = self.EA
                self.CEDA[m] = self.EDA
                self.CRSBA[m] = self.RSBA
                m= m+1
                cont = cont+1
                goi =gj2
        iterpas2= 2*np.ones((B.shape[0],B.shape[0]))
        goi = gj
        goi[p1:p2,p1:p2]=fon*np.exp(1j*np.angle(gj[p1:p2,p1:p2]))
        for k in range(B.size):
            cont=1
            while cont < iterpas[k]:
                Gj = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(goi)))*M
                A = self.Ent*(self.entropySignal(np.angle(Gj)+pi)-pi)
                U_Gj = np.exp(1j*(A+np.angle(Gj)))*MASKholo
                U_Gj1=U_Gj*ILUM
                gj = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(U_Gj1)))/M
                Bj = np.sqrt(sum(sum(np.absolute(gj[p1:p2,p1:p2])**2))/sum(sum(np.absolute(fon)**2)))#bien + phase spherique
                Cj = sum(sum(np.absolute(Bj*fon)*np.absolute(gj[p1:p2,p1:p2])))/sum(sum(np.absolute(Bj*fon)**2))#---libertad de escala wirowsky
                gj2 = (1-self.An)*gj
                gj2[p1:p2,p1:p2] = Cj*fon*np.exp(1j*np.angle(gj[p1:p2,p1:p2]))
                self.EA = f_nmse(go,gj,int(p1),int(p2))
                self.RSBA = f_snr(go,gj,int(p1),int(p2))
                self.EDA = f_efficiency(gj,int(b1),int(b2))
                self.CEA[m],self.CEDA[m],self.CRSBA[m] = self.EA,self.EDA,self.RSBA 
                m,cont,goi= m+1,cont+1,gj2
        holoa = U_Gj[q1:q2,q1:q2]
        return gj,gj2,MASKholo,U_Gj,M,B,holoa

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

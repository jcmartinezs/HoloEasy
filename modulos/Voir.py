#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from Excepciones import EntradaError

class Voir(object):
    """docstring for Voir"""
    def __init__(self):#, arg
        super(Voir, self).__init__()
        #self.arg = arg
        
    def analogique_voir(self,fs, PHo, M, H, r1, r2, valilum):
        Nodd = PHo.shape[0]
        if M <Nodd:
            raise EntradaError('ilumination_circle','plain signal >= object')
        if M == Nodd:
            p1,p2 = r1,r2
            PHo = PHo[p1:p2,p1:p2]
            fs = fs[p1:p2,p1:p2]
            TMP2 = M%2
        else:
            TMP1 = Nodd%2
            TMP2 = M%2
            p1 = (M-TMP2)/2-(Nodd-TMP1)/2
            p2 = p1+Nodd
        #---coordonnes fenetre hologramme
        TMP3 = H%2
        q1 = (M-TMP2)/2-(H-TMP3)/2
        q2 = q1+H
        #---normalizar energia en la ventana de acuerdo al tamano holograma
        Co = np.sqrt(M**2/sum(sum(np.absolute(fs)**2)))
        fs = Co*np.absolute(fs)
        go = np.zeros((M,M),dtype=complex)
        go[p1:p2,p1:p2] = Co*fs*np.exp(1j*PHo)    
        #-----------
        Gj = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(go)))*M
        #---------------------------------------
        g1 = -(q2-q1+1)/2
        g2 =(q2-q1+1)/2
        x=np.arange(-float(M)/2,float(M)/2)
        xr=np.arange(-float(q2-q1+1)/2,float(q2-q1+1)/2)
        if valilum=='circle':
            MASKILUM=np.sqrt((H/2)**2-xr**2)
        
        elif valilum=='gauss':
            TMP3 = M/2%2
            s1 = (M-TMP2)/2-(M/2-TMP3)/2
            s2 = s1+M/2
            h1 = -(s2-s1)/2
            h2 =(s2-s1+1)/2
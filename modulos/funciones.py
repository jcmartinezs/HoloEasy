#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from math import pi
import math
#ZN = f_zeronoise(f,p1,p2,b1,b2). Is the mesure of the intensity present in
#the frame zero that cannot be accounted in the efficiency of the order the
#diffraction inside the area defined by the coordones p1,p2,b1,b2. Where p1 and p2 are the coordinates of the exter nal squar and b1,b2 are de signal windows.     

#def mean2(x):
#    return sum(x[:])/x.size


def f_zeronoise(f,p1,p2,b1,b2):
    maximo = np.amax(np.shape(f))
    MK = np.zeros((maximo,maximo))
    MK[p1:p2,p1:p2]=1
    MK[b1:b2,b1:b2]=0
    #interrumpir aqui
    MK = MK*(np.absolute(f)**2+10)
    I = MK[MK>0]
    I=I-10
    Z = sum(I)/sum(sum(np.absolute(f)**2))
    return Z

#Dibuja linspace
def f_uniformitycircle(f,R,p1,p2):
    fo = f[p1:p2,p1:p2]
    I = np.absolute(fo)**2
    N = np.shape(fo)[0]
    x=np.linspace(-N/2,N/2,N)
    X, Y = np.meshgrid(x,x)
    Io = I[X**2+Y**2<=R**2]#---valores dentro del circulo
    U = float(max(Io)-min(Io))/float(max(Io)+min(Io))
    return U

def f_uniformity(f,b1,b2):
    I = np.absolute(f[b1:b2,b1:b2])**2
    MAX = np.amax(I)
    MIN = np.amin(I)
    U = float(MAX - MIN)/float(MAX + MIN)
    return U

def f_snr(fo,f,p1,p2):
    b =sum(sum(np.absolute(fo[p1:p2,p1:p2]).astype(float)*np.absolute(f[p1:p2,p1:p2])))/sum(sum(np.absolute(fo[p1:p2,p1:p2]).astype(float)**2))
    R = np.absolute(fo[p1:p2,p1:p2]).astype(float)-b*np.absolute(f[p1:p2,p1:p2]).astype(float)
    SNR = sum(sum(np.absolute(fo[p1:p2,p1:p2]).astype(float)**2))/sum(sum(np.absolute(R)**2))
    return SNR
#verificar
def f_sincinterp2v2(fo,flag):
    No = np.shape(fo)[0]
    if flag=='i':
        Ffo = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(fo)))*No
    else:
        Ffo = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(fo)))/No  
    IMP = No%2
    N1 = 2*No
    IMP2=N1%2
    q1 = (N1-IMP2)/2-(No-IMP)/2#+1
    q2 = q1+No#-1
    F = np.zeros((N1,N1),dtype=complex)
    F[q1:q2,q1:q2]=Ffo
    plt.figure('f_sincinterp2v2')
    plt.imshow(np.absolute(F)**2, cmap = plt.cm.Greys_r)
    if flag=='i':
        fs = 2*np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(F)))/N1
    else:
        fs = 2*np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(F)))*N1
    return fs,q1,q2

def f_sincinterp2v1(fo,flag):
    No = np.shape(fo)[0]
    print(fo.shape)
    print(No)
    if flag=='i':
        Ffo = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(fo)))*No
    else:
        Ffo = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(fo)))/No
    M=2
    IMP = No%2
    if IMP==1:
        N1 = M*No#+1;
        q1 = (No+IMP)/2#+1;
        q2 = q1+No#-1;
    else:
        N1 = M*No      #+1;
        q1 = (No)/2    #+1;
        q2 = q1+No     #-1;
    F = np.zeros((N1,N1),dtype=complex)
    print(N1)
    F[q1:q2,q1:q2]=Ffo
    K = N1/No
    if flag=='i':
        fs = M*np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(F)))/N1
    else:
        fs = M*np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(F)))*N1
    return fs,q1,q2

def f_rms(fo,g,px1,px2,py1,py2):
    b = np.sqrt(float(sum(sum(np.absolute(g[px1:px2,py1:py2]**2))))/float(sum(sum(np.absolute(fo[px1:px2,py1:py2])**2))))
    E = np.mean((np.absolute(g[px1:px2,py1:py2]) -np.absolute(b*fo[px1:px2,py1:py2]))**2)
    #E = ((np.absolute(g[px1:px2,py1:py2]) -np.absolute(b*fo[px1:px2,py1:py2]))**2).mean()
    #E = mean2((np.absolute(g[px1:px2,py1:py2]) -np.absolute(b*fo[px1:px2,py1:py2]))**2)
    return  E

def f_pavr(f,p1,p2):
    PAVR= np.amax(np.absolute(f[p1:p2,p1:p2])**2)/np.mean(np.absolute(f[p1:p2,p1:p2])**2)
    return PAVR

def f_OIDWYopt(N,it,K):
    No=np.floor(N/2)
    do = np.exp(1j*2*pi*np.random.rand(1,No))
    TMP = No%2
    Cop = No
    p1 = Cop-(No-TMP)/2
    p2 = p1+No
    D = np.zeros((1,N),dtype=complex)
    D[0,p1:p2]=2*np.fft.fftshift(np.fft.ifft(np.fft.ifftshift(do)))*np.sqrt(N)
    So = max(np.absolute(D[0,p1:p2])**2)/np.mean(np.absolute(D[0,p1:p2])**2)
    Sdes = K*So
    for k in range(it):
        ABS_D = np.absolute(D[0,p1:p2])
        PH_D = np.angle(D[0,p1:p2])
        CLIP = np.sqrt(Sdes*np.mean(ABS_D**2))
        X = ABS_D>=CLIP
        ABS_D[X]=CLIP
        Dj=np.zeros((1,N),dtype=complex)
        Dj[0,p1:p2] = ABS_D*np.exp(1j*PH_D)
        dj = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(Dj)))/np.sqrt(N)
        do = np.exp(1j*np.angle(dj))
        D=np.fft.fftshift(np.fft.ifft(np.fft.ifftshift(do)))*np.sqrt(N)
        Sj = max(np.absolute(D[0,p1:p2])**2)/np.mean(np.absolute(D[0,p1:p2])**2)
        
    d1=np.angle(do)
    d2 =np.angle(do)
    DIF =np.zeros((N,N),dtype=complex)
    for m in range(N):
        for n in range(N):
            DIF[m,n] = np.exp(1j*(d1[0][m]+d2[0][n]))
    PH_OID = np.angle(DIF)
    Df=np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(DIF)))*N
    MASIR= np.amax(np.absolute(Df[p1:p2,p1:p2])**2)/np.mean(np.absolute(Df[p1:p2,p1:p2])**2)
    
    return PH_OID,MASIR,p1,p2

def f_OIDWY(N,it):
    No=np.floor(N/2)
    do = np.exp(1j*2*pi*np.random.rand(No,1))
    TMP = No%2
    Cop = No#+1;
    p1 = Cop-(No-TMP)/2
    p2 = p1+No#-1;
    D = np.zeros((N,1),dtype=complex)
    D[p1:p2]=np.fft.fftshift(np.fft.ifft(np.fft.ifftshift(do)))*np.sqrt(N)
    CLIP = np.sqrt(max(np.absolute(D[p1:p2])**2))
    for k in range(it):
        X = np.absolute(D)>=CLIP
        D[X]=CLIP*np.exp(1j*np.angle(D[X]))
        Dj=np.zeros((N,1),dtype=complex)
        Dj[p1:p2] = D[p1:p2]
        do = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(Dj)))/np.sqrt(N)
        do = np.exp(1j*np.angle(do))
        D=np.fft.fftshift(np.fft.ifft(np.fft.ifftshift(do)))*np.sqrt(N)
        Dmaxj2 =max(np.absolute(D)**2)
        Sj = np.mean(np.absolute(D)**2)/Dmaxj2
    do = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(Dj)))/np.sqrt(N)
    d1=np.angle(do)
    d2 =np.angle(do)
    DIF =np.zeros((N,N),dtype=complex)
    for m in range(N):
        for n in range(N):
            DIF[m,n] = np.exp(1j*(d1[m][0]+d2[n][0]))
    PH_OID = np.angle(DIF)
    Df=np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(DIF)))*N
    MASIR= np.mean(np.absolute(Df)**2)/np.amax(np.absolute(Df)**2)
    return PH_OID,MASIR,p1,p2

def f_OIDBhup(No,pho):
    if No%2==0:
        v1 = np.concatenate((np.ones((No/2,1)),np.zeros((No/2,1))),axis=1)
        v1 = v1.ravel()
        v1[v1==0]=-1
        v2 = np.concatenate((np.zeros((No/2,1)),np.ones((No/2,1))),axis=1)
        v2 = v2.ravel()
        v2[v2==0]=-1
    if No%2==1:
        v1 = np.concatenate((np.ones(((No+1)/2,1)),np.zeros(((No+1)/2,1))),axis=1)
        v1 = v1.ravel()
        v1[v1==0]=-1
        v1=v1[0:No]
        v2 = np.concatenate((np.zeros(((No+1)/2,1)),np.ones(((No+1)/2,1))),axis=1)
        v2 = v2.ravel()
        v2[v2==0]=-1
        v2=v2[0:No]
    SG = np.zeros((No,No))
    for m in range(int(No)):
        if m%2==1:
            SG[m,:]=v1
        else:
            SG[m,:]=v2
    PH =SG
    PH[PH==-1]=pho
    PH[PH==1]=0
    do = np.exp(1j*PH)
    Do = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(do)))*No
    MASIRo = np.amax(np.absolute(Do)**2)/np.mean(np.absolute(Do)**2)
    kk=0
    P = np.random.permutation(int(No)-1)
    Q = np.random.permutation(int(No)-1)
    MASIRj = 0
    TMP = 100000
    while kk<1000:
        for p in P:
            for q in Q:
                P1 = PH[p-1,q]
                P2 = PH[p,q+1]
                P3 = PH[p+1,q]
                P4 = PH[p,q-1]
                Pr = np.random.rand(1)
                if (P1==P2)and(P2==P3)and(P3==P4)and(Pr<=0.5):
                    if PH[p,q] == PH[p-1,q]+pho:
                        PH[p,q] = PH[p-1,q]-pho
                    else:
                        PH[p,q] = PH[p-1,q]+pho
                    Dj = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(np.exp(1j*PH))))*No
                    MASIRj = np.amax(np.absolute(Dj)**2)/np.mean(np.absolute(Dj)**2)
                    if MASIRj > MASIRo:
                        if PH[p,q] == PH[p-1,q]+pho:
                            PH[p,q] = PH[p-1,q]-pho
                        else:
                            PH[p,q] = PH[p-1,q]+pho
                    else:
                        MASIRo = MASIRj
        if MASIRo>=TMP:
            break
        TMP = MASIRo
        kk = kk+1 
    MASIRo =MASIRj
    P = np.random.permutation(int(No)-1)
    while kk<1000:
        for p in P:
            P1 = PH[1,p+1]
            P2 = PH[2,p]
            Pr = np.random.rand(1)
            if (P1==P2)and(Pr<=0.5):
                if PH[1,p] == PH[1,p+1]+pho:
                    PH[1,p] = PH[1,p+1]-pho
                else:
                    PH[1,p] = PH[1,p+1]+pho
                Dj = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(np.exp(1j*PH))))*No
                MASIRj = np.amax(np.absolute(Dj)**2)/np.mean(np.absolute(Dj)**2)
                if MASIRj > MASIRo:
                    if PH[1,p] == PH[1,p+1]+pho:
                        PH[1,p] = PH[1,p+1]-pho
                    else:
                        PH[1,p] = PH[1,p+1]+pho    
                else:
                    MASIRo = MASIRj    
        if MASIRo>=TMP:
            break
        TMP = MASIRo
        kk = kk+1;  
    MASIRo =MASIRj
    di = np.exp(1j*PH)
    DI = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(di)))*No
    P = np.random.permutation(int(No)-1)
    while kk<1000:#estudio
        for p in P:
            P1 = PH[p,2]
            P2 = PH[p+1,1]
            Pr = np.random.rand(1)
            if (P1==P2)and(Pr<=0.5):
                if PH[p,1] == PH[p+1,1]+pho:
                    PH[p,1] = PH[p+1,1]-pho
                else:
                    PH[p,1] = PH[p+1,1]+pho
            Dj = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(np.exp(1j*PH))))*No
            MASIRj = np.amax(np.absolute(Dj)**2)/np.mean(np.absolute(Dj)**2)
            if MASIRj > MASIRo:
                if PH[p,1] == PH[p+1,1]+pho:
                    PH[p,1] = PH[p+1,1]-pho
                else:
                    PH[p,1] = PH[p+1,1]+pho
            else:
                MASIRo = MASIRj    
        if MASIRo>=TMP:
            break
        TMP = MASIRo
        kk = kk+1        
    MASIRo =MASIRj
    di = np.exp(1j*PH)
    DI = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(di)))*No
    P = np.random.permutation(int(No)-1)
    while kk<1000:
        for p in P:
            P1 = PH[No-2,p]
            P2 = PH[No-1,p+1]
            Pr = np.random.rand(1)
            if (P1==P2)and(Pr<=0.5):
                if PH[No-1,p] == PH[No-1,p]-pho:
                    PH[No-1,p] = PH[No-1,1]+pho
                else:
                    PH[No-1,p] = PH[No-1,1]-pho
                Dj = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(np.exp(1j*PH))))*No
                MASIRj = np.amax(np.absolute(Dj)**2)/np.mean(np.absolute(Dj)**2)
                if MASIRj > MASIRo:
                    if PH[No-1,p] == PH[No-1,p]-pho:
                        PH[No-1,p] = PH[No-1,1]+pho
                    else:
                        PH[No-1,p] = PH[No-1,1]-pho
                else:
                    MASIRo = MASIRj
        if MASIRo>=TMP:
            break
        TMP = MASIRo
        kk = kk+1
    MASIRo =MASIRj
    di = np.exp(1j*PH)
    DI = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(di)))*No
    P = np.random.permutation(int(No)-1)
    while kk<1000:
        for p in P:
            P1 = PH[p,No-2]
            P2 = PH[p+1,No-1]
            Pr = np.random.rand(1)
            if (P1==P2)and(Pr<=0.5):
                if PH[p,No-1] == PH[p,No-1]+pho:
                    PH[p,No-1] = PH[p,No-1]-pho
                else:
                    PH[p,No-1] = PH[p,No-1]+pho
                Dj = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(np.exp(1j*PH))))*No
                MASIRj = np.amax(np.absolute(Dj)**2)/np.mean(np.absolute(Dj)**2)
                if MASIRj > MASIRo:
                    if PH[p,No-1] == PH[p,No-1]+pho:
                        PH[p,No-1] = PH[p,No-1]-pho
                    else:
                        PH[p,No-1] = PH[p,No-1]+pho
                else:
                    MASIRo = MASIRj
        if MASIRo>=TMP:
            break
        TMP = MASIRo
        kk = kk+1
    MASIRo =MASIRj
    di = np.exp(1j*PH)
    DI = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(di)))*No
    P = np.random.permutation(int(No)-1)
    Q = np.random.permutation(int(No)-1)
    TMP = 100000
    while kk<1000:
        for p in P:
            for q in Q:
                P1 = PH[p-1,q]
                P2 = PH[p,q+1]
                P3 = PH[p+1,q]
                P4 = PH[p,q-1]
                Pr = np.random.rand(1)
                if (P1==P2)and(P2==P3)and(P3==P4)and(Pr<=0.5):
                    if PH[p,q] == PH[p-1,q]+pho:
                        PH[p,q] = PH[p-1,q]-pho
                    else:
                        PH[p,q] = PH[p-1,q]+pho
                    Dj = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(np.exp(1j*PH))))*No
                    MASIRj = np.amax(np.absolute(Dj)**2)/np.mean(np.absolute(Dj)**2)
                    if MASIRj > MASIRo:
                        if PH[p,q] == PH[p-1,q]+pho:
                            PH[p,q] = PH[p-1,q]-pho
                        else:
                            PH[p,q] = PH[p-1,q]+pho
                    else:
                        MASIRo = MASIRj
        if MASIRo>=TMP:
            break
        TMP = MASIRo
        kk = kk+1
    di = np.exp(1j*PH)
    DI = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(di)))*No
    PH_OID=PH
    return PH_OID,MASIRo

def f_OID(No,pho):
    if No%2==0:
        v1 = np.concatenate((np.ones((1,No/2)),np.zeros((1,No/2))),axis=0)
        v1 = v1.ravel()
        v1[v1==0]=-1
        v2 = np.concatenate((np.zeros((1,No/2)),np.ones((1,No/2))),axis=0)
        v2 = v2.ravel()
        v2[v2==0]=-1
    if No%2==1:
        v1 = np.concatenate((np.ones((1,(No+1)/2)),np.zeros((1,(No+1)/2))),axis=0)
        v1 = v1.ravel()
        v1[v1==0]=-1
        v1=v1[1:No]
        v2 = np.concatenate((np.zeros((1,(No+1)/2)),np.ones((1,(No+1)/2))),axis=0)
        v2 = v2.ravel()
        v2[v2==0]=-1
        v2=v2[1:No]
    SG = np.zeros((No,No))
    for m in range(No):
        if m%2==1:
            SG[m,:]=v1
        else:
            SG[m,:]=v2
    PH =SG
    PH[PH==-1]=pho
    PH[PH==1]=0
    do = np.exp(1j*PH)
    Do = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(do)))/No
    MASIRo = np.amax(np.absolute(Do)**2)/np.mean(np.absolute(Do)**2)
    kk=0
    P = np.random.permutation(int(No)-2)
    P[P==1]=No-1
    Q = np.random.permutation(int(No)-2)
    Q[Q==1]=No-1
    TMP = 100000
    while kk<1000:
        for p in range(P):
            for q in range(Q):
                P1 = PH[p-1,q]
                P2 = PH[p,q+1]
                P3 = PH[p+1,q]
                P4 = PH[p,q-1]
                Pr = np.random.rand(1)
                if (P1==P2)and(P2==P3)and(P3==P4)and(Pr<=0.5):
                    if PH[p,q] == PH[p-1,q]+pho:
                        PH[p,q] = PH[p-1,q]-pho
                    else:
                        PH[p,q] = PH[p-1,q]+pho
                    Dj = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(np.exp(1j*PH))))*No
                    MASIRj = np.amax(np.absolute(Dj)**2)/np.mean(np.absolute(Dj)**2)
                    if MASIRj > MASIRo:
                        if PH[p,q] == PH[p-1,q]+pho:
                            PH[p,q] = PH[p-1,q]-pho
                        else:
                            PH[p,q] = PH[p-1,q]+pho
                    else:
                        MASIRo = MASIRj
        if MASIRo>=TMP:
            break
        TMP = MASIRo
        kk = kk+1
    MASIRo =MASIRj
    P = np.random.permutation(int(No)-2)
    P[P==1]=No-1
    while kk<1000:
        for p in range(P):
            P1 = PH[1,p+1]
            P2 = PH[2,p]
            Pr = np.random.rand(1)
            if (P1==P2)and(Pr<=0.5):
                if PH[1,p] == PH[1,p+1]+pho:
                    PH[1,p] = PH[1,p+1]-pho
                else:
                    PH[1,p] = PH[1,p+1]+pho
                Dj = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(np.exp(1j*PH))))*No
                MASIRj = np.amax(np.absolute(Dj)**2)/np.mean(np.absolute(Dj)**2)
                if MASIRj > MASIRo:
                    if PH[1,p] == PH[1,p+1]+pho:
                        PH[1,p] = PH[1,p+1]-pho
                    else:
                        PH[1,p] = PH[1,p+1]+pho
                else:
                    MASIRo = MASIRj
        if MASIRo>=TMP:
            break
        TMP = MASIRo
        kk = kk+1
    MASIRo =MASIRj
    P = np.random.permutation(int(No)-2)
    P[P==1]=No-1
    
    while kk<1000:
        for p in range(P):
            P1 = PH[p,2]
            P2 = PH[p+1,1]
            Pr = np.random.rand(1)
            if (P1==P2)and(Pr<=0.5):
                if PH[p,1] == PH[p+1,1]+pho:
                    PH[p,1] = PH[p+1,1]-pho
                else:
                    PH[p,1] = PH[p+1,1]+pho
                Dj = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(np.exp(1j*PH))))*No
                MASIRj = np.amax(np.absolute(Dj)**2)/np.mean(np.absolute(Dj)**2)
                if MASIRj > MASIRo:
                    if PH[p,1] == PH[p+1,1]+pho:
                        PH[p,1] = PH[p+1,1]-pho
                    else:
                        PH[p,1] = PH[p+1,1]+pho
                else:
                    MASIRo = MASIRj

        if MASIRo>=TMP:
            break
        TMP = MASIRo
        kk = kk+1
    MASIRo =MASIRj
    P = np.random.permutation(int(No)-2)
    P[P==1]=No-1
    while kk<1000:
        for p in range(P):
            P1 = PH[No-1,p]
            P2 = PH[No,p+1]
            Pr = np.random.rand(1)
            if (P1==P2)and(Pr<=0.5):
                if PH[No,p] == PH[No-1,p]-pho:
                    PH[No,p] = PH[No-1,1]+pho
                else:
                    PH[No,p] = PH[No-1,1]-pho
                Dj = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(np.exp(1j*PH))))*No
                MASIRj = np.amax(np.absolute(Dj)**2)/np.mean(np.absolute(Dj)**2)
                if MASIRj > MASIRo:
                    if PH[No,p] == PH[No-1,p]-pho:
                        PH[No,p] = PH[No-1,1]+pho
                    else:
                        PH[No,p] = PH[No-1,1]-pho
                else:
                    MASIRo = MASIRj
        if MASIRo>=TMP:
            break
        TMP = MASIRo
        kk = kk+1
    MASIRo =MASIRj
    P = np.random.permutation(int(No)-2)
    P[P==1]=No-1
    while kk<1000:
        for p in range(P):
            P1 = PH[p,No-1]
            P2 = PH[p+1,No]
            Pr = np.random.rand(1)
            if (P1==P2)and(Pr<=0.5):
                if PH[p,No] == PH[p,No-1]+pho:
                    PH[p,No] = PH[p,No-1]-pho
                else:
                    PH[p,No] = PH[p,No-1]+pho
                Dj = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(np.exp(1j*PH))))*No
                MASIRj = np.amax(np.absolute(Dj)**2)/np.mean(np.absolute(Dj)**2)
                if MASIRj > MASIRo:
                    if PH[p,No] == PH[p,No-1]+pho:
                        PH[p,No] = PH[p,No-1]-pho
                    else:
                        PH[p,No] = PH[p,No-1]+pho
                else:
                    MASIRo = MASIRj
        if MASIRo>=TMP:
            break
        TMP = MASIRo
        kk = kk+1
    MASIRo =MASIRj
    P = np.random.permutation(int(No)-2)
    P[P==1]=No-1
    Q = np.random.permutation(int(No)-2)
    Q[Q==1]=No-1
    TMP = 100000
    while kk<1000:
        for p in range(P):
            for q in range(Q):
                P1 = PH[p-1,q]
                P2 = PH[p,q+1]
                P3 = PH[p+1,q]
                P4 = PH[p,q-1]
                Pr = np.random.rand(1)
                if (P1==P2)and(P2==P3)and(P3==P4)and(Pr<=0.5):
                    if PH[p,q] == PH[p-1,q]+pho:
                        PH[p,q] = PH[p-1,q]-pho
                    else:
                        PH[p,q] = PH[p-1,q]+pho
                    Dj = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(np.exp(1j*PH))))*No
                    MASIRj = np.amax(np.absolute(Dj)**2)/np.mean(np.absolute(Dj)**2)
                    if MASIRj > MASIRo:
                        if PH[p,q] == PH[p-1,q]+pho:
                            PH[p,q] = PH[p-1,q]-pho
                        else:
                            PH[p,q] = PH[p-1,q]+pho
                    else:
                        MASIRo = MASIRj
        if MASIRo>=TMP:
            break
        TMP = MASIRo
        kk = kk+1
    return PH,MASIRo

def f_ODDWYopt(f,di,q1,q2,K,cont):
    fds = f*di
    N1 = np.shape(fds)[0]
    FD = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(fds)))*N1
    PAVRdes= K*np.amax(np.absolute(FD[q1:q2,q1:q2])**2)/np.mean(np.absolute(FD[q1:q2,q1:q2])**2)
    for k in range(cont):
        ABS_wind = np.absolute(FD[q1:q2,q1:q2])
        PH_wind = np.angle(FD[q1:q2,q1:q2])
        FD_clip = np.sqrt(PAVRdes*np.mean(ABS_wind**2))
        X, Y = np.nonzero(ABS_wind>FD_clip)
        ABS_wind[X,Y]=FD_clip
        FDj =np.zeros((N1,N1),dtype=complex)
        FDj[q1:q2,q1:q2]=ABS_wind*np.exp(1j*PH_wind)
        fdj = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(FDj)))/N1
        PHj = np.angle(fdj)
        X_fdj = np.absolute(f)*np.exp(1j*PHj)
        FD = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(X_fdj)))*N1
        PAVRf= np.amax(np.absolute(FD[q1:q2,q1:q2])**2)/np.mean(np.absolute(FD[q1:q2,q1:q2])**2)
    phase_ODD = PHj
    amp_ODD = np.absolute(fdj)
    #uiwait(msgbox('fin optimisation'));
    return phase_ODD,amp_ODD,PAVRf

def f_ODDWY(f,di,q1,q2,cont):
    fds = f*di
    N1 = np.shape(fds)[0]
    FD = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(fds)))*N1
    MASK = np.zeros((N1,N1))
    MASK[q1:q2,q1:q2]=1
    for k in range(cont):
        FDj=FD*MASK
        fdj = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(FDj)))/N1
        PHj = np.angle(fdj)
        X_fdj = np.absolute(f)*np.exp(1j*PHj)
        FD = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(X_fdj)))*N1
        PAVRf= np.mean(np.absolute(FD[q1:q2,q1:q2])**2)/np.amax(np.absolute(FD[q1:q2,q1:q2])**2)
    phase_ODD = PHj
    amp_ODD = np.absolute(fdj)
    return phase_ODD,amp_ODD,PAVRf

def f_nsd(f,b1,b2):
    I = np.absolute(f[b1:b2,b1:b2])**2
    D = np.sqrt((sum(sum((I-np.mean(I))**2)))**2)/(sum(sum(I)))
    return D

def f_nmse(fo,g,p1,p2):
    Wg = g[p1:p2,p1:p2]
    Wfo =fo[p1:p2,p1:p2]
    N=np.shape(Wfo)[0]
    b1 = np.sqrt(N**2/sum(sum(np.absolute(Wg)**2)))
    b2 = np.sqrt(N**2/sum(sum(np.absolute(Wfo)**2)))
    E = np.mean((np.absolute(b2*Wfo)-np.absolute(b1*Wg))**2)
    return E

def f_msen(fo,g,p1x,p2x,p1y,p2y):
    Wg = g[p1x:p2x,p1y:p2y]
    Wfo =fo[p1x:p2x,p1y:p2y]
    N=np.shape(Wfo)[0]
    b1 = np.sqrt(N**2/sum(sum(np.absolute(Wg)**2)))
    b2 = np.sqrt(N**2/sum(sum(np.absolute(Wfo)**2)))
    E = np.mean((np.absolute(b2*Wfo)-np.absolute(b1*Wg))**2)
    return E

def f_mse(fo,g,p1,p2):
    Z = np.shape(fo)
    M = Z[0]
    N = Z[1]
    E = (np.sqrt(sum(sum((np.absolute(g[p1:p2,p1:p2])-np.absolute(fo))**2))))/(M*N)
    return E

def f_laplacianregularity(f,delta,p1,p2):
    f = f[p1:p2,p1:p2]
    N = f.shape[0]
    M = N+2
    T = np.zeros((M,M))
    T[1:M-1,1:M-1]=f
    L=np.zeros((N+2,N+2))
    for m in range(1,M-1):
        for n in range(1,M-1):
            L[m,n] = (1/delta**2)*(T[m+1,n] + T[m,n+1] + T[m-1,n] + T[m,n-1] +  4*T[m,n])
    L=L[1:M-1,1:M-1]
    return L

def f_efficiency(f,p1,p2):
    ED = 100*sum(sum(np.absolute(f[p1:p2,p1:p2])**2))/sum(sum(np.absolute(f)**2))
    return ED
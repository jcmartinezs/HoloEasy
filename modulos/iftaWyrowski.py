#==========================================================  configrar las variables de sistema para la ruta
#--CALCULO DE COMPONENTES OPTICOS DIFRACTIVOS DE FOURIER
#--METODO: ALGORITMO DE TRANSFORMACIONES DE FOURIER ITERATIVAS 
#===============================Por Alberto Patino-Vanegas

import numpy as np
import cv2
import math
from decimal import Decimal
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import os
import StringIO
import urllib, base64

class Resultado(): 
    imagen1 = "" 
    imagen2 = "" 
    imagen3 = "" 
    imagen4 = "" 
    imagen5 = ""
    
def prueba():
    resultado = Resultado()
    resultado.imagen1 = "a"
    resultado.imagen2 = "b"
    resultado.imagen3 = "c"
    resultado.imagen4 = "d"
    resultado.imagen5 = "e"
    return resultado
#ubsuisutb.pgm,butterfly.jpg

def algoritmo_iftawyrowski(iteracion=20,T=0.9,CODEDOUX=0,ruta="./tmp/butterfly1.jpg"):
    resultado = Resultado()
    #====================================
    #---PARAMETROS DEL ALGORITMO
    #====================================
    #iteracion = 100 #  numero de iteraciones en cada paso
    #--parametros de regularizacion
    #T    = 0.9 # entre 0 y 1: mas valor menos ruido dentro de la ventana pero menor eficiencia de difraccion.
    #---------------
    #CODEDOUX = 0 #tipo de codigo (codigo suave=1, codigo fuerte=0)
    #============================================================
    #---objeto a realizarle el holograma
    #===========================================================
    #OBJ = cv2.imread('C:\Users\Lenierd\Documents\Algoritmo\ubsuisutb.pgm').astype(float)
    OBJ = cv2.imread(ruta,0).astype(float)
    OBJ = OBJ[:,:] # si tiene tres planos solo se toma 1

    #plt.figure(1)
    #plt.imshow(OBJ)
    #plt.axis('off')
    #fig = plt.gcf()
    #imgdata = StringIO.StringIO()
    #fig.savefig(imgdata, format='png')
    #imgdata.seek(0)  # rewind the data
    #resultado.imagen1 = 'data:image/png;base64,' + urllib.quote(base64.b64encode(imgdata.buf))
    
    #resultado.imagen1 = base64.b64encode(Image.fromarray(OBJ))

    #=====================================
    N = np.shape(OBJ) # tamano del objeto
    Nx,Ny = N[0],N[1]
    Mx,My = 4*Nx,4*Ny
    #=====================================
    #---FASE INICIAL
    PH = 2*math.pi*np.random.rand(Nx,Ny)-math.pi

    #plt.figure(2)
    #plt.imshow(PH, cmap = cm.Greys_r)
    #plt.axis('off')
    #fig = plt.gcf()
    #imgdata = StringIO.StringIO()
    #fig.savefig(imgdata, format='png')
    #imgdata.seek(0)  # rewind the data
    #resultado.imagen2 = 'data:image/png;base64,' + urllib.quote(base64.b64encode(imgdata.buf))
    
    #=====================================================
    #---COORDENADAS DEL OBJETO DENTRO DEL PLANO DE ENTRADA
    #=====================================================
    TMP1x,TMP2x = Nx % 2,Mx % 2
    p1x = (Mx-TMP2x)/2-(Nx-TMP1x)/2
    p2x = p1x+Nx
    
    TMP1y,TMP2y = Ny % 2,My % 2
    p1y = (My-TMP2y)/2-(Ny-TMP1y)/2
    p2y = p1y+Ny
    #==================================================================
    #---normalizar energia del objeto de acuerdo al tamano holograma
    #==================================================================
    Co = math.sqrt(Mx*My/sum(sum(np.power(np.absolute(OBJ),2))))
    fs = Co*np.absolute(OBJ)
    #============================
    #---PLANO INICIAL
    #============================
    goi = np.zeros(shape=(Mx,My))
    goi[p1x:p2x,p1y:p2y] = Co*fs*np.exp(1j*PH)
    for k in range(iteracion):
        Gj = np.fft.fftshift(goi)
        Gj = np.fft.ifft2(Gj)
        Gj = np.fft.fftshift(Gj)
        Gj = Gj*np.sqrt(Mx*My)
        U_Gj = np.exp(1j*np.angle(Gj))
        gj = np.fft.fftshift(U_Gj)
        gj = np.fft.fft2(gj)
        gj = np.fft.fftshift(gj)
        gj = gj/np.sqrt(Mx*My)
        Bj = np.sqrt(sum(sum(abs(gj[p1x:p2x,p1y:p2y])**2))/sum(sum(abs(fs)**2)))#bien + phase spherique
        Cj = sum(sum(abs(Bj*fs)*abs(gj[p1x:p2x,p1y:p2y])))/sum(sum(abs(Bj*fs)**2))
        gj2 = T*gj
        gj2[p1x:p2x,p1y:p2y] = Cj*fs*np.exp(1j*np.angle(gj[p1x:p2x,p1y:p2y]))
        goi = gj2
    plt.imshow(abs(goi), cmap = cm.Greys_r)
    plt.axis('off')
    fig = plt.gcf()
    imgdata = StringIO.StringIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)  # rewind the data
    resultado.imagen3 = 'data:image/png;base64,' + urllib.quote(base64.b64encode(imgdata.buf))
    HOLO = np.angle(Gj)
    plt.figure(1)
    plt.imshow(HOLO, cmap = cm.Greys_r)
    plt.axis('off')
    fig = plt.gcf()
    imgdata = StringIO.StringIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)  # rewind the data
    resultado.imagen4 = 'data:image/png;base64,' + urllib.quote(base64.b64encode(imgdata.buf))
    #---VERIFICACION 
    h = np.exp(1j*HOLO) #--Simulacion del EOD de fase una vez fabricado. 
    gj = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(h)))/np.sqrt(Mx*My) #--simulacion de lo que se obtiene por difraccion de Fraunhofer (una distancia grande en comparacion con las dimensiones del holograma) 
    #18figure
    #imagen_gj = abs(gj)**2 #--imagen de lo que se obtiene con el holograma calculado
    plt.figure(2)
    plt.imshow(abs(gj)**2, cmap = cm.Greys_r)
    plt.axis('off')
    fig = plt.gcf()
    imgdata = StringIO.StringIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)  # rewind the data
    resultado.imagen5 = 'data:image/png;base64,' + urllib.quote(base64.b64encode(imgdata.buf))
    
    
    plt.show()
    
    return resultado


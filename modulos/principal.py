#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.backends
matplotlib.use('Agg')

import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np
import StringIO, io
import urllib, base64, json

from PIL import Image
from math import pi
from funciones import f_uniformity, f_snr,f_nsd,f_nmse,f_efficiency,f_zeronoise
from Modelo import Modelo
from Iluminacion import Iluminacion
from Voir import Voir
from Analogique import Analogique
from Cuantificar import Cuantificar
from Difusor import Difusor
from SignalReconstruir import SignalReconstruir
from Correo import Correo

def extensiones():
    _ext = ['eps', 'jpeg', 'jpg', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg', 'svgz', 'tif', 'tiff']
    return _ext

def im2double(im):
    min_val = np.min(im.ravel())
    max_val = np.max(im.ravel())
    out = (im.astype('float') - min_val) / (max_val - min_val)
    return out

def faseInicial(obj, id):
    conn = Modelo()
    conn.guardarEvento("%s begin_faseInicial" % str(id))
    result = conn.actualizarSenal(obj, id)
    conn.guardarEvento("%s end_faseInicial" % str(id))
    return result

def CtrlCalculerOID(id):
    conn = Modelo()
    obj = conn.obtenerDatosSenal(id)
    dif = Difusor(obj['phase'],obj['phaseinitial'])
    dif.controlbande = obj['controlbande']
    dif.diffphase = obj['diffphase']

    conn.guardarEvento("%s begin_calculerOID" % str(id))
    PH,MASIR,obj['ffsin'],obj['TFOID'] = dif.calculerOID(obj['Nobj'])
    conn.guardarEvento("%s end_calculerOID" % str(id))
    
    obj['ODD'],obj['OID']=PH,PH
    obj['masiroid'],obj['masirREF'],obj['s1'],obj['s2'] =MASIR,MASIR,dif.s1,dif.s2
    result = {}
    result['id_oid'] = conn.SaveCalculerOID(obj, id)
    return result


def CtrlOptimizerODD(id):
    conn = Modelo()
    obj = conn.getCalculerDiffuseurOptimiser(id)
    dif = Difusor(obj['phase'],obj['phaseinitial'])
    dif.optimiserODD = obj['optimiserODD']
    dif.iterODD = obj['iterODD']

    result = {}
    if obj['phase'] != 'phasealea' and obj['phaseinitial'] != 'pasbandelimite':
        conn.guardarEvento("%s begin_optimizerODD" % str(id))
        obj['DSdiff'], obj['masirODD'], obj['ODD'], obj['FD'] = dif.optimizerODD(obj['fo'],obj['OID'],obj['MASIRdes'],int(obj['s1']),int(obj['s2']),int(obj['r1']),int(obj['r2']))
        conn.guardarEvento("%s end_optimizerODD" % str(id))
        result['filas'] = conn.UpdateoptimizerODD(obj, id)
    else:
        result['filas'] = 0
    return result
    

def CtrlAnalogiqueIlumination(id):
    conn = Modelo()
    ilum = Iluminacion()
    obj = conn.obtenerIluminacion(id)

    conn.guardarEvento("%s begin_analogique_ilumination" % str(id))
    obj['ILUM'],obj['sg'] = ilum.analogique_ilumination(obj['tipoilum'],obj['ODD'],int(obj['taillesignal']),int(obj['tailleholo']))
    conn.guardarEvento("%s end_analogique_ilumination" % str(id))
    
    id_holo = conn.SaveAnalogiqueIlumination(obj,id)
    result = {'id_holo' : id_holo}
    return result

   
def CtrlAnalogiqueVoir(id):
    conn = Modelo()
    voir = Voir()
    obj = conn.obtenerDataVoir(id)

    conn.guardarEvento("%s begin_analogique_voir" % str(id))
    voir.analogique_voir(obj['fo'], obj['ODD'], int(obj['taillesignal']), int(obj['tailleholo']), int(obj['r1']), int(obj['r2']), obj['tipoilum'])
    conn.guardarEvento("%s end_analogique_voir" % str(id))

    result = {'error' : False }
    return result

def CtrlAnalogiqueOptimiser(id):
    conn = Modelo()
    obj = conn.obtenerDataOptimizar(id)
    opt = Analogique(obj['ILUM'],int(obj['iteropt']),int(obj['tailleimg']),int(obj['taillesignal']),int(obj['tailleholo']),int(obj['pixelmargin']))

    conn.guardarEvento("%s begin_optimiser" % str(id))
    obj['fon'],obj['go'],obj['p1'],obj['p2'],obj['q1'],obj['q2'],obj['b1'],obj['b2'],obj['U_Gj'],obj['gj'] = opt.optimiser(obj['optimiser'],obj['fo'], obj['ODD'],obj['r1'],obj['r2'],obj['lissage2'])
    conn.guardarEvento("%s end_optimiser" % str(id))
    
    filas = conn.UpdateHologramaOptimiser(obj, id)
    result = { 'filas' : filas }
    return result


def CtrlAnalogiqueCalculer(id):
    conn = Modelo()
    obj = conn.obtenerDataCalculer(id)
    calc = Analogique(obj['ILUM'],int(obj['iteropt']),int(obj['tailleimg']),int(obj['taillesignal']),int(obj['tailleholo']),int(obj['pixelmargin']))
    calc.DPRA,calc.PRs,calc.PRb, calc.DPLRA, calc.DPE,calc.CODEDOUX = obj['DPRA'],obj['PRs'],obj['PRb'],obj['DPLRA'],obj['DPE'],obj['code']

    conn.guardarEvento("%s begin_AnalogiqueCalculer" % str(id))
    obj['gj'],obj['gj2'],obj['MASKholo'],obj['U_Gj'],obj['M'],obj['B'], obj['holoa'] = calc.calculer(obj,obj['fon'],obj['go'],obj['iteranalogo'],obj['p1'], obj['p2'], obj['q1'], obj['q2'], obj['b1'], obj['b2'])
    conn.guardarEvento("%s end_AnalogiqueCalculer" % str(id))
    
    obj['CEA'], obj['CEDA']  = calc.CEA, calc.CEDA
    obj['CRSBA'], obj['CUa'] = calc.CRSBA,calc.CUa
    obj['RSBa'], obj['RSBA'] = calc.RSBA,calc.RSBA
    obj['EA'], obj['EDA']    = calc.EA,calc.EDA

    obj['erreura']  = f_nmse(obj['go'], obj['gj'], int(obj['p1']), int(obj['p2']))
    obj['EDa'] = f_snr(obj['go'], obj['gj'], int(obj['p1']), int(obj['p2']))
    obj['EDA'] = f_efficiency(obj['gj'], int(obj['b1']), int(obj['b2']))
    UA  = f_uniformity(obj['gj'], int(obj['b1']), int(obj['b2']))
    obj['uniforma'], obj['UA'] = UA, UA
    obj['zerobruita']  = f_zeronoise(obj['gj'], int(obj['p1']), int(obj['p2']), int(obj['b1']), int(obj['b2']))
    obj['deviationstda']  = f_nsd(obj['gj'], int(obj['p1']), int(obj['p2']))

    filas = conn.UpdateAnalogiqueCalculer(obj,id)
    result = { 'filas' : filas, 
    'enlaceReconstruir' : obtenerUrls(id,'analogico','reconstruir'),
    'enlaceHolograma' : obtenerUrls(id,'analogico','holograma'),
    'analogicoDs' : round(obj['deviationstda'], 4),
    'analogicoZb' : round(obj['zerobruita'], 4),
    'analogicoU'  : round(UA, 4),
    'analogicoRsb': round(obj['EDa'], 4),
    'analogicoEd' : round(obj['EDA'], 4),
    'analogicoEqm': round(obj['erreura'], 4)
    }
    """
    obj['erreura'] = EA
    obj['EDa'] = EDA
    obj['RSBa'] = RSBA
    obj['uniforma'] = UA
    obj['zerobruita'] = ZNA
    obj['deviationstda'] = SDA
    """
    result['holograma'] = guardarImagen(np.angle(obj['holoa']),'analogique_calculer_imagen4')
    result['reconstruccion'] = guardarImagen(np.absolute(obj['gj'])**2,'analogique_calculer_imagen5')
    directorio = conn.rutaArchivos(id)

    imagenData64(np.angle(obj['U_Gj']),conn.concatenarDirectorioConArchivo(directorio,'imagen4'))
    imagenData64(np.absolute(obj['gj'])**2,conn.concatenarDirectorioConArchivo(directorio,'imagen5'))
    return result

def obtenerUrls(id,tipo,opt):
    urls = []
    for ext in extensiones():
        urls.append({'url':"/download/{0}/{1}/{2}/{3}".format(str(id),ext,tipo,opt),'tipo':str.upper(ext)})
    return urls


    
def rec3da(handles):
    print('rec3da')

def imagenData64(array,ruta,ejes='off',formato='png'):
    plt.axis(ejes)
    plt.imsave(ruta, array, cmap=plt.cm.gray)

def guardarImagen(imagen,titulo,ejes='off',formato='png'):
    plt.figure(titulo)
    plt.imshow(imagen, cmap = plt.cm.Greys_r)
    plt.axis(ejes)
    fig = plt.gcf()
    imgdata = StringIO.StringIO()
    fig.savefig(imgdata, format=formato)
    imgdata.seek(0)  # rewind the data
    return 'data:image/png;base64,' + urllib.quote(base64.b64encode(imgdata.buf))

def CtrlQuantifieCalculer(id):
    conn = Modelo()
    obj = conn.obtenerDataOptizer(id)
    quant = Cuantificar(obj['ILUM'],obj['tailleimg'],obj['taillesignal'],obj['pixelmargin'],obj['MASKholo'])
    quant.DPRA,quant.PRs,quant.PRb, quant.DPLRA, quant.DPE,quant.iterquantization,quant.CODEDOUX,quant.NIVELES = obj['DPRA'],obj['PRs'],obj['PRb'],obj['DPLRA'],obj['DPE'],obj['iterquantization'],obj['code'],obj['niveaux']

    conn.guardarEvento("%s begin_quantifieCalculer" % str(id))
    obj['recholoef'],obj['Q_Gj'],obj['Gj'],obj['recq'],obj['holoef'] = quant.calculer(obj['fon'], obj['U_Gj'], obj['go'],int(obj['M']), int(obj['p1']), int(obj['p2']), int(obj['q1']), int(obj['q2']))
    conn.guardarEvento("%s end_quantifieCalculer" % str(id))
    
    obj['erreurq'],obj['EQ'] = quant.EQ,quant.EQ
    obj['EDQ'],obj['EDq'],obj['UQ'] = quant.EDQ,quant.EDQ,quant.UQ
    obj['RSBq'],obj['RSBQ'] = quant.RSBQ,quant.RSBQ
    obj['uniformq'],obj['zerobruitq'],obj['deviationstdq'] = quant.UQ,quant.ZNQ,quant.SDQ
    obj['COURBE_EQ'],obj['COURBE_EDQ'],obj['COURBE_RSBQ'],obj['CUQ'] = quant.COURBE_EQ,quant.COURBE_EDQ,quant.COURBE_RSBQ,quant.CUQ


    filas = conn.SaveQuantifieCalculer(obj,id)
    result = { 'id_holo' : filas , 
    'enlaceReconstruir' : obtenerUrls(id,'cuantificado','reconstruir'),
    'enlaceHolograma' : obtenerUrls(id,'cuantificado','holograma'),
    'cuantificadoDs' : round(quant.SDQ, 4),
    'cuantificadoZb' :round(quant.ZNQ, 4),
    'cuantificadoU'  :round(quant.UQ, 4),
    'cuantificadoRsb':round(quant.RSBQ, 4),
    'cuantificadoEd' :round(quant.EDQ, 4),
    'cuantificadoEqm':round(quant.EQ, 4) }
    DIFUSOR = np.angle(obj['holoef'])
    HOLO = (DIFUSOR+pi)/(2*pi)
    HOLO[HOLO==1]=0
    HOLO = (256*HOLO)/255

    result['imagen6'] = guardarImagen(np.angle(obj['Q_Gj']),'imagen6')
    result['reconstruccion'] = guardarImagen(np.absolute(obj['recq'])**2,'imagen7')
    result['holograma'] = guardarImagen(HOLO,'holograma')
    """
    obj['erreurq'] = EQ
    obj['EDq'] = EDQ
    obj['RSBq'] = RSBQ
    obj['uniformq'] = UQ
    obj['zerobruitq'] = ZNQ    
    obj['deviationstdq'] = SDQ
    """
    directorio = conn.rutaArchivos(id)
    imagenData64(np.angle(obj['Q_Gj']),conn.concatenarDirectorioConArchivo(directorio,'imagen6'))
    imagenData64(np.absolute(obj['recq'])**2,conn.concatenarDirectorioConArchivo(directorio,'imagen7'))
    imagenData64(HOLO,conn.concatenarDirectorioConArchivo(directorio,'holograma'))

    return result

def Base64Encode(ndarray):
    return json.dumps([str(ndarray.dtype),base64.b64encode(ndarray),ndarray.shape])

def Base64Decode(jsonDump):
    loaded = json.loads(jsonDump)
    dtype = np.dtype(loaded[0])
    arr = np.frombuffer(base64.decodestring(loaded[1]),dtype)
    if len(loaded) > 2:
        return arr.reshape(loaded[2])
    return arr

def diccionarioajson(obj):
    aux = {};
    for clave, valor in obj.items():
        if(type(valor) == np.ndarray):
            nuevo = Base64Encode(valor)
            aux[clave] = nuevo
        else:
            aux[clave]=valor
    return aux

def CtrlSignalareconstruire(obj):
    conn = Modelo()
    result = {'Nobj':0,'id_proceso':0,'imagen':''}
    id = conn.guardarHolograma(1)
    if(id > 0):
        conn.guardarEvento("%s begin_signal" % str(id))
        signalareconstruire(obj)
        conn.guardarEvento("%s end_signal" % str(id))
        conn.guardarSenalAReconstruir(obj, id)
        result['id_proceso'] = id
        result['Nobj'] = obj['Nobj']
        result['imagen'] = guardarImagen(obj['fo'],'imagen')
    return result

def signalareconstruire(obj):
    signal = SignalReconstruir()
    obj['img'], obj['fo'],obj['Nimg'],obj['Nimgx'],obj['Nimgy'],obj['Nobj'],obj['Nobjx'],obj['Nobjy'],obj['r1x'],obj['r2x'],obj['r1y'],obj['r2y'] = signal.procesar(obj['ruta'],obj['pixelmargin'])
    obj['tailleobject'] = obj['Nobj']
    obj['tailleimg'] = obj['Nimg']


def CtrlObtenerObjeto(tipoArchivo,tipoHolograma,tipoObjeto,id):
    objeto = ObtenerObjetoImagen(tipoHolograma,tipoObjeto,id)
    if objeto is not None:
        buf = io.BytesIO()
        plt.imshow(objeto, cmap = plt.cm.Greys_r)
        plt.axis('off')
        plt.savefig(buf, format=tipoArchivo)
        buf.seek(0)
        return buf.getvalue()
    return objeto

def ObtenerObjetoImagen(tipoHolograma,tipoObjeto,id):
    if tipoHolograma == 'cuantificado':
        return ObtenerCuantificado(tipoObjeto,id)
    if tipoHolograma == 'analogico':
        return ObtenerAnalogico(tipoObjeto,id)
    return ObtenerImagen(id)

def ObtenerCuantificado(tipo,id):
    conn = Modelo()
    if tipo == 'holograma':
        objeto = conn.ObtenerCuantificado(id)
        if objeto is not None:
            DIFUSOR = np.angle(objeto)
            HOLO = (DIFUSOR+pi)/(2*pi)
            HOLO[HOLO==1]=0
            HOLO = (256*HOLO)/255
            return HOLO
    else:
        U_Gj, ILUM, recholoef = conn.ObtenerReconstrucion(id)
        if recholoef is not None:
            REC = np.absolute(recholoef)**2/np.amax(np.absolute(recholoef)**2)
            return REC
    return None

def ObtenerAnalogico(tipo,id):
    conn = Modelo()
    if tipo == 'holograma':
        objeto = conn.ObtenerAnalogico(id)
        if objeto is not None:
            return (np.angle(objeto)+pi)/(2*pi)
    else:
        U_Gj, ILUM, recholoef = conn.ObtenerReconstrucion(id)
        if U_Gj is not None and ILUM is not None:
            DIFUSOR = U_Gj
            REC = DIFUSOR.shape[0]*np.fft.fftshift(np.fft.fft2(np.fft.fftshift(DIFUSOR*ILUM)))
            REC = np.absolute(REC)**2/np.amax(np.absolute(REC)**2)
            return REC
    return None

def ObtenerReconstrucion(id):
    conn = Modelo()
    U_Gj, ILUM, recholoef = conn.ObtenerReconstrucion(id)
    return conn.ObtenerReconstrucion(id)

def ObtenerImagen(id):
    conn = Modelo()
    return conn.ObtenerImagen(id)
    
def courbes(obj):
    if obj['tipo'] == 'q':
        FIL, COL = obj['array'].shape
        for m in range(FIL):
            plt.plot(np.arange(0,COL),obj['array'][m,:],'r.',np.arange(0,COL),obj['array'][m,:])
    else:
        plt.plot(obj['array'],'.')
    plt.grid(True)
    #plt.show()
    fig = plt.gcf()
    imgdata = StringIO.StringIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)  # rewind the data
    obj['imagen10'] = 'data:image/png;base64,' + urllib.quote(base64.b64encode(imgdata.buf))

def generarArchivo(tipo,tipoArchivo,datos):
    obj = {}
    if tipo == 'C':
        DIFUSOR = np.angle(datos)
        HOLO = (DIFUSOR+pi)/(2*pi)
        HOLO[HOLO==1]=0
        HOLO = (256*HOLO)/255
        plt.imshow(np.angle(HOLO), cmap = plt.cm.Greys_r)   
        DIFUSOR = np.angle(holoef) 
    else:
        DIFUSOR = datos;
        HOLO = (np.angle(DIFUSOR)+pi)/(2*pi);
        plt.imshow(np.angle(HOLO), cmap = plt.cm.Greys_r) 
    plt.axis('off')
    plt.show()
    fig = plt.gcf()
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format=tipoArchivo)
    fig.savefig('imagen_test.png')
    imgdata.seek(0)  # rewind the data
    return imgdata.getvalue()


def CtrlEnviarCorreo(name, email, message):
    conn = Modelo()
    send = Correo()
    conn.GuardarCorreo(name, email, message)
    send.enviarCorreo(name, email, message)
    return "ok"

def getFileName(argument):
    switcher = {
        'png': 'holoeasy-file.png',
        'gif': 'holoeasy-file.gif',
        'pgm': 'holoeasy-file.pgm',
        'tif': 'holoeasy-file.tif',
        'tiff': 'holoeasy-file.tiff',
        'wbmp': 'holoeasy-file.wbmp',
        'xbm': 'holoeasy-file.xbm',
        'xif': 'holoeasy-file.xif',
        'xpm': 'holoeasy-file.xpm',
        'xwd': 'holoeasy-file.xwd',
        'art': 'holoeasy-file.art',
        'bmp': 'holoeasy-file.bmp',
        'dwg': 'holoeasy-file.dwg',
        'dxf': 'holoeasy-file.dxf',
        'fif': 'holoeasy-file.fif',
        'flo': 'holoeasy-file.flo',
        'eps': 'holoeasy-file.eps',
        'jpeg': 'holoeasy-file.jpeg',
        'jpg': 'holoeasy-file.jpg',
        'pdf': 'holoeasy-file.pdf',
        'pgf': 'holoeasy-file.pgf',
        'ps': 'holoeasy-file.ps',
        'raw': 'holoeasy-file.raw',
        'rgb': 'holoeasy-file.rgb'
    }
    return switcher.get(argument, "holoeasy-file")

def getMimeType(argument):
    switcher = {
        'png': 'image/png',
        'gif': 'image/gif',
        'pgm': 'image/x-portable-graymap',
        'tif': 'image/tiff',
        'tiff': 'image/x-tiff',
        'wbmp': 'image/vnd.wap.wbmp',
        'xbm': 'image/x-xbitmap',
        'xif': 'image/vnd.xiff',
        'xpm': 'image/x-xpixmap',
        'xwd': 'image/x-xwindowdump',
        'art': 'image/x-jg',
        'bmp': 'image/bmp',
        'dwg': 'image/vnd.dwg',
        'dxf': 'image/x-dwg',
        'fif': 'image/fif',
        'flo': 'image/florian',
        'eps': 'application/postscript',
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'pdf': 'application/pdf',
        'pgf': 'application/octet-stream',
        'ps': 'application/postscript',
        'raw': 'application/octet-stream',
        'rgb': 'image/x-rgb'
    }
    return switcher.get(argument, "nothing")


def funcionprincipal(obj):
    result = CtrlSignalareconstruire(obj)
    faseInicial(obj,result['id_proceso'])
    CtrlCalculerOID(result['id_proceso'])
    CtrlOptimizerODD(result['id_proceso'])
    CtrlAnalogiqueIlumination(result['id_proceso'])
    CtrlAnalogiqueVoir(result['id_proceso'])
    CtrlAnalogiqueOptimiser(result['id_proceso'])
    CtrlAnalogiqueCalculer(result['id_proceso'])
    CtrlQuantifieCalculer(result['id_proceso'])
    plt.show()    


    

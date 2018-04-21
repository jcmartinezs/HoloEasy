# -*- encoding: utf-8 -*- 

from flask import request
from werkzeug import secure_filename
import os

ALLOWED_EXTENSIONS = set(['pgm', 'png', 'jpg', 'jpeg', 'gif'])
BANDAS = set(['bandelimitee','pasbandelimite'])
PHASES = set(['phasealea','phaheur','phawyr','phaspher'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def ValidatorImagenAReconstruir(UPLOAD_FOLDER):
    obj = { 'tipoimg' : 'file' }# d.has_key(3)
    mensaje = 'Todos los campos estan bien'
    if(request.files.has_key('OBJ')):
        archivo = request.files['OBJ']
        if archivo and allowed_file(archivo.filename):# Check if the file is one of the allowed types/extensions
            filename = secure_filename(archivo.filename)
            # Move the file form the temporal folder to the upload folder we setup
            ruta = os.path.join(UPLOAD_FOLDER, filename)
            archivo.save(ruta)
            obj['ruta'] = ruta
            accion = True
        else:
            return obj, True, 'archivo no permitido'
    else:
        return obj, True, 'No ha cargado un archivo'

    if request.form['pixelmargin']:
        obj['marg'] = int(request.form['pixelmargin'])
        obj['pixelmargin'] = int(request.form['pixelmargin'])
    else: 
        return obj, True, 'No esta definido el tipo de margen entre pixel'
    obj['tailleimg'] = 0
    obj['phase'] = request.form['fase'] if request.form.has_key('fase') else 'phaheur'
    obj['cuantificar'] = request.form['cuantificar'] if request.form.has_key('cuantificar') else 'SI'
    #phaseinitial
    obj['phaseinitial'] = request.form['fase_inicial'] if request.form.has_key('fase_inicial') else 'bandelimitee'
    #iterquantization,iteranalog
    obj['iteraccion'] = int(request.form['iteraccion']) if request.form.has_key('iteraccion') else 20
    #controlbande
    obj['control_banda'] = float(request.form['control_banda']) if request.form.has_key('control_banda') else 0.01
    #diffphase
    obj['diffphase'] = float(request.form['diffphase']) if request.form.has_key('diffphase') else 1.335
    #PRs
    obj['PRs'] = int(request.form['PRs']) if request.form.has_key('PRs') else 1
    #PRb
    obj['PRb'] = int(request.form['PRb']) if request.form.has_key('PRb') else 0
    #DPRA
    obj['DPRA'] = int(request.form['DPRA']) if request.form.has_key('DPRA') else 1
    #DPLRA
    obj['DPLRA'] = int(request.form['DPLRA']) if request.form.has_key('DPLRA') else 0
    #DPE
    obj['DPE'] = int(request.form['DPE']) if request.form.has_key('DPE') else 0
    #niveaux
    obj['nivel'] = int(request.form['nivel']) if request.form.has_key('nivel') else 4
    #MASIRdes
    obj['MASIRdes'] = float(request.form['MASIRdes']) if request.form.has_key('MASIRdes') else 0.8
    #tipoilum
    obj['tipoilum'] = request.form['tipoilum'] if request.form.has_key('tipoilum') else 'carre'
    #taillesignal
    obj['taillesignal'] = int(request.form['taillesignal']) if request.form.has_key('taillesignal') else 128
    #tailleholo
    obj['tailleholo'] = int(request.form['tailleholo']) if request.form.has_key('tailleholo') else 64
    #iterODD
    obj['iterODD'] = int(request.form['iterODD']) if request.form.has_key('iterODD') else 20
    #code
    obj['code'] = request.form['code'] if request.form.has_key('code') else 'codedoux'
    return obj,False, 'Operacion exitosa'

def numeroEnteroValido(numero_str, campo):
    numero = 0
    if numero_str.isdigit():
        numero = int(numero_str)
        if numero <= 0:
            return numero, 'El campo {0} debe ser mayor que cero ({1})'.format(campo, numero_str)   
    else:
        return numero, 'El campo {0} debe ser un numero entero ({1})'.format(campo, numero_str)
    return numero, ''

def is_float(string):

    try:
        return float(str(string)) and '.' in str(string)  
    except ValueError:
        return False

def numeroRealValido(numero_str, campo):
    numero = 0
    if is_float(numero_str):
        numero = float(numero_str)
        if numero < 0:
            return numero, 'El campo {0} debe ser mayor que cero ({1})'.format(campo, numero_str)   
    else:
        return numero, 'El campo {0} debe ser un numero real ({1})'.format(campo, numero_str)
    return numero, ''

def validatorPhaseInitial(data):
    obj = {}
    mensaje = ''
    if (data.has_key('phase') and data.has_key('phaseinitial') and data.has_key('iterODD') and data.has_key('cuantificar') and data.has_key('code') 
        and data.has_key('MASIRdes') and data.has_key('controlbande') and data.has_key('diffphase') and data.has_key('tipoilum') and data.has_key('nivel') 
        and data.has_key('analogo_PRs') and data.has_key('analogo_PRb') and data.has_key('analogo_DPRA') and data.has_key('analogo_DPLRA') and data.has_key('analogo_iteraccion')
        and data.has_key('cuantificar_PRs') and data.has_key('cuantificar_PRb') and data.has_key('cuantificar_DPRA') and data.has_key('cuantificar_DPLRA') and data.has_key('cuantificar_iteraccion')
        and data.has_key('taillesignal') and data.has_key('tailleholo') and data.has_key('id_proceso')):
        obj['phase'] = data['phase']
        obj['phaseinitial'] = data['phaseinitial']#---escoger fase no banda-limitada
        obj['cuantificar'] = data['cuantificar']
        obj['code'] = data['code']
        obj['tipoilum'] = data['tipoilum']
        if obj['phase'] not in PHASES:
            mensaje = '{0}\n{1}'.format(mensaje,'No ha escogido un valor válido para el campo TIPO DE BANDA')
        if obj['phaseinitial'] not in PHASES:
            mensaje = '{0}\n{1}'.format(mensaje,'No ha escogido un valor válido para el campo FASE')
        if data['cuantificar'] not in ('SI','NO'):
            data['cuantificar'] = 'NO'
        if obj['code'] not in ('codedur','codedoux'):
            mensaje = '{0}\n{1}'.format(mensaje,'No ha escogido un valor válido para el campo CODIGO A EMPLEAR')
        if obj['tipoilum'] not in ('carre','circle','gauss'):
            mensaje = '{0}\n{1}'.format(mensaje,'No ha escogido un valor válido para el campo TIPO DE ILUMINACIÓN')
        obj['iterODD'], msg = numeroEnteroValido(data['iterODD'],'iteraciones del difusor')
        if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)
        obj['nivel'], msg = numeroEnteroValido(data['nivel'],'NIVEL')
        if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)
        obj['taillesignal'], msg = numeroEnteroValido(data['taillesignal'],'TAMAÑO SEÑAL')
        if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)
        obj['tailleholo'], msg = numeroEnteroValido(data['tailleholo'],'TAMAÑO HOLOGRAMA')
        print(obj)
        if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)
        obj['MASIRdes'], msg = numeroRealValido(data['MASIRdes'],'MASIR')
        print(obj)
        if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)
        obj['controlbande'], msg = numeroRealValido(data['controlbande'],'CONTROL DE BANDA')
        if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)
        obj['diffphase'], msg = numeroRealValido(data['diffphase'],'DIFERENCIA DE FASE')
        if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)
        obj['analogo_iteraccion'], msg = numeroEnteroValido(data['analogo_iteraccion'],'ITERACIONES ANALOGICAS')
        if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)

        obj['analogo_PRs'], msg = numeroRealValido(data['analogo_PRs'],'PRs')
        if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)
        elif obj['analogo_PRs'] < 0 or obj['analogo_PRs'] > 1:
            mensaje = '{0}\n{1}'.format(mensaje, 'PRs debe ser mayor o igual que cero y menor o igual que uno')

        obj['analogo_PRb'], msg = numeroRealValido(data['analogo_PRb'],'PRb')
        if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)
        elif obj['analogo_PRb'] < 0 or obj['analogo_PRb'] > 1:
            mensaje = '{0}\n{1}'.format(mensaje, 'PRb debe ser mayor o igual que cero y menor o igual que uno')

        obj['analogo_DPRA'], msg = numeroRealValido(data['analogo_DPRA'],'DPRA')
        if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)
        elif obj['analogo_DPRA'] < 0 or obj['analogo_DPRA'] > 1:
            mensaje = '{0}\n{1}'.format(mensaje, 'DPRA debe ser mayor o igual que cero y menor o igual que uno')

        obj['analogo_DPLRA'], msg = numeroRealValido(data['analogo_DPLRA'],'DPLRA')
        if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)
        elif obj['analogo_DPLRA'] < 0 or obj['analogo_DPLRA'] > 1:
            mensaje = '{0}\n{1}'.format(mensaje, 'DPLRA debe ser mayor o igual que cero y menor o igual que uno')
        
        if obj['cuantificar'] == 'SI':
            obj['cuantificar_iteraccion'], msg = numeroEnteroValido(data['cuantificar_iteraccion'],'ITERACIONES ANALOGICAS')
            if len(msg) > 0:
                mensaje = '{0}\n{1}'.format(mensaje, msg)

            obj['cuantificar_PRs'], msg = numeroRealValido(data['cuantificar_PRs'],'PRs')
            if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)
            elif obj['cuantificar_PRs'] < 0 or obj['cuantificar_PRs'] > 1:
                mensaje = '{0}\n{1}'.format(mensaje, 'PRs debe ser mayor o igual que cero y menor o igual que uno')

            obj['cuantificar_PRb'], msg = numeroRealValido(data['cuantificar_PRb'],'PRb')
            if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)
            elif obj['cuantificar_PRb'] < 0 or obj['cuantificar_PRb'] > 1:
                mensaje = '{0}\n{1}'.format(mensaje, 'PRb debe ser mayor o igual que cero y menor o igual que uno')

            obj['cuantificar_DPRA'], msg = numeroRealValido(data['cuantificar_DPRA'],'DPRA')
            if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)
            elif obj['cuantificar_DPRA'] < 0 or obj['cuantificar_DPRA'] > 1:
                mensaje = '{0}\n{1}'.format(mensaje, 'DPRA debe ser mayor o igual que cero y menor o igual que uno')
                
            obj['cuantificar_DPLRA'], msg = numeroRealValido(data['cuantificar_DPLRA'],'DPLRA')
            if len(msg) > 0: mensaje = '{0}\n{1}'.format(mensaje, msg)
            elif obj['cuantificar_DPLRA'] < 0 or obj['cuantificar_DPLRA'] > 1:
                mensaje = '{0}\n{1}'.format(mensaje, 'DPLRA debe ser mayor o igual que cero y menor o igual que uno')
        else:
            obj['cuantificar_iteraccion'], obj['cuantificar_PRs'], obj['cuantificar_PRb'], obj['cuantificar_DPRA'], obj['cuantificar_DPLRA'] = 0, 0, 0, 0, 0
        obj['id_proceso'] = data['id_proceso']
        print(obj)
        return obj, False, 'Operacion exitosa'
    else:
        return obj, True, 'No ha completado todos los datos del formulario'
# -*- encoding: utf-8 -*- 
import logging
from modulos.iftaWyrowski import algoritmo_iftawyrowski
from modulos.principal import CtrlSignalareconstruire, faseInicial, CtrlCalculerOID, CtrlOptimizerODD, CtrlAnalogiqueIlumination, CtrlAnalogiqueVoir, CtrlAnalogiqueOptimiser, CtrlAnalogiqueCalculer, CtrlQuantifieCalculer, diccionarioajson, Base64Decode, courbes, generarArchivo, getFileName, getMimeType,CtrlObtenerObjeto, CtrlEnviarCorreo
from modulos.Excepciones import ExceptionDB, EntradaError, ExceptionData
from modulos import config
from modulos.Validator import ValidatorImagenAReconstruir, validatorPhaseInitial
from flask import Flask, render_template, request, jsonify, make_response, send_file, abort
import os, io, json, sys, MySQLdb


UPLOAD_FOLDER = config.APP_CONFIG['ruta'] + 'tmp'


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['LOGGING_FORMAT'] = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
app.config['LOGGING_LOCATION'] = config.APP_CONFIG['ruta'] + 'bookshelf.log'
app.config['LOGGING_LEVEL'] = logging.DEBUG

handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
handler.setFormatter(formatter)
app.logger.addHandler(handler)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/app')
def appIndex():
    return render_template('app.html')

@app.route('/guia')
def appGuia():
    return render_template('GuiaHoloEasy.html')

@app.route('/documento')
def appDocumento():
    return render_template('GuiaUso.html')

@app.route('/templates/<template_name>', methods=['GET'])
def get_template(template_name):
    return render_template('partials/{}'.format(template_name))

@app.route('/signal_a_reconstruire',methods=['POST'])
def signal_a_reconstruire():
    obj = {}# d.has_key(3)
    mensaje = 'Todos los campos estan bien'
    error = False
    obj,error,mensaje = ValidatorImagenAReconstruir(app.config['UPLOAD_FOLDER'])
    if error is False:
        result = CtrlSignalareconstruire(obj)
        return json.dumps(diccionarioajson(result))
    else:
        raise ExceptionData(mensaje)
    
            
@app.route('/phase_initial', methods = ['POST'])
def phase_initial():
    # Get the parsed contents of the form data
    data = request.json
    obj, error, mensaje = validatorPhaseInitial(data)
    if error is False:
        resultado = {}
        filas = faseInicial(obj, obj['id_proceso'])
        resultado['mensaje'] = "Cambios actualizados correctamente" if filas > 0 else "no hubo cambios por actualizar en el registro"
        resultado['filas'] = filas
        return jsonify(resultado)
    else:
        raise ExceptionData(mensaje)
            
@app.route('/calculer_diffuseur', methods = ['POST'])
def calculer_diffuseur():
    # Get the parsed contents of the form data
    data = request.json
    result = CtrlCalculerOID(data['id_proceso'])
    return json.dumps(diccionarioajson(result))

@app.route('/calculer_diffuseur/optimiser', methods = ['POST'])
def calculer_diffuseur_optimiser():
    # Get the parsed contents of the form data
    data = request.json
    result = CtrlOptimizerODD(data['id_proceso'])
    # Render template
    return json.dumps(diccionarioajson(result))

@app.route('/hologramme_analogique/ilumination', methods = ['POST'])
def hologramme_analogique_ilumination():
    # Get the parsed contents of the form data
    data = request.json
    obj = CtrlAnalogiqueIlumination(data['id_proceso'])
    # Render template
    return json.dumps(diccionarioajson(obj))

@app.route('/hologramme_analogique/voir', methods = ['POST'])
def hologramme_analogique_voir():
    # Get the parsed contents of the form data
    data = request.json
    result = CtrlAnalogiqueVoir(data['id_proceso'])
    # Render template
    return json.dumps(diccionarioajson(result))

@app.route('/hologramme_analogique/optimiser', methods = ['POST'])
def hologramme_analogique_optimiser():
    # Get the parsed contents of the form data
    data = request.json
    obj = CtrlAnalogiqueOptimiser(data['id_proceso'])
    # Render template
    return json.dumps(diccionarioajson(obj))

@app.route('/hologramme_analogique/calculer', methods = ['POST'])
def hologramme_analogique_calculer():
    # Get the parsed contents of the form data
    data = request.json
    obj = CtrlAnalogiqueCalculer(data['id_proceso'])
    return json.dumps(diccionarioajson(obj))

@app.route('/hologramme_quantifie/calculer', methods = ['POST'])
def hologramme_quantifie():
    # Get the parsed contents of the form data
    data = request.json
    obj = CtrlQuantifieCalculer(data['id_proceso'])
    return json.dumps(diccionarioajson(obj))

@app.route('/estadisticas/courbes', methods = ['POST'])
def estadisticas_courbes():
    # Get the parsed contents of the form data
    data = request.json
    obj = {}
    obj['array'] = Base64Decode(data['array'])
    obj['tipo'] = data['tipo']
    courbes(obj)
    # Render template
    return json.dumps(diccionarioajson(obj))

@app.route('/download')
def download():
    csv = """"REVIEW_DATE","AUTHOR","ISBN","DISCOUNTED_PRICE"
"1985/01/21","Douglas Adams",0345391802,5.95
"1990/01/12","Douglas Hofstadter",0465026567,9.95
"1998/07/15","Timothy ""The Parser"" Campbell",0968411304,18.99
"1999/12/03","Richard Friedman",0060630353,5.95
"2004/10/04","Randel Helms",0879755725,4.50"""
    # We need to modify the response, so the first thing we 
    # need to do is create a response out of the CSV string
    response = make_response(csv)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers["Content-Disposition"] = "attachment; filename=books.csv"
    return response

@app.route('/download/<id>/<tipoImagen>/<tipoHolograma>/<tipoObjeto>', methods = ['GET'])
def downloadFile(tipoImagen='png',tipoHolograma='analogico',tipoObjeto='holograma',id=0):
    image_binary = CtrlObtenerObjeto(tipoImagen,tipoHolograma,tipoObjeto,id)
    if image_binary is not None:
        response = make_response(image_binary)
        response.mimetype = getMimeType(tipoImagen)
        return response
    else:
        return abort(404)
    
@app.route('/mail/contact_me',methods=['POST'])
def contactarCorreo():
    return CtrlEnviarCorreo(request.form['name'],request.form['email'],request.form['message'])

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    app.logger.error(str(e))
    return jsonify(error=str(e)), code


@app.errorhandler(ExceptionDB)
def exception_bd_handler(error):
    code = 500
    return jsonify(error="!!!! Error conectando con la base de datos"), code

@app.errorhandler(ExceptionData)
def exception_data_handler(error):
    code = 500
    return jsonify(error=error.mensaje), code

@app.route('/about')
def about():
    app.logger.warning('A warning message is sent.')
    app.logger.error('An error message is sent.')
    app.logger.info('Information: 3 + 2 = %d', 5)
    return "about"

if __name__ == "__main__":
    app.run(threaded=False)

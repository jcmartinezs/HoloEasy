'# -*- coding: utf-8 -*-' 
from sys import path
path.append('C:/xampp/htdocs/HC/')

#   Primer ejemplo de controlador
#def application(environ, start_response): 
#    # Genero la salida HTML a mostrar al usuario 
#    output = "<p>Bienvenido a mi <b>PythonApp</b>!!!</p>" 
#    # Inicio una respuesta al navegador 
#    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')]) 
#    # Retorno el contenido HTML 
#    return output

#from HC.sitioweb import contacto, default 
 
def application(environ, start_response): 
    peticion = environ['REQUEST_URI'] 
 
    if peticion.startswith('/contacto'): 
        output = "<p>Formulario <b>Que me vez</b>!!!</p>" #contacto.formulario() 
    elif peticion.startswith('/gracias'): 
        output = "<p>Gracias <b>Muchas Gracias</b>!!!</p>" #contacto.gracias() 
    else: 
        output = "<p>Bienvenido a mi <b>PythonApp</b>!!!</p>" + peticion  #default.default_page() 
 
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')]) 
    return output

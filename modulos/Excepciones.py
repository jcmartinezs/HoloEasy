#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Error(Exception):
    """Clase base para excepciones en el módulo."""
    pass

class EntradaError(Error):
    """Excepción lanzada por errores en las entradas.

    Atributos:
        expresion -- expresión de entrada en la que ocurre el error
        mensaje -- explicación del error
    """

    def __init__(self, expresion, mensaje):
        self.expresion = expresion
        self.mensaje = mensaje

class ExceptionData(Error):
    """Excepción lanzada por errores en las entradas.

    Atributos:
        expresion -- expresión de entrada en la que ocurre el error
        mensaje -- explicación del error
    """

    def __init__(self, mensaje, info=None):
        self.mensaje = mensaje
        self.info = info

class ExceptionDB(Exception):
    """docstring for ExceptionDB"""
    def __init__(self, mensaje, info=''):
        self.expresion = "No se puede conectar a la base de datos"
        self.mensaje = mensaje
        self.info = info
        
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from Excepciones import ExceptionDB
import datetime
import numpy as np
import cPickle
import os
import sys
import config

class Modelo:
    db_host = config.APP_CONFIG['bd_host']
    usuario = config.APP_CONFIG['bd_usuario']
    clave = config.APP_CONFIG['bd_password']
    base_de_datos = config.APP_CONFIG['bd_nombre']

    def __init__(self):
        try:
            conn = self.conectar()
            conn.close()
        except MySQLdb.Error, e:
            raise ExceptionDB('No se pudo conectar a la base de datos',e)

    def getRutaArchivos(self):
        return config.APP_CONFIG['ruta'] + 'archivos'

    def obtenerRutaArchivosLog(self):
        ruta = self.getRutaArchivos()
        ruta = os.path.join(ruta,'holoeasy.log')
        return ruta        

    def guardarEvento(self,texto):
        fecha_actual = datetime.date.today()
        hora_actual = datetime.datetime.now().time()
        linea = "%s : %s - %s " % (fecha_actual.strftime("%Y-%m-%d"),hora_actual.strftime("%H:%M:%S"),str(texto))
        with open(self.obtenerRutaArchivosLog(), "a") as myfile:
            myfile.write(linea)

    def obtenerRutaArchivos(self, id):
        ruta = self.getRutaArchivos()
        ruta = os.path.join(ruta,str(id))
        return ruta

    def rutaArchivos(self, id):
        ruta = self.obtenerRutaArchivos(id)
        self.carpeta(ruta)
        return ruta

    def nombreObjeto(self, id, clave):
        ruta = self.rutaArchivos(id)
        ruta = os.path.join(ruta,clave)
        return ruta
        
    def obtenerObjeto(self,id,clave):
        ruta = self.nombreObjeto(id,clave)
        file = open(ruta,"r")
        _read = file.read()
        return cPickle.loads(_read)

    def carpeta(self, ruta):
        if not os.path.exists(ruta): os.makedirs(ruta)

    def concatenarDirectorioConArchivo(self,ruta,nombre):
        return os.path.join(ruta,nombre)

    def crearObjeto(self, id, obj, clave):
        ruta = self.rutaArchivos(id)
        ruta = self.concatenarDirectorioConArchivo(ruta,clave)
        self.escribirEnDisco(ruta,cPickle.dumps(obj))

    def escribirEnDisco(self,ruta,array):
        f = open (ruta, "w")
        f.write(array)
        f.close()

    def conectar(self): 
    	conn = MySQLdb.connect(host=self.db_host, user=self.usuario, passwd=self.clave,db=self.base_de_datos)
    	return conn

    def obtenerUltimoConsecutivo(self):
    	ultimo = 0
    	fecha_actual = datetime.date.today()
    	codigo = str(fecha_actual.year)+        str(fecha_actual.month).zfill(2)
    	busqueda_codigo = "SELECT codigo FROM holograma WHERE codigo like '{0}%' ORDER BY codigo DESC LIMIT 1".format(codigo)
    	data = self.ejecutar(busqueda_codigo)
    	if len(data) > 0:
    		numero = data[0][0][6:]
    		ultimo = int(numero)
    	ultimo=ultimo+1
    	return codigo + str(ultimo).zfill(4)

    def guardarHolograma(self,id):
    	codigo = self.obtenerUltimoConsecutivo()
    	fecha_actual = datetime.date.today()
    	hora_actual = datetime.datetime.now().time()
    	add_holo = ('INSERT INTO holograma '
               '(codigo, fecha, hora, id_usuario) '
               'VALUES ({0}, "{1}", "{2}", {3})'.
               format(codigo,fecha_actual.strftime("%Y-%m-%d"),hora_actual.strftime("%H:%M:%S"),id))
    	return self.ejecutar(add_holo)

    def guardarSenalAReconstruir(self, data, id):
    	query = ('INSERT INTO `bd_holoeasy`.`senal_reconstruir` (`id_holograma`, `tam_x`, `tam_y`, `tam_obj_x`, `tam_obj_y`, `r1x`, `r1y`, `r2x`, `r2y`,'
        ' `fase`, `fase_inicial`, `iteraccion`, `control_banda`, `diffphase`, `DPE`, `nivel`, `MASIRdes`, `tipoilum`, '
        ' `taillesignal`, `tailleholo`,`iterODD`, `code`,`cuantificar`, `tam_img`, `tam_obj`, `tailleobject`) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}",'
        ' "{6}", "{7}", "{8}", "{9}", "{10}","{11}","{12}","{13}","{14}","{15}","{16}","{17}","{18}","{19}","{20}","{21}","{22}","{23}","{24}","{25}")'.format(id, 
            data["Nimgx"], data["Nimgy"], data["Nobjx"], data["Nobjy"], data["r1x"], data["r1y"], data["r2x"], data["r2y"],data["phase"],data["phaseinitial"],data["iteraccion"],data["control_banda"],data["diffphase"],
            data["DPE"],data["nivel"],data["MASIRdes"],data["tipoilum"],
            data["taillesignal"],data["tailleholo"],data["iterODD"],data["code"],data['cuantificar'],data["Nimg"],data["Nobj"],data["Nobj"]))
        self.crearObjeto(id,data["fo"],"fo")
        self.crearObjeto(id,data["img"],"img")
    	return self.ejecutar(query)

    def SaveCalculerOID(self, data, id):
        query = ('INSERT INTO `calculo_oid`(`id_holograma`, `masiroid`, `masirREF`, `s1`, `s2`) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}")'.format(id, data["masiroid"], data["masirREF"], data["s1"], data["s2"]))
        id_oid = self.ejecutar(query)
        self.crearObjeto(id,data["ODD"],"ODD")
        self.crearObjeto(id,data["OID"],"OID")
        self.crearObjeto(id,data["ffsin"],"ffsin")
        self.crearObjeto(id,data["TFOID"],"TFOID")
        return id_oid

    def SaveQuantifieCalculer(self, data, id):
        query = ('INSERT INTO `holograma_cuantificado`(`erreurq`, `EDq`, `RSBq`, `uniformq`, '
        '`zerobruitq`, `deviationstdq`, `EQ`, `UQ`, `id_holograma`) VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}",'
        '"{7}","{8}")'.format(data["erreurq"], data["EDq"], data["RSBq"],data["uniformq"], data["zerobruitq"], 
            data["deviationstdq"], data["EQ"],data["UQ"],id))
        self.crearObjeto(id,data["Q_Gj"],"Q_Gj")
        self.crearObjeto(id,data["Gj"],"Gj")
        self.crearObjeto(id,data["COURBE_EQ"],"COURBE_EQ")
        self.crearObjeto(id,data["COURBE_EDQ"],"COURBE_EDQ")
        self.crearObjeto(id,data["COURBE_RSBQ"],"COURBE_RSBQ")
        self.crearObjeto(id,data["CUQ"],"CUQ")
        self.crearObjeto(id,data["recq"],"recq")
        self.crearObjeto(id,data["holoef"],"holoef")
        self.crearObjeto(id,data["recholoef"],"recholoef")
        fila = self.ejecutar(query)
        return fila


    def UpdateoptimizerODD(self, data, id):
        fila = 1
        self.crearObjeto(id,data["DSdiff"],"DSdiff")
        self.crearObjeto(id,data["masirODD"],"masirODD")
        self.crearObjeto(id,data["FD"],"FD")
        return fila

    def SaveAnalogiqueIlumination(self, data, id):
        query = ('INSERT INTO `holograma_analogico`(`id_holograma`, `sg_ilum`, `tipo_ilum`) VALUES ("{0}","{1}","{2}")'.format(id, data["sg"], data["tipoilum"]))
        fila = self.ejecutar(query)
        self.crearObjeto(id,data["ILUM"],"ILUM")
        return fila

    def actualizarSenal(self, data, id):
        #--------------------------
    	queryUpdate = ('UPDATE `bd_holoeasy`.`senal_reconstruir` SET '
        '`fase` = "{0}", `fase_inicial` = "{1}", `iterODD` = "{2}", `code` = "{3}", `MASIRdes` = "{4}", `control_banda` = "{5}"'
        ', `diffphase` = "{6}", `tipoilum` = "{7}", `nivel` = "{8}", `cuantificar` = "{9}"'
        ', `tailleholo` = "{10}", `taillesignal` = "{11}" WHERE id_holograma = "{12}"'.format(data["phase"], 
            data["phaseinitial"], data["iterODD"], data["code"], data["MASIRdes"], data["controlbande"], 
            data["diffphase"], data["tipoilum"], data["nivel"], data["cuantificar"],data["tailleholo"], data["taillesignal"], id))
        filasUpdate = self.ejecutar(queryUpdate)
        print("aqui")
        queryInsert = ('INSERT INTO `bd_holoeasy`.`parametros_regulacion` (`id_holograma`, '
        ' `analogo_PRs`, `analogo_PRb`, `analogo_DPRA`, `analogo_DPLRA`, `analogo_iteraccion`, '
        ' `cuantificar_PRs`, `cuantificar_PRb`, `cuantificar_DPRA`, `cuantificar_DPLRA`, `cuantificar_iteraccion`) VALUES ('
        ' "{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", "{8}", "{9}", "{10}")'.format(id, 
            data["analogo_PRs"], data["analogo_PRb"], data["analogo_DPRA"], data["analogo_DPLRA"], data["analogo_iteraccion"], 
            data["cuantificar_PRs"],data["cuantificar_PRb"],data["cuantificar_DPRA"],data["cuantificar_DPLRA"],data["cuantificar_iteraccion"]))
        filasInsert = self.ejecutar(queryInsert)
    	return filasUpdate + filasInsert

    def UpdateHologramaOptimiser(self, data, id):
        query = ('UPDATE `bd_holoeasy`.`holograma_analogico` SET '
        '`p1` = "{0}", `p2` = "{1}"'
        ', `q1` = "{2}", `q2` = "{3}", `b1` = "{4}", `b2` = "{5}" WHERE id_holograma = "{6}"'.format( 
            data["p1"], data["p2"], data["q1"], data["q2"], data["b1"], data["b2"], id))
        fila = self.ejecutar(query)
        self.crearObjeto(id,data["fon"],"fon")
        self.crearObjeto(id,data["go"],"go")
        self.crearObjeto(id,data["U_Gj"],"U_Gj")
        self.crearObjeto(id,data["gj"],"gj")
        return fila

    def UpdateAnalogiqueCalculer(self, data, id):
        query = ('UPDATE `bd_holoeasy`.`holograma_analogico` SET '
        '`erreura` = "{0}", `EDa` = "{1}", `RSBa` = "{2}", `uniforma` = "{3}", `zerobruita` = "{4}", `deviationstda` = "{5}", '
        '`M` = "{6}", `EA` = "{7}", `RSBA` = "{8}",`UA` = "{9}" WHERE id_holograma = "{10}"'.format(data["erreura"], 
            data["EDa"], data["RSBa"], data["uniforma"], data["zerobruita"], data["deviationstda"], data["M"], 
            data["EA"], data["RSBA"], data["UA"], id))
        fila = self.ejecutar(query) 
        self.crearObjeto(id,data["MASKholo"],"MASKholo")
        self.crearObjeto(id,data["gj2"],"gj2")
        self.crearObjeto(id,data["gj"],"gj")
        self.crearObjeto(id,data["U_Gj"],"U_Gj")
        self.crearObjeto(id,data["B"],"B")
        self.crearObjeto(id,data["CEA"],"CEA")
        self.crearObjeto(id,data["CEDA"],"CEDA")
        self.crearObjeto(id,data["CRSBA"],"CRSBA")
        self.crearObjeto(id,data["CUa"],"CUa")
        self.crearObjeto(id,data["holoa"],"holoa")
        return fila

    def obtenerDatosSenal(self, id):
        obj = {"error" :  False}
        query = ('SELECT `id_holograma`, `fase`, `fase_inicial`, `iterODD`, `tam_obj`, `control_banda`, `diffphase`, `MASIRdes`, `r1x`, `r2x`'
        ' FROM `bd_holoeasy`.`senal_reconstruir` WHERE `id_holograma` = "{0}"'.format(id))
        data = self.ejecutar(query)
        if data:
            obj["phase"], obj["phaseinitial"], obj["iterODD"], obj["Nobj"] = data[0][1], data[0][2], int(data[0][3]), int(data[0][4])
            obj["controlbande"], obj["diffphase"], obj["MASIRdes"] = float(data[0][5]), float(data[0][6]), float(data[0][7])
            obj["fo"] = self.obtenerObjeto(id,"fo")
            obj["r1"] = int(data[0][8])
            obj["r2"] = int(data[0][9])
        else:
            obj["error"] = True
        return obj


    def getCalculerDiffuseurOptimiser(self, id):
        obj = {"error" :  False}
        obj = self.obtenerDatosSenal(id)
        query = ('SELECT `idcalculo_oid`, `optimiserODD`, `s1`, `s2`, `id_holograma` FROM `calculo_oid` WHERE "{0}"'.format(id))
        data = self.ejecutar(query)
        if data:
            obj["optimiserODD"], obj["s1"], obj["s2"] = int(data[0][1]), int(data[0][2]), int(data[0][3])
            obj["OID"] = self.obtenerObjeto(id,"OID")
        else:
            obj["error"] = True
        return obj

    def obtenerIluminacion(self, id):
        obj = {}
        query = ('SELECT `tipoilum`,`taillesignal`,`tailleholo`'
        ' FROM `senal_reconstruir` INNER JOIN `calculo_oid` ON `calculo_oid`.`id_holograma` = `senal_reconstruir`.`id_holograma`'
        ' WHERE `senal_reconstruir`.`id_holograma` = "{0}"'.format(id))
        data = self.ejecutar(query)
        obj["tipoilum"], obj["taillesignal"],obj["tailleholo"]  = data[0][0], data[0][1], data[0][2]
        obj["ODD"] = self.obtenerObjeto(id,"ODD")
        return obj

    def obtenerDataVoir(self, id):
        obj = {}
        query = ('SELECT `taillesignal`, `tailleholo`, `r1x`, `r2x`,`tipoilum` FROM `senal_reconstruir`'
        ' INNER JOIN `calculo_oid` ON `calculo_oid`.`id_holograma` = `senal_reconstruir`.`id_holograma`'
        ' WHERE `senal_reconstruir`.`id_holograma` = "{0}"'.format(id))
        data = self.ejecutar(query)
        obj["taillesignal"], obj["tailleholo"], obj["r1"], obj["r2"], obj["tipoilum"] = float(data[0][0]), float(data[0][1]), int(data[0][2]), int(data[0][3]), data[0][4]
        obj["ODD"] = self.obtenerObjeto(id,"ODD")
        obj["fo"] = self.obtenerObjeto(id,"fo")
        return obj

    def ObtenerCuantificado(self,id):
        archivo = self.nombreObjeto(id,"holoef")
        if(os.path.isfile(archivo)):
            return self.obtenerObjeto(id,"holoef")
        return None

    def ObtenerAnalogico(self,id):
        archivo = self.nombreObjeto(id,"holoa")
        if(os.path.isfile(archivo)):
            return self.obtenerObjeto(id,"holoa")
        return None

    def ObtenerReconstrucion(self,id):
        U_Gj = self.obtenerObjeto(id,"U_Gj") if(os.path.isfile(self.nombreObjeto(id,"U_Gj"))) else None
        ILUM = self.obtenerObjeto(id,"ILUM") if(os.path.isfile(self.nombreObjeto(id,"ILUM"))) else None
        recholoef = self.obtenerObjeto(id,"recholoef") if(os.path.isfile(self.nombreObjeto(id,"recholoef"))) else None    
        return U_Gj, ILUM, recholoef

    def ObtenerImagen(self, id):
        return self.obtenerObjeto(id,"img") if(os.path.isfile(self.nombreObjeto(id,"img"))) else None

    def obtenerDataOptimizar(self, id):
        obj = {}
        query = ('SELECT `taillesignal`, `tailleholo`, `r1x`, `r2x`,`tipoilum`,`pixelmargin`,`tam_img`,`optimiser`,`iteropt`,`lissage2` FROM `senal_reconstruir`'
        ' INNER JOIN `calculo_oid` ON `calculo_oid`.`id_holograma` = `senal_reconstruir`.`id_holograma`'
        ' INNER JOIN `holograma_analogico` ON `holograma_analogico`.`id_holograma` = `senal_reconstruir`.`id_holograma`'
        ' WHERE `senal_reconstruir`.`id_holograma` = "{0}"'.format(id))
        data = self.ejecutar(query)
        obj["taillesignal"], obj["tailleholo"], obj["r1"], obj["r2"], obj["tipoilum"] = float(data[0][0]), float(data[0][1]), int(data[0][2]), int(data[0][3]), data[0][4]
        obj["pixelmargin"], obj["tailleimg"], obj["optimiser"] = int(data[0][5]), int(data[0][6]), int(data[0][7])
        obj["iteropt"], obj["lissage2"] = int(data[0][8]), float(data[0][9])
        obj["fo"] = self.obtenerObjeto(id,"fo")
        obj["ODD"] = self.obtenerObjeto(id,"ODD")
        obj["ILUM"] = self.obtenerObjeto(id,"ILUM")
        return obj

    def obtenerParametrosRegulacion(self, id, tipo = 1):
        if tipo == 1:
            query = ('SELECT `analogo_iteraccion`, `analogo_PRs`, `analogo_PRb`, `analogo_DPRA`, `analogo_DPLRA` FROM `parametros_regulacion` WHERE `id_holograma` = "{0}" ORDER BY `parametros_regulacion`.id DESC LIMIT 1'.format(id))
        else:
            query = ('SELECT `cuantificar_iteraccion`, `cuantificar_PRs`, `cuantificar_PRb`, `cuantificar_DPRA`, `cuantificar_DPLRA` FROM `parametros_regulacion` WHERE `id_holograma` = "{0}" ORDER BY `parametros_regulacion`.id DESC LIMIT 1'.format(id))
        data = self.ejecutar(query)
        return int(data[0][0]), float(data[0][1]), float(data[0][2]), float(data[0][3]), float(data[0][4])


    def obtenerDataCalculer(self, id):
        obj = {}
        query = ('SELECT `p1`, `p2`, `q1`, `q2`, `b1`, `b2`,`iteropt`,`code`,`taillesignal`,`DPE`,'
            '`tam_img`,`tailleholo`,`pixelmargin`, `taillesignal`'
        ' FROM `senal_reconstruir` INNER JOIN `holograma_analogico` ON `holograma_analogico`.`id_holograma` = `senal_reconstruir`.`id_holograma`'
        ' WHERE `senal_reconstruir`.`id_holograma` = "{0}" ORDER by holograma_analogico.idholograma_analogico DESC limit 1'.format(id))

        data = self.ejecutar(query)
        obj["p1"], obj["p2"], obj["q1"], obj["q2"], obj["b1"], obj["b2"] = int(data[0][0]), int(data[0][1]), int(data[0][2]), int(data[0][3]), int(data[0][4]), int(data[0][5])
        obj["iteropt"], obj["code"], obj["taillesignal"], obj["DPE"] = int(data[0][6]), data[0][7],int(data[0][8]), float(data[0][9])
        obj["tailleimg"],obj["tailleholo"], obj["pixelmargin"], obj["taillesignal"] = int(data[0][10]), int(data[0][11]), int(data[0][12]), int(data[0][13])
        obj["iteranalogo"], obj["PRs"], obj["PRb"], obj["DPRA"], obj["DPLRA"] = self.obtenerParametrosRegulacion(id,1)

        obj["fon"] = self.obtenerObjeto(id,"fon")
        obj["go"] = self.obtenerObjeto(id,"go")
        obj["ILUM"] = self.obtenerObjeto(id,"ILUM")
        return obj

    def obtenerDataOptizer(self, id):
        obj = {}
        query = ('SELECT `nivel`,`M`,`p1`, `p2`, `q1`, `q2`,`code`,`taillesignal`,`DPE`,`tam_img`, `pixelmargin`'
        ' FROM `senal_reconstruir` INNER JOIN `calculo_oid` ON `calculo_oid`.`id_holograma` = `senal_reconstruir`.`id_holograma`'
        ' INNER JOIN `holograma_analogico` ON `holograma_analogico`.`id_holograma` = `senal_reconstruir`.`id_holograma`'
        ' WHERE `senal_reconstruir`.`id_holograma` = "{0}"'.format(id))
        data = self.ejecutar(query)
        obj["niveaux"], obj["M"], obj["p1"], obj["p2"], obj["q1"], obj["q2"] = int(data[0][0]), int(data[0][1]), int(data[0][2]), int(data[0][3]), int(data[0][4]), int(data[0][5])
        obj["code"], obj["taillesignal"], obj["DPE"] = data[0][6], int(data[0][7]), float(data[0][8])
        obj["tailleimg"], obj["pixelmargin"] = int(data[0][9]), int(data[0][10])
        obj["iterquantization"], obj["PRs"], obj["PRb"], obj["DPRA"], obj["DPLRA"] = self.obtenerParametrosRegulacion(id,2)
        obj["go"] = self.obtenerObjeto(id,"go")
        obj["MASKholo"] = self.obtenerObjeto(id,"MASKholo")
        obj["ILUM"] = self.obtenerObjeto(id,"ILUM")
        obj["fon"] = self.obtenerObjeto(id,"fon")
        obj["U_Gj"] = self.obtenerObjeto(id,"U_Gj")
        return obj


    def GuardarCorreo(self,name, email, message):
        fecha_actual = datetime.date.today()
        hora_actual = datetime.datetime.now().time()
        query = ('INSERT INTO correo '
               '(nombre, email, mensaje, fecha, hora) '
               'VALUES ("{0}", "{1}", "{2}", "{3}", "{4}")'.
               format(name,email, message,fecha_actual.strftime("%Y-%m-%d"),hora_actual.strftime("%H:%M:%S")))
        return self.ejecutar(query)

    def ejecutar(self, query=""): 
	    conn = self.conectar() # Conectar a la base de datos 
	    cursor = conn.cursor()         # Crear un cursor 
	    cursor.execute(query)          # Ejecutar una consulta
	    if query.upper().startswith("SELECT"): 
	        data = cursor.fetchall()   # Traer los resultados de un select 
	    elif query.upper().startswith("INSERT"):
	        conn.commit()              # Hacer efectiva la escritura de datos 
	    	data = cursor.lastrowid 
	    else: 
	        conn.commit()              # Hacer efectiva la escritura de datos 
	        data = cursor.rowcount
	    cursor.close()                 # Cerrar el cursor 
	    conn.close()                   # Cerrar la conexion 
	    return data

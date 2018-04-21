#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from Excepciones import EntradaError

class Iluminacion:
	def analogique_ilumination(self,tipo,PHo,taillesignal,tailleholo):
		if tipo=='circle':
			return self.ilumination_circle(PHo,taillesignal,tailleholo)
		elif tipo=='gauss':
			return self.ilumination_gauss(PHo,taillesignal,tailleholo)
		else:
			return self.ilumination_carre(PHo,taillesignal,tailleholo)

	def ilumination_circle(self,PHo,M,H):
		Nodd = PHo.shape[0]
		if M < Nodd:
			raise EntradaError('ilumination_circle','plain signal >= object')
		if M == Nodd:
			M = Nodd
			TMP2 = M%2
		else:
			TMP2 = M%2
			TMP3 = H%2
		q1 = (M+TMP2)/2-(H-TMP3)/2
		q2 = q1+H
		x = np.arange(float(-M/2),float(M/2))
		X,Y = np.meshgrid(x,x)
		ILUM=X**2+Y**2<=(H/2-1)**2
		return ILUM, 0

	def ilumination_carre(self,PHo,M,H):
		Nodd = PHo.shape[0]
		if M < Nodd:
			raise EntradaError('ilumination_carre','plain signal >= object')
		if M ==Nodd:
			M = Nodd
			TMP2 = M%2
		else:
			TMP2 = M%2
		TMP3 = H%2
		q1 = (M+TMP2)/2-(H-TMP3)/2
		q2 = q1+H
		ILUM = np.ones((M,M))
		return ILUM, 0
	    
	def ilumination_gauss(self,PHo,M,H):
		Nodd = PHo.shape[0]
		if M < Nodd:
			raise EntradaError('ilumination_gauss','plain signal >= object')
		x = np.arange(float(-M/2),float(M/2))
		X,Y = np.meshgrid(x,x)
		sg = 2
		Wo= 5*H/3
		ILUM=np.exp(-(X**sg+Y**sg)/(Wo)**sg)
		return ILUM, sg

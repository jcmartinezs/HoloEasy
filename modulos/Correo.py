#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# Enviar correo Gmail con Python
# www.pythondiario.com

from email.mime.text import MIMEText
import smtplib
import config

class Correo(object):
	_username = config.APP_CONFIG['email_user']
	_password = config.APP_CONFIG['email_password']
	"""docstring for Correo"""
	def __init__(self):
		super(Correo, self).__init__()
		self.fromaddr = config.APP_CONFIG['email_user']
		self.toaddrs  = config.APP_CONFIG['email_to']
		self.msg = 'Correo enviado utilizano Python + smtplib en www.pythondiario.com'

	def enviarCorreo(self, name,toaddrs,msg):
		# Enviando el correo
		try: 
			#smtp = smtplib.SMTP('localhost') 
			#smtp.sendmail(remitente, destinatario, email)
			message = """
			<html>
				<head></head>
				<body>
					<b>Nombre:</b> %s<br/>
					<b>Email:</b> %s<br/>
					<b>Mensaje:</b> <br/>
					<p>%s</p>
				</body>
			</html>
			""" % (name,toaddrs,msg)
			mime_message = MIMEText(message, "html")#plain
			mime_message["From"] = self.fromaddr
			mime_message["To"] = toaddrs
			mime_message["Subject"] = "Holoeasy"

			server = smtplib.SMTP('smtp.gmail.com:587')
			server.starttls()
			server.login(self.username,self.password)
			server.sendmail(self.fromaddr, toaddrs, mime_message.as_string())
			server.quit()
			print "Correo enviado" 
		except: 
			server.quit()
			print """Error: el mensaje no pudo enviarse. 
			Compruebe que sendmail se encuentra instalado en su sistema"""

	@property
	def username(self):
		return self._username
	
	@property
	def password(self):
		return self._password
		

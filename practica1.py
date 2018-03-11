#!/usr/bin/python3
#ANA MARIA GONZALEZ DIAZ

import webapp
import csv
import os

class cortaURLs(webapp.webApp):
	url_reals = {}			#Diccionario para guardar las url reales.
	url_shortened = {}		#Diccionario para guardar las url acortadas.
	count = -1

	def readcsv(self,file):			#Abrimos el fichero y pasamos lo que hay en el csv a los dos diccionarios
		with open(file,"r") as fd:
			reader = csv.reader(fd)
			for row in reader:
				key = int(row[0])
				url = row[1]
				self.url_shortened[key] = url
				self.url_reals[url] = key
				self.count = key
		fd.close()
	def writecsv(self,dictionary):			#Se pasa lo que hay en el diccionario al csv.
		with open("fichero.csv","a") as fd:
			writer = csv.writer(fd)
			for url in dictionary:
				key = url
				val = dictionary[key]
				writer.writerow([int(key)]+[val])
		fd.close()

	def parse(self,request):
	
		method = request.split()[0]
		resource = request.split()[1]
		body = request.split('\r\n\r\n')[1][4:]
		body = body.replace('%2F','/').replace('%3A',':') 

		return method,resource, body

	def process(self,parsedRequest) :
		method,resource, body = parsedRequest

		form = """
			<form action="" method="POST">
			Introduce url para acortar: <input type="text" name="url">
			<input type="submit" value="Enviar">
			</form>
		"""
		try:
			url_short = int(resource[1:])
			print("La variable es:",str(url_short))
		except ValueError:
			url_short = ""

		if method == "GET":
			if resource == "/": #Se devuelve la pagina HTML con un formulario, comprobando el fichero.
				if os.stat('fichero.csv').st_size == 0:
					print("El fichero esta vacio")
				else:
					self.readcsv('fichero.csv')
				return("200 OK","<html><body>"+ "<h1>BIENVENIDO A LA ACORTADORA DE URLS!\n</h1>" 
					+ form + "<p>" + "URLS ACORTADORAS:" + str(self.url_shortened)+"URLS REALES"+str(self.url_reals)+"</p></body></html>")
			elif url_short in self.url_shortened: #Se redirige a la pagina, en el caso de recibir una url corta.
				print("Redirigiendo...")
				url = self.url_shortened[int(resource[1:])]
				count = self.url_reals[url]
				return("303 See other","<html><body><meta http-equiv='refresh'"+ "content='0 url=" + url +"'>"+"</p></body></html>")
			else: 
				return("404 Not Found","<html><body>ERROR: Url no disponible </body></html>")
		elif method == "POST":
			if len(body) == 0: #No hay url en el formulario
				return ("404 Not Found","<html><body><h1>ERROR:Sal de aqui!</html></body></h1>")
			else: 
				if body.find("http") == -1:	#Tiene que buscar http o https , con que busque http nos vale, si no lo encuentro es un -1
					print("No empieza por HTTP") 
					url = "http://" + body #Añadimos cabecera
				else:						#Si lo encuentra, no hace falta añadir la cabera
					print("Empieza por HTTP")
					url = body
				if url in self.url_reals:   #Se busca la url en el diccionario de url_reales, si esta se devuelve su url acortada
					print(url+ "esta en el diccionario")
					url_s = self.url_reals[url]
				else:						#Al no estar la url, la introduzco en los diccionarios
					self.count = self.count + 1 
					url_s = self.count
					self.url_reals[url] = url_s
					self.url_shortened[self.count] = url
					self.writecsv(self.url_shortened)

				return("200 OK", "<html><body>" + '<p><a href="' + str(url_s) + '">Url corta</a></p>' +
						'<p><a href="' + url + '">Url original</a></p>'+"<body></html>")
		else:
			return("404 Not Found","<html><body><h1>ERROR:Sal de aqui!</h1></body></html>")
if __name__ == "__main__":
	try:
		testWebApp = cortaURLs("localhost",1234)
	except KeyboardInterrupt:
		print("Se ha interrumpido")	






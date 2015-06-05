from subprocess import call
import os
import time
import json

##Preparar datos
fecha = time.strftime("%x") 
fecha += " a las "
fecha += time.strftime("%X")
datos = json.loads(open("config.json").read())

##Leer datos de archivo json
try:
	ruta = datos["ruta"]
	usuario = datos["usr"]
	url = datos["url"]
except KeyError:
	print "No son correctos los datos"

	
##Manejar los cambios git	
try:	
	os.chdir(ruta)
	print os.getcwd()
	call(["git","add", "*.txt"])
	###call(["git", "add", "pruebas.txt"])
	call(["git", "commit", "-am", "Actualizado el " + fecha])
	call(["git", "push"])
	print "Archivos actualizados"
	###call(["git", "status"])
except OSError:
	print "No existe la ruta " + ruta

#except:
#	print "Ocurrio un error inesperado"
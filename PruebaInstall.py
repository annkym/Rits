from subprocess import call
#from git import Repo
import time, json

def cloneRepo(url, ruta):
	##Clonar repositorio (Inicializarlo)
	print "Clonando Repositorio " + url
#	repoCloned = Repo.clone_from(url, ruta)
#	print repoCloned.git.status()
	print "Repositorio creado correctamente en " + ruta

def createTask(sc, mo, tr, tn):
	##Crear tarea windows (SC- MINUTE, HOURLY, DAILY, WEEKLY) (MO- Numero) (TR- Ruta del exe)
	print "Creando tarea"
	call(["schtasks", "/CREATE", "/SC", sc, "/MO", mo, "/TN", tn, "/TR", tr])
	print "Tarea " + tn + " creada exitosamente"
	
if __name__ == "__main__" :
	
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
		archivos = datos["files"]
		schedule = datos["schedule"]
		time = datos["time"]
		exePath = datos["exePath"]
		taskName = datos["taskName"]
		#cloneRepo(url, ruta)
		#checkRepo(ruta)
		#addFileToRepo(ruta, archivos, "Actualizado el " + fecha)
		createTask(schedule, time, exePath, taskName)
	except KeyError:
		print "No son correctos los datos"
	

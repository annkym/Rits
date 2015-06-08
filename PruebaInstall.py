from subprocess import call
#from git import Repo
import time, json

def cloneRepo(url, path):
	##Clonar repositorio (Inicializarlo) (url - URL del repo) (path - Directorio donde se baja)
	print "Clonando Repositorio " + url
#	repoCloned = Repo.clone_from(url, path)
#	print repoCloned.git.status()
	print "Repositorio creado correctamente en " + path

def createTask(sc, mo, tr, tn):
	##Crear tarea windows (SC - MINUTE, HOURLY, DAILY, WEEKLY) (MO - Numero) (TR - Ruta del exe) (TN - Nombre de la tarea)
	print "Creando tarea"
	call(["schtasks", "/CREATE", "/SC", sc, "/MO", mo, "/TN", tn, "/TR", tr])
	print "Tarea " + tn + " creada exitosamente"
	
def deleteTask(tn):
	##Borrar tarea de windows (TN - Nombre de la tarea)
	print "Borrando tarea"
	call(["schtasks", "/DELETE", "/TN", tn, "/F"])
	print "Tarea " + tn + " borrada exitosamente"
	
	
if __name__ == "__main__" :
	
	##Prepare message
	message = time.strftime("%x") 
	message += " at "
	message += time.strftime("%X")
	##Read parameters from json file
	params = json.loads(open("config.json").read())
	try:
		path = params["path"]
		user = params["usr"]
		url = params["url"]
		files = params["files"]
		schedule = params["schedule"]
		time = params["time"]
		exePath = params["exePath"]
		taskName = params["taskName"]
		##Clone repository
		#cloneRepo(url, path)
		#checkRepo(path)
		##Add files
		#addFileToRepo(path, files, "Last Updated : " + message)
		##Create Windows Task
		createTask(schedule, time, exePath, taskName)
	except KeyError:
		print "Configuration file problem, please check..."
	

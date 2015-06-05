from git import Repo, Remote, Actor
import time
import json

def cloneRepo(url, ruta):
	##Clonar repositorio (Inicializarlo)
	print "Clonando Repositorio " + url
	repoCloned = Repo.clone_from(url, ruta)
	print repoCloned.git.status()
	print "Repositorio creado correctamente en " + ruta

def checkRepo(repoName):
	#Checar estatus del repo
	print "Checando estatus de repositorio " + repoName
	repo = Repo(repoName)
	assert not repo.bare
	print repo.git.status()
	#assert not repo.is_dirty()
	lista = repo.untracked_files
	print lista
	
	print Actor.git.util.get_user_id()
	
	print "Chequeo terminado"

def addFileToRepo(repoName, fileName, commitMessage):
	#Agregar archivos al repo y subirlos
	print "Agregando archivos al repositorio " + repoName
	print "Tipo de archivos a actualizar " + fileName
	
	repo = Repo(repoName)
	repo.git.add(fileName)
	try:
		repo.git.commit(m=commitMessage)
		print repo.git.log()
		repo.git.push()
		print "Upload terminado"
	except:
		print "Problemas al actualizar los archivos"
		print repo.git.status()
		
def initRepo(ruta):
	#En pruebas, NO USAR
	newRepo = Repo.init(ruta, True)
	remoto = Remote(newRepo,"MiRepo")
	remoto.add(newRepo,"MiRepo","https://github.com/annkym/MiRepo.git")
	remoto.push()
	print newRepo.git.status()


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
		cloneRepo(url, ruta)
		#checkRepo(ruta)
		#addFileToRepo(ruta, archivos, "Actualizado el " + fecha)
	except KeyError:
		print "No son correctos los datos"
	
	
	
	#initRepo(ruta)
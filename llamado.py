from subprocess import call
import os
import time
fecha = time.strftime("%x") 
fecha += " a las "
fecha += time.strftime("%X")
##@TODO Falta generar la ruta del repositorio
os.chdir("/Users/angelica/hello-world")
call(["git","add", "*.txt"])
###call(["git", "add", "pruebas.txt"])
call(["git", "commit", "-am", "Actualizado el " + fecha])
###call(["git", "status"])
call(["git", "push"])
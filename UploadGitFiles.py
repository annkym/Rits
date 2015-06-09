from subprocess import call
import time, json, os

def addFileToRepo(repoName, fileName, commitMessage):
	##Add files to repo and update
	print "Add files to repo " + repoName
	print "File types to update : " + fileName
	try:	
		os.chdir(repoName)
		print os.getcwd()
		call(["git","add", fileName])
		call(["git", "commit", "-am", commitMessage])
		call(["git", "push"])
		print "Files Updated"
	except OSError:
		print "Trouble ..."

		
if __name__ == "__main__" :
	
	##Prepare message
	message = time.strftime("%x") 
	message += " at "
	message += time.strftime("%X")
	param = json.loads(open("config.json").read())
	
	##Leer datos de archivo json
	try:
		path = param["path"]
		user = param["usr"]
		files = param["files"]
		addFileToRepo(path, files, "Updated on " + message)
	except KeyError:
		print "Config file problem..."
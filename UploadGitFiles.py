from subprocess import call
import time, json, os

jsonFile = "config.json"

def addFileToRepo(repoName, fileName, commitMessage):
	##Add files to repo and update
	print "Add files to repo " + repoName
	print "File types to update : " + fileName
	try:	
		os.chdir(repoName)
		print os.getcwd()
		call(["git","add", fileName])
		#Call function returns 0 if there are changes to upload, 1 if it is up to date
		if (call(["git", "commit", "-am", commitMessage])):
			return
		call(["git", "push"]) 
	except OSError:
		print "Trouble with update..."

		
if __name__ == "__main__" :
	
	##Prepare message
	message = "Updated on " + time.strftime("%x") + " at " + time.strftime("%X")
	param = json.loads(open(jsonFile).read())
	
	##Read parameters from json file
	try:
		path = param["path"]
		files = param["files"]
		addFileToRepo(path, files, message)
	except KeyError:
		print "Config file problem..."
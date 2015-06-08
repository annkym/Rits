from git import Repo, Remote
import time, json

def checkRepo(repoName):
	##Check repo's status
	print "Check " + repoName + " status"
	repo = Repo(repoName)
	assert not repo.bare
	print repo.git.status()
	#assert not repo.is_dirty()
	listed = repo.untracked_files
	print listed

def addFileToRepo(repoName, fileName, commitMessage):
	##Add files to repo and update
	print "Add files to repo " + repoName
	print "File types to update : " + fileName
	
	repo = Repo(repoName)
	repo.git.add(fileName)
	try:
		repo.git.commit(m=commitMessage)
		print repo.git.log()
		repo.git.push()
		print "Upload finished"
	except:
		print "Update trouble..."
		print repo.git.status()
		
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
		url = param["url"]
		files = param["files"]
		cloneRepo(url, path)
		#checkRepo(path)
		#addFileToRepo(path, files, "Updated on " + message)
	except KeyError:
		print "Config file problem..."

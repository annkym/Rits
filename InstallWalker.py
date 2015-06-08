from subprocess import call
from git import Repo
import time, json

def cloneRepo(url, path):
	##clone repository (url - Repo's URL) (path - Repo's path)
	print "Clone Repository " + url
	repoCloned = Repo.clone_from(url, path)
	print repoCloned.git.status()
	print "Repository created at " + path

def createTask(sc, mo, tr, tn):
	##Create windows task (SC - MINUTE, HOURLY, DAILY, WEEKLY) (MO - Number of minutes, hours...) 
	##(TR - Path to exe) (TN - Task name)
	print "Create task"
	call(["schtasks", "/CREATE", "/SC", sc, "/MO", mo, "/TN", tn, "/TR", tr])
	print "Task " + tn + " created"
	
def deleteTask(tn):
	##Delete windows task (TN - Task name)
	print "Delete task"
	call(["schtasks", "/DELETE", "/TN", tn, "/F"])
	print "Task " + tn + " deleted"
	
	
if __name__ == "__main__" :

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
		##Check repository
		#checkRepo(path)
		##Create Windows Task
		createTask(schedule, time, exePath, taskName)
	except KeyError:
		print "Configuration file problem, please check..."
	

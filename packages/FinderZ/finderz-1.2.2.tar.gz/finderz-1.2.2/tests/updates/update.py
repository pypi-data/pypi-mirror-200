import shutil
import os
#For dealing with files:

#moveFiles from one place, to the next
def moveFile(originalFileDir, newFileDir):
	shutil.move(originalFileDir, newFileDir)
	return True
def copyFile(originalFileDir, newFileDir):
	shutil.copy(originalFileDir, newFileDir)
	return True

#For dealing with directories:

#Used to move a directory:
def moveDir(originalDir, newDir):
	shutil.move(originalDir, newDir)
	return True

#Copy a directory and its contents from one place to another:
def copyDir(originalDir, newDir):
	lastdir = os.path.basename(os.path.normpath(originalDir))
	newDirectory = newDir + "/" + lastdir
	shutil.copytree(originalDir, newDirectory)
	return True

#VERSION 1.2.0
def renameFile(newName, filePath):
	#Remove any slash marks:
	newFilePath = os.path.dirname(filePath)
	os.rename(filePath, newFilePath + "/" + newName)
	
def renameDirectory(newName, directoryPath):
	newDirectoryPath = os.path.dirname(os.path.dirname(directoryPath))
	os.rename(directoryPath, newDirectoryPath + "/" + newName)


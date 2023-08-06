#!/usr/bin/env python3

#Functions that will be used frequently:
import os

#Function to scan files, and for each file, replace that keyword for every line.
def findAndReplace(filePath, keyWord, replacementKeyword):
	#Scan for files:
	
	for folder, dirs, files in os.walk(filePath):
		Check = False
		if Check == True:
			break
		for file in files:
			
			fullpath = os.path.join(folder, file)
			
			readable = False
			#Open the file and start scanning:
			fileObject = open(fullpath, 'r')
			
			#Read the lines:
			try:
				fileLines = fileObject.readlines()
				readable = True
			except UnicodeDecodeError:
				print("I: Bypassing some un-decodable files...")
				continue
			#Get the line amount:
			if readable == True:
				lineamount = len(fileLines)
				linecount = 0
				for i in range(lineamount):
					#Line location
					
					
					#Check if the keyword is in the lineCount:
					if keyWord in fileLines[linecount]:
						Check = True
						
						#Get the info in that line.
						foundLocation = fileLines[linecount]
						
						#Replace the word in the line with the new word.
						replacement = foundLocation.replace(keyWord, replacementKeyword)
						
						#Set the line equal to the new value:
						fileLines[linecount] = replacement
					linecount += 1
			#If the check is True, write the file, else, go back to loop and scan for other files.
				if Check == True:
					f = open(fullpath, 'w')
					f.writelines(fileLines)

##UPDATE:
					
#fileOperands:
#Now uses the shutil library:
import shutil
#moveFiles from one place, to the next
#For dealing with files:
def moveFile(originalFileDir, newFileDir):
	shutil.move(originalFileDir, newFileDir)
	return True
def copyFile(originalFileDir, newFileDir):
	shutil.copyfile(originalFileDir, newFileDir)
	return True

#For dealing with directories:
def moveDir(originalDir, newDir):
	shutil.move(originalDir, newDir)
	return True
def copyDir(originalDir, newDir):
	shutil.copy2(originalDir, newDir)
	return True
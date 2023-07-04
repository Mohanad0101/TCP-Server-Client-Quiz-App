# (Earlier code for fileExists, writeFile, readFile)
# #

import os

def fileExists(filePath):
 exists = os.path.exists(filePath)
 return exists
def writeFile(filePath, textToWrite):
 fileHandle = open(filePath, 'w')
 fileHandle.write(textToWrite)
 fileHandle.close()
def readFile(filePath):
 if not fileExists(filePath):
  print('The file, ' + filePath + ' does not exist - cannot read it.')
  return ('')
 fileHandle = open(filePath, 'r')
 data = fileHandle.read()
 fileHandle.close()
 return (data)


#Functions for opening a file, writing & reading a line at a time, and
#closing the file
def openFileForWriting(filePath):
 fileHandle = open(filePath, 'w')
 return fileHandle
def writeALine(fileHandle, lineToWrite):
 # Add a newline character '\n' at the end and write the line
 lineToWrite = lineToWrite + '\n'
 fileHandle.write(lineToWrite)
def openFileForReading(filePath):
 if not fileExists(filePath):
  print('The file, ' + filePath + ' does not exist - cannot read it.')
  return ("")
 fileHandle = open(filePath, 'r')
 return (fileHandle)

def readALine(fileHandle):
 theLine = fileHandle.readline()
  # This is a special check for attempting to read past the end of thefile(EOF).
  # If this occurs, let's return something unusual: False (which is not astring)
  # If the caller wishes to check, their code can easily detect the endof the file this way
 if not theLine:
  return False
  # If the line ends with a newline character '\n', then strip that off the end
 if theLine.endswith('\n'):
  theLine = theLine.rstrip('\n')
  return theLine

def closeFile(fileHandle):
 fileHandle.close()

if '__name__'=='main':
  print('h')
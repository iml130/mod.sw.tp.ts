import urllib
import sys
import getopt


def main(argv):
   inputfile = ''
   outputfile = '' 
   inputfile = argv[0]

   # print 'Output file is "', outputfile
   loadedFile = loadFile(inputfile)
   decodedTl =  decodeTaskLanguage(loadedFile)

   print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ENCODED_LANGUAGE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
   print("\n")
   print loadedFile
   print("\n\n\n")
   print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DECODED TASK_LANGUAGE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
   print("\n")
   print (decodedTl)
   print("\n\n\n")

def loadFile(_file):
	with open(_file) as f:
		content = f.readlines()
	longString = ""

	for line in content:
		longString += line.replace("\r", "")
	return longString 


def decodeTaskLanguage(_tl):
	return urllib.unquote_plus(_tl)

if __name__ == "__main__":
	numberOfArguments = (len(sys.argv[1:]))
	if(numberOfArguments != 1):
		print ("python decodeTaskLanguage INPUTFILE")
		exit(1)
	main(sys.argv[1:])

import urllib
import sys
import getopt


def main(argv):
   inputfile = ''
   outputfile = '' 
   inputfile = argv[0]

   # print 'Output file is "', outputfile
   loadedFile = loadFile(inputfile)
   encodedTl =  encodeTaskLanguage(loadedFile)

   print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TASK_LANGUAGE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
   print("\n")
   print (loadedFile)
   print("\n\n\n")
   print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ENCODED TASK_LANGUAGE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
   print("\n")
   print (encodedTl)
   print("\n\n\n")
   print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ENTITY:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
   print("\n")
   print (createEntity(encodedTl))

def loadFile(_file):
	with open(_file) as f:
		content = f.readlines()
	longString = ""

	for line in content:
		longString += line.replace("\r", "")
	return longString 


def encodeTaskLanguage(_tl):
	return urllib.quote_plus(_tl)

def createEntity(_encodedTl):
	entity = """{
	"id": "Materialflow1",
	"type": "Materialflow",
	"specification": {
		"value":  \"""" + _encodedTl + """\",
		"type": "Text"
	},
	"ownerId": {
		"type": "Text",
		"value": "reviewers hmi"
	},
	"active": {
		"type": "Boolean",
		"value": true
	}
}"""
	return entity


if __name__ == "__main__":
	numberOfArguments = (len(sys.argv[1:]))
	if(numberOfArguments != 1):
		print ("python encodeTaskLanguage INPUTFILE")
		exit(1)
	main(sys.argv[1:])

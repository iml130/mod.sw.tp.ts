import urllib

with open("current.txt") as f:
    content = f.readlines()
longString = ""

for line in content:
    longString += line.replace("\r", "")
 
print "qoute"
print urllib.quote_plus(longString)
print "unqoute"
print urllib.unquote_plus(longString)
# you may also want to remove whitespace characters like `\n` at the end of each line

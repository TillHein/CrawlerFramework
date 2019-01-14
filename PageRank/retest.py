import re

teststring1 = "<a href=yes.de>"
teststring2 = "<a jref=no.de>"
teststring3 = "<al href= no.de>"
teststring4 = "<a href=yes.de>,<al href= no.de>,<a jref=no.de>"
x = re.findall("^<a href=.*>$", teststring1)
print(x)
x = re.findall("^<a href=.*>$", teststring2)
print(x)
x = re.findall("^<a href=.*>$", teststring3)
print(x)
x = re.findall("^<a href=.*>$", teststring4)
print(x)
x = re.search("^<a href=.*>$", teststring4)
print(x)

urls = re.findall(r'href=[\'"]?([^\'" >]+)', teststring4)
print (urls)

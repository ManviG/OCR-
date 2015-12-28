import xml.etree.ElementTree as ET
import unicodedata
import operator
import copy
import re

# Binary converter for strings
def binary(x):
    if x == "yes":
        return "1"
    return "0"

########################################PRIYANK#####################################################

def isEmail(y):
    x=y.strip()
    x = x.strip('.')
    isatr = 0
    for i in range(len(x)):
        if x[i] == "@":
            isatr = 1
        if((isatr==1) and (x[i]==".")):# and (x[i+1]<"z" and x[i+1]>"a")):
            return "1"
    return "0"
directory = "/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/"#raw_input()+"/"#/home/priyank/Desktop/Projects/pdfs/"
a_file = directory + "input_2.xml"#a_file = "pdfs/acl1.xml"
foutMail = open(a_file.split(".")[0] + '_mail_parse.txt','w')
foutMail.write("0\t0\t0\n")
p = []
alp = []
count = 0
bracks = 0

def processTokenForMail(word):

    global bracks
    global p
    global alp
    if word.find("{")!=-1 or word.find("[")!=-1:
        bracks=bracks+1
    isthisemail = (isEmail(word))
    if bracks > 0:
        if(len(word.replace(' ',''))>0):
            #print word.replace(' ','')+"\t"
            alp.append((word.replace(' ','')+"\t").encode("utf-8"))
            alp.append(isthisemail+"\t")
            alp.append(("0\n").encode("utf-8"))
            p.append(copy.copy(alp))
        #print p
            del alp[:]
    
    if(len(word.replace(' ',''))>0) and bracks<=0:
        if (isEmail(word)) == "1":
            foutMail.write((word.replace(' ','').strip(',')+"\t").encode("utf-8"))
            foutMail.write(isthisemail+"\t")
            foutMail.write(("0\n").encode("utf-8"))
    if word.find("}")!=-1 or word.find("]")!=-1:
        bracks -= 1
        if(len(p)!=0):
            if int(p[len(p)-1][1])==1:              #If it is email
                for i in range(len(p)):
                    p[i][1] = "1\t"
            #print p
            for i in range(len(p)):
                for j in p[i]:
                    if p[i][1]=="1\t" or p[i][1]=="1":
                        foutMail.write(str(j))
        del p[:]
    return isthisemail


def processStringForMail(string):
    string = string.strip()
    posAtTheRate = string.find("@")
    if posAtTheRate == -1 or posAtTheRate == 0 or posAtTheRate == len(string)-1:
        return -1
    string = string.replace("@ ","@").replace(" @","@")
    p = re.finditer(r'[.] [a-z]', string)
    p = [m.start() for m in p]
    sub = 0
    for pos in p:
        string = string[:pos-sub+1] + string[pos-sub+2:]
        sub += 1

    for token in string.split(' '):
        if processTokenForMail(token) == "1":
            foutMail.write("0\t0\t0\n")
tree = ET.parse(a_file)
root = tree.getroot()
# page = root.find('PAGE')
# texts = page.findall('TEXT')
# iMail = 0
# stringMail = ""
# twotextstaken = False
# while iMail<len(texts):
#     for tokens in texts[iMail].findall('TOKEN'):
#         if tokens.text is None:
#             #print tokens.text
#             continue
#         if type(tokens.text) is unicode:
#             stringMail += unicodedata.normalize('NFKD', tokens.text).encode('ascii','ignore')
#         else:
#             stringMail += tokens.text
#         stringMail += " "
#     if(twotextstaken == False):
#         twotextstaken = True
#         iMail += 1
#         continue
#     else:
#         #print iMail,
#         if processStringForMail(stringMail)!=-1:
#             iMail += 1
#         stringMail = ""
#         twotextstaken = False
count = 0
twotextstaken = False
for page in root.findall('PAGE'):
    count += 1
    if count > 2:
        break
    texts = page.findall('TEXT')
    iMail = 0
    stringMail = ""
    while iMail<len(texts):
        for tokens in texts[iMail].findall('TOKEN'):
            if tokens.text is None:
                #print tokens.text
                continue
            if type(tokens.text) is unicode:
                stringMail += unicodedata.normalize('NFKD', tokens.text).encode('ascii','ignore')
            else:
                stringMail += tokens.text
            stringMail += " "
        if(twotextstaken == False):
            twotextstaken = True
            iMail += 1
            continue
        else:
            #print iMail, stringMail,
            if processStringForMail(stringMail)!=-1:
                iMail += 1
            stringMail = ""
            twotextstaken = False

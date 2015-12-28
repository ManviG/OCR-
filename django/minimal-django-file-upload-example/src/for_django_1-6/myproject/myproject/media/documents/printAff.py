import os
flag = "0"   # to check if a Affiliation is already going on
directory = "/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/"#raw_input()+"/"#/home/priyank/Desktop/Projects/pdfs/"
filetoread = directory + "input_2_parse.txt"
outfile = open(directory + "input_AllAffiliations.txt",'w')

small_cases = ["of", "for", "and", "in", "at", "do", "a", "di", "de", "the"]

#outfile.write("<" + (filetoread.split(".")[0]).split("/")[-1] + ">\n")

def cutShort(stri):
    cutBefore = stri.find(" with")
    if cutBefore!=-1:
        stri = stri[cutBefore+6:]
    stri = stri.strip()
    striList = stri.split(' ')
    finalStrList = ""
    for word in striList:
        if (word.upper().find("EMAIL")==-1 and word.upper().find("E-MAIL")==-1) and (word[0].isupper() or (len(word)>1 and word[0]>='0' and word[0]<='9') or word in small_cases):
            finalStrList += word + " "
    i=0
    try:
        while not finalStrList[i].isupper():
            i+=1
    except:
        finalStrList = ""
    finalStrList = finalStrList[i:]
    return finalStrList.strip()


with open(filetoread,'r') as f:
    stri = ""
    for line in f:
        abc = line.split()

        if len(abc) >= 1:  # if not a blank line

            if abc[1] == "1":   #output column
                if flag == "0":  #if start of Affiliation
                    outfile.write("\n\t<Affiliation>\n\t\t")
                stri += ((abc[0].strip(',')).strip('.') + ' ')
                flag = "1"
            else:
                if flag == "1":
                    stri = cutShort(stri)
                    if stri.find(" ")==-1 and stri.isupper()==False: #Only one word which isn't an abbreviation => Can't be an affiliation [Note: May fail in cases like "Facebook", "Google", "Amazon" etc]
                        outfile.seek(-18,os.SEEK_END)
                        outfile.truncate()
                    elif stri.isdigit() and len(stri)>=5:
                        outfile.seek(-35,os.SEEK_END)
                        outfile.truncate()
                        outfile.write(" " + stri)
                        outfile.write("\n\t</Affiliation>\n")
                    else:
                        outfile.write(stri)
                        outfile.write("\n\t</Affiliation>\n")
                    flag = "0"
                    stri = ""
                
#outfile.write("\n</" + (filetoread.split(".")[0]).split("/")[-1] + ">\n\n\n")
outfile.close()

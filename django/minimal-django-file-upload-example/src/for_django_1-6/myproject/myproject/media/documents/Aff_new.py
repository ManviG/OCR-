import xml.etree.ElementTree as ET
import unicodedata
import time
import operator

country_list = ["America", "UK", "Afghanistan", "Albania", "Algeria", "Samoa", "Andorra", "Angola", "Anguilla", "Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Herzegowina", "Botswana", "Island", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Ivoire", "Croatia", "Cuba", "Cyprus", "Denmark", "Djibouti", "Timor", "Ecuador", "Egypt", "Salvador", "Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", "France","Territories", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea", "Kuwait", "Kyrgyzstan", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Rico", "Qatar", "Romania", "Russia", "Federation", "Rwanda", "Samoa", "Arabia", "Senegal", "Seychelles", "Singapore", "Slovakia", "Slovenia", "Islands", "Somalia", "South Africa", "Spain", "Lanka", "Helena", "Miquelon", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tokelau", "Tonga", "Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "Emirates", "Kingdom", "States", "Uruguay", "USA", "UAE", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe"]

#US_States = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "Hampshire", "Jersey", "York", "Carolina", "Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "Wisconsin", "Wyoming"]
US_States = []

Exceptional_names = ["MSN", "KU Leuven", "INSEAD", "ESCP Europe", "Sciences Po Paris", "ETH Zurich", "EPFL", "HKUST", "CAIDA", "BITS", "UC Berkeley", "Facebook", "Google", "Amazon", "Twitter", "MIT"]

journal_related = ["Copyright","Journal ", "JOURNAL", "ACM", "Elsevier", "ELSEVIER", "arxiv", "ARXIV", "IEEE", "ieee","Grant","GRANT","grant"]

def hasAbbreviation(string):
    string = string.split(' ')
    for word in string:
        if len(word)>=3 and word.isupper():
            return True
    return False

def isAffiliation(y,fs):
    global titleNotOver
    x=y.strip()
    x=x.strip(',')
    if len(x) <= 1:
        return "0"
    #print x
    if fs == max_font_size and titleNotOver:            #If in Title (Biggest Font Size) it can't be affiliation.
        #print x, max_font_size, fs
        titleNotOver = False
        return "0"              #Done to prevent cases when "Research" comes in title (often)
    for Journal in journal_related:
        if x.find(Journal)!=-1:
            return "0"
    if x[1]==" " or ((not x[0].isupper()) and x[1].isupper()): #Only when there was a superscript before this line (A single character might be joint to it) =>Very IMP to prevent cases in which country name is there but not as affiliation
        for country in country_list:
            if x.find(country)!=-1:
                return "1"
    if x.find("Universit")!=-1 or x.find("Univ. ")!=-1 or x.find("Cntr. ")!=-1 or x.find("Institut")!=-1 or x.find("Department")!=-1 or x.find("Centre ")!=-1 or x.find("Center ")!=-1 or x.find("School")!=-1 or x.find(" Research")!=-1 or x.find("College")!=-1 or x.find(" Lab ")!=-1 or x.find(" Lab,")!=-1 or x.find(" Labs")!=-1 or x.find("Laborator")!=-1 or x.find("Corporat")!=-1 or x.find("Academ")!=-1 or x.find("Normale")!=-1 or x.find("Polytechnique")!=-1 or x.find("Politecnic")!=-1 or x.find("Universidad")!=-1 or x.find("Ecole")!=-1 or x.find("Inc.")!=-1 or x.find("Technologies")!=-1 or x.find("faculty")!=-1 or x.find("Dept.")!=-1 or x in Exceptional_names:# or hasAbbreviation(x):
        return "1"
    return "0"

directory = "/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/"#raw_input()+"/"#/home/priyank/Desktop/Projects/pdfs/"
a_file = directory + "input_2.xml"
AffiliationOutputFile = open(a_file.split(".")[0]+'_parse.txt','w')
AffiliationOutputFile.write("0\t0\t0\n")


def isEmail(y):
    x=y.strip()
    x = x.strip('.')
    isatr = 0
    for i in range(len(x)):
        if x[i] == "@":
            isatr = 1
        if((isatr==1) and (x[i]==".") and (x[i+1]<"z" and x[i+1]>"a")):
            return "1"
    return "0"

def FindAffiliation(block,fs):
    ret = "0"
    #block = block.replace(',','#$#')
    t = block.split('#$#')
    aff = "0"
    flag = False
    for j in t:
        j = j.strip()
        p = isAffiliation(j,fs)
        if p=="1":
            ret = "1"
        if p == "1" or aff == "1":
            aff = "1"
            x = j.split(' ')
            for i in x:
                i = i.strip(".").strip(",")
                if len(i)>0:
                    if isEmail(i) == "1":
                        aff = "0"
                        AffiliationOutputFile.write("0\t0\t0\n")
                    else:
                        AffiliationOutputFile.write((i+"\t").encode("utf-8"))
                        AffiliationOutputFile.write(("1\t").encode("utf-8"))
                        AffiliationOutputFile.write(("0\n").encode("utf-8"))
                    if p == "0" and (i.replace(".","") in country_list or i in US_States):
                        aff = "0"
                        AffiliationOutputFile.write("0\t0\t0\n")
    return ret










#For Chunks


tree = ET.parse(a_file)
root = tree.getroot()

max_fs = 0
p_yloc = None
y_diff={}
fsizes = {}

for pages in root.findall('PAGE'):
    pre_y=0
    for texts in pages.findall('TEXT'):
        for token in texts.findall('TOKEN'):
            try:
                # print(token.attrib)
                fsizes[round(abs(float(token.attrib['font-size'])))]=fsizes.get(round(abs(float(token.attrib['font-size']))),0)+1
                if(p_yloc is None):
                    p_yloc=float(token.attrib['y'])
                if(float(token.attrib['font-size'])>max_fs):
                    max_fs=float(token.attrib['font-size'])
                y_diff[round(abs(float(token.attrib['y'])-pre_y))]=y_diff.get(round(abs(float(token.attrib['y'])-pre_y)),0)+1
                pre_y=float(token.attrib['y'])
            except:
                print
                # print "Oops"
max_font_size = max_fs
max_fs = 0
for shit in fsizes.keys():
    # print fsizes[shit]
    if(max_fs == 0):
        max_fs = shit
        continue
    if(fsizes[shit]>fsizes[max_fs]):
        max_fs=shit
# print max_fs
# print("fsizes!!!")
# print fsizes

# exit(0)
new_l = sorted(y_diff.iteritems(), key=operator.itemgetter(1), reverse=True)[:7]
x_l = []
# print(new_l)
for k in new_l:
    if(k[0]>6.0):
        x_l.append(k)
new_l=x_l

x_l=[]
mode=new_l[0][1]
for k in new_l:
    if(not(k[1]<=mode/2 or abs(new_l[0][0]-k[0])>=4)):
        x_l.append(k)

new_l=x_l
# print(new_l)
del x_l

limit = max([x[0] for x in new_l])+2
# print(limit)
# exit(0)



xroot = ET.Element("Document")
chunk = ET.SubElement(xroot, "chunk")
for pages in root.findall('PAGE'):
    for texts in pages.findall('TEXT'):
        for token in texts.findall('TOKEN'):
            if type(token.text) is unicode:
                word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
            else:
                word = token.text
            # print word
            if(word and len(word.replace(' ',''))>0):
                if( abs(float(token.attrib['y'])-p_yloc)>=limit):
                    chunk = ET.SubElement(xroot, "chunk")
                p_yloc = float(token.attrib['y'])
                ET.SubElement(chunk, "token", y=token.attrib['y'], font_size=token.attrib['font-size'], bold=token.attrib['bold']).text = word

tree = ET.ElementTree(xroot)
#tree.write(directory + "input_2_res.xml")
#print(tree._root)

SectionHeads = ["ABSTRACT", "INTRODUCTION", "REFERENCES"]
stringforAff = ""
count = 0
fs = 0
cnt = 0
boldness = "no"
prev_size = 0
fontSize = 0
skipThis = False
THRESHHOLD_FOR_BODY = 1800
titleNotOver = True
min_result_ys = 700 #Hold value of minimum y (topmost) where there is an affiliation so that if found above, we do not check in the footnotes
for achunk in xroot.findall('chunk'):
    stringforAff = ""
    cnt = 0
    pre_y = 0
    AllTokens = achunk.findall('token')
    if fontSize == AllTokens[0].attrib['font_size']:    #Still in body
        skipThis = False
        continue
    if len(AllTokens)<=2 and (AllTokens[0].text.upper() in SectionHeads or (len(AllTokens)>1 and AllTokens[1].text.upper() in SectionHeads)):#or AllTokens[0].attrib['bold']=="yes"):
        skipThis = True #Section Heading... Body starts from next line
        continue
    if skipThis:    #Body Starts... Record the font size of this body
        fontSize = AllTokens[0].attrib["font_size"]
        #print fontSize, AllTokens[0].text
        skipThis = False
        continue
    for tokens in AllTokens:
        
        if tokens is None or tokens.text is None:
            continue
        if float(tokens.attrib['y']) - min_result_ys >=300:    #We Found result above and this is footnote => Don't consider this block, go to the next one
            break

        prev_size = tokens.attrib['font_size']
        if pre_y == 0:
            pre_y = tokens.attrib['y']
        elif pre_y != tokens.attrib['y']:
            if pre_y < tokens.attrib['y']:
                if float(tokens.attrib['y']) - float(pre_y) < float(prev_size)/2:       #Encounter a SuperScript => New aff starts in case it is aff. 
                    if(FindAffiliation(stringforAff.replace("- #$#",""),fs)=="1"):
                        if min_result_ys>float(tokens.attrib['y']):
                            min_result_ys = float(tokens.attrib['y'])
                    AffiliationOutputFile.write("0\t0\t0\n")
                    stringforAff = stringforAff[-2:]
                else:
                    stringforAff += "#$#"

            else:
                if(FindAffiliation(stringforAff.replace("- #$#",""),fs)=="1"):
                    if min_result_ys>float(tokens.attrib['y']):
                        min_result_ys = float(tokens.attrib['y'])
                AffiliationOutputFile.write("0\t0\t0\n")
                stringforAff = ""
            pre_y = tokens.attrib['y']
        else:
            pass


        if type(tokens.text) is unicode:
            tokens.text = unicodedata.normalize('NFKD', tokens.text).encode('ascii','ignore')
        elif type(tokens.text) is str:
            tokens.text = tokens.text
        else:
            print type(tokens.text)

        stringforAff += tokens.text + " "
        try:
            fs = float(tokens.attrib['font_size'])
        except:
            pass
        cnt += 1
    
    if cnt > THRESHHOLD_FOR_BODY:
        continue
    if(FindAffiliation(stringforAff.replace("- #$#",""),fs)=="1"):
        if min_result_ys>float(tokens.attrib['y']):
            min_result_ys = float(tokens.attrib['y'])
                    
    AffiliationOutputFile.write("0\t0\t0\n")



import xml.etree.ElementTree as ET
import unicodedata
import time

country_list = ["America", "Afghanistan", "Albania", "Algeria", "Samoa", "Andorra", "Angola", "Anguilla", "Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Herzegowina", "Botswana", "Island", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Ivoire", "Croatia", "Cuba", "Cyprus", "Denmark", "Djibouti", "Timor", "Ecuador", "Egypt", "Salvador", "Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", "France","Territories", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea", "Kuwait", "Kyrgyzstan", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Rico", "Qatar", "Romania", "Russia", "Federation", "Rwanda", "Samoa", "Arabia", "Senegal", "Seychelles", "Singapore", "Slovakia", "Slovenia", "Islands", "Somalia", "South Africa", "Spain", "Lanka", "Helena", "Miquelon", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tokelau", "Tonga", "Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "Emirates", "Kingdom", "States", "Uruguay", "USA", "UAE", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe"]

US_States = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "Hampshire", "Jersey", "York", "Carolina", "Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "Wisconsin", "Wyoming"]

Exceptional_names = ["MSN", "KU Leuven", "INSEAD", "ESCP Europe", "Sciences Po Paris", "ETH Zurich", "EPFL"]



def isAffiliation(y,fs):
    x=y.strip()
    x=x.strip(',')
    #print x
    if fs == max_fs:            #If in Title (Biggest Font Size) it can't be affiliation.
        #print x
        return "0"              #Done to prevent cases when "Research" comes in title (often)
    if x.find("Universit")!=-1 or x.find("Institut")!=-1 or x.find(" Research")!=-1 or x.find("College")!=-1 or x.find(" Labs")!=-1 or x.find("Laboratories")!=-1 or x.find("Corporat")!=-1 or x.find("Academy")!=-1 or x.find("Normale")!=-1 or x.find("Polytechnique")!=-1 or x.find("Politecnic")!=-1 or x.find("Universidad")!=-1 or x.find("Ecole")!=-1 or x in Exceptional_names:
        #print x
        t = x.split(' ')
        countsmall = 0
        countall = 0
        for word in t:
            countall += 1
            if word == word.lower():
                countsmall += 1
        if countsmall > 3:
                return "0"
        return "1"
    return "0"

directory = "/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/"
a_file = directory + "input.xml"
AffiliationOutputFile = open(a_file.split(".")[0]+'_parse.txt','w')
AffiliationOutputFile.write("0\t0\t0\n")

def FindAffiliation(stri,fs,NoSecText):
    l = []
    a = []
    stri = ((((((((((stri.strip('1')).strip('2')).strip('3')).strip('4')).strip('5')).strip('6')).strip('7'))).strip('8')).strip('9')).strip('0')
    t1 = stri.split("#@# ")
    stri = t1[0]
    t = stri.split(',')
    aff = "0"
    flag = False
    for j in t:
        j = j.strip()
        p = isAffiliation(j,fs)
        if p == "1" or aff == "1":
            aff = "1"
            x = j.split(' ')
            for i in x:
                i = i.strip(".").strip(",")
                if len(i)>0:
                    AffiliationOutputFile.write((i+"\t").encode("utf-8"))
                    AffiliationOutputFile.write(("1\t").encode("utf-8"))
                    AffiliationOutputFile.write(("0\n").encode("utf-8"))
                    if p == "0" and (i in country_list or i in US_States):
                        return

    if NoSecText == True:
        return
    stri = t1[1]
    stri = stri.split(' ')
    take = "0"
    if aff == "1":
        for word in stri:
            if word.strip(',') in country_list or word.strip(',') in US_States:
                take = "1"
                break
        for i in stri:
            if take == "1":
                AffiliationOutputFile.write((i+"\t").encode("utf-8"))
                AffiliationOutputFile.write(("1\t").encode("utf-8"))
                AffiliationOutputFile.write(("0\n").encode("utf-8"))
                if p == "0" and (i in country_list or i in US_States):
                    flag = "1"
                    break
#to = time.time()
tree = ET.parse(a_file)
#t1 = time.time()
#print t1-to
root = tree.getroot()
max_fs = 0
count = 0
for pages in root.findall('PAGE'):
    count+=1
    if count>1:
        break
    for texts in pages.findall('TEXT'):
        for tokens in texts.findall('TOKEN'):
            if tokens is None:
                continue
            try:
                if(float(tokens.attrib['font-size'])>max_fs):
                    max_fs=float(tokens.attrib['font-size'])
            except:
                pass
#print max_fs


stringForAff = ""
count = 0
SecondText = True
for pages in root.findall('PAGE'):
    count+=1
    NoSecText = False
    if count>2:
        break
    texts = pages.findall('TEXT')
    i = 0
    while(i < len(texts)):
        tokens = texts[i].findall('TOKEN')
        NoSecText = False
        for j in range(len(tokens)):
            if type(tokens[j].text) is not str:
                continue
            font = tokens[j].attrib['font-name']
            if SecondText == False:
                if font != token[j].attrib['font-name']:
                    NoSecText = True
                    break
            if type(tokens[j].text) is unicode:
                stringForAff += unicodedata.normalize('NFKD', tokens[j].text).encode('ascii','ignore')
            else:
                stringForAff += tokens[j].text
            stringForAff += " "
        SecondText = ~SecondText
        stringForAff += "#@# "
        if(SecondText == True):
            FindAffiliation(stringForAff,float(tokens[j].attrib['font-size']), NoSecText)
            stringForAff = ""
            AffiliationOutputFile.write("0\t0\t0\n")
            i -= 1
        i+=1
#t3 = time.time()
#print t3 - t1


from __future__ import division
import xml.etree.ElementTree as ET
import unicodedata
import re
import os
import string
import sys
import types
import copy

root_folder = ''

# Binary coverter for strings
def binary(x):
    if x == "yes":
        return "1"
    return "0"


def search_name_year(Reference,name,year):
    name = name.replace(" ","")
    for i in range(len(Reference)):
        refs = Reference[i]    
        if name in refs and year in refs:
            return i
    return 0                                  # make it -1
		
def search_doublename(Reference,name1,name2,year):
    name1 = name1.replace(" ","")
    name2 = name2.replace(" ","")
    for i in range(len(Reference)):
        refs = Reference[i]
        if name1 in refs and name2 in refs and year in refs:
            return i		
    return 0                                 # make it -1


directory = "/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/"
a_file = directory + "input.xml"
cit2ref = open("inputcit2ref.txt",'w')
count = 0
tree = ET.parse(a_file)
root = tree.getroot()

flag = False
Reference = []

for pages in root.findall('PAGE'):
    #pre_y = 0;
    texts = pages.findall('TEXT')
    for i  in range(len(texts)):
        #tot_txt += 1        
        tokens = texts[i].findall('TOKEN')        
        if flag==False:            
            for j in range(len(tokens)):

                if type(tokens[j].text) is unicode:
                    word = unicodedata.normalize('NFKD', tokens[j].text).encode('ascii','ignore')
                else:
                    word = tokens[j].text
                    if isinstance(word, types.NoneType): 
                        #print " word type is NoneType" 
                        continue

                if(len(word.replace(' ',''))>0):
                    if ((word=="REFERENCES" or word=="References") and binary(tokens[j].attrib['bold'])):
                        #print word + " now that's it"
                        flag = True
                        first_text = True
                        continue
        else:
            cur_x = texts[i].attrib['x']
            cur_y = texts[i].attrib['y'] 
            cur_size = float(tokens[0].attrib['font-size'])
            cur_font = tokens[0].attrib['font-name']
            cur_font = cur_font.lower()
            cur_bold = tokens[0].attrib['bold']
            cur_italic = tokens[0].attrib['italic']
         
            if first_text:              
                start_ref = cur_x
                idx = 0
                Reference.append("")
                first_height = float(texts[i+1].attrib['y']) - float(cur_y)
                first_size = float(tokens[0].attrib['font-size'])
                first_font = tokens[0].attrib['font-name'].lower()
                first_lower = first_font.lower()
                first_bold = tokens[0].attrib['bold']
                first_italic = tokens[0].attrib['italic']
                first_text = False                
            else:               
                if (float(cur_y) < float(prev_y)):
                    if cur_size < first_size - 0.1 or cur_size > first_size + 0.1 or cur_font != first_font or cur_bold != first_bold or cur_italic != first_italic:
                        continue
                    k = i + 1
                    while(True):
                        if k >= len(texts):
                            start_ref = cur_x
                            break
                        next_x = texts[k].attrib['x']
                        if(float(next_x) > float(cur_x) + 0.1):
                            start_ref = cur_x
                            idx = idx + 1
                            Reference.append("")
                            break
                        if(float(next_x) < float(cur_x) - 0.1):
                            start_ref = next_x
                            break
                        k = k + 1
                else:
                    if float(cur_y) - float(prev_y) > 3 * first_height:
                        continue                                         
                    if (float(cur_x) < float(start_ref) + 0.1 ):
                        idx = idx + 1
                        Reference.append("")   
             
            prev_x = cur_x
            prev_y = cur_y 

            for j in range(len(tokens)):

                if type(tokens[j].text) is unicode:
                    word = unicodedata.normalize('NFKD', tokens[j].text).encode('ascii','ignore')
                else:
                    word = tokens[j].text
                    if isinstance(word, types.NoneType): 
                        print " word type is NoneType" 
                        continue
                if(len(word.replace(' ',''))>0):
                    Reference[idx] += word
                    Reference[idx] += " "
					
#cit2ref.write("<?xml version=\"1.0\" ?>\n")
for i in range(len(Reference)):
    cit2ref.write("<Reference")
    cit2ref.write(" id=\"" + str(i + 1) + "\" >");
    cit2ref.write(Reference[i]);
    cit2ref.write("</Reference>\n\n")
cit2ref.write("\n\n")

###########################################
citations_no = 0
flag = True

for pages in root.findall('PAGE'):
    count+=1    
    texts = pages.findall('TEXT')
    for i  in range(len(texts)):
        line = ""
        tokens = texts[i].findall('TOKEN')
        for j in range(len(tokens)):            
            if type(tokens[j].text) is unicode:
                word = unicodedata.normalize('NFKD', tokens[j].text).encode('ascii','ignore')

                
            else:
                word = tokens[j].text
                if isinstance(word, types.NoneType):
                    continue
                if (len(word)>0) and flag==True:
                    if ((word=="REFERENCES" or word=="References") and binary(tokens[j].attrib['bold'])):
                        flag = False
                    word += " "
                    line += word
    
        if flag==True:    
            regex = re.compile("([A-Z][a-zA-Z]* et al[.] \[(\d{1,3})\])")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    cit2ref.write("<citation ref_id=\"" + a[1] + "\"")
                    cit2ref.write("  reference=\"" + Reference[int(a[1])-1] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n")
                    


            regex = re.compile("([A-Z][a-zA-Z]* \[(\d{2})\])")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    cit2ref.write("<citation ref_id=\"" + a[1] + "\"")
                    cit2ref.write("  reference=\"" + Reference[int(a[1])-1] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")
            
            regex = re.compile("([A-Z][a-zA-Z]* et al[.][ ]*\[(\d{1})\])")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    cit2ref.write("<citation ref_id=\"" + a[1] + "\"")
                    cit2ref.write("  reference=\"" + Reference[int(a[1])-1] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")
            
            regex = re.compile("(([A-Z][a-zA-Z]*) et al[.][,] (\d{4}))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_name_year(Reference,a[1],a[2])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")
                
            regex = re.compile("(([A-Z][a-zA-Z]*) et al[.] (\d{4}))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_name_year(Reference,a[1],a[2])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")                

            regex = re.compile("(([A-Z][a-zA-Z]*) and ([A-Z][a-zA-Z]*) \((\d{4})\))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_doublename(Reference,a[1],a[2],a[3])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")

        
            regex = re.compile("(([A-Z][a-zA-Z]*) and ([A-Z][a-zA-Z]*)[,] (\d{4}))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_doublename(Reference,a[1],a[2],a[3])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")             
        
            regex = re.compile("(([A-Z][a-zA-Z]*)[,] (\d{4}))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_name_year(Reference,a[1],a[2])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")
            
            regex = re.compile("(([A-Z][a-zA-Z]*) (\d{4}))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_name_year(Reference,a[1],a[2])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")                   
        
            regex = re.compile("(([A-Z][a-zA-Z]*) \((\d{4}[a-z]*)\))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_name_year(Reference,a[1],a[2])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")  
                
            regex = re.compile("(([A-Z][a-zA-Z]*) et al[.], (\d{4}[a-z]))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_name_year(Reference,a[1],a[2])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")  
        
            regex = re.compile("(.*?\((.*?)\))")
            result = re.findall(regex, line)
            if len(result) > 0:
                    for a in result:
                        citations_no += 1
                        temp = a[0]
                        regex1 = re.compile("\d{4}$")
                        cits = a[1].split(';')
                        for citation in cits:
                            citation = citation.replace(" ","")
                            if regex1.match(citation):
                                #print citation
                                #print "a"
                                #print line
                                temp = temp.replace(citation,'CITATION')
                                #print Reference[int(citation)-1]
                                #print
                    line = line.replace(a[0],temp)
            
            regex = re.compile("(.*?\[(.*?)\])")
            result = re.findall(regex, line)
            if len(result) > 0:
                for a in result:
                    citations_no += 1
                    temp = a[0]
                    regex1 = re.compile("\d{1,3}$")
                    cits = a[1].split(',')
                    #print cits
                    #print "b"
                    for citation in cits:
                        citation = citation.replace(" ","")
                        if regex1.match(citation):
                            #print citation
                            #print "a"
                            #print line
                            temp = temp.replace(citation,'CITATION')
                            cit2ref.write("<citation ref_id=\"" + citation + "\"")
                            cit2ref.write("  reference=\"" + Reference[int(citation)-1] + "\" >")
                            cit2ref.write(a[0] + "</citation>\n\n")                              
                line = line.replace(a[0],temp)

            regex = re.compile("(([A-Z][a-zA-Z]*) et al[.], (\d{4}[a-z]))")    
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_name_year(Reference,a[1],a[2])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n") 


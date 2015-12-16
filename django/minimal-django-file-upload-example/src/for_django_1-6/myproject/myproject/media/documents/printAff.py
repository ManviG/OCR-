flag = "0"   # to check if a Affiliation is already going on
directory = "/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/"
filetoread = directory + "input_parse.txt"
outfile = open(directory + "input_AllAffiliations.txt",'w')
#outfile.write("<" + (filetoread.split(".")[0]).split("/")[-1] + ">\n")
with open(filetoread,'r') as f:
    for line in f:
        abc = line.split()

        if len(abc) >= 1:  # if not a blank line

	        if abc[1] == "1":   #output column
	        	if flag == "0":  #if start of Affiliation
	        		outfile.write("\n\t<Affiliation>\n\t\t")
	        	outfile.write((abc[0].strip(',')).strip('.') + ' ')
	        	flag = "1"
	        else:
			if flag == "1":
				outfile.write("\n\t</Affiliation>\n")
				flag = "0"
	        	
#outfile.write("\n</" + (filetoread.split(".")[0]).split("/")[-1] + ">\n\n\n")
outfile.close()

author = "barno"

directory = '/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/'


flag = "0"   # to check if a title is already going on
end = 0
titl = 0;
# print("<?xml version=\"1.0\" ?>\n")
# print("<title_author>\n")
fi = open(directory + 'test_aut.txt','w')
titl_done = 0
tokens = 0
caps = 0
upper = 0
titl_ext = "<?xml version=\"1.0\" ?>\n<title_author>\n"
with open(directory + 'final.txt','r') as f:
	for line in f:
		abc = line.split()

		if len(abc) > 1:  # if not a blank line

			# print "***" + abc[0]
			abc[0] = abc[0].replace('&','&amp;')

			# if(abc[9]=="00"):
			# 	print

			if titl_done == 0:
			    if abc[9] == "1":   #output column
			    	titl = 1;
			    	if flag == "0":  #if start of title
			    		titl_ext = titl_ext + "\t<title>\n\t"
			    	titl_ext = titl_ext + abc[0] + " "
			    	flag = "1"
			    else:
			    	if abc[0] != "0" and flag == "1":
			    		if(titl==1):
			    			# print("\n\t</title>")
			    			titl_done = 1
			    			titl = 0;
			    		flag = "0"
			    		# print

			    if abc[9] == "2": #first name
			    	if(titl==1):
			    			# print("\n\t</title>")
			    			titl_done = 1
			    			titl = 0;
			    	x = abc[0].strip(',')
			    	# print("\t<name>\n\t\t<first_name> " + x + " </first_name>\n")

			    # if abc[9] == "3": #middle name
			    # 	x = abc[0].strip(',')
			    # 	print("\t\t<middle_name> " + x + " </middle_name>\n")

			    # if abc[9] == "4":  #last name
			    # 	x = abc[0].strip(',')
			    # 	print("\t\t<last_name> " + x + " </last_name>\n\t</name>")

			else:
				if abc[9] == '1':
					titl_ext = titl_ext + abc[0] + " "
					
				if abc[5] == '0': 
					if caps == 1:
						fi.write("00\t00\t00\t00\t00\t00\t00\t00\t00\n")
					caps = 0
				if abc[5] == '1': 
					if caps == 0:
						fi.write("00\t00\t00\t00\t00\t00\t00\t00\t00\n")
					caps = 1

				# if not abc[0].isupper(): 
				# 	if upper == 1:
				# 		fi.write("00\t00\t00\t00\t00\t00\t00\t00\t00\n")
				# 	upper = 0
				# if abc[0].isupper(): 
				# 	if upper == 0:
				# 		fi.write("00\t00\t00\t00\t00\t00\t00\t00\t00\n")
				# 	upper = 1

				if ',' in abc[0]:
					if len(abc[0]) > 1:
					    line = line.strip(abc[0])
					    abc[0] = abc[0].strip(',')
					    line = abc[0] + line + ',' + line

			   	fi.write(line)
			   	if abc[0] != '00':
			   		tokens = tokens + 1
			   	if tokens >= 100:
			   		break

fi.close()	
print titl_ext
print "\n\t</title>"        	
# print("</title_author>\n")
author = "barno"
import nltk

directory = '/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/'


flag = "0"   # to check if a title is already going on
end = 0
titl = 0;
affils = []

with open(directory + 'input_AllAffiliations.txt','r') as f:
	for line in f:
		if "Affiliation" in line:
			continue
		line = line.strip('\t')
		line = line.strip('\n')
		affils.append(line)

fout = open(directory + 'TitleAuthor.xml','a')

titl_done = 0
tokens = 0
caps = 0
name = ""
cont = 0
pending_names = []
with open(directory + 'final_aut.txt','r') as f:
	for line in f:
		# print lineno
		# lineno = lineno + 1 
		abc = line.split()

		if len(abc) == 11:  # if not a blank line
			# print "yo1"
			# print "***" + abc[0]
			abc[0] = abc[0].replace('&','&amp;')

			if int(abc[9]) != 0 or int(abc[10]) != 0:
				# print abc[9]
				# print abc[10]
				if abc[0]!=',':
					name = name + abc[0] + " "
					continue

			# print name

			if len(name.split()) > 1:
				# print "yo2"
				for a in affils[1:]:
					# a = a.strip('.')
					# print a 
					# print name.replace('.','')
					if a in name.replace('.',''):
						# print "yo"
						if len(a.split()) > 0:

							name = name.replace('.','')
							# print name
							pending_names.append(name.split(a)[0])
							if len(name.split(a))>0:
								name = name.split(a)[1]
							# name = names.split(a)[0]						
							# name = name.replace(a,'')

				# print pending_names

				for name in pending_names:
					tag = nltk.pos_tag(name.split())
					propernoun = [word for word,pos in tag if pos == 'NNP']

					if len(propernoun) == len(name.split()):
						names = name.split()
						# print name
						wrt = "\t<name>\n"
						wrt = wrt + "\t\t<first_name>\n"
						wrt = wrt + "\t\t\t" + names[0] + "\n"
						wrt = wrt + "\t\t</first_name>\n"
						if len(names)>2:
							# print len(name)
							wrt = wrt + "\t\t<middle_name>\n"
							wrt = wrt + "\t\t\t"
							for n in names[1:-1]:
								wrt = wrt + n + " "
							wrt = wrt + "\n"
							wrt = wrt + "\t\t</middle_name>\n"
						wrt = wrt + "\t\t<last_name>\n"
						wrt = wrt + "\t\t\t" + names[-1] + "\n"
						wrt = wrt + "\t\t</last_name>\n" 
						wrt = wrt + "\t</name>\n\n"
						fout.write(wrt)
					name = ""

				if len(pending_names)>0:
					pending_names = []
					continue

				# print name
				tag = nltk.pos_tag(name.split())
				propernoun = [word for word,pos in tag if pos == 'NNP']

				if len(propernoun) == len(name.split()):
					name = name.split()
					# print name
					wrt = "\t<name>\n"
					wrt = wrt + "\t\t<first_name>\n"
					wrt = wrt + "\t\t\t" + name[0] + "\n"
					wrt = wrt + "\t\t</first_name>\n"
					if len(name)>2:
						# print len(name)
						wrt = wrt + "\t\t<middle_name>\n"
						wrt = wrt + "\t\t\t"
						for n in name[1:-1]:
							wrt = wrt + n + " "
						wrt = wrt + "\n"
						wrt = wrt + "\t\t</middle_name>\n"
					wrt = wrt + "\t\t<last_name>\n"
					wrt = wrt + "\t\t\t" + name[-1] + "\n"
					wrt = wrt + "\t\t</last_name>\n" 
					wrt = wrt + "\t</name>\n\n"
					fout.write(wrt)

				name = ""

fout.write("</title_author>")
fout.close()
# fi.close()
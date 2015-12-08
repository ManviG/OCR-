Directory=/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents

$Directory/files/pdftoxml.linux64.exe.1.2_7 $Directory/input.pdf

# barno
python $Directory/files/TitleAuthor_parse.py
python $Directory/files/extra.py
crf_test -m $Directory/files/model_new.txt $Directory/test_file.txt > $Directory/final.txt
python $Directory/files/printNameAuthor.py > $Directory/TitleAuthor.xml
# barno

#samuel
#rm $Directory/input.pdf
rm -r $Directory/input.xml_data
python $Directory/files/Secmapping.py > $Directory/Secmap.xml
#samuel

#Priyank
python $Directory/Aff_new.py
python $Directory/Email_new.py
python $Directory/printEmail.py
python $Directory/printAff.py
#Priyank

#Tulasi
python $Directory/cit2ref.py
#Tulasi

$Directory/Mapping.sh

#ayush
python $Directory/url.py > $Directory/URLop.txt
python $Directory/footnotes.py > $Directory/FOOTNOTEop.txt
python $Directory/tables_figures.py > $Directory/TABFIGop.txt
#ayush

rm $Directory/input.xml

#$Directory/Clean.sh

$Directory/eval_op.sh

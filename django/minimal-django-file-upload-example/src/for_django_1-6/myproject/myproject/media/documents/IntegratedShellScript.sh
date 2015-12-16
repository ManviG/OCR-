Directory=/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents

$Directory/files/pdftoxml.linux64.exe.1.2_7 $Directory/input.pdf

#samuel
#rm $Directory/input.pdf
rm -r $Directory/input.xml_data
echo "1/10 section starting"
python $Directory/files/Secmapping.py > $Directory/Secmap.xml
echo "1/10 section done"
#samuel

# barno
python $Directory/files/TitleAuthor_parse.py
echo "2/10 titleauthor parse done"
python $Directory/files/extra.py
echo "3/10 extra done"
crf_test -m $Directory/files/model_all_com.txt $Directory/test_file.txt > $Directory/final.txt
python $Directory/files/TitleAuthorFinalTouch.py
echo "4/10 final touch done"
python $Directory/files/printTitle.py > $Directory/TitleAuthor.xml
crf_test -m $Directory/files/model_all_com.txt $Directory/test_aut.txt > $Directory/final_aut.txt
echo "5/10 title done"
# barno

#Priyank
echo "6/10 palod starting"
python $Directory/Aff_new.py
python $Directory/Email_new.py
python $Directory/printEmail.py
python $Directory/printAff.py
echo "6/10 palod done"
#Priyank
echo "7/10 getting author"
python $Directory/files/printAuthor.py
echo "7/10 getting author done"
#Tulasi
echo "8/10 cit starting"
python $Directory/cit2ref.py
echo "8/10 cit done"
#Tulasi
echo "9/10 mapping starting"
$Directory/Mapping.sh
echo "9/10 mapping done"
#ayush
echo "10/10 ayush starting"
python $Directory/url.py > $Directory/URLop.txt
python $Directory/footnotes.py > $Directory/FOOTNOTEop.txt
python $Directory/tables_figures.py > $Directory/TABFIGop.txt
echo "9/9 ayush done"
#ayush

rm $Directory/input.xml

#$Directory/Clean.sh

$Directory/eval_op.sh

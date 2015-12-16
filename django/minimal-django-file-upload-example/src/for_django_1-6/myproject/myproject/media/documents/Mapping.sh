# echo "mail"
Directory=/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents

python $Directory/printMailformap.py <<EOF
$f
EOF

# echo "name"
python $Directory/printnameformap.py
# echo "map"
python $Directory/email_matching.py > $Directory/map.txt
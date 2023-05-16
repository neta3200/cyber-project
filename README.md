# cyber-project
Cyber project for HIT college course.

Prepare in advanced:
    pip install django-extensions Werkzeug
    pip install pyOpenSSL





Windows Path for hosts file : C:\Windows\System32\drivers\etc\
Linux: /etc/hosts
add to hosts file in your system:
    127.0.0.1 cyber


Run the Server with port https ( port 443 ) with the command:
    python manage.py runserver_plus 127.0.0.1:443 --cert-file certs/cyber.pem --key-file certs/cyberprivate.pem
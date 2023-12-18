from os import system

from time import sleep

sleep(5)
system('py manage.py makemigrations shop_app shop_auth')
system('py manage.py migrate')
sleep(5)
system('py manage.py makemigrations shop_app')
system('py manage.py migrate')
system('py manage.py runserver')
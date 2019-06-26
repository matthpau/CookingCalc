#!/usr/bin/env bash

#workon matthpau.pythonanywhere.com
#cd matthpau.pythonanywhere.com/CookingCalc

#if need to set permissions:

#chmod u+x deploy_server.sh

#./deploy_server



#couldn't get it to work with the git pull inside the comment
#git pull https://matthpau:6N0k0vg6@github.com/matthpau/CookingCalc
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata dumps/MeatType.json
python manage.py loaddata dumps/CookingLevel.json
python manage.py loaddata dumps/CookingInfo.json
python manage.py loaddata dumps/Converter.json





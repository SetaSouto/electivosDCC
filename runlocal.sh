# Script that automatizes deployment of electivosDCC in localhost
#!/bin/bash

FRONTDIR=$PWD/front
BASEDIR=$PWD

git submodule init 
git submodule update

# Install NPM dependencies
cd $FRONTDIR
npm install
npm run build

cd $BASEDIR

# Virtual Environment
if [[ ! -e "venv/bin/python3" ]]; then
    echo "Creating virtual environment..."
    virtualenv venv --python=python3
fi
source venv/bin/activate

# Django
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver &
P1=$! # Save PID

cd $FRONTDIR

npm run start &
P2=$! # Save PID

wait $P1 $P2

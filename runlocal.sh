# Script that automatizes deployment of electivosDCC in localhost
#!/bin/bash

FRONTDIR=$PWD/electivosDCC-frontend
HOME=$PWD

# Install NPM dependencies
cd $FRONTDIR
npm install
npm run build

# Update
cp $FRONTDIR/build/{,asset-}manifest.json $HOME/electivos/static/electivos -v
rm $HOME/electivos/static/electivos/css/* -v
cp $FRONTDIR/build/static/css/*.css $HOME/electivos/static/electivos/css/ -v
rm $HOME/electivos/static/electivos/js/* -v
cp $FRONTDIR/build/static/js/*.js $HOME/electivos/static/electivos/js/ -v

cd $HOME

# FIXME Editar templates/electivos/index.html (línea 13 y 18) y actualizar los hashes
# Se podría hacer con `sed`

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

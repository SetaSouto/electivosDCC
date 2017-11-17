# Script that automatizes deployment of electivosDCC in localhost
#!/bin/bash

HOME=$PWD

# Install NPM dependencies
cd $HOME/electivosDCC-frontend
# npm install
# npm run build

# Update
cp build/{,asset-}manifest.json ../electivos/static/electivos -v
rm ../electivos/static/electivos/css/* -v
cp build/static/css/*.css ../electivos/static/electivos/css/ -v
rm ../electivos/static/electivos/js/* -v
cp build/static/js/*.js ../electivos/static/electivos/js/ -v

cd $HOME/

# TODO Editar templates/electivos/index.html (línea 13 y 18) y actualizar los hashes
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

cd $HOME/electivosDCC-frontend

npm run start &
P2=$! # Save PID

wait $P1 $P2

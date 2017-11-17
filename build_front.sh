#!/bin/bash
echo "Updating front..."
git submodule update --recursive
cd electivosDCC-frontend
npm install
npm run build
cd ..
echo "Update done"

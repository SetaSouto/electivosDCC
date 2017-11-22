#!/bin/bash
echo "Updating front..."
cd electivosDCC-frontend
npm install
npm run build
cd ..
echo "Update done"

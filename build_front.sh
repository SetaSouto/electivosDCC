#!/bin/bash
git submodule update --recursive
cd electivosDCC-frontend
npm run build
cd ..

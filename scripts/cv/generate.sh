#!/bin/bash
set -e
set +x

generatecv () {
  INPUT_FILENAME="$1.yaml" make clean all
  mv build/cv.pdf "../../$1.pdf"
}

cvs=("cv_backend" "cv_frontend" "cv_art")

cd ../
source venv/bin/activate
cd cv

for cv in "${cvs[@]}"
do
  generatecv "$cv"
done

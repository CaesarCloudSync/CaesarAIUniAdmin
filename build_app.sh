#!/bin/bash
artifact_repo="us-central1-docker.pkg.dev/caesaraiapis/caesaraiapis"
image="caesaraiaptemotj"

newv=$(head -c 32 /dev/urandom | sha256sum | cut -d' ' -f1)

# Auth GCP Cloud
gcloud auth application-default login

full_image="$artifact_repo/$image:$newv"
export FULL_IMAGE=$full_image
export IMAGE=$image
export NEWV=$newv

# Push Docker
docker compose build
docker push $full_image


export TF_VAR_image=$full_image
echo $full_image
cd deployment
# Terraform Push Google Cloud
terraform init
terraform plan 
terraform apply -auto-approve
cd ..
# Push Github
git add .
git commit -m "$1"
git push origin -u main:main

docker compose up






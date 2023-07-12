#!/usr/bin/env bash

set -ex

image=$1
region=$2
tag=${3:-latest}

if [ "$image" == "" ]
then
    echo "Usage: $0 <image-name> <region> [tag]"
    exit 1
fi

chmod +x src/train
chmod +x src/serve

account=$(aws sts get-caller-identity --query Account --output text)

if [ $? -ne 0 ]
then
    echo "Failed to get Account"
    exit 255
fi

if [ -z "$region" ]
then
    region=$(aws configure get region)
fi

aws ecr describe-repositories --repository-names "${image}" > /dev/null 

if [ $? -ne 0 ]
then
    echo "Repository does not exist. Creating repository..."
    aws ecr create-repository --repository-name "${image}" > /dev/null

    if [ $? -ne 0 ]
    then
        echo "Failed to create repository"
        exit 255
    fi
fi

version=0
tag_name="${tag}${version}"
exist=$(aws ecr describe-images --repository-name ${image} --region ${region} --query 'imageDetails[].imageTags[]' --output text | grep -o -w ${tag_name})

while [[ "${exist}" != "" ]]; do
  version=$((version+1))
  tag_name="${tag}${version}"
  exist=$(aws ecr describe-images --repository-name ${image} --region ${region} --query 'imageDetails[].imageTags[]' --output text | grep -o -w ${tag_name})
done

fullname="${account}.dkr.ecr.${region}.amazonaws.com/${image}:${tag_name}"

aws ecr get-login-password --region "${region}" | docker login --username AWS --password-stdin "${account}".dkr.ecr."${region}".amazonaws.com

docker build  -t ${image} .
docker tag ${image} ${fullname}

docker push ${fullname}

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

echo "Fetching AWS account details..."
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

echo "Checking if ECR repository exists..."
repositoryExists=$(aws ecr describe-repositories --region "${region}" --query 'repositories[?repositoryName==`'$image'`]' --output text)

if [ -z "$repositoryExists" ]
then
    echo "Repository does not exist. Creating repository..."
    aws ecr create-repository --repository-name "${image}" --region "${region}" > /dev/null

    if [ $? -ne 0 ]
    then
        echo "Failed to create repository"
        exit 255
    fi
fi

version=0
tag_name="${tag}${version}"

echo "Checking if images exist in the repository..."
imageDetails=$(aws ecr describe-images --repository-name ${image} --region ${region} --output text 2>/dev/null)

if [ $? -eq 0 ] && [ ! -z "$imageDetails" ]
then
    exist=$(echo $imageDetails | grep -o -w ${tag_name})

    while [[ "${exist}" != "" ]]; do
      version=$((version+1))
      tag_name="${tag}${version}"
      exist=$(echo $imageDetails | grep -o -w ${tag_name})
    done
fi

fullname="${account}.dkr.ecr.${region}.amazonaws.com/${image}:${tag_name}"

echo "Logging into ECR..."
aws ecr get-login-password --region "${region}" | docker login --username AWS --password-stdin "${account}".dkr.ecr."${region}".amazonaws.com

echo "Building Docker image..."
docker build  -t ${image} .

echo "Tagging Docker image..."
docker tag ${image} ${fullname}

echo "Pushing Docker image to ECR..."
docker push ${fullname}

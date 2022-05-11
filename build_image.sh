#! /bin/sh

echo "Building SyntaClean";
docker build . -t syntaclean:latest;
if [ $? -ne 0 ]
then 
    echo "Failed to build the image, error code: $?";
    exit;
fi;
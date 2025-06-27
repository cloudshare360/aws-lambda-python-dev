#!/bin/bash

# Create project directory
mkdir -p aws-s3-crud
cd aws-s3-crud || exit

# Create root-level files
touch app.py
touch requirements.txt
touch s3_crud_stack.py

# Create lambda directory and its files
mkdir -p lambda
cd lambda || exit
touch requirements.txt
touch handler.py

echo "Folder structure and files created successfully!"
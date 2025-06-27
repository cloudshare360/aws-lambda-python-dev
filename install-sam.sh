# Update package info and install dependencies
sudo apt-get update
sudo apt-get install -y unzip curl

# Download latest SAM CLI Linux binary
curl -Lo sam-installation.zip https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip

# Unzip the package
unzip sam-installation.zip -d sam-installation

# Run the install script with sudo
sudo ./sam-installation/install

# Clean up install files
rm -rf sam-installation sam-installation.zip

# Verify the installation
sam --version

#!/bin/bash
apt-get update -y
apt-get install git -y
cd $HOME
git clone https://github.com/samsesh/SocialBox-Termux.git 
cd SocialBox-Termux
chmod +x install-sb.sh
bash install-sb.sh
clear
bash SocialBox.sh
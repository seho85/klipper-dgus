#!/bin/bash

echo "#####################################"
echo "DGUS for Klipper (MainsailOS Install)"
echo "#####################################"

#Check that script is exectuted in klipper-dgus folder
if [ "${0%/*}" != "." ]
    then echo "The script needs to be runned from 'klipper-dgus' folder"
    exit
fi

#Install python3-venv
echo -e "\nInstalling python3-venv package"
sudo apt-get install python3-venv -y

echo -e "\nCreating Python Virtual Environment"

if [ -d ./venv ]; then
    echo "Found existing Python Virtual Environment"
    echo "Removing it..."
    rm -rf ./venv
fi

python3 -m venv venv
echo "Created Python Virtual Environment"


echo -e "\nActivating Python Virtual Environment"
source ./venv/bin/activate

echo -e "\nInstalling python dependencies"
pip3 install -r requirements.txt

echo -e "\nCopying config to klipper_config"
conf_dir=/home/$(whoami)/klipper_config/dgus_display
cp -r config $conf_dir

echo -e "\nCreating systemd service (autostart)"

#replace variables in template
cp klipper_dgus.service.templ klipper_dgus.service.tmp
dgus_dir=$(pwd)
#set dgus-klipper folder in service
sed -i "s|<dgus_dir>|$dgus_dir|g" klipper_dgus.service.tmp
sed -i "s|<config_dir>|$conf_dir|g" klipper_dgus.service.tmp

echo -e "\nInstalling DGUS for Klipper Service"
sudo cp klipper_dgus.service.tmp /etc/systemd/system/klipper_dgus.service
rm klipper_dgus.service.tmp

echo -e "\nReloading systemd services..."
sudo systemctl daemon-reload

echo -e "\nEnabling dgus_klipper.service"
sudo systemctl enable klipper_dgus.service

echo -e "\nStarting initial configuration"
echo -e "\n"
python3 src/config_edit.py -c $conf_dir

echo -e "\nDisplay should be available in arround 15 seconds"
sudo systemctl start klipper_dgus

exit



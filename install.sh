#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SERVICE_NAME=$(basename $SCRIPT_DIR)

# set permissions for script files
chmod 744 $SCRIPT_DIR/$SERVICE_NAME.py
chmod 744 $SCRIPT_DIR/install.sh
chmod 744 $SCRIPT_DIR/restart.sh
chmod 744 $SCRIPT_DIR/uninstall.sh
chmod 755 $SCRIPT_DIR/service/run

if [ ! -f $SCRIPT_DIR/ve_utils.py ]
then
    echo "File ve_utils.py does not exist in folder"
    wget https://raw.githubusercontent.com/victronenergy/velib_python/master/ve_utils.py
else
    echo "File ve_utils.py found."
fi

if [ ! -f $SCRIPT_DIR/vedbus.py ]
then
    echo "File vedbus.py does not exist in folder"
    wget https://raw.githubusercontent.com/victronenergy/velib_python/master/vedbus.py
else
    echo "File vedbus.py found."
fi

# create sym-link to run script in deamon
ln -s $SCRIPT_DIR/service /service/$SERVICE_NAME

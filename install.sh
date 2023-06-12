#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
LIB_DIR=/data/etc/vebus
SERVICE_NAME=$(basename $SCRIPT_DIR)

# set permissions for script files
chmod 744 $SCRIPT_DIR/$SERVICE_NAME.py
chmod 744 $SCRIPT_DIR/install.sh
chmod 744 $SCRIPT_DIR/restart.sh
chmod 744 $SCRIPT_DIR/uninstall.sh
chmod 755 $SCRIPT_DIR/service/run

# check dependencies
if [ ! -f $LIB_DIR/ve_utils.py ]
then
    echo "File ve_utils.py does not exist in folder"
    wget https://raw.githubusercontent.com/victronenergy/velib_python/master/ve_utils.py -P $LIB_DIR
else
    echo "File ve_utils.py already in folder."
fi

if [ ! -f $LIB_DIR/vedbus.py ]
then
    echo "File vedbus.py does not exist in folder"
    wget https://raw.githubusercontent.com/victronenergy/velib_python/master/vedbus.py -P $LIB_DIR
else
    echo "File vedbus.py already in folder."
fi

# create sym-link to run script in deamon
ln -s $SCRIPT_DIR/service /service/$SERVICE_NAME

# add install-script to rc.local to be ready for firmware update
filename=/data/rc.local
if [ ! -f $filename ]
then
    touch $filename
    chmod 777 $filename
    echo "#!/bin/bash" >> $filename
    echo >> $filename
fi

# if not alreay added, then add to rc.local
grep -qxF "bash $SCRIPT_DIR/install.sh" $filename || echo "bash $SCRIPT_DIR/install.sh" >> $filename
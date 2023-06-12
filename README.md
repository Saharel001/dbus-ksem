# dbus-ksem Service (Kostal SEM as EM540)

### Purpose

This service is meant to be run on Venus OS from Victron.

The Python script cyclically reads data from the Kostal inverter via the Modbus TCP API and publishes information on the dbus, using the service name com.victronenergy.grid. This makes the Venus OS work as if you had a physical Victron Grid Meter installed.


### Configuration

Rename or copy the config.sample.ini in config.ini an change the Parameter in this file.


### Pre-condition

Two files from the [velib_python](https://github.com/victronenergy/velib_python):

   - vedbus.py
   - ve_utils.py

The install.sh Script load this files automatically.


### Installation

1. Copy the files to the /data folder on your venus:

   - /data/dbus-ksem/dbus-ksem.py
   - /data/dbus-ksem/install.sh
   - /data/dbus-ksem/uninstall.sh
   - /data/dbus-ksem/restart.sh
   - /data/dbus-ksem/service/run
   - /data/dbus-ksem/config.ini

2. start install:

   `bash /data/dbus-ksem/install.sh`

### Debugging

You can check the status of the service with svstat:

`svstat /service/dbus-ksem`

It will show something like this:

`/service/dbus-ksem: up (pid 10078) 12 seconds`

If the number of seconds is always 0 or 1 or any other small number, it means that the service crashes and gets restarted all the time.

When you think that the script crashes, start it directly from the command line:

`python /data/dbus-ksem/dbus-ksem.py`

and see if it throws any error messages.

If the script stops with the message

`dbus.exceptions.NameExistsException: Bus name already exists: com.victronenergy.grid"`

it means that the service is still running or another service is using that bus name.

#### Restart the service

If you want to restart the script, for example after changing it, just run the following command:

`/data/dbus-ksem/restart.sh`

The daemon-tools will restart the scriptwithin a few seconds.

### My Hardware

In my installation at home, I am using the following Hardware:

- Kostal Plenticore 7 and Kostal Smart EnergyMeter G1
- Victron MultiPlus-II - Battery Inverter (single phase)
- Cerbo GX - Venus OS 2.93
- 2x DIY Seplos 280Ah Box - LiFePO Battery

### Credits 🙌🏻

This project is build upon the basis of the inspirational work of:

- Paul1974 via photovoltaikforum.de
- kruki via photovoltaikforum.de
- RalfZim via GitHub https://github.com/RalfZim
- Kaeferfreund via Github https://github.com/kaeferfreund
- mr-manuel via Github https://github.com/mr-manuel/venus-os_dbus-mqtt-battery
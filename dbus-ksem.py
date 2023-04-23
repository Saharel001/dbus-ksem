#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#  Please note that any incorrect or careless usage of this module as well as errors in the implementation can damage your hardware!
#  Therefore, the author does not provide any guarantee or warranty concerning to correctness, functionality or performance and does not accept any liability for damage caused by this module, examples or mentioned information.
#  Thus, use it at your own risk!
#
#  Based on the documentation provided by Kostal:
#
import pymodbus
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from vedbus import VeDbusService
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib as gobject  # Python 3.x
import dbus
import dbus.service
import sys
import os
import platform
import configparser # for config/ini file
import collections
import logging


# our own packages
#sys.path.insert(1, os.path.join(os.path.dirname(__file__), '/opt/victronenergy/dbus-modem'))

# Again not all of these needed this is just duplicating the Victron code.
class SystemBus(dbus.bus.BusConnection):
    def __new__(cls):
        return dbus.bus.BusConnection.__new__(cls, dbus.bus.BusConnection.TYPE_SYSTEM)

class SessionBus(dbus.bus.BusConnection):
    def __new__(cls):
        return dbus.bus.BusConnection.__new__(cls, dbus.bus.BusConnection.TYPE_SESSION)

def dbusconnection():
    return SessionBus() if 'DBUS_SESSION_BUS_ADDRESS' in os.environ else SystemBus()

# Have a mainloop, so we can send/receive asynchronous calls to and from dbus
DBusGMainLoop(set_as_default=True)

class kostal_modbusquery:
    def __init__(self):
        #Change the IP address and port to suite your environment:
        self.grid_ip=config['MODBUS']['ipaddress']
        self.grid_port=config['MODBUS']['port']
        #No more changes required beyond this point
        #self.KostalRegister = []

        self.Adr = collections.OrderedDict()
        self.Adr[0] = [0,"Active power+","U32",0]
        self.Adr[2] = [2,"Active power-","U32",0]
        self.Adr[40] = [40,"Active power+ L1","U32",0]
        self.Adr[42] = [42,"Active power- L1","U32",0]
        self.Adr[60] = [60,"Current L1","U32",0]
        self.Adr[62] = [62,"Voltage L1","U32",0]
        self.Adr[80] = [40,"Active power+ L2","U32",0]
        self.Adr[82] = [42,"Active power- L2","U32",0]
        self.Adr[100] = [60,"Current L2","U32",0]
        self.Adr[102] = [62,"Voltage L2","U32",0]
        self.Adr[120] = [40,"Active power+ L3","U32",0]
        self.Adr[122] = [42,"Active power- L3","U32",0]
        self.Adr[140] = [60,"Current L3","U32",0]
        self.Adr[142] = [62,"Voltage L3","U32",0]
        self.Adr[512] = [512,"Total active power+","U64",0]
        self.Adr[516] = [516,"Total active power-","U64",0]
        self.Adr[592] = [592,"Total active power+ L1","U64",0]
        self.Adr[596] = [596,"Total active power- L1","U64",0]
        self.Adr[672] = [672,"Total active power+ L2","U64",0]
        self.Adr[676] = [676,"Total active power- L2","U64",0]
        self.Adr[752] = [752,"Total active power+ L3","U64",0]
        self.Adr[756] = [756,"Total active power- L4","U64",0]
        self.Adr[8195] = [8195,"Firmware Revision","U16",0]
        self.Adr[8228] = [8228,"Serialnumber","String",0]

    # Routine to read a U16 from one address with 1 registers
    def ReadU16(self, myadr_dec):
        r1 = self.client.read_holding_registers(myadr_dec, 1, unit=1)
        U16register = BinaryPayloadDecoder.fromRegisters(
            r1.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        result_U16register = U16register.decode_16bit_uint()
        return(result_U16register)
    # -----------------------------------------

    # Routine to read a U32 from one address with 2 registers
    def ReadU32(self, myadr_dec):
        r1 = self.client.read_holding_registers(myadr_dec, 2, unit=1)
        U32register = BinaryPayloadDecoder.fromRegisters(
            r1.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        result_U32register = U32register.decode_32bit_uint()
        return(result_U32register)
    # -----------------------------------------
    
    # Routine to read a U64 from one address with 4 registers
    def ReadU64(self, myadr_dec):
        r1 = self.client.read_holding_registers(myadr_dec, 4, unit=1)
        U64register = BinaryPayloadDecoder.fromRegisters(
            r1.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        result_U64register = U64register.decode_64bit_uint()
        return(result_U64register)
    # -----------------------------------------

    # Routine to read a String from one address with 16 registers
    def ReadString(self, myadr_dec):
        r1 = self.client.read_holding_registers(myadr_dec, 4, unit=1)
        StringRegister = BinaryPayloadDecoder.fromRegisters(
            r1.registers, byteorder=Endian.Big )
        result_StringRegister = StringRegister.decode_string(16)
        return(result_StringRegister)
    # -----------------------------------------

    try:
        def run(self):
            self.client = ModbusTcpClient(self.grid_ip, port=self.grid_port)
            self.client.connect()
            
            for key in self.Adr:
                dtype = self.Adr[key][2]
                if dtype == "String":
                    reader = self.ReadString
                elif dtype == "U16":
                    reader = self.ReadU16
                elif dtype == "U32":
                    reader = self.ReadU32
                elif dtype == "U64":
                    reader = self.ReadU64
                else:
                    raise ValueError("Data type not known: %s"%dtype)

                val = reader(key)
                self.Adr[key][3] = val

            self.client.close()
            
            # smartmeter
            
            dbusservice['grid']['/Ac/Power'] = (self.Adr[0][3]/10)-(self.Adr[2][3]/10) # <- W    - total of all phases, real power

            dbusservice['grid']['/Ac/L1/Current'] = self.Adr[60][3]/1000
            dbusservice['grid']['/Ac/L2/Current'] = self.Adr[100][3]/1000
            dbusservice['grid']['/Ac/L3/Current'] = self.Adr[140][3]/1000

            dbusservice['grid']['/Ac/L1/Voltage'] = self.Adr[62][3]/1000
            dbusservice['grid']['/Ac/L2/Voltage'] = self.Adr[102][3]/1000
            dbusservice['grid']['/Ac/L3/Voltage'] = self.Adr[142][3]/1000

            dbusservice['grid']['/Ac/L1/Power'] = (self.Adr[40][3]/10)-(self.Adr[42][3]/10) # <- W    - total of L1 phases, real power
            dbusservice['grid']['/Ac/L2/Power'] = (self.Adr[80][3]/10)-(self.Adr[82][3]/10) # <- W    - total of L2 phases, real power
            dbusservice['grid']['/Ac/L3/Power'] = (self.Adr[120][3]/10)-(self.Adr[122][3]/10) # <- W    - total of L3 phases, real power

            dbusservice['grid']['/Ac/L1/Energy/Forward'] = self.Adr[592][3]/10000.0
            dbusservice['grid']['/Ac/L2/Energy/Forward'] = self.Adr[672][3]/10000.0
            dbusservice['grid']['/Ac/L3/Energy/Forward'] = self.Adr[752][3]/10000.0

            dbusservice['grid']['/Ac/Energy/Forward'] = self.Adr[512][3]/10000.0

            dbusservice['grid']['/Ac/L1/Energy/Reverse'] = self.Adr[596][3]/10000.0
            dbusservice['grid']['/Ac/L2/Energy/Reverse'] = self.Adr[676][3]/10000.0
            dbusservice['grid']['/Ac/L3/Energy/Reverse'] = self.Adr[756][3]/10000.0

            dbusservice['grid']['/Ac/Energy/Reverse'] = self.Adr[516][3]/10000.0


    except Exception as ex:
        logging.error("ERROR: Hit the following error :From subroutine kostal_modbusquery.run() : %s" % ex)
    # -----------------------------

    try:
        def updateStaticInformations(self):
            self.client = ModbusTcpClient(self.grid_ip, port=self.grid_port)
            self.client.connect() 
            logging.info("MODBUS client: Update static Informations")

            for key in self.Adr:
                dtype = self.Adr[key][2]
                if dtype == "String":
                    reader = self.ReadString
                elif dtype == "U16":
                    reader = self.ReadU16
                elif dtype == "U32":
                    reader = self.ReadU32
                elif dtype == "U64":
                    reader = self.ReadU64
                else:
                    raise ValueError("Data type not known: %s"%dtype)

                val = reader(key)
                self.Adr[key][3] = val

            self.client.close()
            
            # smartmeter

            dbusservice['grid']['/Serial'] = self.Adr[8228][3].decode('UTF-8')
            VersionHelper = list("{:04x}".format(self.Adr[8195][3]))

            dbusservice['grid']['/FirmwareVersion'] = VersionHelper[1] + "." + VersionHelper[3]

            dbusservice['grid']['/ProductName'] = config['DEFAULT']['name']

    except Exception as ex:
        logging.error("ERROR: Hit the following error :From subroutine kostal_modbusquery.updateStaticInformations() : %s" % ex)
    # -----------------------------
# Here is the bit you need to create multiple new services - try as much as possible timplement the Victron Dbus API requirements.

def new_service(base, type, physical, id, instance):
    self = VeDbusService("{}.{}.{}_id{:02d}".format(
        base, type, physical,  id), dbusconnection())

    def gettextforkWh(path, value): return ("%.1FkWh" % (float(value)))
    def gettextforW(path, value): return ("%.0FW" % (float(value)))
    def gettextforV(path, value): return ("%.0FV" % (float(value)))
    def gettextforA(path, value): return ("%.1FA" % (float(value)))

    # Create the management objects, as specified in the ccgx dbus-api document
    self.add_path('/Mgmt/ProcessName', __file__)
    self.add_path('/Mgmt/ProcessVersion','Unkown version, and running on Python ' + platform.python_version())
    self.add_path('/Mgmt/Connection','Python ' + platform.python_version())
    self.add_path('/Connected', 1)
    self.add_path('/HardwareVersion', 0)
    self.add_path('/Ac/L1/Voltage', None, gettextcallback=gettextforV)
    self.add_path('/Ac/L2/Voltage', None, gettextcallback=gettextforV)
    self.add_path('/Ac/L3/Voltage', None, gettextcallback=gettextforV)
    self.add_path('/Ac/L1/Current', None, gettextcallback=gettextforA)
    self.add_path('/Ac/L2/Current', None, gettextcallback=gettextforA)
    self.add_path('/Ac/L3/Current', None, gettextcallback=gettextforA)
    self.add_path('/Ac/L1/Power', None, gettextcallback=gettextforW)
    self.add_path('/Ac/L2/Power', None, gettextcallback=gettextforW)
    self.add_path('/Ac/L3/Power', None, gettextcallback=gettextforW)
    self.add_path('/Ac/Power', None, gettextcallback=gettextforW)
    self.add_path('/Ac/L1/Energy/Forward', None, gettextcallback=gettextforkWh)
    self.add_path('/Ac/L2/Energy/Forward', None, gettextcallback=gettextforkWh)
    self.add_path('/Ac/L3/Energy/Forward', None, gettextcallback=gettextforkWh)
    
    # Create device type specific objects
    if physical == 'grid':
        self.add_path('/DeviceInstance', instance)
        self.add_path('/Serial', None)
        self.add_path('/FirmwareVersion', None)
        # value used in ac_sensor_bridge.cpp of dbus-cgwacs
        self.add_path('/ProductId', 45094)
        self.add_path('/ProductName',None)
        self.add_path('/Ac/Energy/Forward', None, gettextcallback=gettextforkWh)
        self.add_path('/Ac/Energy/Reverse', None, gettextcallback=gettextforkWh)
        self.add_path('/Ac/L1/Energy/Reverse', None, gettextcallback=gettextforkWh)
        self.add_path('/Ac/L2/Energy/Reverse', None, gettextcallback=gettextforkWh)
        self.add_path('/Ac/L3/Energy/Reverse', None, gettextcallback=gettextforkWh)
        # energy bought from the grid
    return self

def _run():
    try:
        Kostalquery = kostal_modbusquery()
        Kostalquery.run()
    except Exception as ex:
        logging.error("MODBUS: Error in retrying to connect: %s" % ex)
    return True

def _updateStaticInformations():
    try:
        Kostalquery = kostal_modbusquery()
        Kostalquery.updateStaticInformations()
    except Exception as ex:
        logging.error("MODBUS: Error in retrying to connect: %s" % ex)
    return True

try:
    config = configparser.ConfigParser()
    config.read("%s/config.ini" % (os.path.dirname(os.path.realpath(__file__))))
    if (config['MODBUS']['ipaddress'] == "IP_ADDR"):
        print("ERROR: config.ini file is using invalid default values like IP_ADDR. The driver restarts in 60 seconds.")
        time.sleep(60)
        sys.exit()
except:
    print("ERROR: config.ini file not found. Copy or rename the config.sample.ini to config.ini. The driver restarts in 60 seconds.")
    time.sleep(60)
    sys.exit()

# Get logging level from config.ini
# ERROR = shows errors only
# WARNING = shows ERROR and warnings
# INFO = shows WARNING and running functions
# DEBUG = shows INFO and data/values
if 'DEFAULT' in config and 'logging' in config['DEFAULT']:
    if config['DEFAULT']['logging'] == 'DEBUG':
        logging.basicConfig(level=logging.DEBUG)
    elif config['DEFAULT']['logging'] == 'INFO':
        logging.basicConfig(level=logging.INFO)
    elif config['DEFAULT']['logging'] == 'ERROR':
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.WARNING)

dbusservice = {}  # Dictonary to hold the multiple services

# service defined by (base*, type*, id*, instance):
# * items are include in service name
# Create all the dbus-services we want
dbusservice['grid'] = new_service('com.victronenergy','grid','grid',0, 31)

# Everything done so just set a time to run an update function to update the data values every x second
_updateStaticInformations()
gobject.timeout_add((1000 / int(config['DEFAULT']['freqency'])), _run)
#gobject.timeout_add(60000, _updateStaticInformations)

logging.info("Connected to dbus, and switching over to gobject.MainLoop() (= event based)")
mainloop = gobject.MainLoop()
mainloop.run()

#if __name__ == "__main__":
#    try:
#        Kostalquery = kostal_modbusquery()
#        Kostalquery.run()
#    except Exception as ex:
#        print("Issues querying KSEM -ERROR :", ex)

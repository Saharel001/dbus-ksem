#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  kostal_modbusquery - Read only query of the Kostal Plenticore Inverters using TCP/IP modbus protocol
#  Copyright (C) 2018  Kilian Knoll
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
#  Please note that any incorrect or careless usage of this module as well as errors in the implementation can damage your Inverter!
#  Therefore, the author does not provide any guarantee or warranty concerning to correctness, functionality or performance and does not accept any liability for damage caused by this module, examples or mentioned information.
#  Thus, use it at your own risk!
#
#
#  Purpose:
#           Query values from Kostal inverter
#           Used with Kostal Plenticore Plus 10
#  Based on the documentation provided by Kostal:
#           https://www.kostal-solar-electric.com/en-gb/download/download#PLENTICORE%20plus/PLENTICORE%20plus%204.2/Worldwide/Interfaces%20protocols/
#
# Requires pymodbus
# Tested with:
#           python 3.5
#           pymodbus 2.10
# Please change the IP address of your Inverter (e.g. 192.168.178.41 and Port (default 1502) to suite your environment - see below)
#
import pymodbus
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from vedbus import VeDbusService
from dbus.mainloop.glib import DBusGMainLoop
try:
    import gobject  # Python 2.x
except:
    from gi.repository import GLib as gobject  # Python 3.x
import dbus
import dbus.service
import sys
import os
import platform

# our own packages
sys.path.insert(1, os.path.join(os.path.dirname(
    __file__), '/opt/victronenergy/dbus-modem'))

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
        self.grid_ip="192.168.178.211"
        self.grid_port="502"
        #No more changes required beyond this point
        self.KostalRegister = []

        self.Adr0=[]
        self.Adr0=[0]
        self.Adr0.append("Active power+")
        self.Adr0.append("U32")
        self.Adr0.append(0)

        self.Adr2=[]
        self.Adr2=[2]
        self.Adr2.append("Active power-")
        self.Adr2.append("U32")
        self.Adr2.append(0)

        self.Adr40=[]
        self.Adr40=[40]
        self.Adr40.append("Aktive Power+ L1")
        self.Adr40.append("U32")
        self.Adr40.append(0) 

        self.Adr42=[]
        self.Adr42=[42]
        self.Adr42.append("Aktive Power- L1")
        self.Adr42.append("U32")
        self.Adr42.append(0) 

        self.Adr60=[]
        self.Adr60=[60]
        self.Adr60.append("Current L1")
        self.Adr60.append("U32")
        self.Adr60.append(0) 

        self.Adr62=[]
        self.Adr62=[62]
        self.Adr62.append("Voltage L1")
        self.Adr62.append("U32")
        self.Adr62.append(0) 

        self.Adr80=[]
        self.Adr80=[80]
        self.Adr80.append("Aktive Power+ L2")
        self.Adr80.append("U32")
        self.Adr80.append(0) 

        self.Adr82=[]
        self.Adr82=[82]
        self.Adr82.append("Aktive Power+- L2")
        self.Adr82.append("U32")
        self.Adr82.append(0) 

        self.Adr100=[]
        self.Adr100=[100]
        self.Adr100.append("Current L2")
        self.Adr100.append("U32")
        self.Adr100.append(0) 

        self.Adr102=[]
        self.Adr102=[102]
        self.Adr102.append("Voltage L2")
        self.Adr102.append("U32")
        self.Adr102.append(0) 

        self.Adr120=[]
        self.Adr120=[120]
        self.Adr120.append("Aktive Power+ L3")
        self.Adr120.append("U32")
        self.Adr120.append(0) 

        self.Adr122=[]
        self.Adr122=[122]
        self.Adr122.append("Aktive Power- L3")
        self.Adr122.append("U32")
        self.Adr122.append(0) 

        self.Adr140=[]
        self.Adr140=[140]
        self.Adr140.append("Current L3")
        self.Adr140.append("U32")
        self.Adr140.append(0) 

        self.Adr142=[]
        self.Adr142=[142]
        self.Adr142.append("Voltage L2")
        self.Adr142.append("U32")
        self.Adr142.append(0) 

        self.Adr512=[]
        self.Adr512 =[512]
        self.Adr512.append("Total active power + (powermeter)")
        self.Adr512.append("Float")
        self.Adr512.append(0) 

        self.Adr592=[]
        self.Adr592 =[592]
        self.Adr592.append("L1 Total active power + (powermeter)")
        self.Adr592.append("Float")
        self.Adr592.append(0) 

        self.Adr672=[]
        self.Adr672 =[672]
        self.Adr672.append("L2 Total active power + (powermeter)")
        self.Adr672.append("Float")
        self.Adr672.append(0) 

        self.Adr752=[]
        self.Adr752 =[752]
        self.Adr752.append("L3 Total active power + (powermeter)")
        self.Adr752.append("Float")
        self.Adr752.append(0) 

        self.Adr516=[]
        self.Adr516 =[516]
        self.Adr516.append("Total active power - (powermeter)")
        self.Adr516.append("Float")
        self.Adr516.append(0) 

        self.Adr596=[]
        self.Adr596 =[596]
        self.Adr596.append("L1 Total active power - (powermeter)")
        self.Adr596.append("Float")
        self.Adr596.append(0) 

        self.Adr676=[]
        self.Adr676 =[672]
        self.Adr676.append("L2 Total active power - (powermeter)")
        self.Adr676.append("Float")
        self.Adr676.append(0) 

        self.Adr756=[]
        self.Adr756 =[756]
        self.Adr756.append("L3 Total active power - (powermeter)")
        self.Adr756.append("Float")
        self.Adr756.append(0) 

    # Routine to read a U32 from one address with 2 registers
    def ReadU32(self, myadr_dec):
        r1 = self.client2.read_holding_registers(myadr_dec, 2, unit=1)
        U32register = BinaryPayloadDecoder.fromRegisters(
            r1.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        result_U32register = U32register.decode_32bit_uint()
        return(result_U32register)
    # -----------------------------------------
    
    # Routine to read a U64 from one address with 4 registers
    def ReadU64(self, myadr_dec):
        r1 = self.client2.read_holding_registers(myadr_dec, 4, unit=1)
        U64register = BinaryPayloadDecoder.fromRegisters(
            r1.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        result_U64register = U64register.decode_64bit_uint()
        return(result_U64register)
    # -----------------------------------------

    try:
        def run(self):
            self.client2 = ModbusTcpClient(self.grid_ip, port=self.grid_port)
            self.client2.connect()
            
            self.Adr0[3] = self.ReadU32(self.Adr0[0])
            self.Adr2[3] = self.ReadU32(self.Adr2[0])
            self.Adr40[3] = self.ReadU32(self.Adr40[0])
            self.Adr42[3] = self.ReadU32(self.Adr42[0])
            self.Adr60[3] = self.ReadU32(self.Adr60[0])
            self.Adr62[3] = self.ReadU32(self.Adr62[0])
            self.Adr80[3] = self.ReadU32(self.Adr80[0])
            self.Adr82[3] = self.ReadU32(self.Adr82[0])
            self.Adr100[3] = self.ReadU32(self.Adr100[0])
            self.Adr102[3] = self.ReadU32(self.Adr102[0])
            self.Adr120[3] = self.ReadU32(self.Adr120[0])
            self.Adr122[3] = self.ReadU32(self.Adr122[0])
            self.Adr140[3] = self.ReadU32(self.Adr140[0])
            self.Adr142[3] = self.ReadU32(self.Adr142[0])
            self.Adr512[3] = self.ReadU64(self.Adr512[0])
            self.Adr592[3] = self.ReadU64(self.Adr592[0])
            self.Adr672[3] = self.ReadU64(self.Adr672[0])
            self.Adr752[3] = self.ReadU64(self.Adr752[0])
            self.Adr516[3] = self.ReadU64(self.Adr516[0])
            self.Adr596[3] = self.ReadU64(self.Adr596[0])
            self.Adr676[3] = self.ReadU64(self.Adr676[0])
            self.Adr756[3] = self.ReadU64(self.Adr756[0])
            
            self.KostalRegister.append(self.Adr0)
            self.KostalRegister.append(self.Adr2)
            self.KostalRegister.append(self.Adr40)
            self.KostalRegister.append(self.Adr42)
            self.KostalRegister.append(self.Adr60)
            self.KostalRegister.append(self.Adr62)
            self.KostalRegister.append(self.Adr80)
            self.KostalRegister.append(self.Adr82)
            self.KostalRegister.append(self.Adr100)
            self.KostalRegister.append(self.Adr102)
            self.KostalRegister.append(self.Adr120)
            self.KostalRegister.append(self.Adr122)
            self.KostalRegister.append(self.Adr140)
            self.KostalRegister.append(self.Adr142)
            self.KostalRegister.append(self.Adr512)
            self.KostalRegister.append(self.Adr592)
            self.KostalRegister.append(self.Adr672)
            self.KostalRegister.append(self.Adr752)
            self.KostalRegister.append(self.Adr516)
            self.KostalRegister.append(self.Adr596)
            self.KostalRegister.append(self.Adr676)
            self.KostalRegister.append(self.Adr756)
            
            self.client2.close()
            
            # smartmeter
            
            dbusservice['grid']['/Ac/Power'] = (self.Adr0[3]/10)-(self.Adr2[3]/10) # <- W    - total of all phases, real power

            dbusservice['grid']['/Ac/L1/Current'] = self.Adr60[3]/1000
            dbusservice['grid']['/Ac/L2/Current'] = self.Adr100[3]/1000
            dbusservice['grid']['/Ac/L3/Current'] = self.Adr140[3]/1000

            dbusservice['grid']['/Ac/L1/Voltage'] = self.Adr62[3]/1000
            dbusservice['grid']['/Ac/L2/Voltage'] = self.Adr102[3]/1000
            dbusservice['grid']['/Ac/L3/Voltage'] = self.Adr142[3]/1000

            dbusservice['grid']['/Ac/L1/Power'] = (self.Adr40[3]/10)-(self.Adr42[3]/10) # <- W    - total of L1 phases, real power
            dbusservice['grid']['/Ac/L2/Power'] = (self.Adr80[3]/10)-(self.Adr82[3]/10) # <- W    - total of L2 phases, real power
            dbusservice['grid']['/Ac/L3/Power'] = (self.Adr120[3]/10)-(self.Adr122[3]/10) # <- W    - total of L3 phases, real power

            dbusservice['grid']['/Ac/L1/Energy/Forward'] = self.Adr592[3]/10000.0
            dbusservice['grid']['/Ac/L2/Energy/Forward'] = self.Adr672[3]/10000.0
            dbusservice['grid']['/Ac/L3/Energy/Forward'] = self.Adr752[3]/10000.0

            dbusservice['grid']['/Ac/Energy/Forward'] = self.Adr512[3]/10000.0

            dbusservice['grid']['/Ac/L1/Energy/Reverse'] = self.Adr596[3]/10000.0
            dbusservice['grid']['/Ac/L2/Energy/Reverse'] = self.Adr676[3]/10000.0
            dbusservice['grid']['/Ac/L3/Energy/Reverse'] = self.Adr756[3]/10000.0

            dbusservice['grid']['/Ac/Energy/Reverse'] = self.Adr516[3]/10000.0


    except Exception as ex:
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXX- Hit the following error :From subroutine kostal_modbusquery :", ex)
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
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
        self.add_path('/Serial', "75022295")
        self.add_path('/FirmwareVersion', "2.1.0")
        # value used in ac_sensor_bridge.cpp of dbus-cgwacs
        self.add_path('/ProductId', 45094)
        self.add_path('/ProductName', "Kostal KSEM")
        self.add_path('/Ac/Energy/Forward', None, gettextcallback=gettextforkWh)
        self.add_path('/Ac/Energy/Reverse', None, gettextcallback=gettextforkWh)
        self.add_path('/Ac/L1/Energy/Reverse', None, gettextcallback=gettextforkWh)
        self.add_path('/Ac/L2/Energy/Reverse', None, gettextcallback=gettextforkWh)
        self.add_path('/Ac/L3/Energy/Reverse', None, gettextcallback=gettextforkWh)
        # energy bought from the grid
    return self


def _update():
    try:
        Kostalvalues = []
        Kostalquery = kostal_modbusquery()
        Kostalquery.run()
    except Exception as ex:
        print("Issues querying Kostal SEM -ERROR :", ex)

    return True


dbusservice = {}  # Dictonary to hold the multiple services

base = 'com.victronenergy'

# service defined by (base*, type*, id*, instance):
# * items are include in service name
# Create all the dbus-services we want
dbusservice['grid'] = new_service(
    base, 'grid',           'grid',              0, 31)

# Everything done so just set a time to run an update function to update the data values every 1 second
gobject.timeout_add(100, _update)


print("Connected to dbus, and switching over to gobject.MainLoop() (= event based)")
mainloop = gobject.MainLoop()
mainloop.run()

if __name__ == "__main__":
    try:

        Kostalquery = kostal_modbusquery()
        Kostalquery.run()
    except Exception as ex:
        print("Issues querying Kostal SEM -ERROR :", ex)

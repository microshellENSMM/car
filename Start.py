# This script start all !! :
# Server, SensorManager, and Activities
# It uses also to stop all process

# --------------------------------------------------------------------------
# Follow instructions to correctly fill up this file to launch your Activity
# Please read also ActivitySample.py Pin.py and Commands.py
# --------------------------------------------------------------------------


#   1  ---------------------------------------------------------------------
# You need to import your activity here to use it below. To do that you have
# to use python syntax :
# from file_name import class_name
# --------------------------------------------------------------------------
from LightActivity import LightActivity

#   2  ---------------------------------------------------------------------
# Append this list with your activity instance like this :
# activities.append(name_class())
# --------------------------------------------------------------------------
activities = []
activities.append(LightActivity())


#   3  ---------------------------------------------------------------------
# It's Done. Enjoy :)
# --------------------------------------------------------------------------


import Commands
from Socket import Server
from GPIO import SensorManager

# catch message receved by the server in this method
# We want only catch poweroff commmand to switch off all process
def serverUpdate(tab) :
    if tab[0] == Commands.poweroff:
        for activity in activities :
            activity.stop()

        sensorManager.stop()

# Start SensorManager and server
sensorManager = SensorManager()
server = Server(2014)
server.addListener(serverUpdate)

#--------------------------------#
# Author: Alex Moriconi          |
# Date: 10-06-2019               |
# Example Library Patlite La6    |
# Protocol: HTTP Basic           |
#--------------------------------#
#----- necessary streams import
import streams

# the ethernet module needs a networking driver to be loaded
# in order to control the board hardware.
# FOR THIS EXAMPLE TO WORK, A NETWORK DRIVER MUST BE SELECTED BELOW

# uncomment the following line to use the ESP32 driver
# from espressif.esp32net import esp32eth as ethernet

# uncomment the following line to use INFINEON xmc4eth driver
# from infineon.xmc4eth import xmc4eth as ethernet

from patlite.la6 import la6
#----- Network initialization
ethernet.init()
ethernet.set_link_info("192.168.10.2","255.255.255.0","0.0.0.0","0.0.0.0")
ethernet.link()
#----- Serial PC initialization
streams.serial()
#----- initialization
try:
    lamp=la6.la6HTTP()
except Exception as e:
    print(e)
while True:
    #----- Animation Example
    lamp.set_LED_colors(["green","green","green","green","green"])
    sleep(2000)
    lamp.set_LED_colors(["white","white","white","white","white"])
    sleep(2000)
    lamp.set_LED_colors(["red","red","red","red","red"])
    sleep(2000)

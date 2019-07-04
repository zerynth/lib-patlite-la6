"""
.. patilite:: la6

***************
PATLITE LA6 Library
***************
    To talk with a lamp device an object of type HTTP protocol or MODBUS TCP

    Example::
	
	#----- HTTP Protocol
	import la6
	lamp=la6.la6HTTP()
	lamp.set_LED_colors(["green","green","white","red","red"])
	
	#----- MODBUS TCP Protocol
	import la6
	lamp=la6.la6MODBUS()
	lamp.set_LED_colors(["green","green","white","red","red"])

.. warning:: To be able to communicate via HTTP or MODBUS TCP the patlite la6 must be previously configured to accept commands via these protocols. Set the "Control-system Switchover" parameter on the "Main Unit Setup" page to the "Command Control" value via the web interface.

    """
import requests
from modbus import modbus

#----- Dichiarazione Exceptions HTTP Protocol
new_exception(la6HTTP_ColorsLength,Exception,"ERROR: wrong array colors length")
new_exception(la6HTTP_ColorNonexistent,Exception,"ERROR: color nonexistent")
new_exception(la6HTTP_GetIncorrect,Exception,"ERROR: GET incorrect")
new_exception(la6HTTP_BuzzerStateNonexistent,Exception,"ERROR: buzzer state nonexistent")
new_exception(la6HTTP_FlashState,Exception,"ERROR: falsh state nonexistent")
new_exception(la6HTTP_SmartModeCommand,Exception, "ERROR: smart mode command nonexistent")

#----- Dichiarazione Exceptions MODBUS TCP Protocol
new_exception(la6MODBUS_DeviceConnect,Exception,"ERROR: Unable to establish a connection")
new_exception(la6MODBUS_ColorsLength,Exception,"ERROR: wrong array colors length")
new_exception(la6MODBUS_BuzzerStateNonexistent,Exception,"ERROR: buzzer state nonexistent")
new_exception(la6MODBUS_ColorNonexistent,Exception,"ERROR: color nonexistent")
new_exception(la6MODBUS_FlashState,Exception,"ERROR: falsh state nonexistent")
new_exception(la6MODBUS_SmartModeCommand,Exception, "ERROR: smart mode command nonexistent")
class la6HTTP():
    """

===============
la6HTTP class
===============

.. class:: la6HTTP(colors=["off,"off,"off","off","off"], buzzer="off", flash="off", address="192.168.10.1")

    Create an instance of the la6HTTP class for control patlite la6 lamp with HTTP protocol.
    
    :param colors: Array of 5 positions containing the colors of the led strips.
		
		+------------+------------+
		| String     | Color      |
		+============+============+
		| off        | off        |
		+------------+------------+
		| red        | Red        |
		+------------+------------+
		| amber      | Amber      |
		+------------+------------+
		| lemon      | Lemon      |
		+------------+------------+
		| green      | Green      |
		+------------+------------+
		| skyblue    | Sky Blue   |
		+------------+------------+
		| blue       | Blue       |
		+------------+------------+
		| purple     | Purple     |
		+------------+------------+
		| pink       | Pink       |
		+------------+------------+
		| white      | White      |
		+------------+------------+

    :param buzzer: Buzzer status upon initialization.
		
		+------------+----------------------+
		| Value      | Effect               |
		+============+======================+
		| off        | Turned off           |
		+------------+----------------------+
		| on         | Turned on            |
		+------------+----------------------+
		| 2-11       | audio effects set by |
		|            | set by the lamp      |
		|            | manufacturer         |
		+------------+----------------------+
		
    :param flash: Flash LED unit status upon initialization ["off" or "on"].
    :param address: The IP address of the devices concerned.

    """
    #----- Attributi della Classe Privati
    _url="http://"
    _colors=[0,0,0,0,0]
    _buzzer=0
    _flash=0
    #----- Metodo di Inizializzazione
    def __init__(self,colors=["off","off","off","off","off"], buzzer="off",flash="off",address="192.168.10.1"):
        #Convalida e conversione Parametri
        serviceColors=self.__check_colors(colors)
        serviceBuzzer=self.__check_buzzer(buzzer)
        serviceFlash=self.__check_flash(flash)
        #Copia Array Colori
        self._colors=serviceColors
        #Cambiamento Valore Buzzer
        self._buzzer=serviceBuzzer
        #Cambiamento Valore Flash
        self._flash=serviceFlash
        #Aggiornamento URL con IP
        self._url+=address+"/api/control"
        #Applicazione Colori
        self.__set_colors_buzzer_flash()
    #----- Metodo Applicazione Stato Colori, Buzzer e Flash
    def __set_colors_buzzer_flash(self):
        stringColor=str(self._colors[0])+str(self._colors[1])+str(self._colors[2])+str(self._colors[3])+str(self._colors[4])
        params={"color":stringColor,"buzzer":self._buzzer,"flash":self._flash}
        response=requests.get(self._url,params)
        if not self.__check_response(response):
            raise la6HTTP_GetIncorrect
    #----- Metodo Conversione Vettore Colori
    def __conv_colors(self,valore):
        switcher = {
            "off":0,
            "red":1,
            "amber":2,
            "lemon":3,
            "green":4,
            "skyblue":5,
            "blue":6,
            "purple":7,
            "pink":8,
            "white":9
        }
        valore=valore.lower()# Trasformo Tutto in Minuscolo
        return switcher.get(valore,-1) #Ritorna -1 in caso di errore paramero
    #----- Metodo Conversione Comandi Buzzer
    def __conv_buzzer(self,valore):
        switcher = {
            "off":0,
            "on":1,
            "2":2,
            "3":3,
            "4":4,
            "5":5,
            "6":6,
            "7":7,
            "8":8,
            "9":9,
            "10":10,
            "11":11
        }
        valore=str(valore.lower())# Trasformo il Vaore in Stringa e Poi Rendo Tutto in Minuscolo
        return switcher.get(valore,-1) #Ritorna -1 in caso di errore paramero
    #----- Metodo Coversione Comandi falsh
    def __conv_flash(self,valore):
        switcher = {
            "on":1,
            "off":0
        }
        valore=valore.lower()# Trasformo Tutto in Minuscolo
        return switcher.get(valore,-1) #Ritorna -1 in caso di errore paramero
    #----- Metodo di convalida Comando
    def __check_response(self, response):
        risultato=response.text()
        return "Success" in risultato
    #----- Metodo di convalida Colori
    def __check_colors(self,colors):
        serviceColors=[0,0,0,0,0]
        #Convalidazione Vettore Colori     
        if len(colors)==5:
            #Conversione Formato Colori
            i=0
            while i<5:
                serviceColors[i]=self.__conv_colors(colors[i])
                if serviceColors[i]==-1:
                    raise la6HTTP_ColorNonexistent
                i+=1
            return serviceColors
        else:
            raise la6HTTP_ColorsLength
    #----- Metodo di convalida Buzzer
    def __check_buzzer(self,buzzer):
        serviceBuzzer=self.__conv_buzzer(buzzer)
        if serviceBuzzer==-1:
            raise la6HTTP_BuzzerStateNonexistent  
        else:
            return serviceBuzzer
    #----- Metodo di convalida flash
    def __check_flash(self,flash):
        serviceFlash=0
        serviceFlash=self.__conv_flash(flash)
        if serviceFlash==-1:
            raise la6HTTP_FlashState
        else:
            return serviceFlash
    #----- Metodo di Controllo LED
    def set_LED_colors(self,colors):
        """
        .. method:: set_LED_colors(colors)
            
            :param colors: Array of 5 positions containing the colors of the led strips.

        """
        serviceColors=self.__check_colors(colors)
        self._colors=serviceColors
        self.__set_colors_buzzer_flash()
    #----- Metodo di controllo Buzzer
    def set_buzzer(self,buzzer):
        """
        .. method:: set_buzzer(buzzer)
            
            :param buzzer: Buzzer status.

        """
        serviceBuzzer=self.__check_buzzer(buzzer)
        self._buzzer=serviceBuzzer
        self.__set_colors_buzzer_flash()
    #----- Metodo di controllo Flash
    def set_flash(self,flash):
        """
        .. method:: set_flash(flash)
            
            :param flash: Flash LED unit status.

        """
        serviceFlash=self.__check_flash(flash)
        self._flash=serviceFlash

        self.__set_colors_buzzer_flash()
    #----- Metodo di Clear Totale
    def clear(self):
        """
        .. method:: clear
            
            LED unit and buzzer reset.

        """
        params={"clear":1}
        response=requests.get(self._url,params)
        if not self.__check_response(response):
            raise la6HTTP_GetIncorrect
    #----- Metodo di Controllo SmartMode
    def set_smartmode(self,command):
        """
        .. method:: set_smartmode(command)
            
            :param command: Through this parameter composed of the digits from 1 to 15 it is possible to draw on the SmartMode LED animation functions sanctioned by the lamp manufacturer.

        """
        if command<1 or command>15:
            raise la6HTTP_SmartModeCommand
        else:
            params={"smart":command}
            response=requests.get(self._url,params)
            if not self.__check_response(response):
                raise la6HTTP_GetIncorrect


#----- Classe Implementazione Comuniazione Tramite Protocollo MODBUS
class la6MODBUS():
    """

===============
la6MODBUS class
===============

.. class:: la6MODBUS(colors=["off,"off,"off","off","off"], buzzer="off", flash="off", address="192.168.10.1", port=502)

    Create an instance of the la6MODBUS class for control patlite la6 lamp with MODBUS TCP protocol.
    
    :param colors: Array of 5 positions containing the colors of the led strips.
		
		+------------+------------+
		| String     | Color      |
		+============+============+
		| off        | off        |
		+------------+------------+
		| red        | Red        |
		+------------+------------+
		| amber      | Amber      |
		+------------+------------+
		| lemon      | Lemon      |
		+------------+------------+
		| green      | Green      |
		+------------+------------+
		| skyblue    | Sky Blue   |
		+------------+------------+
		| blue       | Blue       |
		+------------+------------+
		| purple     | Purple     |
		+------------+------------+
		| pink       | Pink       |
		+------------+------------+
		| white      | White      |
		+------------+------------+

    :param buzzer: Buzzer status upon initialization.
		
		+------------+----------------------+
		| Value      | Effect               |
		+============+======================+
		| off        | Turned off           |
		+------------+----------------------+
		| on         | Turned on            |
		+------------+----------------------+
		| 2-11       | audio effects set by |
		|            | set by the lamp      |
		|            | manufacturer         |
		+------------+----------------------+
		
    :param flash: Flash LED unit status upon initialization ["off" or "on"].
    :param address: The IP address of the devices concerned.
    :param port: Network port for connection in modbus protocol.

    """
    #----- Attributi della Classe Privati
    _IP="192.168.10.1"
    _port=502
    _device=""
    #----- Metodo di Inizializzazione
    def __init__(self,colors=["off","off","off","off","off"], buzzer="off",flash="off",address="192.168.10.1",port=502):
        #Aggiornamento IP e Porta
        self._IP=address
        self._port=port
        #Creazione Istanza Classe MODBUS TCP
        self._device = modbus.ModbusTCP(1)
        try:
            self._device.connect(self._IP, self._port)
        except Exception as e:
            raise la6MODBUS_DeviceConnect
        #Applicazione Colori
        self.set_LED_colors(colors)
        #Applicazione Buzzer
        self.set_buzzer(buzzer)
        #Applicazione Flash
        self.set_flash(flash)
    #----- Metodo Cambiamento Colori
    def set_LED_colors(self,colors):
        """
        .. method:: set_LED_colors(colors)
            
            :param colors: Array of 5 positions containing the colors of the led strips.

        """
        serviceColors=self.__check_colors(colors)
        #Cambiamento Stato Registri
        self._device.write_multiple_registers(0x0B, 5, serviceColors)
    #----- Metodo Conversione Vettore Colori
    def __conv_colors(self,valore):
        switcher = {
            "off":0x0100,
            "red":0x0101,
            "amber":0x0102,
            "lemon":0x0103,
            "green":0x0104,
            "skyblue":0x0105,
            "blue":0x0106,
            "purple":0x0107,
            "pink":0x0108,
            "white":0x0109
        }
        valore=valore.lower()# Trasformo Tutto in Minuscolo
        return switcher.get(valore,-1) #Ritorna -1 in caso di errore paramero
    #----- Metodo Conversione Comandi Buzzer
    def __conv_buzzer(self,valore):
        switcher = {
            "off":0x0100,
            "on":0x0101,
            "2":0x0102,
            "3":0x0103,
            "4":0x0104,
            "5":0x0105,
            "6":0x0106,
            "7":0x0107,
            "8":0x0108,
            "9":0x0109,
            "10":0x010A,
            "11":0x010B
        }
        valore=str(valore.lower())# Trasformo il Vaore in Stringa e Poi Rendo Tutto in Minuscolo
        return switcher.get(valore,-1) #Ritorna -1 in caso di errore paramero
    #----- Metodo Coversione Comandi falsh
    def __conv_flash(self,valore):
        switcher = {
            "on":0x0101,
            "off":0x0100
        }
        valore=valore.lower()# Trasformo Tutto in Minuscolo
        return switcher.get(valore,-1) #Ritorna -1 in caso di errore paramero
    #----- Metodo di convalida Colori
    def __check_colors(self,colors):
        serviceColors=[0,0,0,0,0]
        #Convalidazione Vettore Colori     
        if len(colors)==5:
            #Conversione Formato Colori
            i=0
            while i<5:
                serviceColors[i]=self.__conv_colors(colors[i])
                if serviceColors[i]==-1:
                    raise la6MODBUS_ColorNonexistent
                i+=1
            return serviceColors
        else:
            raise la6MODBUS_ColorsLength
    #----- Metodo di convalida Buzzer
    def __check_buzzer(self,buzzer):
        serviceBuzzer=self.__conv_buzzer(buzzer)
        if serviceBuzzer==-1:
            raise la6MODBUS_BuzzerStateNonexistent  
        else:
            return serviceBuzzer
    #----- Metodo di convalida flash
    def __check_flash(self,flash):
        serviceFlash=0
        serviceFlash=self.__conv_flash(flash)
        if serviceFlash==-1:
            raise la6MODBUS_FlashState
        else:
            return serviceFlash
    #----- Metodo di controllo Buzzer
    def set_buzzer(self,buzzer):
        """
        .. method:: set_buzzer(buzzer)
            
            :param buzzer: Buzzer status.

        """
        serviceBuzzer=self.__check_buzzer(buzzer)
        self._device.write_register(0x11, serviceBuzzer)
    #----- Metodo di controllo Flash
    def set_flash(self,flash):
        """
        .. method:: set_flash(flash)
            
            :param flash: Flash LED unit status.

        """
        serviceFlash=self.__check_flash(flash)
        self._device.write_register(0x10, serviceFlash)
    #----- Metodo di Controllo SmartMode
    def set_smartmode(self,command):
        """
        .. method:: set_smartmode(command)
            
            :param command: Through this parameter composed of the digits from 1 to 15 it is possible to draw on the SmartMode LED animation functions sanctioned by the lamp manufacturer.

        """
        if command<1 or command>15:
            raise la6MODBUS_SmartModeCommand
        else:
            self._device.write_register(0x06, command+256)
    #----- Metodo di Clear Totale
    def clear(self):
        """
        .. method:: clear()
            
            LED unit and buzzer reset.
        """
        self._device.write_register(0x07, 0x0001)

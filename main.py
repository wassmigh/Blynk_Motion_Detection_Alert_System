import machine
import time
import BlynkLib 
import network

pir_pin = machine.Pin(36, machine.Pin.IN)  
led_pin = machine.Pin(22, machine.Pin.OUT) 

SSID = "your router SSID"  # Replace with your Wi-Fi network name
PASSWORD = "your router password"  # Replace with your Wi-Fi password
BLYNK_AUTH = "your blynk auth token"  # Replace with your Blynk Auth token

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
        print("Connexion en cours...")
    print("Connecté au réseau Wi-Fi")
    print("Adresse IP:", wlan.ifconfig()[0])


connect_wifi()


blynk = BlynkLib.Blynk(BLYNK_AUTH)


alarm_active = True  


def alert():
    if alarm_active:  
        print("Intrusion détectée !")
        blynk.virtual_write(1, 1)  
        start_time = time.time()
        while time.time() - start_time < 6:
            led_pin.value(1)  
            time.sleep(1)  
            led_pin.value(0) 
            time.sleep(1)  
        blynk.virtual_write(1, 0) 


def pir_callback(pin):
    if alarm_active: 
        alert()

pir_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_callback)

@blynk.on("V0")  
def v0_write_handler(value):
    global alarm_active
    alarm_active = bool(int(value[0]))  
    print("Alarme est", "activée" if alarm_active else "désactivée")


while True:
    blynk.run()  # Exécuter Blynk
    time.sleep(0.1)

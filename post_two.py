import ujson as json
import urequests as requests
import time
import dht
import machine
from machine import Pin
from machine import SPI
from machine import I2C
import onewire, ds18x20



index=0


done_pin=Pin(13,Pin.OUT)
done_pin.value(0)


time.sleep(3)


base_url='https://wolfesneck.farmos.net/farm/sensor/listener/'
#public_key='054d3116a74fae5dd36550013d50c848'
#private_key='014d3116a74fae5dd36550013d50c848'

public_key='645b7f8bcac73d298ffe2e035c0d1266'
private_key='3f79ca9545ed872c94c7dd917ac8f357'

url = base_url+public_key+'?private_key='+private_key

headers = {'Content-type':'application/json', 'Accept':'application/json'}

time.sleep(2)

def post_data():
    try:
    
    
        d = dht.DHT22(machine.Pin(18))
        
        # the device is on GPIO12
        dat = machine.Pin(5)

        # create the onewire object
        ds = ds18x20.DS18X20(onewire.OneWire(dat))

        d.measure()
        t=d.temperature()
        h=d.humidity()

        adc = machine.ADC(machine.Pin(35))

        adc_val=adc.read()

        ds.convert_temp()

        time.sleep_ms(1000)

        roms = ds.scan()
        
        print(roms)

        probe_temp=ds.read_temp(roms[0])

        payload ={"room_temp": t,"room_humidity":h,"probe_temp":probe_temp}

        print(payload)
    
    
    	r = requests.post(url,data=json.dumps(payload),headers=headers)
    except Exception as e:
	print(e)
	#r.close()
	return "timeout"
    else:
	r.close()
	print('Status', r.status_code)
   	return "posted"

WIFI_NET = 'Southbridge Hotel Guest'
WIFI_PASSWORD = 'SHCC2018'

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)	
    if not sta_if.isconnected():
        print('connecting to network...')
	sta_if.active(False)
        sta_if.active(True)
        sta_if.connect(WIFI_NET, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

while True:

    do_connect()

    
    
    post_data()




    time.sleep(1)

    done_pin.value(1)

    index+=1

    time.sleep(5)


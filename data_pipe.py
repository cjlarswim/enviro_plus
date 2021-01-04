import time
from bme280 import BME280
from pms5003 import PMS5003, ReadTimeoutError as pmsReadTimeoutError
from enviroplus import gas
import json

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

bme280 = BME280()
pms5003 = PMS5003()
proximity = ltr559.get_proximity()


def temperature_collect():
    data = bme280.get_temperature()
    return data

def humidity_collect():
    unit = "%"
    data = bme280.get_humidity()
    return data

def light_collect(): 
    unit = "Lux"
    data = ltr559.get_lux()
    return data

def pressure_collect():
    unit = "hPa"
    data = bme280.get_pressure()
    return data

def oxidised_collect():
    unit = "kO"
    data = gas.read_all()
    data = data.oxidising / 1000
    return data

def reduced_collect():
    unit = "kO"
    data = gas.read_all()
    data = data.reducing / 1000
    return data

def nh3_collect():
    unit = "kO"
    data = gas.read_all()
    data = data.nh3 / 1000
    return data

def write_to_json(data, filename = 'data.json'):
    with open(filename, 'w+') as f:
        json.dump(data, f, indent = 2, sort_keys = True)

def initial_writing():
#create file and log initial reading 
    h = humidity_collect()
    t = temperature_collect()
    l = light_collect()
    p = pressure_collect()
    o = oxidised_collect()
    r = reduced_collect()
    n = nh3_collect()
 

    values = {'time': time.time(),
                'Sensor Readings':
                {"temperature": t,
                "humidity": h,
                'light': l,
                'pressure': p,
                'oxidised': o,
                'reduced': r,
                'nh3': n
                }
    }

    write_to_json(values, 'data.json')

#Main Loop
if True:
    initial_writing()
    while True:
        h = humidity_collect()
        t = temperature_collect()
        l = light_collect()
        p = pressure_collect()
        o = oxidised_collect()
        r = reduced_collect()
        n = nh3_collect()

        values = {'time': time.time(),
                    'Sensor Readings':
                    {"temperature": t,
                    "humidity": h,
                    'light': l,
                    'pressure': p,
                    'oxidised': o,
                    'reduced': r,
                    'nh3': n
                    }
        }

        with open('data.json') as fi:
            data = [json.load(fi)]
            y = values
            data.append(y)

        write_to_json(data)
        time.sleep(10)

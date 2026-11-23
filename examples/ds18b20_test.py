from machine import Pin
import ds18x20
import onewire
import time

sensor = ds18x20.DS18X20(onewire.OneWire(Pin(4)))
addresses = sensor.scan()

print("Найдено датчиков:", len(addresses))

if not addresses:
    raise SystemExit("Проверь подключение датчика и резистор 4,7 кОм.")

for address in addresses:
    print("Адрес:", address.hex())

while True:
    try:
        sensor.convert_temp()
        time.sleep_ms(750)

        for address in addresses:
            temperature = sensor.read_temp(address)
            print("{}: {:.2f} °C".format(address.hex(), temperature))

    except Exception as error:
        print("Ошибка чтения:", error)

    time.sleep(1)
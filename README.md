# DIY Ventilation Controller

An ESP32-controlled DIY wall-mounted fresh-air ventilation unit for an apartment. The project combines multi-stage air filtration, a variable-speed fan, electric air heating, temperature monitoring, and filter pressure-drop monitoring.

Planned features include physical buttons, a local display, airflow and temperature control, and local Home Assistant integration. Hardware protection will provide heater shutdown independently of the main software.

The project is under development. The current prototype runs MicroPython on an ESP32-S3 and has a tested DS18B20 temperature sensor.

## О проекте

Самодельная настенная приточная установка — бризер под управлением ESP32. Предусмотрены многоступенчатая фильтрация воздуха, регулирование скорости вентилятора, электрический подогрев, измерение температуры и контроль перепада давления на фильтрах.

Планируются физические кнопки, локальный экран, управление расходом и температурой воздуха, интеграция с Home Assistant. Аппаратная защита должна отключать нагреватель независимо от основной программы.

Проект находится в разработке. На текущем этапе ESP32-S3 работает под управлением MicroPython, подключён и проверен датчик температуры DS18B20.

## Development setup — Linux Mint

Clone the repository and enter its directory:

```bash
mkdir -p ~/Documents/projects
cd ~/Documents/projects
git clone git@github.com:USERNAME/ventilation-controller.git
cd ventilation-controller
```

Install Python virtual environment support and create a project environment:

```bash
sudo apt update
sudo apt install python3-venv wget
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Activate the environment again whenever you open a new terminal:

```bash
source .venv/bin/activate
```

Allow access to serial ports:

```bash
sudo usermod -aG dialout "$USER"
```

Log out and log back in for the group membership to take effect.

## Install MicroPython

These instructions target the ESP32-S3 DevKitC-1 N16R8 with Octal PSRAM.

Connect the board using a USB data cable. Use USB power alone during this setup. Find its serial port:

```bash
mpremote connect list
```

The commands below use `/dev/ttyACM0`. Replace it with the port shown on your computer.

Download MicroPython 1.29.0 with Octal-SPIRAM support:

```bash
mkdir -p firmware
wget -O firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20260824-v1.29.0.bin \
  https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20260824-v1.29.0.bin
```

Erase the board's flash memory. This removes its existing firmware and files:

```bash
esptool --chip esp32s3 --port /dev/ttyACM0 erase-flash
```

If connection fails, hold BOOT, press and release RESET, then release BOOT. Check the serial port again and retry.

Write the firmware:

```bash
esptool --chip esp32s3 --port /dev/ttyACM0 --baud 460800 write-flash 0x0 \
  firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20260824-v1.29.0.bin
```

If the transfer fails, retry with `--baud 115200`.

Press RESET and verify MicroPython:

```bash
mpremote connect /dev/ttyACM0 exec "import sys; print(sys.implementation)"
```

Expected output includes `micropython` and `ESP32_GENERIC_S3-SPIRAM_OCT`.

## Run hardware tests

The DS18B20 test uses the following connections:

| Sensor connection | ESP32 connection |
| --- | --- |
| VDD | 3V3 |
| GND | GND |
| DQ | GPIO4 |

Connect a 4.7 kΩ resistor between DQ and 3V3. For a wired probe, confirm the manufacturer's wire assignments before connecting it.

Run the test:

```bash
mpremote connect /dev/ttyACM0 run examples/ds18b20_test.py
```

The program prints detected sensor addresses and temperatures. Hold the probe in your hand to check its response.

Press Ctrl+C to stop. The `run` command executes the local script on the controller without saving it to the board's filesystem.

To run another standalone test, use the same command with its file path.

## Development workflow

Review and commit changes, then push the working branch to GitHub:

```bash
git status
git diff
git add path/to/file
git diff --cached
git commit -m "Describe the change"
git push
```

Keep the `.venv/` directory and local credentials excluded from Git.
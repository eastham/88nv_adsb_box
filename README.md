<h2>88nv_adsb_box: modifications to the adsb-exchange image to support operations at 88NV.</h2>

Files in here enable:
- Logging of all aircraft seen at 1/5 Hz
- Support for a small OLED (SSD1306) display that shows system status and IP address
- Support for an illuminated button that allows easy reset of the wifi setup to stock each year (maybe not needed if we switch to Ethernet)

Install process as of 4/5/24:
- Flash adsbx (or airplanes.live) image -- adsbx-8.2.220910.zip is known to work: https://downloads.adsbexchange.com/downloads/adsbx-8.2.220910.zip
- Boot up sdcard, setup wifi
- (Optional: run update from UI, updates raspbian)
- Update tar1090 to latest from our forked repo:
  - sudo bash -c "rm -rf /usr/local/share/tar1090/git ;  $(wget -nv -O - https://github.com/eastham/tar1090/raw/master/install.sh)"


- Pull this repo to the home directory: cd ~ ; git clone https://github.com/eastham/88nv_adsb_box.git
- Copy over files from 88nv_adsb_box directory into active filesystem 
- Change ssh password
- Consider adding other feeders
  - instructions for airplanes.live: https://airplanes.live/how-to-feed/

New approach on raspi 5:
- flash 64-bit raspi image to sd, boot it up
- in pi gui, enable ssh, enable vnc
- install adsbx

sudo bash -c "$(wget -O - https://raw.githubusercontent.com/ADSBexchange/image-builder/master/image-setup.sh)"
add user pi (for adsbx admin access)
sudo reboot now

- add airplanes.live feed:
curl -L -o /tmp/feed.sh https://raw.githubusercontent.com/airplanes-live/feed/main/install.sh
 sudo bash /tmp/feed.sh 


XXX futz around with ttyusb0 permissions
- gpsd using USB port
sudo apt-get remove gpsd

- Update tar1090 to latest from our forked repo:
  - sudo bash -c "rm -rf /usr/local/share/tar1090/git ;  $(wget -nv -O - https://github.com/eastham/tar1090/raw/redo/install.sh)"

- go to localhost web ui, update receiver position and radio config

- clone this repo

cd ~ ; git clone https://github.com/eastham/88nv_adsb_box.git

- Copy over files from 88nv_adsb_box directory into active filesystem

XXX

- install mesh_adsb (not used on all boxes)

git clone https://github.com/eastham/mesh_adsb.git
cd mesh_adsb
python3 -m venv .
source bin/activate
pip3 install -r requirements.txt
(update rc.local to run mesh_receiver.py --host READSB_HOST [--port READSB_PORT])


- install adsb_actions

(follow instructions on https://github.com/eastham/adsb_actions)


Optional commands to set up display, if installed:
- sudo apt-get install pip
- sudo raspi-config, enable i2c
- sudo pip3 install Adafruit_GPIO
- sudo pip3 install Adafruit_SSD1306
- sudo pip3 install netifaces

![Image of device](adsb_box.jpg?raw=true "Image of Device")

<h2>88nv_adsb_box: modifications to the adsb-exchange image to support operations at 88NV.</h2>

Files in here enable:
- Logging of all aircraft seen at 1/5 Hz
- Support for a small OLED (SSD1306) display that shows system status and IP address
- Support for an illuminated button that allows easy reset of the wifi setup to stock each year (maybe not needed if we switch to Ethernet)
- Outdated mods to tar1090 -- moved to fork of tar1090 at https://github.com/eastham/tar1090) -- see below on how to pull them in

Install process as of 4/5/24:
- Flash adsbx (or airplanes.live) image
- Boot it up, setup wifi
- (Optional: run update from UI, updates raspbian)
- Update tar1090 to latest from our forked repo: sudo bash -c "rm -rf /usr/local/share/tar1090/git ;  $(wget -nv -O - https://github.com/eastham/tar1090/raw/master/install.sh)"
- Pull this repo to the home directory: cd ~ ; git clone https://github.com/eastham/88nv_adsb_box.git
- Copy over files from 88nv_adsb_box directory into active filesystem 
- Change ssh password
- Consider adding other feeders


![Image of device](adsb_box.jpg?raw=true "Image of Device")

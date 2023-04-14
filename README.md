## Euro Truck Simulator 2 / American Truck Simulator Live Radio Transcoder

### Project info
This is simple live radio transcoder server for **Euro Truck Simulator 2 / American Truck Simulator** games.

As you may know internet radio player in these games does not support anything but plain MP3 streams.
But there are lots of internet radios novadays that use AAC / AAC+ codecs combined with HLS. Of course, you can play
such radios in your favourite player just in the background on a regular PC but this is not so easy to do on devices
like Steam Deck.

So this is probably the main reason you would use this project for.
You can run this script on your own VPS or (if you don't have it) even directly on your Steam Deck (SD surprisingly has 
everything to run it out of the box).

### Requirements
- python 3
- ffmpeg

### Stations file (stations.json)
Before usage, you should modify **stations.json** file from the repo. It's a simple JSON file which holds all the 
stations you need to be transcoded. Format is very simple and self-explanatory:

```json
{
	"radio1": {
		"name": "Record Innocence",
		"url": "https://radiorecord.hostingradio.ru/ibiza96.aacp",
		"bitrate": 128
	},
	"radio2": {
		"name": "Record Mix",
		"url": "https://radiorecord.hostingradio.ru/mix96.aacp",
		"bitrate": 128
	}
}
```

According to this example corresponding radios should be added to your **live_streams.sii** ATS/ETS file with following URLs:
- `http://IP_ADDRESS:PORT/radio1` for "Record Innocence" station 
- `http://IP_ADDRESS:PORT/radio2` for "Record Mix" station

These MP3 streams will have output bitrate at 128 kbit/s. You can change it to whatever you want up to 320 kbit/s, but 
keep in mind that higher bitrates will result in higher power consumption.

You should replace **IP_ADDRESS** with real IP address of your VPS or in case you run it directly on SD with just
**localhost**. Replace **PORT** with port on which you run the server.

### Running the server on SD
`$ ./server.py --port 48042`

### Running the server on VPS
`$ ./server.py --host 0.0.0.0 --port 48042`

### Automatic startup on system boot
If you want to automatically start the service on system boot - modify the **etsradiotc.service** (set the actual path to
server.py script on your VPS/SD) and add it to systemd autostart:

```
$ sudo cp etsradiotc.service /etc/systemd/system/
$ sudo systemctl enable --now etsradiotc.service
```

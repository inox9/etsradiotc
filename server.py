#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import argparse
import functools
import subprocess
import json


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, stations: Path, ffmpeg: str, *args, **kwargs):
        self._stations = stations
        self._ffmpeg = ffmpeg
        super().__init__(*args, **kwargs)

    def do_GET(self):
        with open(self._stations) as fp:
            stations = json.load(fp)
        path = self.path[1:]
        if len(path) == 0 or path not in stations:
            self.send_error(404)
            return

        station: dict = stations[path]
        bitrate = station.get('bitrate', 128)
        cmd = (self._ffmpeg, '-i', station['url'], '-c:a', station.get('codec', 'libmp3lame'), '-b:a',
               f'{bitrate}k', '-f', station.get('format', 'mp3'), '-map_metadata', '-1', 'pipe:1')
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as proc:
            self.send_response(200)
            self.send_header('content-type', station.get('contentType', 'audio/mpeg'))
            self.send_header('accept-ranges', 'none')
            self.send_header('connection', 'close')
            self.send_header('icy-name', station['name'])
            self.send_header('icy-br', bitrate)
            self.end_headers()
            chunk_size = int(bitrate * 1024 / 16)
            while proc.poll() is None:
                try:
                    self.wfile.write(proc.stdout.read(chunk_size))
                except (BrokenPipeError, ConnectionResetError):
                    proc.terminate()
                    proc.wait(10)


if __name__ == '__main__':
    def validate_file(arg):
        if (file := Path(arg)).is_file():
            return file
        raise FileNotFoundError(arg)

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, help='listen host', default='127.0.0.1')
    parser.add_argument('--port', type=int, help='listen port', required=True)
    parser.add_argument('--stations', type=validate_file, help='custom stations.json file path',
                        default='./stations.json')
    parser.add_argument('--ffmpeg', type=str, help='custom path to ffmpeg binary', default='ffmpeg')
    argv = parser.parse_args()
    httpd = HTTPServer((argv.host, argv.port), functools.partial(RequestHandler, argv.stations, argv.ffmpeg))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

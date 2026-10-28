import json
import re
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import requests

from event_helper import DEFAULT_ROOM_IDS, find_free_rooms, get_events


ROOT = Path(__file__).parent


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            self.send_error(404)
            return

        content = (ROOT / 'index.html').read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        if self.path not in ('/search', '/rooms'):
            self.send_error(404)
            return

        try:
            data = self._read_json()
            start, end = self._parse_interval(data)
            minimum_capacity = self._parse_capacity(data)
            if end <= start:
                raise ValueError('end time must be after start time')
            if self.path == '/search':
                rooms = find_free_rooms(start, end, DEFAULT_ROOM_IDS)
            else:
                rooms = [room['Name'] for room in get_events(
                    start, end, DEFAULT_ROOM_IDS
                )]
            rooms = [
                room for room in rooms
                if self._room_capacity(room) >= minimum_capacity
            ]
        except (
            KeyError,
            TypeError,
            ValueError,
            json.JSONDecodeError,
            requests.RequestException,
        ) as error:
            self._send_json({'error': str(error)}, status=400)
            return

        self._send_json({'rooms': rooms})

    def _read_json(self):
        length = int(self.headers['Content-Length'])
        return json.loads(self.rfile.read(length))

    @staticmethod
    def _parse_interval(data):
        start = datetime.fromisoformat(
            f"{data['date']}T{data['start']}"
        ).replace(tzinfo=timezone.utc)
        end = datetime.fromisoformat(
            f"{data['date']}T{data['end']}"
        ).replace(tzinfo=timezone.utc)
        return start, end

    @staticmethod
    def _parse_capacity(data):
        capacity = int(data['capacity'])
        if capacity < 0:
            raise ValueError('capacity must not be negative')
        return capacity

    @staticmethod
    def _room_capacity(room_name):
        match = re.search(r'\((\d+)\)\s*$', room_name)
        if match is None:
            return 0
        return int(match.group(1))

    def _send_json(self, payload, status=200):
        content = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == '__main__':
    server = ThreadingHTTPServer(('0.0.0.0', 8000), RequestHandler)
    print('Open http://localhost:8000 in your browser.')
    server.serve_forever()

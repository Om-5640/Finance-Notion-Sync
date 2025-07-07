import json

class StateStore:
    def __init__(self, path: str = 'state.json'):
        self.path = path
        try:
            data = json.load(open(path))
        except FileNotFoundError:
            data = {'last_timestamp': None}
        self._ts = data.get('last_timestamp')

    def get_last_timestamp(self) -> str:
        return self._ts

    def set_last_timestamp(self, ts: str):
        self._ts = ts
        with open(self.path, 'w') as f:
            json.dump({'last_timestamp': ts}, f)

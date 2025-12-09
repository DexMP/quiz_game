# core/logger.py
from datetime import datetime

class Logger:
    def __init__(self):
        self.history = []

    def log(self, text):
        ts = datetime.utcnow().isoformat() + 'Z'
        entry = {
            'ts': ts,
            'text': f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}"
        }
        self.history.append(entry)
        self.history = self.history[-1000:]

    def get_text(self):
        return ''.join(e['text'] + '\n' for e in self.history)

    def load_from(self, history):
        self.history = []
        for e in history or []:
            if not isinstance(e, dict):
                continue
            text = e.get('text')
            ts = e.get('ts')
            if not text:
                continue
            if not ts:
                ts = datetime.utcnow().isoformat() + 'Z'
            self.history.append({'ts': ts, 'text': text})
        self.history = self.history[-1000:]

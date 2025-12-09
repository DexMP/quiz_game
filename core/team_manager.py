# core/team_manager.py
from datetime import datetime

class TeamManager:
    def __init__(self):
        self.teams = []

    def add_team(self, name):
        tid = int(datetime.utcnow().timestamp() * 1000)
        team = {"id": tid, "name": name, "score": 0}
        self.teams.append(team)
        return team

    def remove_by_index(self, idx):
        if 0 <= idx < len(self.teams):
            del self.teams[idx]

    def adjust(self, idx, delta):
        if 0 <= idx < len(self.teams):
            self.teams[idx]['score'] += delta

    def get_sorted(self):
        return [{'name': t['name'], 'score': t['score']} for t in sorted(self.teams, key=lambda x: -x['score'])]

    def load_from(self, teams):
        self.teams = teams

# core/state_manager.py
import json, csv

class StateManager:
    def build_state(self, team_mgr, logger, theme_mgr, timer, round_name):
        return {
            'teams': team_mgr.teams,
            'history': logger.history,
            'theme': theme_mgr.get(),
            'round_name': round_name,
            'remaining': timer.remaining
        }

    def save(self, path, state):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def load(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def export_csv(self, path, teams):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['team', 'score'])
            for t in teams:
                w.writerow([t['name'], t['score']])

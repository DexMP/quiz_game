# core/state_manager.py
import json, csv

class StateManager:
    def build_state(self, team_mgr, logger, theme_mgr, timer, round_name):
        return {
            'teams': team_mgr.to_dict_list(),  # ← ПРАВИЛЬНО! Конвертируем в список словарей
            'history': logger.history,
            'theme': theme_mgr.get(),
            'remaining': timer.remaining,
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
            w.writerow(['name', 'score'])          # ← ИСПРАВЛЕНО
            for t in teams:
                w.writerow([t.name, t.score])       # ← ИСПРАВЛЕНО

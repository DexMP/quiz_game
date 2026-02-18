# core/team_manager.py
"""Менеджер команд"""

from typing import List, Dict, Union
from core.team import Team


class TeamManager:
    """Управление командами с типизацией"""
    
    def __init__(self) -> None:
        self.teams: List[Team] = []
    
    def add_team(self, name: str) -> Team:
        team = Team(name=name)
        self.teams.append(team)
        return team
    
    def remove_by_index(self, idx: int) -> None:
        if 0 <= idx < len(self.teams):
            del self.teams[idx]
    
    def adjust(self, idx: int, delta: float) -> None:
        # Этот метод использовался в контекстном меню (ПКМ), там мы искали original_idx
        # так что его можно оставить, но лучше переписать на имена тоже, если будет время.
        # Пока оставим как есть, так как в open_menu логика правильная.
        if 0 <= idx < len(self.teams):
            self.teams[idx].add_score(delta)
    
    def set_score_by_name(self, name: str, new_value: float) -> None:
        """Находим команду по имени и ставим ей очки"""
        for team in self.teams:
            if team.name == name:
                team.score = new_value
                break
    
    def get_sorted(self) -> List[Team]:
        """Получить команды отсортированные по очкам (убывание)
        
        Returns:
            Отсортированный список Team
        """
        return sorted(self.teams, key=lambda x: -x.score)
    
    def load_from(self, teams: Union[List[Dict], List[Team]]) -> None:
        self.teams = []
        for team_data in teams:
            if isinstance(team_data, dict):
                self.teams.append(Team.from_dict(team_data))
            elif isinstance(team_data, Team):
                self.teams.append(team_data)
    
    def to_dict_list(self) -> List[Dict]:
        return [team.to_dict() for team in self.teams]

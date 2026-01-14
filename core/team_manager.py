# core/team_manager.py
"""Менеджер команд"""

from typing import List, Dict, Union
from core.team import Team


class TeamManager:
    """Управление командами с типизацией"""
    
    def __init__(self) -> None:
        self.teams: List[Team] = []
    
    def add_team(self, name: str) -> Team:
        """Добавить новую команду
        
        Args:
            name: Имя команды
            
        Returns:
            Созданный объект Team
        """
        team = Team(name=name)
        self.teams.append(team)
        return team
    
    def remove_by_index(self, idx: int) -> None:
        """Удалить команду по индексу
        
        Args:
            idx: Индекс команды
        """
        if 0 <= idx < len(self.teams):
            del self.teams[idx]
    
    def adjust(self, idx: int, delta: int) -> None:
        """Изменить очки команды
        
        Args:
            idx: Индекс команды
            delta: Изменение (может быть отрицательное)
        """
        if 0 <= idx < len(self.teams):
            self.teams[idx].add_score(delta)
    
    def get_sorted(self) -> List[Team]:
        """Получить команды отсортированные по очкам (убывание)
        
        Returns:
            Отсортированный список Team
        """
        return sorted(self.teams, key=lambda x: -x.score)
    
    def load_from(self, teams: Union[List[Dict], List[Team]]) -> None:
        """Загрузить команды из списка словарей или Team объектов
        
        Args:
            teams: Список словарей или Team объектов
        """
        self.teams = []
        for team_data in teams:
            if isinstance(team_data, dict):
                self.teams.append(Team.from_dict(team_data))
            elif isinstance(team_data, Team):
                self.teams.append(team_data)
    
    def to_dict_list(self) -> List[Dict]:
        """Конвертировать все команды в список словарей (для JSON)
        
        Returns:
            Список словарей
        """
        return [team.to_dict() for team in self.teams]

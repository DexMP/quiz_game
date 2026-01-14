# core/team.py
"""Модель команды для квиза"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Team:
    """Представление команды с типизацией"""
    
    name: str
    score: int = 0
    id: Optional[int] = None  # ID на основе timestamp
    
    def __post_init__(self) -> None:
        """Генерировать ID если не задан"""
        if self.id is None:
            self.id = int(datetime.utcnow().timestamp() * 1000)
    
    def __hash__(self) -> int:
        """Позволяет использовать Team в set и dict"""
        return hash(self.id)
    
    def __eq__(self, other: object) -> bool:
        """Сравнение по ID"""
        if not isinstance(other, Team):
            return NotImplemented
        return self.id == other.id
    
    def __repr__(self) -> str:
        return f"Team(id={self.id}, name={self.name!r}, score={self.score})"
    
    def add_score(self, amount: int) -> None:
        """Добавить очки (может быть отрицательное)"""
        self.score = max(0, self.score + amount)
    
    def set_score(self, score: int) -> None:
        """Установить очки"""
        self.score = max(0, score)
    
    def to_dict(self) -> dict:
        """Конвертировать в словарь (для JSON)"""
        return {"id": self.id, "name": self.name, "score": self.score}
    
    @staticmethod
    def from_dict(data: dict) -> "Team":
        """Создать Team из словаря"""
        return Team(
            name=data["name"],
            score=data["score"],
            id=data.get("id")
        )

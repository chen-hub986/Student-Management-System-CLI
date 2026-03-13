from abc import ABC, abstractmethod
from src.student import Student


class BaseRepository(ABC):
    @abstractmethod
    def load_students(self) -> list[Student]:
        pass

    @abstractmethod
    def save_students(self, students_list: list[Student]) -> None:
        pass

    @abstractmethod
    def export_to_csv(self, students, filename: str) -> None:
        pass

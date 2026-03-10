from scr.manager import StudentManager
from scr.student import Student
from scr.exceptions import StudentNotFoundException, DuplicateStudentException, InvalidScoreException, EmptyStudentListException
from scr.base_repository import BaseRepository
from scr.logger import Logger

import pytest


class InMemoryRepository(BaseRepository):
    def __init__(self):
        self.students = []

    def load_students(self) -> list[Student]:
        return self.students

    def save_students(self, students_list: list[Student]) -> None:
        self.students = students_list
    
    def export_to_csv(self, students: list[Student], filename: str) -> None:
        """
        Mock implementation for testing.
        在單元測試中，我們不需要真的把檔案寫入硬碟，所以使用 pass 即可。
        """
        pass

@pytest.fixture
def students_manager():
    repo = InMemoryRepository()
    logger = Logger()
    return StudentManager(repository=repo, logger=logger)

def test_average_empty_scores():
    with pytest.raises(InvalidScoreException):
        student = Student(name="Empty", scores=[])
    

def test_add_student(students_manager):
    student = students_manager.add_student("Alice", [90, 95, 85])
    assert student.name == "Alice"
    assert student.scores == [90, 95, 85]
    assert student.average_score == 90.0

def test_add_student_invalid_scores(students_manager):
    with pytest.raises(InvalidScoreException):
        students_manager.add_student("Bob", [90, -5, 85])  # Invalid score

def test_add_student_non_numeric_scores(students_manager):
    with pytest.raises(InvalidScoreException):
        students_manager.add_student("Charlie", [90, "A", 85])  # Non-numeric score

def test_add_student_empty_scores(students_manager):
    with pytest.raises(InvalidScoreException):
        students_manager.add_student("David", []) # Empty scores list

def test_add_duplicate_student(students_manager):
        students_manager.add_student("Alice", [90, 95, 85])
        with pytest.raises(DuplicateStudentException):
            students_manager.add_student("Alice", [80, 85, 90])

def test_delete_student(students_manager):
    students_manager.add_student("Bob", [80, 85, 90])
    students_manager.delete_student("Bob")
    assert None == next((student for student in students_manager.students if student.name == "Bob"), None)
    assert all(student.name != "Bob" for student in students_manager.students)

def test_delete_student_not_found(students_manager):
    students_manager.add_student("Alice", [90, 95, 85])
    with pytest.raises(StudentNotFoundException):
        students_manager.delete_student("NonExistentStudent")

def test_modify_student(students_manager):
    students_manager.add_student("Charlie", [70, 75, 80])
    modified_student = students_manager.modify_student("Charlie", [85, 90, 95])
    assert modified_student is not None
    assert modified_student.scores == [85, 90, 95]
    assert modified_student.average_score == 90.0

def test_get_avg_score(students_manager):    
    students_manager.add_student("David", [60, 65, 70])
    students_manager.add_student("Alice", [90, 95, 85])
    students_manager.add_student("Charlie", [80, 85, 90])
    avg_score = students_manager.get_class_statistics()
    assert avg_score["overall_average"] == (90.0 + 85.0 + 65.0) / 3
    assert avg_score["max_student"] == "Alice"
    assert avg_score["min_student"] == "David"

def test_get_ranking(students_manager):
    students_manager.add_student("David", [60, 65, 70])  # Average: 65
    students_manager.add_student("Alice", [90, 95, 85])  # Average: 90
    students_manager.add_student("Charlie", [80, 85, 90]) # Average: 85
    
    ranking = students_manager.get_sorted_students(
        sort_key=lambda s: s.average_score, 
        reverse=True
    )
    assert ranking[0].name == "Alice"
    assert ranking[1].name == "Charlie"
    assert ranking[2].name == "David"

def test_get_ranking_empty(students_manager):
    with pytest.raises(EmptyStudentListException):
        students_manager.get_sorted_students(sort_key=lambda s: s.average_score)

def test_get_sorted_students_by_name(students_manager):
    students_manager.add_student("Zac", [60, 60, 60])
    students_manager.add_student("Bob", [70, 70, 70])
    students_manager.add_student("Alice", [80, 80, 80])
    
    # 測試 A -> Z 排序
    result = students_manager.get_sorted_students(sort_key=lambda s: s.name.lower(), reverse=False)
    
    assert result[0].name == "Alice"
    assert result[1].name == "Bob"
    assert result[2].name == "Zac"

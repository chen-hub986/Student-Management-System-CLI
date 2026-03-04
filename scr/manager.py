from scr.student import Student
from scr.exceptions import StudentNotFoundException, DuplicateStudentException,  emptyStudentListException
from typing import List, Optional, Callable
from scr.base_repository import BaseRepository
from scr.logger import Logger


class StudentManager:
    def __init__(self, repository: BaseRepository, logger: Logger):
        self.repository = repository
        self.students = self.repository.load_students()
        self.logger = logger

    def save_students(self) -> None:
        self.repository.save_students(self.students)

    def find_student(self, name: str) -> Student:
        for student in self.students:
            if student.name == name:
                return student
        raise StudentNotFoundException(f"學生 {name} 不存在。")
        
    def _validate_name(self, name: str) -> None:
        if any(student.name == name for student in self.students):
            raise DuplicateStudentException(f"學生 {name} 已存在，無法重複添加。")
        
    def _validate_empty_student_list(self) -> None:
        if not self.students:
            raise emptyStudentListException("沒有學生資料，無法進行操作。")
        
    def get_students(self):
        self._validate_empty_student_list()
        return self.students
        
    def add_student(self, name: str, scores: List[float]) -> Student:
         self._validate_name(name)

         student = Student(name, scores)
         self.students.append(student)

         self.save_students()

         self.logger.log_info(f"成功添加學生 {name} 的資料，平均成績為 {student.average_score:.2f}")

         return student

    def delete_student(self, name: str) -> None:
        self._validate_empty_student_list()

        student_to_deleted = self.find_student(name)
        
        self.students.remove(student_to_deleted)
        
        self.save_students()
        self.logger.log_info(f"成功刪除學生 {name}")
        return

    def modify_student(self, name: str, scores: List[float]) -> Optional[Student]:
        self._validate_empty_student_list()

        student = self.find_student(name)
        student.scores = scores

        self.save_students()
        self.logger.log_info(f"成功修改學生 {name} 的資料，平均成績為 {student.average_score:.2f}")
        return student  # 返回修改後的學生資料

    def get_class_statistics(self) -> dict:
        self._validate_empty_student_list()
        
        averages = [student.average_score for student in self.students]
        total_students = len(averages)

        overall_average = sum(averages) / total_students

        student_average = list(zip([student.name for student in self.students], averages))
        
        max_student, max_average_score = max(student_average, key=lambda x: x[1])
        min_student, min_average_score = min(student_average, key=lambda x: x[1])

        passing_count = sum(1 for score in averages if score >= 60)
        passing_rate = (passing_count / total_students) * 100

        sorted_averages = sorted(averages)
        mid_index = total_students // 2

        if total_students % 2 == 0:
            median = (sorted_averages[mid_index - 1] + sorted_averages[mid_index]) / 2
        else:
            median = sorted_averages[mid_index]
        
        return {
            "student_averages": student_average,
            "overall_average": overall_average,
            "max_student": max_student,
            "max_average_score": max_average_score,
            "min_student": min_student,
            "min_average_score": min_average_score,
            "total_students" : total_students,
            "median" : median,
            "passing_rate" : passing_rate
        }
        
    def get_ranking(self) -> List[Student]:
        self._validate_empty_student_list()
        sorted_students = sorted(self.students, key=lambda student: student.average_score, reverse=True)
        return sorted_students
    
    def search_student_by_name(self, query: str) -> List[Student]:
        query = query.lower()
        return [student for student in self.students 
                if query in student.name.lower()
            ]
    
    def filter_students(self, criteria: Callable[[Student], bool]) ->List[Student]:
        return list(filter(criteria, self.students))
    

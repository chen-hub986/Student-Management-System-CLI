class StudentNotFoundException(Exception):
    # This exception is raised when a student is not found in the database.
    pass

class DuplicateStudentException(Exception):
    # This exception is raised when trying to add a student that already exists.
    pass

class InvalidScoreException(Exception):
    # This exception is raised when a score is invalid (e.g., negative or above 100).
    pass

class EmptyStudentListException(Exception):
    # This exception is raised when the student list is empty and an operation requires at least one student.
    pass


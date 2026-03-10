from functools import wraps
from typing import Any
from scr.logger import Logger
from scr.exceptions import StudentNotFoundException, DuplicateStudentException, EmptyStudentListException, InvalidScoreException


class MenuErrorHandler:
    def __init__(self, func):
        wraps(func)(self)
        self.func = func
        self.Logger = Logger()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        try:
            return self.func(*args, **kwds)
        except (EmptyStudentListException, StudentNotFoundException,
                DuplicateStudentException, InvalidScoreException) as e:
            self.Logger.log_error(str(e))
        except ValueError:
            self.Logger.log_error("成績輸入無效，請確保成績是數字並用逗號分隔。")
        except Exception as e:
            self.Logger.log_error(f"系統發生非預期錯誤: {e}")
            


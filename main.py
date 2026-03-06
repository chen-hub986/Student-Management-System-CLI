from scr.manager import StudentManager
from scr.repository import StudentRepository
from scr.logger import Logger
from scr.decorators import MenuErrorHandler


@MenuErrorHandler
def student_add(students_manager):
    while True:
        name = input("請輸入學生姓名（或輸入 'q' 結束）：")

        if not name.strip():
            print("請輸入學生姓名!")
            continue

        if name.lower() == 'q':
            break
                
        score = input("請輸入學生的成績（用逗號分隔）：")
        scores = [float(s.strip()) for s in score.split(',')]
        students_manager.add_student(name, scores)
    
@MenuErrorHandler
def show_students(students_manager):
    students_manager.get_students()

    print("\n" + "=" * 35)
    print(f"{'學生資料列表:':^30}")
    print("=" * 35)

    for student in students_manager.students:
        print(f"{student.name} - 平均成績: {student.average_score:.2f}")

@MenuErrorHandler
def sorting_menu(students_manager):
    while True:
            print("\n請選擇:")
            print("1. 依平均成績排序 (高 -> 低) ")
            print("2. 依平均成績排序 (低 -> 高) ")
            print("3. 依學生姓名排序 (A -> Z) ")
            print("4. 依學生姓名排序 (Z -> A) ")
            print("5. 返回")
            choice = input("請輸入選項 (1-5) :")
            
            if choice == '1':
                sorted_list = students_manager.get_sorted_students(sort_key = lambda s: s.average_score, reverse = True)
                sort_title = "成績排序 (高 -> 低)"
            elif choice == '2':
                sorted_list = students_manager.get_sorted_students(sort_key = lambda s: s.average_score, reverse = False)
                sort_title = "成績排序 (低 -> 高)"
            elif choice == '3':
                sorted_list = students_manager.get_sorted_students(sort_key = lambda s: s.name.lower(), reverse = False)
                sort_title = "姓名排序 (A -> Z)"
            elif choice == '4':
                sorted_list = students_manager.get_sorted_students(sort_key = lambda s: s.name.lower(), reverse = True)
                sort_title = "姓名排序 (Z -> A)"
            elif choice == '5':
                break
            else:
                print("無效的選項，請重新輸入！")
                continue

            print(f"\n{sort_title}結果：")
            for rank, student in enumerate(sorted_list, 1):
                print(f"{rank:>2}. {student.name:<10} - 平均成績: {student.average_score:>6.2f}")

@MenuErrorHandler
def delete_student(students_manager):
    students_manager.get_students()

    print(f"學生資料列表: {[student.name for student in students_manager.students]}")   
    name = input("請輸入要刪除的學生姓名：")
            
    if not name.strip():
        print("請輸入學生姓名!")
        return
    
    students_manager.find_student(name)

    print(f"正在刪除學生 {name} 的資料...")
                
    students_manager.delete_student(name)

@MenuErrorHandler
def modify_student(students_manager):
    students_manager.get_students()

    print(f"學生資料列表: {[student.name for student in students_manager.students]}")
    name = input("請輸入要修改的學生姓名：")

    if not name.strip():
        print("請輸入學生姓名!")
        return

    students_manager.find_student(name)
    
    score = input("請輸入新的成績（用逗號分隔）：")
    print(f"正在修改學生 {name} 的資料...")

    scores = [float(s.strip()) for s in score.split(',')]
    update_result = students_manager.modify_student(name, scores)
    if update_result:
        return
    
@MenuErrorHandler
def search_students(students_manager):

    name = input("請輸入學生姓名關鍵字:")

    if not name.strip():
        print("請輸入學生姓名!")
        return

    search_result = students_manager.search_student_by_name(name)
    
    if not search_result:
        print(f"找不到包含{name}關鍵字的學生。")
        return
    else:
        print(f"找到了{len(search_result)}筆結果:")
        print("-" * 30)
        for s in search_result:
            print(f"姓名:{s.name} | 平均成績:{s.average_score:.2f}")
            print("-" * 30)

@MenuErrorHandler
def show_top_students(students_manager):

    print("尋找優等生 (平均成績 > 80)...")

    top_students = students_manager.filter_students(lambda s: s.average_score >= 80)

    if not top_students:
        print("沒有結果。")
        return
    else:
        for s in top_students:
            print("-" * 30)
            print(f"姓名:{s.name} | 平均成績:{s.average_score:.2f}")
            print("-" * 30)

@MenuErrorHandler
def search_filter_menu(students_manager):
    while True:
        print("\n請選擇:")
        print("1. 搜尋學生")
        print("2. 列出優等生")
        print("3. 返回")
        choice = input("請輸入選項（1-3）：")

        if choice == '1':
            search_students(students_manager)
        elif choice == '2':
            show_top_students(students_manager)
        elif choice == '3':
            break
        else:
            print("無效的選項，請重新輸入！")

@MenuErrorHandler
def class_statistics(students_manager):

    print("\n統計中...")

    class_statistics = students_manager.get_class_statistics()
    
    print("\n" + "=" * 35)
    print(f"{'班級統計報告':^30}")
    print("=" * 35)

    print("-" * 35)
    print(f"總人數:{class_statistics['total_students']:>10}人")
    print(f"全班總平均:{class_statistics['overall_average']:>10.2f}分")
    print(f"分數中位數:{class_statistics['median']:>10.2f}分")
    print(f"及格率:{class_statistics['passing_rate']:>10.1f}%")
    print(f"\n最高平均成績的學生是: {class_statistics['max_student']}，成績為 {class_statistics['max_average_score']:.2f}")
    print(f"\n最低平均成績的學生是: {class_statistics['min_student']}，成績為 {class_statistics['min_average_score']:.2f}")

    print("-" * 35)

@MenuErrorHandler
def class_statistics_menu(students_manager):
    while True:
        print("\n請選擇:")
        print("1. 顯示學生資料")
        print("2. 顯示班級統計報告")
        print("3. 返回")
        choice = input("請輸入選項（1-3）：")

        if choice == '1':
            show_students(students_manager)
        elif choice == '2':
            class_statistics(students_manager)
        elif choice == '3':
            break
        else:
            print("無效的選項，請重新輸入！")

@MenuErrorHandler
def export_to_csv(students_manager):
    print("\n準備匯出資料...")

    students_manager.export_to_csv()

    print("資料已成功匯出至 'students.csv'!")
    print("小提示：你可以直接在資料夾找到它，並用 Excel 或 VS Code 打開查看。")
    print("-" * 35)


def main():
    Logger().log_info("學生管理系統啟動")
    students_repository = StudentRepository('students.json')
    logger = Logger()
    students_manager = StudentManager(students_repository, logger)
    while True:
        print("\n選擇操作：")
        print("1. 添加學生資料")
        print("2. 排序成績排名選單")
        print("3. 刪除學生資料")
        print("4. 修改學生資料")
        print("5. 列出優等生或搜尋學生")
        print("6. 班級統計報告頁面")
        print("7. 匯出成.csv")
        print("8. 退出程式")
        choice = input("請輸入選項（1-8）：")
        
        if choice == '1':
            student_add(students_manager)
        elif choice == '2':
            sorting_menu(students_manager)
        elif choice == '3':
            delete_student(students_manager)
        elif choice == '4':
            modify_student(students_manager)
        elif choice == '5':
            search_filter_menu(students_manager)
        elif choice == '6':
            class_statistics_menu(students_manager)
        elif choice == '7':
            export_to_csv(students_manager)
        elif choice == '8':
            print("退出程式。")
            Logger().log_info("學生管理系統關閉")
            break
        else:
            print("無效的選項，請重新輸入！")

if __name__ == "__main__":
    main()

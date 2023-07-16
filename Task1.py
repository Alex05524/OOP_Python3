import csv

class NameDescriptor:
    def __get__(self, instance, owner):
        return instance._name
    
    def __set__(self, instance, value):
        if not value.isalpha() or not value.istitle():
            raise ValueError("Invalid name format. Only alphabetical characters with first letter capitalized are allowed.")
        instance._name = value

class SubjectDescriptor:
    def __init__(self, subjects_file):
        self.subjects = self.load_subjects(subjects_file)
    
    def load_subjects(self, file):
        with open(file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            subjects = next(reader, [])
        return subjects
    
    def __get__(self, instance, owner):
        return self.subjects
    
    def __set__(self, instance, value):
        raise AttributeError("Can't modify subjects directly. Use the 'add_score' method.")

class Student:
    name = NameDescriptor()
    subjects = SubjectDescriptor('subjects.csv')
    
    def __init__(self):
        self.scores = {subject: {'grades': [], 'test_results': []} for subject in self.subjects}
    
    def add_score(self, subject, grade, test_result):
        if subject not in self.subjects:
            raise ValueError(f"{subject} is not a valid subject for this student.")
        
        if grade < 2 or grade > 5:
            raise ValueError("Invalid grade. Only values between 2 and 5 are allowed.")
        
        if test_result < 0 or test_result > 100:
            raise ValueError("Invalid test result. Only values between 0 and 100 are allowed.")
        
        self.scores[subject]['grades'].append(grade)
        self.scores[subject]['test_results'].append(test_result)
    
    def get_average_test_score(self, subject):
        if subject not in self.subjects:
            raise ValueError(f"{subject} is not a valid subject for this student.")
        
        test_results = self.scores[subject]['test_results']
        if not test_results:
            return 0
        
        return sum(test_results) / len(test_results)
    
    def get_average_grades(self):
        all_grades = []
        for subject in self.subjects:
            all_grades.extend(self.scores[subject]['grades'])
        
        if not all_grades:
            return 0
        
        return sum(all_grades) / len(all_grades)
student = Student()
student.name = "John Smith"

# Добавление оценок и результатов тестов для каждого предмета
student.add_score('Math', 4, 80)
student.add_score('Math', 3, 75)
student.add_score('English', 5, 90)
student.add_score('English', 4, 85)

# Получение среднего балла по тестам для каждого предмета
math_average = student.get_average_test_score('Math')
english_average = student.get_average_test_score('English')
print(f"Average test score for Math: {math_average}")
print(f"Average test score for English: {english_average}")

# Получение среднего балла по оценкам для всех предметов
average_grades = student.get_average_grades()
print(f"Average grades for all subjects: {average_grades}")    
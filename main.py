from collections import defaultdict


# Вычисление средней оценки
def aver(grades):
	all_grades = sum(grades.values(), [])
	if len(all_grades):
		average = sum(all_grades) / len(all_grades)
	else:
		average = 0  # Если оценок нет, ставим 0, для удобства сравнения и вычисления
	return average


class Student:
	def __init__(self, name, surname, gender):
		self.name = name
		self.surname = surname
		self.gender = gender
		self.finished_courses = []
		self.courses_in_progress = []
		self.grades = defaultdict(list)  # Словарь из collections для удобства добавления оценок

	def rate_hw(self, lector, course, grade):
		if (
				isinstance(lector, Lecturer)
				and course in lector.courses_attached
				and course in self.courses_in_progress
				and isinstance(grade, int)
		):
			if grade in range(1, 11):
				lector.grades[course].append(grade)
				# Словарь из collections позволяет заменить данной строчкой следующий код:
				# if course in lector.grades:
				# 	lector.grades[course] += [grade]
				# else:
				# 	lector.grades[course] = [grade]
		else:
			return 'Ошибка'

	def __str__(self):
		return (
			f'Имя: {self.name}\n'
			f'Фамилия: {self.surname}\n'
			f'Средняя оценка за домашние задания: {aver(self.grades)}\n'
			f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
			f'Завершенные курсы: {", ".join(self.finished_courses)}\n'
		)

	def __lt__(self, other):  # При сравнении выводим только сообщение у кого лучше оценки
		winner = "self" if aver(self.grades) > aver(other.grades) else "other"
		return "Оценки лучше у " + eval(winner).name


class Mentor:
	def __init__(self, name, surname):
		self.name = name
		self.surname = surname
		self.courses_attached = []


class Lecturer(Mentor):
	def __init__(self, name, surname):
		super().__init__(name, surname)
		self.grades = defaultdict(list)  # Словарь из collections для удобства добавления оценок

	def __str__(self):
		return (
			f'Имя: {self.name}\n'
			f'Фамилия: {self.surname}\n'
			f'Средняя оценка за лекции: {aver(self.grades)}\n'
		)

	def __lt__(self, other):
		return Student.__lt__(self, other)  # Чтобы не дублировать код, ссылаемся на такую же ф-ию у Student


class Reviewer(Mentor):
	def __init__(self, name, surname):
		super().__init__(name, surname)

	def rate_hw(self, student, course, grade):
		if (
				isinstance(student, Student)
				and course in self.courses_attached
				and course in student.courses_in_progress
				and isinstance(grade, int)
		):
			if grade in range(1, 11):
				student.grades[course].append(grade)
		else:
			return 'Ошибка'

	def __str__(self):
		return (
			f'Имя: {self.name}\n'
			f'Фамилия: {self.surname}\n'
		)


# Функции из задания 4:
def grades_aver_course(people_list, course):
	all_grades = []
	for person in people_list:  # Перебираем всех студентов или лекторов
		# Расширяем пустой список (extend) оценками студентов или лекторов, если курс в списке
		[all_grades.extend(person.grades[attached_course]) for attached_course in person.grades if attached_course == course]
	if all_grades:  # Проверяем что список не пустой чтобы избежать делиния на 0
		return sum(all_grades)/len(all_grades)


if __name__ == "__main__":

	Stas = Student('Stas', 'Romanov', 'm')
	Sergei = Student('Sergei', 'Nicolaev', 'm')
	Stas.courses_in_progress = ["Math", "Literature", "History"]
	Sergei.courses_in_progress = ["Math", "Literature", "Python"]

	Lena = Lecturer('Lena', 'Ivanova')
	Liza = Lecturer('Liza', 'Petrova')
	Lena.courses_attached = ["Math", "Literature", "History"]
	Liza.courses_attached = ["Math", "Literature", "Python"]

	Roman = Reviewer('Roman', 'Nicolich')
	Rita = Reviewer('Rita', 'Zapalova')
	Roman.courses_attached = ["Math", "Literature", "History"]
	Rita.courses_attached = ["Math", "Java", "Python"]

	for i in range(4, 11, 2):
		Stas.rate_hw(Lena, 'Math', i)
	Sergei.rate_hw(Lena, 'Python', 10)
	Sergei.rate_hw(Liza, 'Python', 11)
	Sergei.rate_hw(Liza, 'Python', "a")

	for i in range(1, 11, 3):
		Roman.rate_hw(Stas, 'Math', i)
	Roman.rate_hw(Stas, 'Literature', 10)
	Rita.rate_hw(Stas, 'Literature', "a")
	Rita.rate_hw(Stas, 'Math', "a")
	Rita.rate_hw(Stas, 'Math', "12")
	for i in range(6, 10):
		Rita.rate_hw(Sergei, 'Python', i)
	for i in range(6, 10):
		Rita.rate_hw(Sergei, 'Math', i)

	print(Stas)
	print(Sergei)
	print(Lena)
	print(Liza)
	print(Stas > Sergei)
	print(Liza > Lena)
	print("Проверка ф-ий задания 4:\n", "*"*40)

	print(Stas.grades)
	print(Sergei.grades)
	print(grades_aver_course([Stas, Sergei], 'Math'))

	print(Lena.grades)
	print(Liza.grades)
	print(grades_aver_course([Lena, Liza], 'Math'))


'''Функции хакинга электронного журнала'''

from .models import Mark, Chastisement, Commendation, Lesson, Schoolkid, Subject
import random


def find_schoolkid(name):
    try:
        child = Schoolkid.objects.get(full_name__contains=name)
    except  Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников по предоставленным данным. Укажите ФИО более подробно')
        return None
    except Schoolkid.DoesNotExist:
        print(f'Ученик "{name}" не найден')
        return None
    else:
        print(f'Найден ученик: {child}')
        return child

def find_subject(title, schoolkid):
    try:
        subject = Subject.objects.get(title__contains=title, year_of_study=schoolkid.year_of_study)
    except Subject.MultipleObjectsReturned:
        print('Найдено несколько предметов. Укажите название предмета более точно')
        return None
    except Subject.DoesNotExist:
        print(f'Предмета "{title}" не существует')
        return None
    else:
        print(f'Найден предмет: {subject}')
        return subject


def fix_marks(name):
    if not (schoolkid := find_schoolkid(name)):
        return
    print('Все двойки и тройки этого ученика будут заменены на пятерки!')    
    while not (choice := input('Продолжить (y/n)?')) in ['y', 'Y', 'n', 'N']:
        pass
    if choice in ['n', 'N']:
        print('Операция не выполнена!')
        return
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3]).update(points=5)


def remove_chastisements(name):
    if not (schoolkid := find_schoolkid(name)):
        return
    print('Все замечания этого ученика будут удалены!')
    while not (choice := input('Продолжить (y/n)?')) in ['y', 'Y', 'n', 'N']:
        pass
    if choice in ['n', 'N']:
        print('Операция не выполнена!')
        return
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(name, title):
    '''Создает похвалу'''

    if not (child := find_schoolkid(name)):
        return
    if not (subject := find_subject(title, child)):
        return

    lesson = random.choice(Lesson.objects.filter(
                                    year_of_study=child.year_of_study,
                                    group_letter=child.group_letter,
                                    subject__title=subject.title,
                                  ))
    print(f'Выбран урок {lesson.date} - {lesson}')

    with open("commendation.txt", "r") as _:
        file_contents = _.read()
    commendation_text = random.choice(file_contents.split("\n"))
    print(f'Выбрана фраза: {commendation_text}')
    while not (choice := input('Продолжить (y/n)?')) in ['y', 'Y', 'n', 'N']:
        pass
    if choice in ['n', 'N']:
        print('Операция не выполнена!')
        return

    if Commendation.objects.create(
                                text=commendation_text,
                                created=lesson.date,
                                subject=lesson.subject,
                                schoolkid=child,
                                teacher=lesson.teacher
                                                        ):
        print('Запись успешно добавлена в базу!')

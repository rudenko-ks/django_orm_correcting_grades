from datacenter.models import (Chastisement, Schoolkid, Mark, Lesson,
                               Commendation, Subject)
from django.core.exceptions import (MultipleObjectsReturned, ObjectDoesNotExist)
import random

COMMENDATIONS = [
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Ты меня очень обрадовал!",
    "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!",
]


def fix_marks(schoolkid_name: str) -> None:
    if not (schoolkid := _get_schoolkid(schoolkid_name)):
        return
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid_name: str) -> None:
    if not (schoolkid := _get_schoolkid(schoolkid_name)):
        return
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid_name: str, subject: str) -> None:
    if not (schoolkid := _get_schoolkid(schoolkid_name)):
        return
    subjects = [
        subject.title for subject in Subject.objects.filter(
            year_of_study=schoolkid.year_of_study)
    ]
    if subject not in subjects:
        subjects_list = "\n".join(sorted(subjects))
        print(f"Некорректное название предмета: '{subject}'")
        print(
            f"Список предметов для {schoolkid.year_of_study} класса:\n{subjects_list}"
        )
        return
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title__contains=subject).order_by('?').first()
    Commendation.objects.create(text=random.choice(COMMENDATIONS),
                                created=lesson.date,
                                schoolkid=schoolkid,
                                subject=lesson.subject,
                                teacher=lesson.teacher)


def _get_schoolkid(name: str) -> Schoolkid | None:
    if not name:
        print(f'Введите имя ученика.')
        return
    try:
        return Schoolkid.objects.get(full_name__contains=name.strip())
    except MultipleObjectsReturned:
        print(f'Найдено несколько учеников с именем "{name}".'
              ' Уточните имя для поиска.')
    except ObjectDoesNotExist:
        print(f'Ученик с именем "{name}" не найден.')


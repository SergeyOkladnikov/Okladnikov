"""Модуль, содержащий вспомогательные функции и словари, использующиеся в программме"""
from itertools import islice
import re
from datetime import datetime


class Dicts:
    """Класс, содержащий словари, используемые для печати, фильтрации и сортировки таблицы, формирования статистики"""
    dic_naming = {
        'name': 'Название',
        'description': 'Описание',
        'key_skills': 'Навыки',
        'experience_id': 'Опыт работы',
        'premium': 'Премиум-вакансия',
        'employer_name': 'Компания',
        'salary_from': 'Нижняя граница вилки оклада',
        'salary_to': 'Верхняя граница вилки оклада',
        'salary_gross': 'Оклад указан до вычета налогов',
        'salary_currency': 'Идентификатор валюты оклада',
        'area_name': 'Название региона',
        'published_at': 'Дата и время публикации вакансии',
        'TRUE': 'Да',
        'FALSE': 'Нет',
        'False': 'Нет',
        'True': 'Да',
        'noExperience': 'Нет опыта',
        'between1And3': 'От 1 года до 3 лет',
        'between3And6': 'От 3 до 6 лет',
        'moreThan6': 'Более 6 лет',
        'AZN': 'Манаты',
        'BYR': 'Белорусские рубли',
        'EUR': 'Евро',
        'GEL': 'Грузинский лари',
        'KGS': 'Киргизский сом',
        'KZT': 'Тенге',
        'RUR': 'Рубли',
        'UAH': 'Гривны',
        'USD': 'Доллары',
        'UZS': 'Узбекский сум'
    }

    experience_in_numbers = {
        'noExperience': 0,
        'between1And3': 3,
        'between3And6': 6,
        'moreThan6': 7,
    }


class Utils:
    """Класс, содержащий вспомогательные функции"""
    @staticmethod
    def cut_string(string):
        """
        Обрезает строку больше 100 символов, добавляя '...' в конце

        Args:
            string (str): Исходная строка

        Returns:
            str: Обрезанная строка
        """
        if string is None:
            return None
        if len(string) > 100:
            return string[0: 100] + '...'
        else:
            return string

    @staticmethod
    def format_num_string(num):
        """
        Удаляет дробную часть числа, разделяет группы разрядов пробелами

        Args:
            num (str): Исходная строка

        Returns:
            str: Строка формата X XXX XXX
        """
        num = Utils.cut_frac(num)
        num = num[::-1]
        return ' '.join(num[i:i + 3] for i in range(0, len(num), 3))[::-1]

    @staticmethod
    def format_date(string):
        """
        Принимает строки формата 'YYYY-mm-ddTHH:MM:SS+TZTZ', возвращает словарь, содержащий строку для вывода в таблице и соответствующее время в DateTime

        Args:
            string (str): Исходная строка в формате 'YYYY-mm-ddTHH:MM:SS+TZTZ'

        Returns:
            dict: {'output': Строка формата DD.MM.YYYY, 'time': Объект DateTime}
        """
        return {'output': f'{string[8:10]}.{string[5:7]}.{string[0:4]}',
                'time': datetime.strptime(string[:-5], "%Y-%m-%dT%H:%M:%S")}

    @staticmethod
    def get_split_count(string, sep):
        """
        Вычисляет количество элементов результата split по разделителю sep

        Args:
            string (str): Исходная строка
            sep (str): Разделитель

        Returns:
            int: Количество элементов результата split
        """
        if string == '':
            return 0
        else:
            return len(string.split(sep))

    @staticmethod
    def get_year(string):
        """
        Получает строку с годом из строки формата 'YYYY-mm-ddTHH:MM:SS+TZTZ'

        Args:
            string (str): Исходная строка

        Returns:
            str: Строка, в которой записан год из исходной строки
        """
        return datetime.strptime(string[:-5], "%Y-%m-%dT%H:%M:%S").year

    @staticmethod
    def format_string(input_string):
        """
        Форматирует строку, удаляя html-теги

        Args:
            input_string (str): Исходная строка

        Return:
            str: Отформатированная строка
        """
        result = re.sub(r'<[^<>]*>', '', input_string)
        result = re.sub(r'\n', '!crutch!!', result)
        result = str.strip(re.sub(r'\s+', ' ', result))
        return result

    @staticmethod
    def cut_frac(string):
        """
        Удаляет дробную часть строки, содержащей число

        Args:
            string (str): Исходная строка, может содержать дробную часть

        Return:
            str: Строка, в которой записано число без дробной части
        """
        if '.' in string:
            return string[:string.find('.')]
        return string

    @staticmethod
    def split_list(original, key_getter):
        """
        Разбивает список на группы по признаку, определяемому функцией key_getter

        Функция key_getter определяет значение признака у каждого элемента списка,
        формируется словарь, состоящий из пар "признак - список элементов"

        Args:
            original (list): Несгруппированный список
            key_getter (func): функция, вычисляющая у каждого элемента значение, но основании которого идёт группировка

        Returns:
            dict[Any, list]: Словарь с парами 'Общий признак - список'
        """
        groups = {}
        keys = []
        for element in original:
            key = key_getter(element)
            if key not in keys:
                keys.append(key)
                groups[key] = list()
            groups[key].append(element)
        return groups

    @staticmethod
    def get_first_dict_elements(dictionary, n):
        """
        Возвращает словарь с не более чем n первых элементов исходного

        Args:
            dictionary (dict): Исходный словарь
            n (int): Число нужных элементов

        Returns:
            dict: Обрезанный словарь
        """
        result = {}
        if n < 0:
            raise ValueError('index out of range')
        for key in list(islice(dictionary, n)):
            result[key] = dictionary[key]
        return result
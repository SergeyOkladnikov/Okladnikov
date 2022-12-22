"""Модуль - парсер csv-файлов"""
from utils import Dicts
from utils import Utils
import csv
import math


class Salary:
    """
    Класс, представляющий характеристики оклада

    Attributes:
        salary_from (int): Нижняя граница оклада
        salary_to (int): Верхняя граница оклада
        salary_gross (str): Приводится ли оклад до вычета налогов
        salary_currency (str): Валюта оклада
    """
    currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }

    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        """
        Инициализация объекта

        Args:
            salary_from (str): Нижняя граница оклада
            salary_to (str): Верхняя граница оклада
            salary_gross (str): Приводится ли оклад до вычета налогов
            salary_currency (str): Валюта оклада


        >>> type(Salary('10000', '20000', 'True', 'RUR')).__name__
        'Salary'
        >>> Salary('10000.0', '20000.1', 'True', 'RUR').salary_from
        '10000.0'
        >>> Salary('10000.0', '20000.1', 'True', 'RUR').salary_to
        '20000.1'
        >>> Salary('10000.0', '20000.1', 'True', 'RUR').salary_gross
        'True'
        >>> Salary('10000.0', '20000.1', 'True', 'RUR').salary_currency
        'RUR'
        """
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency

    def get_mean_salary(self):
        """
        Вычисляет целочисленное среднее значение оклада

        Returns:
            int: среднее арифметическое оклада

        >>> Salary('200', '300', 'True', 'EUR').get_mean_salary()
        250
        """
        return int((int(Utils.cut_frac(self.salary_from)) + int(Utils.cut_frac(self.salary_to))) / 2)

    def get_salary_in_rur(self):
        """
        Переводит объект Salary в российские рубли

        Returns:
            Salary: объект зарплаты в RUR

        >>> Salary('200', '300', 'True', 'EUR').get_salary_in_rur().salary_from
        '11980.0'
        >>> Salary('200', '300', 'True', 'EUR').get_salary_in_rur().salary_to
        '17970.0'
        >>> Salary('200', '300', 'True', 'EUR').get_salary_in_rur().salary_gross
        'True'
        >>> Salary('200', '300', 'True', 'EUR').get_salary_in_rur().salary_currency
        'RUR'

        >>> Salary('200', '300', 'True', 'RUR').get_salary_in_rur().salary_from
        '200.0'
        >>> Salary('200', '300', 'True', 'RUR').get_salary_in_rur().salary_to
        '300.0'
        >>> Salary('200', '300', 'True', 'RUR').get_salary_in_rur().salary_gross
        'True'
        >>> Salary('200', '300', 'True', 'RUR').get_salary_in_rur().salary_currency
        'RUR'
        """
        return Salary(salary_from=str(float(Utils.cut_frac(self.salary_from)) * Salary.currency_to_rub[self.salary_currency]),
                      salary_to=str(float(Utils.cut_frac(self.salary_to)) * Salary.currency_to_rub[self.salary_currency]),
                      salary_gross=self.salary_gross,
                      salary_currency='RUR')


class Vacancy:
    """
    Класс, описывающий вакансию

    Attributes:
        name (str): Название вакансии
        description (str): Описание вакансии
        key_skills (list[str]): Основные навыки
        experience_id (str): Опыт работы
        premium (str):  Является ли вакансия премиум-вакансией
        employer_name (str): Работадатель
        salary (Salary): данные об окладе в объекте класса Salary
        area_name (str): Название региона
        published_at (str): Дата публикации
    """
    def __init__(self,
                 name,
                 description,
                 key_skills,
                 experience_id,
                 premium,
                 employer_name,
                 salary_from,
                 salary_to,
                 salary_gross,
                 salary_currency,
                 area_name,
                 published_at):
        """
        Инициализация объекта

        Args:
            name (str): Название вакансии
            description (str): Описание вакансии
            key_skills (list[str]): Основные навыки
            experience_id (str): Опыт работы
            premium (str):  Является ли вакансия премиум-вакансией
            employer_name (str): Работадатель
            salary_from (str): Нижняя граница оклада
            salary_to (str): Верхняя граница оклада
            salary_gross (str): Приводится ли оклад до вычета налогов
            salary_currency (str): Валюта оклада
            area_name (str): Название региона
            published_at (str): Дата публикации

        >>> Vacancy('Инженер', 'Чё-то там', ['XXX', 'YYY'], 'between3and6', 'False', 'XYZ', '200', '300', 'True', 'EUR', 'Екатеринбург', '2022-07-15T09:56:52+0300').name
        'Инженер'
        >>> Vacancy('Инженер', 'Чё-то там', ['XXX', 'YYY'], 'between3and6', 'False', 'XYZ', '200', '300', 'True', 'EUR', 'Екатеринбург', '2022-07-15T09:56:52+0300').description
        'Чё-то там'
        >>> Vacancy('Инженер', 'Чё-то там', ['XXX', 'YYY'], 'between3and6', 'False', 'XYZ', '200', '300', 'True', 'EUR', 'Екатеринбург', '2022-07-15T09:56:52+0300').key_skills
        ['XXX', 'YYY']
        >>> Vacancy('Инженер', 'Чё-то там', ['XXX', 'YYY'], 'between3and6', 'False', 'XYZ', '200', '300', 'True', 'EUR', 'Екатеринбург', '2022-07-15T09:56:52+0300').experience_id
        'between3and6'
        >>> Vacancy('Инженер', 'Чё-то там', ['XXX', 'YYY'], 'between3and6', 'False', 'XYZ', '200', '300', 'True', 'EUR', 'Екатеринбург', '2022-07-15T09:56:52+0300').premium
        'False'
        >>> Vacancy('Инженер', 'Чё-то там', ['XXX', 'YYY'], 'between3and6', 'False', 'XYZ', '200', '300', 'True', 'EUR', 'Екатеринбург', '2022-07-15T09:56:52+0300').employer_name
        'XYZ'
        >>> type(Vacancy('Инженер', 'Чё-то там', ['XXX', 'YYY'], 'between3and6', 'False', 'XYZ', '200', '300', 'True', 'EUR', 'Екатеринбург', '2022-07-15T09:56:52+0300').salary).__name__
        'Salary'
        >>> Vacancy('Инженер', 'Чё-то там', ['XXX', 'YYY'], 'between3and6', 'False', 'XYZ', '200', '300', 'True', 'EUR', 'Екатеринбург', '2022-07-15T09:56:52+0300').area_name
        'Екатеринбург'
        >>> Vacancy('Инженер', 'Чё-то там', ['XXX', 'YYY'], 'between3and6', 'False', 'XYZ', '200', '300', 'True', 'EUR', 'Екатеринбург', '2022-07-15T09:56:52+0300').published_at
        '2022-07-15T09:56:52+0300'

        >>> Vacancy('Инженер', 'Чё-то там', ['XXX'], 'between3and6', 'False', 'XYZ', '200', '300', 'True', 'EUR', 'Екатеринбург', '2022-07-15T09:56:52+0300').key_skills
        ['XXX']
        >>> type(Vacancy('Инженер', 'Чё-то там', None, None, 'False', 'XYZ', '200', '300', 'True', 'EUR', 'Екатеринбург', '2022-07-15T09:56:52+0300').key_skills).__name__
        'NoneType'
        """
        self.name = name
        self.description = description
        self.key_skills = key_skills
        self.experience_id = experience_id
        self.premium = premium
        self.employer_name = employer_name
        self.salary = Salary(salary_from, salary_to, salary_gross, salary_currency)
        self.area_name = area_name
        self.published_at = published_at


class DataSet:
    """
    Класс, содержащий имя файла-списка вакансий, а также список объектов класса Vacancy, сформированный из данных файла

    Attributes:
        file_name (str): имя csv-файла
        vacancies_objects (list[Vacancy]): список объектов класса Vacancy
    """
    sorting = {
        'Название': lambda x: x.name,
        'Описание': lambda x: x.description,
        'Компания': lambda x: x.employer_name,
        'Навыки': lambda x: len(x.key_skills),
        'Опыт работы': lambda x: Dicts.experience_in_numbers[x.experience_id],
        'Премиум-вакансия': lambda x: x.premium,
        'Оклад': lambda x: x.salary.get_salary_in_rur().get_mean_salary(),
        'Название региона': lambda x: x.area_name,
        'Дата публикации вакансии': lambda x: Utils.format_date(x.published_at)['time'],
        'Идентификатор валюты оклада': lambda x: x.salary.salary_currency,
        'Оклад указан до вычета налогов': lambda x: x.salary.salary_gross
    }

    def __init__(self, file_name):
        """
        Инициализирует объект, составляя список объектов Vacancy со свойствами, соответствующими значениям строк файла

        Args:
            file_name (str): Путь к csv-файлу

        >>> type(DataSet('v.csv')).__name__
        'DataSet'
        >>> DataSet('v.csv').file_name
        'v.csv'
        >>> type(DataSet('v.csv').vacancies_objects).__name__
        'list'
        >>> type(DataSet('v.csv').vacancies_objects[0]).__name__
        'Vacancy'
        >>> type(DataSet('v.csv').vacancies_objects[0].key_skills).__name__
        'list'
        >>> DataSet('v.csv').vacancies_objects[0].key_skills
        ['Организаторские навыки', 'Проведение презентаций', 'MS PowerPoint', 'Информационные технологии', 'Аналитическое мышление', 'Автоматизированное рабочее место (АРМ)', 'техническая грамотность']
        >>> type(DataSet('test_partial.csv').vacancies_objects[0].key_skills).__name__
        'NoneType'
        >>> type(DataSet('test_partial.csv').vacancies_objects[0].description).__name__
        'NoneType'
        >>> type(DataSet('test_partial.csv').vacancies_objects[0].experience_id).__name__
        'NoneType'
        >>> type(DataSet('test_partial.csv').vacancies_objects[0].premium).__name__
        'NoneType'
        >>> type(DataSet('test_partial.csv').vacancies_objects[0].employer_name).__name__
        'NoneType'
        >>> type(DataSet('test_partial.csv').vacancies_objects[0].salary.salary_gross).__name__
        'NoneType'
        """
        self.file_name = file_name
        self.vacancies_objects = []
        vacancies = []
        labels = []
        with open(file_name, encoding='utf-8-sig') as data:
            reader = csv.reader(data, delimiter=',')
            checker = 0
            for row in reader:
                if checker == 0:
                    checker += 1
                    labels = row
                else:
                    vacancies.append(row)
        cleaned_rows = []
        for row in vacancies:
            if all(row) and len(labels) == len(row):
                temp = []
                for i in range(len(row)):
                    temp.append(Utils.format_string(row[i]))
                cleaned_rows.append(temp)
        for row in cleaned_rows:
            vacancy = {}
            for i in range(len(labels)):
                vacancy[labels[i]] = row[i]

            def check_presence(vacancy, label):
                """
                Возвращает None, если искомого заголовка не существует

                Args:
                    vacancy (dict[str, str]) словарь  данными о вакансиях: 'Название характеристики - содержание'
                    label (str) - проверяемый заголовок
                """
                return None if label not in vacancy.keys() else vacancy[label]

            self.vacancies_objects.append(Vacancy(check_presence(vacancy, 'name'),
                                                  check_presence(vacancy, 'description'),
                                                  None if 'key_skills' not in vacancy.keys() else vacancy['key_skills'].split('!crutch!!'),
                                                  check_presence(vacancy, 'experience_id'),
                                                  check_presence(vacancy, 'premium'),
                                                  check_presence(vacancy, 'employer_name'),
                                                  check_presence(vacancy, 'salary_from'),
                                                  check_presence(vacancy, 'salary_to'),
                                                  check_presence(vacancy, 'salary_gross'),
                                                  check_presence(vacancy, 'salary_currency'),
                                                  check_presence(vacancy, 'area_name'),
                                                  check_presence(vacancy, 'published_at')))

    def length(self):
        """
        Возвращает длину списка вакансий

        Returns:
            int: Длина vacancies_objects
        """
        return len(self.vacancies_objects)

    def sort(self, sorting_criteria, is_reversed):
        """
        Сортирует vacancies_objects данного объекта по критерию из клчей словаря sorting

        Args:
            sorting_criteria (str): Критерий сортировки - название столбца - критерия
            is_reversed (str): При значении 'Да' сортировка происходит по убыванию

        >>> data = DataSet('sorting_test.csv')
        >>> data.sort('Название', 'Нет')
        >>> [x.name for x in data.vacancies_objects]
        ['HTML-верстальщик', 'HTML-верстальщик (remote)', 'Information Security Policy Specialist (Methodology)', 'Senior Python Developer (Crypto)', 'Руководитель проекта по системам связи и информационным технологиям']
        >>> data = DataSet('sorting_test.csv')
        >>> data.sort('Навыки', 'Нет')
        >>> [x.name for x in data.vacancies_objects]
        ['Information Security Policy Specialist (Methodology)', 'Senior Python Developer (Crypto)', 'Руководитель проекта по системам связи и информационным технологиям', 'HTML-верстальщик (remote)', 'HTML-верстальщик']
        >>> data = DataSet('sorting_test.csv')
        >>> data.sort('Опыт работы', 'Нет')
        >>> [x.name for x in data.vacancies_objects]
        ['HTML-верстальщик', 'HTML-верстальщик (remote)', 'Руководитель проекта по системам связи и информационным технологиям', 'Senior Python Developer (Crypto)', 'Information Security Policy Specialist (Methodology)']
        >>> data = DataSet('sorting_test.csv')
        >>> data.sort('Оклад', 'Нет')
        >>> [x.name for x in data.vacancies_objects]
        ['Руководитель проекта по системам связи и информационным технологиям', 'HTML-верстальщик', 'HTML-верстальщик (remote)', 'Senior Python Developer (Crypto)', 'Information Security Policy Specialist (Methodology)']
        >>> data = DataSet('sorting_test.csv')
        >>> data.sort('Дата публикации вакансии', 'Нет')
        >>> [x.name for x in data.vacancies_objects]
        ['Senior Python Developer (Crypto)', 'HTML-верстальщик', 'HTML-верстальщик (remote)', 'Information Security Policy Specialist (Methodology)', 'Руководитель проекта по системам связи и информационным технологиям']
        >>> data = DataSet('sorting_test.csv')
        >>> data.sort('Название', 'Да')
        >>> [x.name for x in data.vacancies_objects]
        ['Руководитель проекта по системам связи и информационным технологиям', 'Senior Python Developer (Crypto)', 'Information Security Policy Specialist (Methodology)', 'HTML-верстальщик (remote)', 'HTML-верстальщик']
        """

        is_reversed = is_reversed == 'Да'
        self.vacancies_objects.sort(key=self.sorting[sorting_criteria], reverse=is_reversed)

    @staticmethod
    def format_filter_criteria(filter_criteria):
        """
        Возвращает словарь, содержащий название и значение параметра фильтрации

        Args:
            filter_criteria (str): Критерий фильтрации - строка формата 'Название столбца: содержание ячейки'
        Returns:
             dict: {'label': Название поля-критерия,
                    'content': Подходящее значение поля-критерия}
        """
        filter_criteria = filter_criteria.split(': ')
        return {
            'label': filter_criteria[0] if filter_criteria[0] not in Dicts.dic_naming.keys() else Dicts.dic_naming[
                filter_criteria[0]],
            'content': '' if filter_criteria[0] == '' else (
                filter_criteria[1] if filter_criteria[1] not in Dicts.dic_naming.keys() else Dicts.dic_naming[
                    filter_criteria[1]])
        }

    def filter(self, filter_criteria):
        """
        Фильтрует свойство vacancies_objects данного DataSet по критерию

        Args:
            filter_criteria (str): Критерий фильтрации - строка формата 'Название столбца: содержание ячейки'
        """
        filter_criteria = self.format_filter_criteria(filter_criteria)
        filtering = {
            '': lambda x: True,
            'Название': lambda x: x.name == filter_criteria['content'],
            'Описание': lambda x: x.description == filter_criteria['content'],
            'Компания': lambda x: x.employer_name == filter_criteria['content'],
            'Навыки': lambda x: set(filter_criteria['content'].split(', ')).issubset(x.key_skills),
            'Опыт работы': lambda x: Dicts.dic_naming[x.experience_id] == filter_criteria['content'],
            'Премиум-вакансия': lambda x: Dicts.dic_naming[x.premium] == filter_criteria['content'],
            'Оклад': lambda x: int(Utils.cut_frac(x.salary.salary_from)) <= int(filter_criteria['content']) <= int(
                Utils.cut_frac(x.salary.salary_to)),
            'Название региона': lambda x: x.area_name == filter_criteria['content'],
            'Дата публикации вакансии': lambda x: Utils.format_date(x.published_at)['output'] == filter_criteria[
                'content'],
            'Идентификатор валюты оклада': lambda x: Dicts.dic_naming[x.salary.salary_currency] == filter_criteria[
                'content'],
            'Оклад указан до вычета налогов': lambda x: Dicts.dic_naming[x.salary.salary_gross] == filter_criteria[
                'content']
        }
        self.vacancies_objects = list(filter(filtering[filter_criteria['label']], self.vacancies_objects))

    def get_filtered_vacancies(self, filter_criteria):
        """
        Возвращает отфильтрованное по критерию свойство vacancies_objects данного DataSet

        Args:
            filter_criteria (str): критерий сортировки - строка формата 'Название столбца: содержание ячейки'

        Returns:
            list[Vacancy]: отфильтрованный список вакансий
        """
        filter_criteria = self.format_filter_criteria(filter_criteria)
        filtering = {
            '': lambda x: True,
            'Название': lambda x: x.name == filter_criteria['content'],
            'Описание': lambda x: x.description == filter_criteria['content'],
            'Компания': lambda x: x.employer_name == filter_criteria['content'],
            'Навыки': lambda x: set(filter_criteria['content'].split(', ')).issubset(x.key_skills),
            'Опыт работы': lambda x: Dicts.dic_naming[x.experience_id] == filter_criteria['content'],
            'Премиум-вакансия': lambda x: Dicts.dic_naming[x.premium] == filter_criteria['content'],
            'Оклад': lambda x: int(Utils.cut_frac(x.salary.salary_from)) <= int(filter_criteria['content']) <= int(
                Utils.cut_frac(x.salary.salary_to)),
            'Название региона': lambda x: x.area_name == filter_criteria['content'],
            'Дата публикации вакансии': lambda x: Utils.format_date(x.published_at)['output'] == filter_criteria[
                'content'],
            'Идентификатор валюты оклада': lambda x: Dicts.dic_naming[x.salary.salary_currency] == filter_criteria[
                'content'],
            'Оклад указан до вычета налогов': lambda x: Dicts.dic_naming[x.salary.salary_gross] == filter_criteria[
                'content']
        }
        return list(filter(filtering[filter_criteria['label']], self.vacancies_objects))


if __name__ == "__main__":
    import doctest
    doctest.testmod()

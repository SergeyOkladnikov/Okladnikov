"""Модуль, отвечающий за печать, фильтрацию и сортировку таблицы вакансий"""
from utils import Utils
import os
from prettytable import PrettyTable


class TablePrinter:
    """
    Класс, отвечающий за печать таблицы вакансий

    Attributes:
        data (DataSet): объект DataSet с вакансиями для печати
        filter_criteria (str): Критерий фильтрации - строка формата 'Название столбца: содержание ячейки'
        sorting_criteria (str): Критерий сортировки - название столбца - критерия
        sort_reversed (str): При значении true сортировка происходит по убыванию
        from_to (str): Диапазон вывода - строка 'номер строки - номер строки', первая строка включается, последняя - нет
        fields (str): Названия требуемых столбцов, разделённые запятой и пробелом
    """
    possible_criteria = ['Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия',
                         'Компания', 'Оклад', 'Название региона', 'Дата публикации вакансии',
                         'Идентификатор валюты оклада', 'Оклад указан до вычета налогов']

    def __init__(self, data_set):
        """
        Инициализация объекта, получение параметров таблицы

        Args:
            data_set (DataSet): объект DataSet, содержание которого нужно представить в таблице
        """
        self.data = data_set
        self.filter_criteria = input('Введите параметр фильтрации: ')
        self.sorting_criteria = input('Введите параметр сортировки: ')
        self.sort_reversed = input('Обратный порядок сортировки (Да / Нет): ')
        self.from_to = input('Введите диапазон вывода: ')
        self.fields = input('Введите требуемые столбцы: ')

    def print_table(self, dictionary):
        """
        Печатает таблицу с помощью библиотеки PrettyTable

        Args:
            dictionary (dict{string: string}): Словарь для перевода названий столбцов и некоторых значений ячеек таблицы
        """
        if self.filter_criteria != '' and not ':' in self.filter_criteria:
            print('Формат ввода некорректен')
            return
        if self.filter_criteria.split(': ')[0] != '' and not self.filter_criteria.split(': ')[0] in self.possible_criteria:
            print('Параметр поиска некорректен')
            return
        if self.sorting_criteria not in self.possible_criteria and self.sorting_criteria != '':
            print('Параметр сортировки некорректен')
            return
        if self.sort_reversed not in ['Да', 'Нет', '']:
            print('Порядок сортировки задан некорректно')
            return
        if os.stat(self.data.file_name).st_size == 0:
            print("Пустой файл")
            return

        if self.data.length() == 0:
            print('Нет данных')
            return
        if self.sorting_criteria != '':
            self.data.sort(self.sorting_criteria, self.sort_reversed)

        def check_for_none(content, handler=lambda x: x, stub=''):
            """
            В случае, если проверяемое значение - None, возвращает строку-"заглушку", иначе - результат обработки значения функцией handler

            Args:
                content (str): Проверяемое значение
                handler (func): Функция-обработчик значения, по умолчанию - не обрабатывает значение
                stub (str): Заглушка, по умолчанию - пустая строка
            """
            return handler(content) if content is not None else stub

        vacancies = self.data.get_filtered_vacancies(self.filter_criteria)
        if len(vacancies) == 0:
            print('Ничего не найдено')
            return
        labels = ['№', 'Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия',
                  'Компания', 'Оклад', 'Название региона', 'Дата публикации вакансии']
        table = PrettyTable(field_names=labels)

        table.hrules = 1
        table.max_width = 20
        table.align = 'l'

        for i in range(len(vacancies)):
            vacancy = vacancies[i]
            salary = vacancy.salary
            table.add_row([
                i + 1,
                check_for_none(vacancy.name),
                check_for_none(vacancy.description, lambda x: Utils.cut_string(x)),
                check_for_none(vacancy.key_skills, lambda x: Utils.cut_string('\n'.join(x))),
                check_for_none(vacancy.experience_id, lambda x: dictionary[x]),
                check_for_none(vacancy.premium, lambda x: dictionary[x]),
                check_for_none(vacancy.employer_name),
                check_for_none(salary, lambda x: f'{Utils.format_num_string(x.salary_from)} - {Utils.format_num_string(x.salary_to)} ({dictionary[x.salary_currency]}) ' + (
                    '(Без вычета налогов)' if (x.salary_gross == 'TRUE' or x.salary_gross == 'true' or x.salary_gross == 'True') else '(С вычетом налогов)')),
                check_for_none(vacancy.area_name),
                check_for_none(vacancy.published_at, lambda x: Utils.format_date(x)['output'])
            ])

        border_variant = Utils.get_split_count(self.from_to, ' ')
        from_to = self.from_to.split(' ')
        fields = self.fields

        cut_borders_variants = {
            0: lambda: (0, len(vacancies)),
            1: lambda: ((int(from_to[0]) - 1), len(vacancies)),
            2: lambda: (int(from_to[0]) - 1, int(from_to[1]) - 1)
        }
        start = cut_borders_variants[border_variant]()[0]
        end = cut_borders_variants[border_variant]()[1]
        if fields != '':
            fields = fields.split(', ')
            fields.insert(0, '№')
            print(table.get_string(start=start, end=end, fields=fields))
        else:
            print(table.get_string(start=start, end=end))
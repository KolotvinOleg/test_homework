from datetime import datetime, date
from typing import Union
import csv


class BankAccount:
    def __init__(self, name: str, balance: Union[int, float], file_name: str):
        self.name = name
        self.__balance = balance
        self.file_name = file_name
        self.number = 1  # Порядковый номер операции получения или расходования денежных средств
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Порядковый номер', 'Дата', 'Категория', 'Сумма', 'Описание'])

    @property
    def balance(self) -> Union[int, float]:
        return self.__balance

    def validate_money(self, value: str) -> None:
        try:
            value = float(value)
        except ValueError:
            raise ValueError('Сумма денежных средств должна быть положительным числом')
        if float(value) <= 0:
            raise ValueError('Сумма денежных средств для совершения операции должна быть больше нуля.')

    def expenditure_operation(self) -> None:
        """Метод списания денежных средств со счета"""

        value = input('Укажите сумму расходной операции: ')
        self.validate_money(value)
        value = float(value)
        date_1 = input('Укажите дату расходной операции в формате "дд.мм.гггг": ')
        try:
            date_operation = datetime.strptime(date_1, '%d.%m.%Y').date()
            today = date.today()
            if date_operation > today:
                raise TypeError()
        except TypeError:
            raise ValueError('Введите дату не позднее текущей.')
        except ValueError:
            raise ValueError('Дата совершения операции должна быть указана в формате "dd.mm.YYYY".')
        description = input('Укажите описание расходной операции: ')
        if value > self.__balance:
            raise ValueError(f'Недостаточно средств для данной операции. Текущий баланс: {self.__balance}')
        self.__balance -= value
        print(f'Списание денежных средств прошло успешно. Текущий баланс: {self.__balance}\n')
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.number, date_operation, 'Расход', value, description])
        self.number += 1

    def profitable_operation(self) -> None:
        """Метод добавления денежных средств на счет"""
        value = input('Укажите сумму доходной операции: ')
        self.validate_money(value)
        value = float(value)
        date_1 = input('Укажите дату доходной операции в формате "дд.мм.гггг": ')
        try:
            date_operation = datetime.strptime(date_1, '%d.%m.%Y').date()
            today = date.today()
            if date_operation > today:
                raise TypeError()
        except TypeError:
            raise ValueError('Введите дату не позднее текущей.')
        except ValueError:
            raise ValueError('Дата совершения операции должна быть указана в формате "dd.mm.YYYY".')
        description = input('Укажите описание доходной операции: ')
        self.__balance += value
        print(f'Поступление денежных средств прошло успешно. Текущий баланс: {self.__balance} \n')
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.number, date_operation, 'Доход', value, description])
        self.number += 1

    def find_info_in_file(self):
        """Функция поиска записей по одному из условий: "Категория", "Дата" или "Сумма". """

        category = input('Выберете условие для поиска записей: "Категория", "Дата" или "Сумма"  ')
        if category not in ["Категория", "Дата", "Сумма"]:
            raise ValueError('Указана неверная категория для поиска.')
        if category == 'Категория':
            search_value = input('Выберете доступную категорию: "Доход" или "Расход"  ')
            if search_value not in ['Доход', 'Расход']:
                raise ValueError('Для поиска по категории доступны только 2 значения: "Доход" и "Расход"')
        elif category == 'Дата':
            search_date = input('Укажите дату для поиска в формате "дд.мм.гггг": ')
            try:
                search_value = datetime.strptime(search_date, '%d.%m.%Y').date()
            except Exception:
                raise ValueError('Дата совершения операции должна быть указана в формате "dd.mm.YYYY".')
        elif category == 'Сумма':
            search_value = input('Укажите сумму для поиска записей: ')
            self.validate_money(search_value)
            search_value = float(search_value)
        with open(self.file_name) as file:
            reader = csv.DictReader(file)
            result = []
            for row in reader:
                if row[category] == str(search_value):
                    result.append(row)
            if not result:
                print('По данному условию записей не найдено.')
            else:
                print('Найденные записи по заданному условию:')
                for row in result:
                    print(f'Запись №{row["Порядковый номер"]}, дата операции: {row["Дата"]}, сумма - {row["Сумма"]}'
                          f', Описание: {row["Описание"]}')
        print()

    def change_row(self):
        """Функция для изменения записи по ее порядковому номеру"""
        try:
            number = int(input('Введите номер записи, которую хотите изменить: '))
            if number <= 0:
                raise ValueError()
        except ValueError as e:
            raise ValueError('Порядковый номер записи может быть только положительным целым числом.')
        change_category = input('Укажите какое поле записи вы хотите изменить: "Дата", "Сумма" или "Описание": ')
        if change_category not in ['Дата', 'Сумма', 'Описание']:
            raise ValueError('Указано несуществующее поле для изменения')
        new_value = input('Укажите новое значение: ')
        if change_category == 'Сумма':
            self.validate_money(new_value)
        if change_category == 'Дата':
            try:
                new_value = datetime.strptime(new_value, '%d.%m.%Y').date()
            except Exception:
                raise ValueError('Новая дата операции должна иметь формат "dd.mm.YYYY".')
        with open(self.file_name) as file:
            reader = list(csv.DictReader(file))
        for row in reader:
            if row['Порядковый номер'] == str(number):
                if change_category == 'Сумма':  # Если меняем сумму, меняем баланс и проверяем, чтобы он не стал меньше нуля
                    if row['Категория'] == 'Расход':
                        if self.__balance - (float(new_value) - float(row['Сумма'])) < 0:
                            raise ValueError('Данная операция запрещена, так как баланс после изменения '
                                             'станет меньше нуля.')
                        self.__balance -= (float(new_value) - float(row['Сумма']))
                    else:
                        self.__balance += float(new_value) - float(row['Сумма'])
                row[change_category] = new_value
                break
            else:
                raise ValueError('Указанный номер записи отсутствует в файле.')

        with open(self.file_name, 'w', newline='') as file:
            writer = csv.DictWriter(file, ['Порядковый номер', 'Дата', 'Категория', 'Сумма', 'Описание'])
            writer.writeheader()
            writer.writerows(reader)
        print('Обновление записи прошло успешно.')


info_str = """
 'Баланс' - Показать текущий баланс
 'Расход' - Добавить расходную операцию
 'Доход' - Добавить доходную операцию
 'Поиск' - Поиск записей по одному из условий: "Категория", "Дата" или "Сумма"
 'Изменение' - Изменение одного из полей записи по ее номеру 
 """

if __name__ == '__main__':
    name = input('Введите имя владельца финансового кошелька: ')
    balance = input('Укажите начальный баланс: ')
    while not balance.isdigit() or float(balance) < 0:
        print('Баланс должен быть положительным числом!')
        balance = input('Укажите начальный баланс: ')
    balance = float(balance)
    file_name = input('Укажите имя файла для хранения информации о финансовых операциях в формате csv: ')
    while len(file_name) < 5 or file_name[-4:] != '.csv':
        print('Имя файла должно иметь разрешение csv')
        file_name = input('Укажите имя файла для хранения информации о финансовых операциях в формате csv: ')
    my_banc_account = BankAccount(name, balance, file_name)
    while True:
        command = input('Укажите тип финансовой операции. Для просмотра всех доступных операций введите "Инфо". ')
        try:
            if command.lower() == 'инфо':
                print(info_str)
            elif command.lower() == 'баланс':
                print(f'Текущий баланс составляет {my_banc_account.balance}\n')
            elif command.lower() == 'расход':
                my_banc_account.expenditure_operation()
            elif command.lower() == 'доход':
                my_banc_account.profitable_operation()
            elif command.lower() == 'поиск':
                my_banc_account.find_info_in_file()
            elif command.lower() == 'изменение':
                my_banc_account.change_row()
            else:
                print('Недоступная операция!\n')
        except Exception as e:
            print(f'Ошибка: {e}\n')

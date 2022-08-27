"""
Менеджмент билетов.
Пользователь должен иметь возможность вести учёт проданных билетов.

Функции:
1) продажа билета: пользователь поочерёдно указывает имя, класс билета и
желаемое место (если доступно);
2) возврат билета по номеру места;
3) смена места в пределе класса (за доплату);
4) вывод списка билетов (порядок по номеру места);
5) вывод итоговой суммы с продажи билетов.

Общие параметры программы:
1) цена на билет эконом-класса;
2) цена на билет бизнес-класса;
3) цена за смену места.

Параметры билета:
1) имя - str с именем пассажира;
2) класс - str, один из двух символов: "E" (эконом), "B" (бизнес);
3) цена продажи - Decimal;
4) номер места - int в диапазоне 1-100 (бизнес: 1-10, эконом: 11-100).
"""
import textwrap
from decimal import Decimal
from operator import itemgetter

# textwrap.dedent() обрезает отступы в начале строк
MAIN_MENU = textwrap.dedent("""
    Список команд:
    1) добавить билет;
    2) вернуть билет;
    3) смена места в пределе класса;
    4) вывод списка билетов (порядок по номеру места);
    5) вывод итоговой суммы с продажи билетов;
    q) выход.
""").strip()

ECONOMY_COST = Decimal('79.99')  # цена за эконом-класс
BUSINESS_COST = Decimal('139.99')  # цена за бизнес-класс
SEAT_CHANGE_COST = Decimal('9.99')  # цена за смену места

ECONOMY_SEATS = range(11, 101)  # диапазон мест эконом-класса
BUSINESS_SEATS = range(1, 11)  # диапазон мест бизнес-класса

tickets = [
    ('Julia', 'e', ECONOMY_COST, 12),
    ('Igor', 'b', BUSINESS_COST, 2),
]

# Типичный вариант консольной программы:
# бесконечный цикл: выбор команды и выполнение -
# пока пользователь не напишет спец. команду выхода "Q"
while True:
    print()  # пустые строки (вертикальный отступ)
    print()
    print(MAIN_MENU)  # выводим список команд
    print()
    commandlet = input('Введите команду из списка [1-5/Q]: ')
    commandlet = commandlet.lower()  # команды и большими, и маленькими буквами
    print()

    if commandlet == 'q':  # Q - это выход
        break  # завершаем бесконечный цикл

    if commandlet == '1':
        # 1) продажа билета: пользователь поочерёдно указывает имя,
        # класс билета и желаемое место (если доступно)
        info = textwrap.dedent("""
            Введите поочерёдно:
            1) имя пассажира (строка);
            2) класс билета (буква "E" - эконом, буква "B" - бизнес);
            3) число: для бизнеса: 1-10, для эконом: 11-100.
        """).strip()
        print(info)
        print()

        name = input('Введите имя пассажира: ')
        if not name:
            print()
            print('Имя не может быть пустым.')
            continue

        ticket_type = input('Введите класс билета [E/B]: ')
        ticket_type = ticket_type.lower()
        if ticket_type not in ['e', 'b']:
            print()
            print(f'Введён неверны класс билета: "{ticket_type}".')
            continue

        possible_seats = \
            ECONOMY_SEATS if ticket_type == 'e' else BUSINESS_SEATS
        seat = input(
            f'Введите место '
            f'[{possible_seats.start}-{possible_seats.stop-1}]: '
        )
        if not seat.isdigit() or int(seat) not in possible_seats:
            print()
            print(f'Введён неверный номер места: "{seat}"')
            continue

        is_seat_reserved = False
        for ticket in tickets:
            if ticket[3] == int(seat):
                is_seat_reserved = True
                break

        if is_seat_reserved:
            print()
            print(f'Место "{seat}" занято.')
            continue

        if ticket_type == 'e':
            ticket_cost = ECONOMY_COST
        else:
            ticket_cost = BUSINESS_COST

        ticket = (name, ticket_type, ticket_cost, int(seat))
        tickets += [ticket]
        print('Билет добавлен!')

    elif commandlet == '2':
        # 2) возврат билета по номеру места: пользователь вводит номер места,
        # билет для данного места удаляется из списка билетов.
        # Тут необходим цикл по tickets, чтобы найти индекс удаляемого объекта:
        # для этого можно использовать range() либо enumerate().
        print(tickets)
        my_seat = input('Введите номер места, указанный в приобретенном билете: ')
        if not my_seat.isdigit():
            #  or int(my_seat) not in [ticket[3] for ticket in tickets]
            print(f'Некорректный номер: {my_seat}')

        else:
            for i in range(len(tickets)):
                if tickets[i][3] == int(my_seat):
                    del tickets[i]
                    print('Возврат билета прошёл успешно!')
                    break
            else:
                print('Билет с указанным местом не выкуплен')

        print(tickets)



    elif commandlet == '3':
        # 3) смена места в пределе класса (за доплату): пользователь вводит
        # номер старого места (если билет на такое места нет, вывести ошибку и
        # закончить функцию), после этого пользователь вводит номер нового
        # места в пределах класса его билета (бизнес/эконом).
        #
        # Сначала нужно НАЙТИ старый билет по номеру старого места.
        # Если старый билет НЕ НАЙДЕН, вывести ошибку и закончить функцию.
        # Далее
        # Если новое место УЖЕ ЗАНЯТО, вывести ошибку и закончить функцию.
        # Если новое место НЕ ЗАНЯТО, то
        # СОЗДАЁТСЯ НОВЫЙ БИЛЕТ, у которого
        # ИМЯ и КЛАСС берётся из СТАРОГО БИЛЕТА,
        # ЦЕНА - вносится значение `ЦЕНА СТАРОГО БИЛЕТА + ЦЕНА СМЕНЫ МЕСТА`,
        # МЕСТО - вносится номер НОВОГО МЕСТА.
        # Далее
        # НОВЫЙ билет вносится в список билетов,
        # СТАРЫЙ билет удаляется из списка билетов
        prev_seat = input("Ведите номер вашего места: ")
        seats_list = [ticket[3] for ticket in tickets]    #список занятых мест
        print(seats_list)
        if  not prev_seat.isdigit() or (int(prev_seat) not in seats_list):   # проверка корректности введенного номера
            print(f'Некорректный номер: {prev_seat}')
            break
        else:
            for i in range(len(tickets)):
                if (int(prev_seat)) == tickets[i][3]:
                    my_ticket = i         # номер индекса старого билета в списке tickets
                    print(my_ticket)
                    my_ticket_class = i[1]  # допустимый класс
                    if my_ticket_class == 'e':
                        numbers_for_choose = ECONOMY_SEATS
                    else:
                        numbers_for_choose = BUSINESS_SEATS



            new_seat = input('Введите желаемый номер места: ')
            if not new_seat.isdigit() or int(new_seat) in seats_list or int(new_seat) not in numbers_for_choose:
                print(f'Место занято либо введён некорректный номер: {new_seat}')
                continue
            else:
                ticket = (my_ticket[0], my_ticket[1], my_ticket[2]+SEAT_CHANGE_COST, int(new_seat))
                del tickets[my_ticket]
                tickets += [ticket]
                print('Билет добавлен!')




    elif commandlet == '4':
        # 4) вывод списка билетов (порядок по номеру места).
        print('Список купленных билетов:')

        # `sort_key` - ключ сортировки по 3-му элементу билета
        # (3-й элемент билета - это ПОСАДОЧНОЕ МЕСТО).
        #
        # `itemgetter(3)` - функция, которая создаёт ФУНКЦИЮ (функциональное
        # программирование), которая будет возвращать элемент под индексом 3
        # (можно использовать любую цифру),
        # например (пример можно запустить):
        #
        # >>> from operator import itemgetter  # импорт функции itemgetter
        # >>> list_1 = ['a', 'b', 'C', 'd', 'e']
        # >>> index = 2
        # >>> sort_key = itemgetter(index)
        # >>> print('Элемент:', sort_key(list_1))  # эквивалентно list_1[index]
        # Элемент: C
        #
        # Мы же далее эту функцию будем использовать как КЛЮЧ для сортировки
        # (можно не только для сортировки).
        sort_key = itemgetter(3)

        for ticket in sorted(tickets, key=sort_key):
            name = ticket[0]
            ticket_type = ticket[1]
            ticket_cost = ticket[2]
            seat = ticket[3]
            print(f'{seat}{ticket_type}: {name} (${ticket_cost})')

        input('Нажмите Enter, чтобы продолжить...')

    elif commandlet == '5':
        # 5) вывод итоговой суммы с продажи билетов.
        # В переменную total_cost нужно записать итоговую сумму по всем
        # проданным билетам и вывести её в консоль.
        # Использовать можно цикл FOR (простой вариант, был на КР)
        # или функцию sum в связке с key=itemgetter(???)
        # (чуть посложнее, пример есть в команде 4)
        total_cost = ...
        print(f'Общая стоимость проданных билетов: ${total_cost}.')
        input('Нажмите Enter, чтобы продолжить...')

from datetime import date
import os
import subprocess
import sys

from art import tprint
from prettytable import PrettyTable
from simple_term_menu import TerminalMenu

from database.db import Category, create_db
from database.repository import BalanceRepository, TransactionRepository


FIELDS = ["Идентификатор", "Дата", "Сумма", "Описание"]


def change_transaction(trans_id: int) -> None:
    """Функция рендеринга страницы изменения данных транзакции (выбранной по id)"""
    print("Выбери поля, которые хочешь поменять (нажми Enter, чтобы не изменять поле):")
    try:
        ymd = list(map(lambda x: int(x), input("Дата (формат: гггг-мм-дд; Enter = сегодняшнее число): ").split()))
        created_at = date(year=ymd[0], month=ymd[1], day=ymd[2])
    except:
        created_at = None
    summa = input("Сумма: ")
    try:
        summa = float(summa)
    except:
        summa = None
    description = input("Описание: ") or None
    
    change_dict = {"created_at": created_at, "sum": summa, "description": description}
    valid_dict = {k: v for k, v in change_dict.items() if v is not None}
    TransactionRepository.change_data(trans_id, **valid_dict)
    main()



def page_selected_transaction_by_id(trans_id: int) -> None:
    """Функция рендеринга страницы с выбранной транзакцией (действия - изменить/удалить)"""
    subprocess.call("clear", shell=True)
    tprint("Personal Wallet\n")

    trans_one = TransactionRepository.find_one(trans_id)
    sel_table = PrettyTable(FIELDS)
    sel_table.align = "c"
    sel_table.add_row(trans_one)
    print(sel_table)
    print("\n")

    menu = ["1. Изменить", "2. Удалить"]
    ch = TerminalMenu(menu).show()
    if menu[ch] == "1. Изменить":
        change_transaction(trans_id)
    elif menu[ch] == "2. Удалить":
        TransactionRepository.pop(id=trans_one[0])
        main()


def page_padding_transactions(category: str, limit: int = 20, offset: int = 0) -> None:
    """Функция рендеринга страницы со всеми транзакциями выбранной категории"""
    subprocess.call("clear", shell=True)
    tprint("Personal Wallet\n")

    transs = TransactionRepository.find_all(limit=limit, offset=offset, category=category)
    sel_table = PrettyTable(FIELDS)
    sel_table.align = "c"
    sel_table.add_rows(transs)
    print(sel_table)
    print("\n")

    if len(transs) == 0 and offset == 0:
        TerminalMenu(["0. Назад"]).show()
        page_selected_transactions(category)
    elif len(transs) < 20 and offset == 0:
        menu = ["1. Выбрать ID", "2. Вернуться в главное меню"]
    elif len(transs) < 20 and offset != 0:
        menu = ["1. Выбрать ID", "2. Назад", "3. Вернуться в главное меню"]
    elif len(transs) == 20 and offset == 0:
        menu = ["1. Выбрать ID", "2. Вперед", "3. Вернуться в главное меню"]
    elif len(transs) == 20 and offset != 0:
        menu = ["1. Выбрать ID", "2. Вперед", "3. Назад", "4. Вернуться в главное меню"]

    ch = TerminalMenu(menu).show()
    if menu[ch][3:] == "Выбрать ID":
        trans_id = int(input("Введите ID: "))
    elif menu[ch][3:] == "Вперед":
        page_padding_transactions(category=category, offset=offset+20)
    elif menu[ch][3:] == "Назад":
        page_padding_transactions(category=category, offset=offset-20)
    elif menu[ch][3:] == "Вернуться в главное меню":
        main()

    page_selected_transaction_by_id(trans_id)



def page_add_transaction(category: str) -> None:
    """Функция рендеринга страницы добавления новой транзакции (выбранной категории)"""
    subprocess.call("clear", shell=True)
    tprint("Personal Wallet\n")
    print("Добавление транзакции\n\n")

    print(f"Категория: {'Доходы' if category == Category.income.value else 'Расходы'}")
    try:
        ymd = list(map(lambda x: int(x), input("Дата (формат: гггг-мм-дд; Enter = сегодняшнее число): ").split()))
        created_at = date(year=ymd[0], month=ymd[1], day=ymd[2])
    except:
        created_at = date.today()
    summa = float(input("Сумма: "))
    description = input("Описание: ") or None
    TransactionRepository.add_one(created_at=created_at, category=category, sum=summa, description=description)
    print("\nТранзакция успешно добавлена\n")

    menu = ["1. Назад", "2. Вернуться в главное меню"]
    ch = TerminalMenu(menu).show()
    if menu[ch] == "1. Назад":
        page_selected_transactions(category)
    elif menu[ch] == "2. Вернуться в главное меню":
        main()

    

def page_selected_transactions(category: str):
    """Функция рендеринга страницы выбранной категории транзакций"""
    subprocess.call("clear", shell=True)
    tprint("Personal Wallet\n")
    print("Доходы" if category == Category.income.value else "Расходы")

    selected_trans = TransactionRepository.find_all(limit=20, category=category)
    sel_table = PrettyTable(FIELDS)
    sel_table.align = "c"
    sel_table.add_rows(selected_trans)
    print(sel_table)
    print("\n")

    options = ["1. Добавить", "2. Выбрать", "3. Вернуться в главное меню"]
    ch = TerminalMenu(options, title="Действия с транзакциями").show()
    if options[ch] == "1. Добавить":
        page_add_transaction(category)
    elif options[ch] == "2. Выбрать":
        page_padding_transactions(category)
    elif options[ch] == "3. Вернуться в главное меню":
        main()


def page_select_category() -> None:
    """Функция рендеринга страницы выбора категории транзакций"""
    category_menu = ["1. Доходы", "2. Расходы", "3. Назад"]
    ch = TerminalMenu(category_menu, title="Выбор категории").show()
    if category_menu[ch] == "1. Доходы":
        category = Category.income.value
    elif category_menu[ch] == "2. Расходы":
        category = Category.expense.value
    elif category_menu[ch] == "3. Назад":
        main()

    page_selected_transactions(category)


def main():
    """Функция рендеринга главной страницы приложения"""
    try:
        subprocess.call("clear", shell=True)
        tprint("Personal Wallet\n")
        print(f"Текущий баланс: {BalanceRepository.get()}\n\n")
        
        print("Последние транзакции: \n")
        inc_trans = TransactionRepository.find_all(category=Category.income.value)
        inc_table = PrettyTable(FIELDS)
        inc_table.title = "Доходы"
        inc_table.align = "c"
        inc_table.add_rows(inc_trans)
        print(inc_table)
        print()
        exp_trans = TransactionRepository.find_all(category=Category.expense.value)
        exp_table = PrettyTable(FIELDS)
        exp_table.title = "Расходы"
        exp_table.align = "c"
        exp_table.add_rows(exp_trans)
        print(exp_table)
        print("\n")

        main_menu = ["1. Посмотреть все транзакции", "2. Выход"]
        ch = TerminalMenu(main_menu, title="Главное меню").show()
        if main_menu[ch] == "1. Посмотреть все транзакции":
            page_select_category()
        elif main_menu[ch] == "2. Выход":
            raise KeyboardInterrupt
    except KeyboardInterrupt:
        subprocess.call("clear", shell=True)
        print("Good buy")
        sys.exit(1)


if __name__ == "__main__":
    if not os.path.exists("./wallet.db"):
        create_db()
        BalanceRepository.insert()
    main()
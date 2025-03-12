import pytest
from main_loto import Card, Game

def test_card_generation():
    card = Card("Тестовый игрок")
    assert len(card.card) == 3  # 3 строки
    assert all(len(row) == 9 for row in card.card)  # 9 колонок

def test_card_numbers_count():
    card = Card("Тест")
    numbers_count = sum(1 for row in card.card for cell in row if cell is not None)
    assert numbers_count == 15  # В каждой карточке ровно 15 чисел

def test_mark_number():
    card = Card("Тест")
    number = card.card[0][0]
    card.mark_number(number)
    assert card.marked[0][0] == True

def test_has_number():
    card = Card("Тест")
    number = card.card[0][0]
    assert card.has_number(number) == True
    assert card.has_number(999) == False  # Такого номера нет

def test_card_completion():
    card = Card("Тест")
    for row_idx, row in enumerate(card.card):
        for col_idx, cell in enumerate(row):
            if cell is not None:
                card.marked[row_idx][col_idx] = True
    assert card.is_complete() == True

def test_game_creation():
    game = Game(3)  # Компьютер - Компьютер
    assert game.player1 is not None
    assert game.player2 is not None
    assert len(game.barrels) == 90

def test_card_str():
    card1 = Card("Тест")
    card2 = Card("Тест")
    assert str(card1) == str(card2)  # Проверка строкового представления

def test_card_equality():
    card1 = Card("Тест")
    card2 = Card("Тест")
    assert card1 == card2  # Проверка равенства

def test_game_str():
    game = Game(3)
    assert str(game) == "Игра между комп 1 и комп 2"

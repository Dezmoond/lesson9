import random

class Card:
    def __init__(self, owner):
        self.owner = owner
        self.card = self.generate_lotto_card()
        self.marked = [[False for _ in range(9)] for _ in range(3)]

    def generate_lotto_card(self):
        columns = {i: list(range(i * 10 + 1, i * 10 + 11)) for i in range(9)}
        card = [[None for _ in range(9)] for _ in range(3)]

        for row in card:
            cols_with_numbers = random.sample(range(9), 5)
            for col in cols_with_numbers:
                number = random.choice(columns[col])
                row[col] = number
                columns[col].remove(number)

        for row in card:
            numbers = [num for num in row if num is not None]
            numbers.sort()
            num_index = 0
            for col in range(9):
                if row[col] is not None:
                    row[col] = numbers[num_index]
                    num_index += 1

        return card

    def __str__(self):
        return "\n".join(
            " | ".join(
                f"{num:2}{'X' if self.marked[row_idx][col_idx] else ' '}"
                if num is not None else "   "
                for col_idx, num in enumerate(row)
            ) for row_idx, row in enumerate(self.card)
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __contains__(self, number):
        return self.has_number(number)

    def has_number(self, number):
        return any(number in row for row in self.card)

    def print_card(self):
        print(str(self))

    def mark_number(self, number):
        for row_idx, row in enumerate(self.card):
            for col_idx, cell in enumerate(row):
                if cell == number:
                    self.marked[row_idx][col_idx] = True

    def is_complete(self):
        return all(
            self.marked[row_idx][col_idx]
            for row_idx, row in enumerate(self.card)
            for col_idx, cell in enumerate(row)
            if cell is not None
        )


class Game:
    def __init__(self, typegame):
        self.typegame = typegame
        self.player1 = None
        self.player2 = None

        if typegame == 1:
            self.player1 = Card("Человек 1")
            self.player2 = Card("Человек 2")
        elif typegame == 2:
            self.player1 = Card("Человек")
            self.player2 = Card("Компьютер")
        elif typegame == 3:
            self.player1 = Card("Компьютер 1")
            self.player2 = Card("Компьютер 2")
        else:
            raise ValueError("Неизвестный тип игры")

        self.barrels = list(range(1, 91))
        random.shuffle(self.barrels)

        self.start()

    def __str__(self):
        return f"Игра между {self.player1.owner} и {self.player2.owner}"

    def __eq__(self, other):
        return self.player1 == other.player1 and self.player2 == other.player2

    def __ne__(self, other):
        return not self.__eq__(other)

    def start(self):
        print(self)
        print("=" * 30)
        self.show_cards()

        while self.barrels:
            barrel = self.barrels.pop(0)
            print(f"\nБочонок номер: {barrel}")
            print("=" * 30)

            # Проверка игроков поочередно
            if self.check_player(self.player1, barrel):
                print(f"{self.player1.owner} ПОБЕДИЛ!")
                break

            if self.check_player(self.player2, barrel):
                print(f"{self.player2.owner} ПОБЕДИЛ!")
                break

        print("\nИгра окончена.")

    def check_player(self, player, barrel):
        print(f"\nКарточка игрока: {player.owner}")
        player.print_card()

        if "Компьютер" in player.owner:
            if player.has_number(barrel):
                player.mark_number(barrel)
                print(f"{player.owner} зачеркнул число {barrel}.")
        else:
            answer = input("Зачеркнуть значение? (y/n): ").strip().lower()
            if answer == 'y':
                if player.has_number(barrel):
                    player.mark_number(barrel)
                    print(f"{player.owner} зачеркнул число {barrel}.")
                else:
                    print(f"Ошибка! Числа {barrel} нет на карточке {player.owner}.")
                    print(f"{player.owner} ПРОИГРАЛ!")
                    print(f"{self.get_opponent(player).owner} ПОБЕДИЛ!")
                    return True  # Игра завершается, если произошла ошибка
            elif answer == 'n':
                if player.has_number(barrel):
                    print(f"Ошибка! Число {barrel} было на карточке {player.owner}, но не зачеркнуто.")
                    print(f"{player.owner} ПРОИГРАЛ!")
                    print(f"{self.get_opponent(player).owner} ПОБЕДИЛ!")
                    return True  # Игра завершается, если произошла ошибка

        return player.is_complete()

    def show_cards(self):
        print("=" * 30)
        print(f"Карточка игрока: {self.player1.owner}")
        self.player1.print_card()
        print("\n" + "-" * 30 + "\n")
        print(f"Карточка игрока: {self.player2.owner}")
        self.player2.print_card()

    def get_opponent(self, player):
        """ Возвращает противника игрока """
        return self.player1 if player != self.player1 else self.player2

def main():
    while True:
        print("\n" + "=" * 50)
        print("Меню:")
        print("1. Человек - Человек")
        print("2. Человек - Компьютер")
        print("3. Компьютер - Компьютер")
        print("4. Выход")
        print("=" * 50)

        choice = input("Выберите пункт меню: ")

        try:
            if choice == "1":
                Game(1)
            elif choice == "2":
                Game(2)
            elif choice == "3":
                Game(3)
            elif choice == "4":
                print("Выход из программы...")
                break
            else:
                print("Неверный пункт меню")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()

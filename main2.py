from pprint import pprint
import random
import math

# Определение констант
TIMESTAMPS_COUNT = 50000  # Количество временных меток в матче
PROBABILITY_SCORE_CHANGED = 0.0001  # Вероятность изменения счета
PROBABILITY_HOME_SCORE = 0.45  # Вероятность забить гол домашней команде
OFFSET_MAX_STEP = 3  # Максимальный шаг смещения по времени

# Исходная временная метка
INITIAL_STAMP = {
    "offset": 0,
    "score": {
        "home": 0,
        "away": 0
    }
}


# Функция для генерации следующей временной метки
def generate_stamp(previous_value):
    # Определение, изменился ли счет
    score_changed = random.random() > 1 - PROBABILITY_SCORE_CHANGED

    # Определение, забила ли домашняя команда
    home_score_change = 1 if score_changed and random.random() > 1 - \
                             PROBABILITY_HOME_SCORE else 0

    # Определение, забила ли гостевая команда
    away_score_change = 1 if score_changed and not home_score_change else 0

    # Изменение смещения по времени
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    # Возвращение новой временной метки
    return {
        "offset": previous_value["offset"] + offset_change,
        "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change
        }
    }


# Функция для генерации хода матча
def generate_game():
    stamps = [INITIAL_STAMP, ]  # Список временных меток
    current_stamp = INITIAL_STAMP  # Текущая временная метка

    # Генерация временных меток
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps


# Генерация временных меток для игры
game_stamps = generate_game()
pprint(game_stamps)


# Этот вариант решения организован с помощью бинарного поиска
def binary_search(game_stamps, offset):
    # Инициализация границ поиска
    left, right = 0, len(game_stamps) - 1

    while left <= right:
        # Находим середину массива
        middle = (left + right) // 2
        # Получаем значение смещения (offset) для текущей середины массива
        current_offset = game_stamps[middle]["offset"]

        # Если текущее смещение равно искомому, возвращаем индекс
        if current_offset == offset:
            return middle
        # Если текущее смещение меньше искомого, смещаем левую границу поиска
        elif current_offset < offset:
            left = middle + 1
        # Иначе, смещаем правую границу поиска
        else:
            right = middle - 1

    # Возвращаем индекс элемента с наибольшим смещением, которое меньше или равно искомому смещению
    return right


def get_score(game_stamps, offset):
    # Инициализация переменных для счета домашней и гостевой команд
    home, away = 0, 0

    # Проверка значения offset
    if offset < 0:
        raise ValueError("Offset не может быть отрицательным числом")
        #print("Значение offset должно быть положительным.")
        #return home, away


    # Используем бинарный поиск для нахождения индекса ближайшей временной метки
    index = binary_search(game_stamps, offset)

    # Если индекс в пределах массива и временная метка не превышает заданный интервал
    if 0 <= index < len(game_stamps) and game_stamps[index]["offset"] <= offset:
        # Проверяем наличие информации об очках в текущей временной метке
        if "score" in game_stamps[index]:
            home, away = game_stamps[index]["score"]["home"], game_stamps[index]["score"]["away"]
        else:
            # Если информация об очках отсутствует, ищем последний элемент с информацией об очках перед найденным индексом
            for i in range(index, -1, -1):
                if "score" in game_stamps[i]:
                    home, away = game_stamps[i]["score"]["home"], game_stamps[i]["score"]["away"]
                    break

    # Возвращаем счет домашней и гостевой команд на заданной временной метке
    return home, away


offset = 45500
# Вызов функции get_score с заданными параметрами
home_score, away_score = get_score(game_stamps, offset)
print(f"На смещении времени {offset}, счет: домашняя команда - {home_score}, гостевая команда - {away_score}")

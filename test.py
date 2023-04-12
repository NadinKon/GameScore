import unittest
from main2 import get_score


class TestGetScore(unittest.TestCase):

    # Проверяет работу функции с пустым списком
    def test_empty_game_stamps(self):
        game_stamps = []
        offset = 20
        expected = (0, 0)
        result = get_score(game_stamps, offset)
        self.assertEqual(result, expected)

    # Проверяет работу функции с одной временной меткой, попадающей в заданный интервал
    def test_single_game_stamp_within_offset(self):
        game_stamps = [{"offset": 10, "score": {"home": 1, "away": 0}}]
        offset = 20
        expected = (1, 0)
        result = get_score(game_stamps, offset)
        self.assertEqual(result, expected)

    # Проверяет работу функции с одной временной меткой, не попадающей в заданный интервал
    def test_single_game_stamp_outside_offset(self):
        game_stamps = [{"offset": 30, "score": {"home": 1, "away": 0}}]
        offset = 20
        expected = (0, 0)
        result = get_score(game_stamps, offset)
        self.assertEqual(result, expected)

    # Проверяет работу функции с несколькими метками, последняя из которых находится внутри заданного интервала
    def test_multiple_game_stamps_within_offset(self):
        game_stamps = [
            {"offset": 10, "score": {"home": 1, "away": 0}},
            {"offset": 20, "score": {"home": 1, "away": 1}},
            {"offset": 30, "score": {"home": 2, "away": 1}},
        ]
        offset = 25
        expected = (1, 1)
        result = get_score(game_stamps, offset)
        self.assertEqual(result, expected)

    # Проверяет работу функции с несколькими временными метками, некоторые из которых не содержат информацию об очках
    def test_multiple_game_stamps_with_missing_scores(self):
        game_stamps = [
            {"offset": 5},
            {"offset": 10, "score": {"home": 1, "away": 0}},
            {"offset": 20},
            {"offset": 25, "score": {"home": 2, "away": 1}},
        ]
        offset = 15
        expected = (1, 0)
        result = get_score(game_stamps, offset)
        self.assertEqual(result, expected)

    # Проверяет работу функции с отрицательным значением смещения
    def test_game_stamps_with_negative_offset(self):
        game_stamps = [
            {"offset": 10, "score": {"home": 1, "away": 0}},
            {"offset": 20, "score": {"home": 2, "away": 1}},
        ]
        offset = -5
        with self.assertRaises(ValueError) as cm:
            get_score(game_stamps, offset)
        self.assertEqual(str(cm.exception), "Offset не может быть отрицательным числом")

    # Проверяет работу функции, когда информация об очках отсутствует
    def test_game_stamps_without_scores(self):
        game_stamps = [
            {"offset": 5},
            {"offset": 10},
            {"offset": 15},
            {"offset": 20},
        ]
        offset = 12
        expected = (0, 0)
        result = get_score(game_stamps, offset)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

import logging
import argparse


def setup_logging(debug):
    """
    Настройка логгирования в зависимости от режима отладки
    :param debug: bool - если True, то уровень логов DEBUG,
                         если False, то INFO
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level,
                        format='%(asctime)s [%(levelname)s] %(message)s')


def str_to_bool(value):
    """
    Преобрзует значение из строкового типа к булевому

    Принимает строку и возвращает True или False в зависимости от значения.
    """
    values_true = ('1', 'true', 'True', 'y', 'Y', 'yes')
    values_false = ('0', 'false', 'False', 'n', 'N', 'no')
    func_value = str(value).strip()
    if func_value in values_true:
        return True
    elif func_value in values_false:
        return False
    else:
        raise argparse.ArgumentTypeError(f"Некорректное значение {value}")


def parse_args():
    """
    Парсит аргументы командной строки для настройки
    начальных параментров приложения

    Поддерживаемые аргументы:
        -r / --rub: начальный баланс в рублях (float)
        -u / --usd: начальный баланс в долларах (float)
        -e / --eur: начальный баланс в евро (float)
        -p / --period: период обновления в минутах (int)
        -d / --debug: включение режима отладки (bool)
    """

    parser = argparse.ArgumentParser(prog='Валюты')

    parser.add_argument('-r', '--rub', default=0.0, type=float,
                        help='Начальный баланс в рублях')
    parser.add_argument('-u', '--usd', default=0.0, type=float,
                        help='Начальный баланс в долларах')
    parser.add_argument('-e', '--eur', default=0.0, type=float,
                        help='Начальный баланс в евро')
    parser.add_argument('-p', '--period', default=1, type=int,
                        help='Обновления курса в минутах')
    parser.add_argument('-d', '--debug', default=False, type=str_to_bool,
                        help='Режим отладки')

    return parser.parse_args()

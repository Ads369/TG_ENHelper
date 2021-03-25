# -*- coding: utf-8 -*-

import TG_Helper_DB
from pydantic import BaseModel
import json


def number_to_letter(in_int=1, lang='RU'):
    """
    Function convert Number to Letter for RU and EN dictionary
    :param in_int: Number (only one) of latter in alphabet
    :param lang: What language alphabet use 'RU' or 'EN'
    :return: letter or '_'
    """

    if lang == 'RU':
        letter_tuple = TG_Helper_DB.RUSSIAN_ALPHABET
    elif lang == 'EN':
        letter_tuple = TG_Helper_DB.ENGLISH_ALPHABET
    else:
        raise ValueError('Не верный парамтр языка')

    if len(letter_tuple) > in_int > 0:
        return letter_tuple[in_int - 1]
    else:
        return '_'


def list_of_number_to_letters(in_array_numb=()):
    """
    Prepare list for convert Number to Letter
    :param in_array_numb: list of number
    :return: dict RU and EN words
    """
    rus_letters = ""
    eng_letters = ""

    for num in in_array_numb:
        rus_letters += number_to_letter(num, 'RU')
        eng_letters += number_to_letter(num, 'EN')

    result = {'RU': rus_letters,
              'EN': eng_letters}

    return result


def handler_for_ntl(in_string=''):
    """
    Handler string and prepare list for 'Convert Number to Letter':
    - split
    - if digit convert to int
    - add to tuple

    :param in_string: just sting
    :return: dict RU and EN words
    """
    numbers = [int(i) for i in in_string.split() if i.isdigit()]
    result = list_of_number_to_letters(numbers)
    return result


def letter_to_number(in_char='', lang='RU'):

    if lang == 'RU':
        letter_tuple = TG_Helper_DB.RUSSIAN_ALPHABET
    elif lang == 'EN':
        letter_tuple = TG_Helper_DB.ENGLISH_ALPHABET
    else:
        raise ValueError('Не верный парамтр языка')

    try:
        result = str(letter_tuple.index(in_char.upper()))
    except ValueError:
        result = '_'

    return result


def sorting_letters(in_str=''):
    """
    Function sorting characters of string by type: RU, EN, digit or other
    :param in_str:
    :return: dict
    """
    en_letters = []
    ru_letters = []
    digit = []
    characters = []

    for char in in_str:
        char = char.upper()
        if char.isdigit():
            digit.append(char)
        elif char in TG_Helper_DB.RUSSIAN_ALPHABET:
            ru_letters.append(char)
        elif char in TG_Helper_DB.ENGLISH_ALPHABET:
            en_letters.append(char)
        else:
            characters.append(char)

    result = {
        'en': en_letters,
        'ru': ru_letters,
        'digit': digit,
        'char': characters
    }

    return result


def hendler_alphabet_convert(in_str=''):
    """
    Main function for convert NUMBER to LETTER and back

    -Sort Letter by language and digital
    -Spend this to convert

    :param in_str: just string the best format "abc" or "12 3 4"
    :return: dictionary
    """
    sorted_letters = sorting_letters(in_str)
    en_string = ''
    ru_string = ''
    digit_string = ''

    if sorted_letters['en']:
        for char in sorted_letters['en']:
            en_string += letter_to_number(char, 'EN') + ' '
    elif sorted_letters['ru']:
        for char in sorted_letters['ru']:
            ru_string += letter_to_number(char, 'RU') + ' '
    elif sorted_letters['digit']:
        digit_string = handler_for_ntl(in_str)

    result = {
        'en_num': en_string,
        'ru_num': ru_string,
        'digit_string': digit_string
    }
    return result


def periodic_table_convert(in_string):
    in_elements_list = [i for i in in_string.split()]

    element_list = []

    for element in in_elements_list:
        if element.isdigit():
            element_list.append({"number": int(element), "symbol": "_"})
        elif element.isalpha():
            element_list.append({"number": 0, "symbol": element})
        else:
            pass

    elements = json.loads(TG_Helper_DB.PERIOD_TABLE)

    for element in elements['elements']:
        for item in element_list:
            if element['symbol'].lower() == item['symbol'].lower():
                item['number'] = element['number']
                item['symbol'] = element['symbol']
            elif element['number'] == item['number']:
                item['symbol'] = element['symbol']
            else:
                pass

    return element_list


def braille_convert(in_str=''):
    characters = json.loads(TG_Helper_DB.BRAILLE_CODE)['characters']

    for char in characters:
        if char['bit'] == in_str:
            return char

    return None


if __name__ == '__main__':
    print(braille_convert('qwe'))


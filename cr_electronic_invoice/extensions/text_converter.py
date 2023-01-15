
import logging

_logger = logging.getLogger(__name__)

UNITS = (
    '',
    'UN ',
    'DOS ',
    'TRES ',
    'CUATRO ',
    'CINCO ',
    'SEIS ',
    'SIETE ',
    'OCHO ',
    'NUEVE ',
    'DIEZ ',
    'ONCE ',
    'DOCE ',
    'TRECE ',
    'CATORCE ',
    'QUINCE ',
    'DIECISEIS ',
    'DIECISIETE ',
    'DIECIOCHO ',
    'DIECINUEVE ',
    'VEINTE '
)

TENS = (
    'VENTI',
    'TREINTA ',
    'CUARENTA ',
    'CINCUENTA ',
    'SESENTA ',
    'SETENTA ',
    'OCHENTA ',
    'NOVENTA ',
    'CIEN ',
)

HUNDREDS = (
    'CIENTO ',
    'DOSCIENTOS ',
    'TRESCIENTOS ',
    'CUATROCIENTOS ',
    'QUINIENTOS ',
    'SEISCIENTOS ',
    'SETECIENTOS ',
    'OCHOCIENTOS ',
    'NOVECIENTOS ',
)


def number_to_text_es(number_in, join_dec=' Y ', separator=',', decimal_point='.'):
    converted = ''

    # Check type and convert to str
    if isinstance(number_in, str):
        number = number_in
    else:
        number = str(number_in)

    # Remove the separator from the string
    try:
        number = number.replace(separator, '')
    except ValueError:
        _logger.info("An error occurred while replacing the separator an error may occur.")

    # Get the integer and decimal part of the numbers
    try:
        number_int, number_dec = number.split(decimal_point)
    except ValueError:
        number_int = number
        number_dec = ""
        _logger.info("No decimal part found on the number.")

    number = number_int.zfill(9)
    millions = number[:3]
    thousands = number[3:6]
    hundreds = number[6:]

    if millions:
        if millions == '001':
            converted += 'UN MILLON '
        elif int(millions) > 0:
            converted += f'{_convert_number(millions)}MILLONES '

    if thousands:
        if thousands == '001':
            converted += 'MIL '
        elif int(thousands) > 0:
            converted += f'{_convert_number(thousands)}MIL'

    if hundreds:
        if hundreds == '001':
            converted += 'UN '
        elif int(hundreds) > 0:
            converted += f'{_convert_number(hundreds)} '

    if number_dec == "":
        number_dec = "00"
    if len(number_dec) < 2:
        number_dec += '0'

    has_decimal = (join_dec + number_dec + '/100' if float(number_dec) != 0 else ' EXACTOS')
    converted += has_decimal

    return converted


def _convert_number(number):
    output = ''

    if number == '100':
        output = "CIEN "
    elif number[0] != '0':
        output = HUNDREDS[int(number[0])-1]

    k = int(number[1:])
    if k <= 20:
        output += UNITS[k]
    else:
        if (k > 30) & (number[2] != '0'):
            output += f'{TENS[int(number[1])-2]}Y {UNITS[int(number[2])]}'
        else:
            output += f'{TENS[int(number[1])-2]}{UNITS[int(number[2])]}'

    return output

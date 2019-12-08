"""
Configuration file for invoice_mole.py
Contains regex patterns and mapping between <keyword>:<regex pattern>
New pattens and mappings can be added here
"""

# If a sequence of numbers ends with 'kr' we assume it's a price.
# The price can have
# > single comma/dot to separate decimals, e.g:
#     123,00 kr
# > space in between the digits, to indicate hundreds, thousands, millions
#     1 234 456.35 kr
# The regex works with the assumption that a valid price can only have ONE
# space separating the digits. Left part of the potential price is ignored if
# it's separated by two spaces or more. E.g.:
#     234  456.35 kr will be matched as 456.35 kr
_PRICE = '((?:\d+\s)+\d+[,.]\d+)\s?kr'
# match date with separators " /-:"
_DATE = '\d{2,4}[\s|:|-|\/]\d{1,2}[\s|:|-|\/]\d{1,2}'
# match two _DATE patterns separated by '-' and optional single whitespaces on
# the both sides
_PERIOD = f'({_DATE}\s{{0,1}}-\s{{0,1}}{_DATE})'

SIX_DIGIT = '(\d{6})'
EIGHT_DIGIT = '(\d{8})'

# Make match non-greedy by adding .*? after the keywords
MAP = {
    'Fakturaperiod': f'Fakturaperiod.*?{_PERIOD}',
    'Anl.nr': f'Anl\.nr.*?{EIGHT_DIGIT}',
    'Mätarnr': f'Mätarnr.*?{SIX_DIGIT}',
    'Summa exkl. moms': f'Summa exkl. moms.*?{_PRICE}',
    'Summa inkl. moms': f'Summa inkl. moms.*?{_PRICE}',
    'Energipris': f'Energipris.*?{_PRICE}',
    'Effektpris': f'Effektpris.*?{_PRICE}',
    'Flödespris': f'Flödespris.*?{_PRICE}',
}

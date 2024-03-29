"""
This module accepts an invoice in the form of a text file or a string, parses
it base on the mapping defined in config.py file, and returns parsed data.
Output data is returned in a text file
"""
import re
import argparse
import invoice_mole.config


def arguments():
    """
    Let's add possibility to pass a string or a text file to the script.
    Arguments are mutually exclusive, so it's possible to pass EITHER a
    textfile OR a string
    :return: argparse object
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', '--string',
                       help="Pass invoice as a string, if you REALLY need it")
    group.add_argument('-t', '--txt',
                       help="Pass invoice in a text file. My favorite choice!")

    return parser.parse_args()


def validate_price(hits):
    """
    This function validates that the sequence of numbers is a proper format
    to be considered a 'price'. Rules for proper price:
    - price can have only one digit before the decimal separator if it starts
      with 0
    - price can have only two digits after decimal separator
    :param: hit, list of potential prices
    :return:
    """
    hit = []
    for price in hits:
        if price[0] == '0':
            try:
                assert price[1] == ','
            except AssertionError:
                continue
        try:
            assert len(price.split(',')[-1]) == 2
            hit.append(price)
        except AssertionError:
            continue
    return hit


def find_key(key, text) -> list:
    """
    Iterate through the string find substrings as defined in regex patterns
    in config.MAP
    :param key: str, dictionary key
    :param text: str, invoice
    :return: If re.findall(), return a list of matches
    :rtype: list
    """
    if key in text:
        pattern = invoice_mole.config.MAP[key]
        hit = re.findall(pattern, text)
        if hit:
            if pattern.endswith('kr'):
                hit = validate_price(hit)
            return hit


def parse_invoice(invoice):
    """
    Iterate through MAP keys and build up a dictionary containing key:match
    pairs
    :param invoice: str
    :return: dictionary of key:match pairs
    :rtype: dict
    """
    d = {}
    for key in invoice_mole.config.MAP:
        match = find_key(key, invoice)
        # If there was a match, extract it, otherwise return empty list
        match = match[0] if match else ''
        d[key] = match
    return d


def txt_to_str(_path):
    """
    Helper function to open a .txt file and return it in one string. Script
    will exit if text file was not found
    :param _path: str, Path to a text file
    :return: Entire document in one string
    :rtype: str
    """
    try:
        with open(_path, 'r') as f:
            return f.read()
    except FileNotFoundError as e:
        print(e)
        exit(1)


def pretty_print(d):
    """
    This is not required in functional requirements, but
    let's add some formatting to our string. We can take a key that has the
    most characters in it and use it as an indentation point for all values
    :param d: key:value mapping
    :return: void
    """

    longest_key = len(max(d.keys(), key=len))
    for key, value in d.items():
        # We'll add 'len_diff' empty spaces to the strings
        len_diff = longest_key - len(key)
        print('{}'.format(key), end='')
        print("{}:".format(' ' * len_diff), end=' ')  # add missing spaces
        print('{}'.format(value))


def main():
    """
    Entry point of the script. Parse the arguments and let the magic happen
    :return: void
    """
    args = arguments()
    # depending on which arguments was provided _invoice can be
    # arts.string or args.txt
    invoice = args.string if args.string else txt_to_str(args.txt)
    clean_data = parse_invoice(invoice)
    pretty_print(clean_data)


if __name__ == '__main__':
    main()

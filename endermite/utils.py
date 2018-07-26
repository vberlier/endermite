import re


# String transformation


RE_STRING_PARTS = re.compile(r'[a-z]+|[A-Z][a-z]+|[A-Z]+|[0-9]+')


def underscore(string):
    """Turn a string into a valid snake-cased python identifier."""
    result = '_'.join(RE_STRING_PARTS.findall(string))
    if result[0].isdigit():
        result = '_' + result
    return result.lower()

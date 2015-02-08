# tools for converting integer ids to alphabetical chars

# use combinations of characters a..z, A...Z, 0...1


def str2int(cha):
    """Representation of a char as an integer"""
    if 'a' <= cha <= 'z':
        return ord(cha) - ord('a')
    elif 'A' <= cha <= 'Z':
        return ord(cha) - ord('A') + 26
    elif cha.isdigit():
        return ord(cha) - ord('0') + 52

def int2str(integer):
    """Representation of an integer as character"""
    if integer < 26:
        return chr(integer + ord('a'))
    elif integer < 52:
        return chr(integer - 26 + ord('A'))
    elif integer < 62:
        return chr(integer - 52 + ord('0'))
    else:
        raise ValueError("Invalid integer, can't convert")


def to_text(integer):
    """Convert integer to alphanumeric char string"""
    if integer == 0:
        return int2str(0)
    text = ""
    while integer > 0:
        r = integer % 62
        text += int2str(r)
        integer /= 62
    return text

def to_int(text):
    """Convert text id back to integer"""
    integer = 0
    for i, cha in enumerate(text):
        integer += str2int(cha) * 62**i
    return integer


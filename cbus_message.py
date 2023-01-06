def get_str(msg, start, length):
    return msg[start: start + length]


def pad(num, length):
    output = '0000000000' + hex(num)[2:].upper()
    return output[length * -1:]


def get_int(msg, start, length):
    return int(msg[start: start + length], 16)


def node_id(msg):
    return int(get_str(msg, 9, 4), 16)


def opcode(msg):
    return get_str(msg, 7, 2)


def checkbit(number, bit):
    check_number = 1<<bit
    return number & check_number == check_number


def flags(flags):
    output = {}
    output['consumer'] = checkbit(flags, 0)
    output['producer'] = checkbit(flags, 1)
    output['flim'] = checkbit(flags, 2)
    output['bootloading'] = checkbit(flags, 3)
    output['coe'] = checkbit(flags, 4)
    output['learn'] = checkbit(flags, 5)
    return output


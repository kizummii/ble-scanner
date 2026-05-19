import random


def generate_ble_flag(length=8):
    chars = []
    for _ in range(length):
        if random.random() < 0.5:
            chars.append(random.choice("0123456789"))
        else:
            chars.append(random.choice("ABCDEF"))
    return "".join(chars)

from nanoid import generate


def generate_nano_id(short=False):
    return generate('1234567890abcdefghi', size=12) if short else generate()

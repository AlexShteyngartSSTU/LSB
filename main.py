from typing import IO, Iterator, Union
from stegano import tools
from stegano.lsb.generators import identity

def hide(
    image: Union[str, IO[bytes]],
    message: str,
    generator: Union[None, Iterator[int]] = None,
    shift: int = 0,
    encoding: str = "UTF-8",
    auto_convert_rgb: bool = False,
):

    hider = tools.Hider(image, message, encoding, auto_convert_rgb)
    width = hider.encoded_image.width

    if not generator:
        generator = identity()

    while shift != 0:
        next(generator)
        shift -= 1

    while hider.encode_another_pixel():
        generated_number = next(generator)

        col = generated_number % width
        row = int(generated_number / width)

        hider.encode_pixel((col, row))

    return hider.encoded_image


def reveal(
    encoded_image: Union[str, IO[bytes]],
    generator: Union[None, Iterator[int]] = None,
    shift: int = 0,
    encoding: str = "UTF-8",
):

    revealer = tools.Revealer(encoded_image, encoding)
    width = revealer.encoded_image.width

    if not generator:
        generator = identity()

    while shift != 0:
        next(generator)
        shift -= 1

    while True:
        generated_number = next(generator)

        col = generated_number % width
        row = int(generated_number / width)

        if revealer.decode_pixel((col, row)):
            return revealer.secret_message


secret = hide("img/1.png", "secret password")
secret.save("img/1_stegano.png")

result = reveal("img/1_stegano.png")
print(result)
import concurrent.futures
from operator import attrgetter

from PIL import Image

from .config import IMG_DIM


class Collage:
    def __init__(self, user):
        self.user = user # LetterboxdUser instance
        self.image = None

    def __repr__(self):
        return f"Collage(username={self.user})"

    def create(self, size: tuple[int, int]=(5, 5)):
        """Creates the collage from user's diary. Returns a PIL Image"""
        cols, rows = size
        if cols * rows > 50:
            raise NotImplementedError("Collages of more than 50 films are not yet implemented")
        diary_entries = self.user.diary(page=1)[:cols*rows]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            images = list(executor.map(
                attrgetter("poster_image"),
                diary_entries
            ))

        collage_width = cols * IMG_DIM.width
        collage_height = rows * IMG_DIM.height
        collage = Image.new("RGB", (collage_width, collage_height))
        for row in range(rows):
            for col in range(cols):
                i = row * cols + col
                collage.paste(
                    images[i],
                    (col * IMG_DIM.width, row * IMG_DIM.height)
                )
        self.image = collage
        return collage

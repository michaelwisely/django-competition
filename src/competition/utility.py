from PIL import Image


def create_thumbnail(original_path, thumb_path, thumb_size):
    image = Image.open(original_path)

    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')

    image.thumbnail(thumb_size, Image.ANTIALIAS)

    # save the thumbnail
    image.save(thumb_path, 'png')

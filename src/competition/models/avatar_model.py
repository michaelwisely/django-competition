from django.db import models
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image
from cStringIO import StringIO

import os

THUMB_SIZE = (180, 300)


def image_location(instance=None, filename=None):
    """Determines location of regular sized images
    example path: MEDIA_ROOT/competition_images/12/my_image.png
    """
    return os.path.join(settings.MEDIA_ROOT, "competition_images", filename)


def thumbnail_location(instance=None, filename=None):
    """Determines location of thumbnail images
    example path: MEDIA_ROOT/competition_images/profile/12/t_my_image.png
    """
    directory = os.path.dirname(image_location(instance, filename))
    return os.path.join(directory, "t_" + filename)


class Avatar(models.Model):
    """Represents an image
    Written based on this snippet: http://djangosnippets.org/snippets/2094/
    """
    class Meta:
        app_label = 'competition'

    image = models.ImageField(upload_to=image_location)
    image_height = models.IntegerField()
    image_width = models.IntegerField()
    thumbnail = models.ImageField(upload_to=thumbnail_location)
    thumbnail_height = models.IntegerField()
    thumbnail_width = models.IntegerField()

    def __str__(self):
        return os.path.basename(self.image.path)

    def __unicode__(self):
        return os.path.basename(self.image.path)

    def save(self, force_update=False, force_insert=False,
             thumb_size=THUMB_SIZE):

        image = Image.open(self.image)

        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')

        # save the original size
        self.image_width, self.image_height = image.size

        image.thumbnail(thumb_size, Image.ANTIALIAS)

        # save the thumbnail to memory
        temp_handle = StringIO()
        image.save(temp_handle, 'png')
        temp_handle.seek(0)  # rewind the file

        # save to the thumbnail field
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                                 temp_handle.read(),
                                 content_type='image/png')
        self.thumbnail.save(suf.name + '.png', suf, save=False)
        self.thumbnail_width, self.thumbnail_height = image.size

        # save the image object
        super(Avatar, self).save(force_update, force_insert)

from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Чоловіча'),
        ('female', 'Жіноча'),
    ]
    TYPE_ACCOUNT = (
        ('full', 'Повний пакет'),
        ('free', 'Безкоштовний пакет')
    )


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField('Фото користувача', default='default.png', upload_to='user_images')
    gender = models.CharField('Стать', max_length=10, choices=GENDER_CHOICES, blank=True)
    subscribe = models.BooleanField('Підписка на розсилку', default=False)
    account_type = models.CharField(choices=TYPE_ACCOUNT, default='free', max_length=30)

    def __str__(self):
        return f'Профайл користувача {self.user.username}'


    def save(self, **args):
        super().save()

        image = Image.open(self.img.path)

        if image.height > 256 or image.width > 256:
            resize = (256, 256)
            image.thumbnail(resize)
            image.save(self.img.path)


    class Meta:
        verbose_name = 'Профайл'
        verbose_name_plural = 'Профайли'
    

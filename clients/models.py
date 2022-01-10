from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from PIL import Image
from io import BytesIO
from django.core.files import File

def upload_to(instance, filename):
    # filename = filename.split('.')[0]
    first_letter = instance.email[0]
    return f'clients/{first_letter}/{filename}'


class ClientManager(BaseUserManager):

    def create_client(self, email, first_name, second_name, password, **kwargs):
        if not email:
            raise ValueError('Provide email!')
        email = self.normalize_email(email)
        
        img = kwargs.pop('image')
        img_name = img.name
        img = Image.open(img.file).convert('RGBA')
        watermark = Image.open('media/watermark.png').resize((200,200)).convert('RGBA')
        img.paste(watermark, (0,0), mask=watermark)
        buf = BytesIO()
        img.save(fp=buf,format ='PNG')
        img = File(buf, name=f'{img_name}')
        kwargs['image'] = img
        client = self.model(email=email, first_name=first_name,
                            second_name=second_name, **kwargs)
        client.set_password(password)
        client.save()
        return client

    def create_superuser(self, email, first_name, second_name, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        return self.create_client(email, first_name, second_name, password, **kwargs)


class Client(AbstractBaseUser, PermissionsMixin):

    # user_name = models.CharField(max_length=250, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(_('Name'), max_length=100)
    second_name = models.CharField(_('Surname'), max_length=100)
    gender = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to=upload_to,default = 'default.png')
    is_staff = models.BooleanField(default=False)

    objects = ClientManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'second_name']

    def __str__(self):
        return self.email

class Profile(models.Model):
    
    owner = models.ForeignKey('Client', verbose_name=_("owner"),related_name='owner', on_delete=models.CASCADE)
    likes = models.ManyToManyField('Client', verbose_name=_("likes"),blank=True)
    
    def __str__(self):
        return f"{self.owner} profile"
    

# def watermarking(**kwargs):
#     print(kwargs)
#     image = kwargs.pop('image').file
#     print(image)
#     img = Image.open(image).convert('RGBA')
#     # image.show()
#     watermark = Image.open('media/watermark.png').resize((200,200)).convert('RGBA')
#     # watermark.show()
#     # img.paste(watermark,(0,0))
#     # transparent = Image.new('RGBA', img.size, (255,255,255))
#     transparent = img
#     # transparent.paste(img, (0,0))
#     transparent.paste(watermark, (0,0), mask=watermark)
#     buf = BytesIO()
#     transparent.save(fp=buf,format ='PNG')
#     # transparent.save(self.image.path)
#     transparent.show()
#     image = File(buf, name='resssssult.png')
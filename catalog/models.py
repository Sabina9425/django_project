from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, help_text='Введите имя категории')
    description = models.TextField(max_length=100, help_text="Введите описание категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, help_text='Введите имя продукта')
    description = models.TextField(max_length=100, help_text="Введите описание продукта")
    image = models.ImageField(upload_to='products/photo', blank=True, null=True, verbose_name='Превью',
                              help_text='Загрузите фото продукта')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name="Категория",
                                 help_text="Введите категорию продукта", related_name="products", null=True, blank=True)
    price = models.IntegerField(verbose_name='Цена', help_text='Введите цену продукта')
    created_at = models.DateField(verbose_name='Дата создания продукта', auto_now_add=True)
    updated_at = models.DateField(verbose_name='Дата изменения продукта', auto_now=True)
    owner = models.ForeignKey(User, verbose_name="Владелец", help_text="Укажите владельца продукта", blank=True, null=True,on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['name', 'price']

    def __str__(self):
        return self.name


class Post(models.Model):
    header = models.CharField(max_length=50, help_text='Введите заголовок поста')
    slug = models.CharField(max_length=100, help_text="Введите slug")
    content = models.TextField(max_length=500, help_text='Введите заголовок поста')
    preview = models.ImageField(upload_to='posts/preview', blank=True, null=True, verbose_name='Превью',
                                help_text='Загрузите превью')
    created_at = models.DateField(verbose_name='Дата создания продукта', auto_now_add=True)
    published = models.BooleanField(verbose_name="Признак публикации", default=False)
    views = models.IntegerField(verbose_name="Количество просмотров", default=0)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['created_at', 'views']

    def __str__(self):
        return self.header


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, verbose_name="Продукт",
                                help_text="Введите продукт", related_name="versions", null=True, blank=True)
    version_number = models.IntegerField(help_text='Введите номер версии')
    version_name = models.CharField(max_length=50, help_text='Введите название версии')
    is_current_version = models.BooleanField(verbose_name="Признак текущей версии", default=False)

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ['is_current_version', 'version_number']

    def __str__(self):
        return self.version_name

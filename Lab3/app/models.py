from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, User
from django.db import models


class Item(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(max_length=500, verbose_name="Описание",)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(verbose_name="Фото", blank=True, null=True)

    price = models.IntegerField(verbose_name="Цена")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вещь"
        verbose_name_plural = "Вещи"
        db_table = "items"


class Declaration(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершен'),
        (4, 'Отклонен'),
        (5, 'Удален')
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(verbose_name="Дата создания", blank=True, null=True)
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Создатель", related_name='owner', null=True)
    moderator = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Сотрудник", related_name='moderator', blank=True,  null=True)

    date = models.DateField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Декларация №" + str(self.pk)

    class Meta:
        verbose_name = "Декларация"
        verbose_name_plural = "Декларации"
        db_table = "declarations"
        ordering = ('-date_formation', )


class ItemDeclaration(models.Model):
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, blank=True, null=True)
    declaration = models.ForeignKey(Declaration, on_delete=models.DO_NOTHING, blank=True, null=True)
    value = models.IntegerField(verbose_name="Поле м-м", default=0)

    def __str__(self):
        return "м-м №" + str(self.pk)

    class Meta:
        verbose_name = "м-м"
        verbose_name_plural = "м-м"
        db_table = "item_declaration"
        constraints = [
            models.UniqueConstraint(fields=['item', 'declaration'], name="item_declaration_constraint")
        ]

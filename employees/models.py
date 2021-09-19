from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.exceptions import ValidationError

class Employee(MPTTModel):

    MAX_TREE_DEPTH = 3

    name = models.CharField(max_length=255, verbose_name='Имя')
    surname = models.CharField(max_length=255, verbose_name='Фамилия')
    third_name = models.CharField(max_length=255, verbose_name='Отчество')
    position = models.CharField(max_length=500, verbose_name='Должность')
    employment_date = models.DateField(verbose_name='Дата приема на работу')
    salary = models.PositiveIntegerField(verbose_name='Размер заработной платы')
    chief = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='employees', verbose_name='Начальник')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = "Сотрудники"

    class MPTTMeta:
        parent_attr = 'chief'

    def __str__(self):
        return self.get_full_name()

    def clean(self):
        if self.chief is not None:
            self.chiefs = self.chief
            chief_level = self.chiefs.get_level()
            if chief_level + 2 > self.MAX_TREE_DEPTH:
                raise ValidationError({'chief': f'Nesting limit, maximum - {self.MAX_TREE_DEPTH}'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f'{self.surname} {self.name} {self.third_name}'
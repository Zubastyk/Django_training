from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError

# Связь один с одним
class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

# Связь многие со многими
# модель ведомая (отдельные детали)
class Spare(models.Model):
    name = models.CharField(max_length=30)
# модель ведущая (готовые машины)    
class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)

# Класс-валидатор(стр. 116)
class MinMaxValueValidator:  
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
        
    def __call__(self, val):
        if val < self.min_value or val > self.max_value:
            raise ValidationError('Введеное число должно ' +\
                                'находиться в диапазоне от %(min)s до %(max)s',
                                  code='out_of_range',
                                  params={'min': self.min_value, 'max': self.max_value})
          

class Bb(models.Model):
    # Поле со списком 
    KINDS = (
        ('Купля-продажа', (
            ('b', 'Куплю'),
            ('s', 'Продам'),
        )),
        ('Обмен', (
        ('c', 'Обменяю'),
        ))
    )
    kind = models.CharField(max_length=1, choices=KINDS, default='s', verbose_name='Категория объявления')
    title = models.CharField(max_length=50, verbose_name='Товар',
                             validators=[validators.RegexValidator(regex='^.{3,}$')],
                             error_messages={'invalid': 'Неправильное название товара'})
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(null=True, blank=True, verbose_name='Цена', max_digits=10, decimal_places=2)
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True,
                               on_delete=models.PROTECT, verbose_name='Рубрика')
    
    # Функциональное поле
    def title_and_price(self):
        if self.price:
            return '%s (%.2f)' % (self.title, self.price)
        else:
            return self.title
    title_and_price.short_description = 'Название и цена'

    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание ' +\
                                                'продаваемого товара')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите ' +\
                                    'неотрицательное значение цены')
        if errors:
            raise ValidationError(errors)
    

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']
        
class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']


# Перечисления, содержащие внутренние значения
class Measure(models.Model):
    class Measurements(float, models.Choices):
        МETERS = 1.0, 'Метры'
        FEET = 0.3048, 'Футы'
        YARDS = 0.9144, 'Ярды'
        
    measurement = models.FloatField(choices=Measurements.choices)
from django.db import models
from django.urls import reverse_lazy


class TestModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=155)
    filial = models.ManyToManyField('Filial', related_name='tests', verbose_name="Филиал")


class Filial(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(max_length=255, verbose_name="URL")
    prog_id = models.IntegerField(default=0, verbose_name="Код программы Логистика")
    url_wms = models.CharField(max_length=255, verbose_name="Наименование базы WMS")
    path_saved_order = models.CharField(max_length=255, verbose_name="Сетевая папка филиала")
    position = models.IntegerField(default=0, verbose_name="Позиция в меню")
    as_active = models.BooleanField(default=True, verbose_name="Признак активности")

    def __str__(self):
        return self.name

    def get_path_saved_filial(self):
        return self.path_saved_order

    def get_home_url(self):
        return reverse_lazy(f'{self.slug}')

    class Meta:
        ordering = ('position',)
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Наименование")
    filial = models.ManyToManyField(Filial, related_name='menus', verbose_name="Филиал")
    slug = models.SlugField(max_length=255, verbose_name="URL")
    position = models.IntegerField(default=0, verbose_name="Позиция в меню")
    as_active = models.BooleanField(default=True, verbose_name="Признак активности")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('position',)
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


class SubMenu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Наименование")
    menu = models.ManyToManyField(Menu, related_name='menus', verbose_name="Меню")
    slug = models.SlugField(max_length=255, verbose_name="URL")
    position = models.IntegerField(default=0, verbose_name="Позиция в меню")
    as_active = models.BooleanField(default=True, verbose_name="Признак активности")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy(self.slug)

    class Meta:
        ordering = ('position',)
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'


class Contracts(models.Model):
    id = models.AutoField(primary_key=True)
    filial = models.ManyToManyField(Filial, related_name='contracts', verbose_name="Филиал")
    menu = models.ManyToManyField(Menu, related_name='contracts', verbose_name="Меню")
    name = models.CharField(max_length=255, verbose_name="Наименование")
    submenu = models.ManyToManyField(SubMenu, related_name='contracts', verbose_name="Операция")
    slug = models.SlugField(max_length=255, verbose_name="URL")
    position = models.IntegerField(default=0, verbose_name="Позиция в меню")
    as_active = models.BooleanField(default=True, verbose_name="Признак активности")
    id_groups_goods = models.IntegerField(default=0, verbose_name="Код папки товаров")
    id_postav = models.IntegerField(default=0, verbose_name="Код поставщика", null=True, blank=True)
    id_client = models.IntegerField(default=0, verbose_name="Код клиента", null=True, blank=True)
    id_sklad = models.IntegerField(default=0, verbose_name="Код склада", null=True, blank=True)
    id_agent = models.IntegerField(default=0, verbose_name="Код агента", null=True, blank=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse_lazy('operations-detail', kwargs={'slug': self.slug})
    #
    def get_home_url(self):
        return reverse_lazy(f'{self.slug}')

    #
    # def handler_form(self):
    #     return reverse_lazy(f'handler_form', kwargs={'_filial_slug': self.filial.slug, '_contract_slug': self.slug})

    class Meta:
        ordering = ('position',)
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'

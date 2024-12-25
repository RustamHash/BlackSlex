from django import template

from base_app.models import Menu, Filial, SubMenu

register = template.Library()


@register.simple_tag()
def get_filials():
    return Filial.objects.all()


@register.simple_tag()
def get_menu(filial_slug=None):
    if not filial_slug:
        return None
    else:
        return Menu.objects.filter(filial__slug=filial_slug, as_active=True)


@register.simple_tag()
def get_main_url(menu_slug, app_slug):
    url = f'{app_slug}:{menu_slug}'
    return url


@register.simple_tag()
def get_main_url_processing(app_slug):
    menu_slug = 'processing_add_orders'
    url = f'{app_slug}:{menu_slug}'
    return url


@register.inclusion_tag('base_app/templates_tags/submenu.html')
def show_sub_menu(menu_slug, test):
    sub_menus = SubMenu.objects.filter(menu__slug=menu_slug)
    return {"sub_menus": sub_menus}

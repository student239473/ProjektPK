from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_links(context):
    user = context['user']
    links = [
        {
            'name': 'Strona główna',
            'href': '/',
            'icon': 'fa-house',
        },
        {
            'name': 'Nasze auta',
            'href': '/cars',
            'icon': 'fa-car',
        },
        {
            'name': 'Kontakt',
            'href': '/contact',
            'icon': 'fa-paper-plane',
        },
        {
            'name': 'O nas',
            'href': '/about',
            'icon': 'fa-address-card',
        },
        {
            'name': 'Aktualności',
            'href': '/news/',
            'icon': 'fa-newspaper',
        },
        {
            'name': 'Forum',
            'href': '/forum',
            'icon': 'fa-comment',
        },
    ]

    if user.is_staff:
        links.append({
            'name': 'Dodaj aktualność',
            'href': '/news/create',
            'icon': 'fa-plus',
        })

    return links
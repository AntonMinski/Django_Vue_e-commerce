from django import template
from django.db.models import Sum
from django.urls import reverse

from store import settings
from order.models import ShopCart
from products.models import Category
from webstore.models import Setting

register = template.Library()



@register.simple_tag
def category_list():  # чтобы не писать все время category во view
    return Category.objects.all()


@register.simple_tag
def setting_list():  # чтобы не писать все время category во view
    return Setting.objects.get(pk=1)


@register.simple_tag
def shop_cart_count(user_id):
    count = ShopCart.objects.filter(user_id=user_id).count()
    return count


@register.simple_tag
def shopcart(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_price, total_quantity = 0, 0
    for rs in shopcart:
        total_price += rs.product.price * rs.quantity
        total_quantity += 1
    context = {
        'shopcart': shopcart,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'current_user': current_user,
    }
    return context


    # total_price, total_quantity = 0, 0
    # for rs in shop_cart:
    #     total_price += rs.product.price * rs.quantity
    #     total_quantity += 1
    # return shop_cart


# views-> "category =  categoryTree(0,'','tr')"
# html-> "categoryTree 0 '' LANGUAGE_CODE as category" :
@register.simple_tag
def category_tree(id, menu, lang):  # для смены языка в меню категорий
    default_lang = settings.LANGUAGE_CODE[0:2]  # lang='tr'
    # Main categories (отобрать категориями, что являются корневыми ):
    if id <= 0:
        if lang == default_lang:  # default language
            query = Category.objects.filter(parent_id__isnull=True)\
                .order_by("id")
            # отобрать обьекты, что в корневых категориями
        else:  # non default language
            query = Category.objects.raw(
                'SELECT c.id,l.title, l.keywords, l.description,l.slug'
                '  FROM product_category as c'
                '  INNER JOIN product_categorylang as	l'
                '  ON c.id = l.category_id'
                '  WHERE  parent_id IS NULL and lang=%s ORDER BY c.id', [lang])
        query_count = Category.objects.filter(parent_id__isnull=True).count()
    else:  # Sub Categories
        if lang == default_lang:  # default language
            query = Category.objects.filter(parent_id=id)
        else:  # non default language
            query = Category.objects.raw(
                'SELECT c.id,l.title, l.keywords, l.description,l.slug'
                '  FROM product_category as c'
                '  INNER JOIN product_categorylang as	l'
                '  ON c.id = l.category_id'
                '  WHERE  parent_id =%s AND lang=%s', [id, lang])
        query_count = Category.objects.filter(parent_id=id).count()
    if query_count > 0:
        for rs in query:
            sub_count = Category.objects.filter(parent_id=rs.id).count()
            if sub_count > 0:
                menu += '\t<li class="dropdown side-dropdown">\n'
                # t - tab_space (\t\t\t - 3x tab_space)
                menu += '\t<a class ="dropdown-toggle"' \
                        ' data-toggle="dropdown" aria-expanded="true">'\
                        + rs.title + '<i class="fa fa-angle-right"></i></a>\n'
                menu += '\t\t<div class="custom-menu">\n'
                menu += '\t\t\t<ul class="list-links">\n'
                menu += category_tree(int(rs.id), '', lang)
                menu += '\t\t\t</ul>\n'
                menu += '\t\t</div>\n'
                menu += "\t</li>\n\n"
            else:
                menu += '\t\t\t\t<li><a href="' + reverse('category_products',
                                                          args=(rs.id,
                                                                rs.slug)) +\
                        '">' + rs.title + '</a></li>\n'
                # последняя категория в дереве, в которой уже товары
    return menu

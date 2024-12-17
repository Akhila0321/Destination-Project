from tours.models import Destiny, Accommodation


def menu_links(request):
    d = Destiny.objects.all()
    return {'links': d}


def menu_links1(request):
    a = Accommodation.objects.all()
    return {'link': a}

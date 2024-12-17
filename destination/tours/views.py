from django.shortcuts import render, redirect
from tours.models import Destiny, Attraction, Accommodation


# Create your views here.


def place(request):
    d = Destiny.objects.all()
    context = {'dest': d}
    return render(request, 'place.html', context)


def attracts(request, p):
    d = Destiny.objects.get(id=p)
    a = Attraction.objects.filter(destiny=d)
    context = {'dest': d, 'attract': a}
    return render(request, 'attract.html', context)


def details(request, p):
    a = Attraction.objects.get(id=p)
    context = {'attract': a, 'i': a}
    print(context)
    return render(request, 'details.html', context)


def stay(request, p):
    d = Destiny.objects.get(id=p)
    ac = Accommodation.objects.filter(destiny=d)
    context = {'dest': d, 'accommodate': ac}
    return render(request, 'accommodate.html', context)


# views.py

def accommodation_detail(request, p):
    accommodation = Accommodation.objects.get(id=p)
    room_images = accommodation.room_images.prefetch_related('facilities')  # Fetch related facilities
    return render(request, 'accommodate_details.html', {
        'accommodation': accommodation,
        'room_images': room_images,
    })


def add_destiny(request):
    if request.method == "POST":
        c = request.POST['c']
        d = request.POST['d']
        i = request.FILES['i']
        p = request.POST['p']
        d = Destiny.objects.create(country=c, description=d, image=i, price_range=p)
        d.save()
        return redirect('tours:place')
    return render(request, 'adddestiny.html')


def add_accommodate(request):
    if request.method == 'POST':
        n = request.POST['n']
        c = request.POST['c']
        i = request.FILES['i']
        p = request.POST['p']
        d = request.POST['d']
        dest = Destiny.objects.get(country=d)
        ac = Accommodation.objects.create(name=n, description=c, image=i, price_per_night=p, destiny=dest)
        ac.save()
        return redirect('tours:place')

    return render(request, 'addaccommodate.html')

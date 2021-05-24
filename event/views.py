from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Models
from .models import Image, Event


def gallery(request):
    event = Event.objects.all()
    image = Image.objects.filter(id__range=(1, 1000)).order_by("?")[:100]
    data =  {
        'images': image, 'events': event
    }
    return render(request, 'gallery/gallery.html', data)

def events(request):
    event = Event.objects.all()
    return render(request, 'event/event.html', {'events': event})


@login_required(login_url='login')
def event_details(request, id):
    event = Event.objects.get(id=id)
    events = Event.objects.filter(id__range=(1, 10)).order_by("?")[:3]
    return render(request, 'event/event-details.html', {'event': event, 'events': events})





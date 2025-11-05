from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime
from datacenter.visit_time import get_duration, format_duration, is_visit_long


def storage_information_view(request):
    # Программируем здесь

    active_visits = Visit.objects.filter(leaved_at=None)

    non_closed_visits = []

    for visit in active_visits:
        duration = get_duration(visit)
        formatted_duration = format_duration(duration)

        non_closed_visits.append({
            'who_entered': visit.passcard.owner_name,
            'entered_at': localtime(visit.entered_at),
            'duration': formatted_duration,
        })
    


    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)


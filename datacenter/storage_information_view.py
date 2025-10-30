from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime


def get_duration(visit):
    entered_time = localtime(visit.entered_at)
      
    if visit.leaved_at:
        leaved_time = localtime(visit.leaved_at)
    else:
        leaved_time = localtime()

    duration = leaved_time - entered_time
    return duration


def format_duration(duration):
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    return f"{hours:02}:{minutes:02}"


def is_visit_long(visit, minutes=60):
    duration = get_duration(visit)
    return duration.total_seconds() > minutes * 60



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


from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime
from datacenter.models import Passcard, Visit


def get_duration(visit):
    entered_time = localtime(visit.entered_at)
    if visit.leaved_at:
        leaved_time = localtime(visit.leaved_at)
    else:
        leaved_time = localtime()
    return leaved_time - entered_time


def format_duration(duration):
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def is_visit_long(visit, minutes=60):
    duration = get_duration(visit)
    return duration.total_seconds() > minutes * 60


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)

    visits = Visit.objects.filter(passcard=passcard)

    this_passcard_visits = []
    for visit in visits:
        duration = get_duration(visit)
        this_passcard_visits.append({
            'entered_at': localtime(visit.entered_at),
            'duration': format_duration(duration),
            'is_strange': is_visit_long(visit),
        })

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)

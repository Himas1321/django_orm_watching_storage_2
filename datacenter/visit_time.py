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
    SECONDS_PER_HOUR = 3600
    SECONDS_PER_MINUTE = 60
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, SECONDS_PER_HOUR)
    minutes = remainder // SECONDS_PER_MINUTE
    return f"{hours:02}:{minutes:02}"


def is_visit_long(visit, minutes=60):
    SECONDS_PER_MINUTE = 60
    duration = get_duration(visit)
    return duration.total_seconds() > minutes * SECONDS_PER_MINUTE

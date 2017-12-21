from datetime import datetime


def my_cp(request):
    ctx = {
        "version": "1.0",
        "actual_date": datetime.now()
    }
    return ctx


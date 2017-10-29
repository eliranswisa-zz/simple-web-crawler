from decimal import *
from slugify import slugify


def slugify_filename(url):
    filename = slugify(url)
    return filename


def calculate_ratio(total, same_domain):
    getcontext().prec = 3
    total = Decimal(total)
    same_domain = Decimal(same_domain)
    if total == 0:
        return total
    return same_domain / total

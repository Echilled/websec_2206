import validators as vads


def is_valid_url(url):
    return vads.url(url)

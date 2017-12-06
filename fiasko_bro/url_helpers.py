

def is_url_with_params(string):
    if not string.startswith('http') or '?' not in string:
        return False
    query_part = string.split('?')[-1]
    for key_value_pair in query_part.split('&'):
        if '=' not in key_value_pair:
            return False
    return True

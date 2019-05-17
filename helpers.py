def len_check(string):
    if len(string) < 3 or len(string) > 20:
        return True
    else:
        return False

def not_blank(s):
    return bool(s and s.strip())

def blank(s):
    if " " in s:
        return True
    return False

def check_list(lst):
    for i in lst:
        if i:
            return False
    return True
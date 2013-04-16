def reverse_range(reverse, start, stop=None, step=1):
    if stop is None:
        stop = start
        start = 0
    if reverse:
        step = -step
        start, stop = stop-1, start-1
    return range(start, stop, step)

def smart_range(start, stop, step=1):
    if stop < start:
        step = -step
    return range(start, stop, step)

def safe_input(ask, type):
    run = True
    ret = None
    while run:
        try:
            ret = type(input(ask))
        except ValueError:
            print("Entrée invalide.")
        else:
            run = False
    return ret
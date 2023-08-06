import os,sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from local.bon_file import rjson, rlines, puser
from time import sleep
from datetime import datetime
from pydirectinput import move
from pynput import mouse,keyboard
from pyperclip import copy

from contextlib import contextmanager

def km(fn):
    """ Decorator function to replace func string param with corresponding value from key management: ~/KM/targetFile

    Args:
        fn: file name pointing to key management service/file

    Return:
        Decorated function.
    """
    rows = rlines(puser('KM',fn))
    kd = {}
    for row in rows:
        kd[row.split('=',1)[0]]=row.split('=',1)[1].rstrip('\n')
    def decorator(func):
        def wrapper(*args, **kwargs):
            arr = [kd[x] if x in kd else x for x in args]
            func(*arr,**kwargs)
        return wrapper
    return decorator

def afk(): 
    """ A while-true loop call to constantly move mouse up and down.

    Args:
        None

    Return:
        None
    """
    cnt, t = 0, 60
    while True:
        if cnt % t == 0:
            print(f"{datetime.now()}: {cnt//t}")
        move(-1, None)
        move(1, None)
        sleep(1.0)
        cnt+=1

def hk():
    """ A demon process to catch and process predefined hot keys, under ~/Scripts/hk.json.

    Args:
        <shift>+<alt>+ch: ch is within [a-z] and [0-9]
        <shift>+<alt>+`: quit hk mode

    Return:
        None
    """
    mp = rjson(puser('Scripts', 'hk.json'))
    def on_activate(e):
        if e in mp:
            copy(mp[e])
        else:
            print(f"{e} not in hk map")

    def quit():
        h.stop()

    with keyboard.GlobalHotKeys({
        '<shift>+<alt>+a': lambda: on_activate('a'),
        '<shift>+<alt>+b': lambda: on_activate('b'),
        '<shift>+<alt>+c': lambda: on_activate('c'),
        '<shift>+<alt>+d': lambda: on_activate('d'),
        '<shift>+<alt>+e': lambda: on_activate('e'),
        '<shift>+<alt>+f': lambda: on_activate('f'),
        '<shift>+<alt>+g': lambda: on_activate('g'),
        '<shift>+<alt>+h': lambda: on_activate('h'),
        '<shift>+<alt>+i': lambda: on_activate('i'),
        '<shift>+<alt>+j': lambda: on_activate('j'),
        '<shift>+<alt>+k': lambda: on_activate('k'),
        '<shift>+<alt>+l': lambda: on_activate('l'),
        '<shift>+<alt>+m': lambda: on_activate('m'),
        '<shift>+<alt>+n': lambda: on_activate('n'),
        '<shift>+<alt>+o': lambda: on_activate('o'),
        '<shift>+<alt>+p': lambda: on_activate('p'),
        '<shift>+<alt>+q': lambda: on_activate('q'),
        '<shift>+<alt>+r': lambda: on_activate('r'),
        '<shift>+<alt>+s': lambda: on_activate('s'),
        '<shift>+<alt>+t': lambda: on_activate('t'),
        '<shift>+<alt>+u': lambda: on_activate('u'),
        '<shift>+<alt>+v': lambda: on_activate('v'),
        '<shift>+<alt>+w': lambda: on_activate('w'),
        '<shift>+<alt>+x': lambda: on_activate('x'),
        '<shift>+<alt>+y': lambda: on_activate('y'),
        '<shift>+<alt>+z': lambda: on_activate('z'),
        '<shift>+<alt>+0': lambda: on_activate('0'),
        '<shift>+<alt>+1': lambda: on_activate('1'),
        '<shift>+<alt>+2': lambda: on_activate('2'),
        '<shift>+<alt>+3': lambda: on_activate('3'),
        '<shift>+<alt>+4': lambda: on_activate('4'),
        '<shift>+<alt>+5': lambda: on_activate('5'),
        '<shift>+<alt>+6': lambda: on_activate('6'),
        '<shift>+<alt>+7': lambda: on_activate('7'),
        '<shift>+<alt>+8': lambda: on_activate('8'),
        '<shift>+<alt>+9': lambda: on_activate('9'),
        '<shift>+<alt>+`': quit}) as h:
        h.join()

def monitor_mouse():
    """Monitor and print out mouse activity.

    Args:
        None
    
    Return:
        None
    """
    with mouse.Events() as events:
        with mouse.Events() as events:
            for event in events:
                try:
                    if event.button == mouse.Button.right:
                        print('Right button clicked!')
                        break
                except: 
                    pass
                finally:
                    print('Received event {}'.format(event))

def monitor_keyboard():
    """Monitor and print out mouse activity.

    Args:
        None
    
    Return:
        None
    """
    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.Key.esc:
                break
            else:
                print('Received event {}'.format(event))


@contextmanager
def change_dir(destination):
    try:
        cwd = os.getcwd()
        os.chdir(destination)
        yield
    finally:
        os.chdir(cwd)

@km(fn='test.km')
def test(s):
    print(s)

if __name__ == "__main__":
    print('### ghost ###')
    test('name')

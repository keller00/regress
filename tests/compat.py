from sys import platform


def on_windows():
    return platform == 'win32'


def on_mac():
    return platform == 'darwin'


def on_linux():
    return platform == 'linux'


def on_cygwin():
    return platform == 'cygwin'

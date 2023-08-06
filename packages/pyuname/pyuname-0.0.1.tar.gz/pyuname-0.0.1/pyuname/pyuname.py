import os

def uname_kernel():
    result = os.popen("uname -s").read()
    return result


def uname_nodename():
    result = os.popen("uname -n").read()
    return result


def uname_kernel_rev():
    result = os.popen("uname -r").read()
    return result


def uname_kernel_ver():
    result = os.popen("uname -v").read()
    return result


def uname_machine():
    result = os.popen("uname -m").read()
    return result


def uname_processor():
    result = os.popen("uname -p").read()
    return result


def uname_platform():
    result = os.popen("uname -i").read()
    return result


def uname_os():
    result = os.popen("uname -o").read()
    return result


def uname_all():
    result = os.popen("uname -a").read()
    return result


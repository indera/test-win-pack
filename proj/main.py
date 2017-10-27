"""
Goal: Test packaging multiproc apps for windows
"""
import os
import sys
import argparse
import multiprocessing
from time import sleep
from version import __VERSION__

# From: https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
# Module multiprocessing is organized differently in Python 3.4+
try:
    # Python 3.4+
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking

if sys.platform.startswith('win'):
    # First define a modified version of Popen.
    class _Popen(forking.Popen):
        def __init__(self, *args, **kw):
            if hasattr(sys, 'frozen'):
                # We have to set original _MEIPASS2 value from sys._MEIPASS
                # to get --onefile mode working.
                os.putenv('_MEIPASS2', sys._MEIPASS)
            try:
                super(_Popen, self).__init__(*args, **kw)
            finally:
                if hasattr(sys, 'frozen'):
                    # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                    # available. In those cases we cannot delete the variable
                    # but only set it to the empty string. The bootloader
                    # can handle this case.
                    if hasattr(os, 'unsetenv'):
                        os.unsetenv('_MEIPASS2')
                    else:
                        os.putenv('_MEIPASS2', '')

    # Second override 'Popen' class with our modified version.
    forking.Popen = _Popen


def version():
    print("deduper, version {}".format(__VERSION__))
    sys.exit()

def _yes(i, text="yes"):
    sleep(1)
    return "{}:{}".format(i, text)

def yes(args):
    cpus = int(args.cpus)
    secs = int(args.secs)
    pool = multiprocessing.Pool(processes=cpus)
    jobs = []

    for i in range(0, secs):
        job = pool.apply_async(_yes, (i, args.text, ))
        # job = pool.map(_yes, (i, what, ))
        jobs.append(job)

    for index, job in enumerate(jobs):
        print(job.get())

    pool.close()
    pool.join()

def main(args=None):
    # to support multiproc on windows this line *must* be the first
    multiprocessing.freeze_support()

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version",
                        default=False,
                        action='store_true',
                        help="Show the version number")
    parser.add_argument("-s", "--secs",
                        default=5,
                        help="how many seconds")
    parser.add_argument("-c", "--cpus",
                        default=5,
                        help="how many cpus")
    parser.add_argument("-t", "--text",
                        default="yes",
                        help="what to print")


    args = parser.parse_args()

    if args.version:
        version()

    print("Running proj version: {}".format(__VERSION__))
    yes(args)


if __name__ == "__main__":
    main()

import sys
import urllib.request

def macos_proxies_crash_fix():
    # calling the mac os API to get proxies from the system
    # after doing fork() causes crashes because those APIs
    # expect to be re-initialized after fork() but that
    # doesn't happen, so we

    if '--print-proxies' in sys.argv:
        proxies = urllib.request.getproxies()


    else:
    old_getproxies = urllib.request.getproxies



    def new(*n, **kw):
        import traceback
        traceback.print_stack()
        return old_getproxies(*n, **kw)

    urllib.request.getproxies = new

macos_proxies_crash_fix()

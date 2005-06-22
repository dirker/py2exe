# This support script is executed as the entry point for ctypes com servers.
# XXX Currently, this is always run as part of a dll.

import sys
import _ctypes

if 1:
    ################################################################
    # XXX Remove later!
    import ctypes
    class LOGGER:
        def __init__(self):
            self.softspace = None
        def write(self, text):
            ctypes.windll.kernel32.OutputDebugStringA(text)
    sys.stderr = sys.stdout = LOGGER()
##    sys.stderr.write("PATH is %s\n" % sys.path)

################################################################
# tell the win32 COM registering/unregistering code that we're inside
# of an EXE/DLL

if not hasattr(sys, "frozen"):
    # standard exes have none.
    sys.frozen = _ctypes.frozen = 1
else:
    # com DLLs already have sys.frozen set to 'dll'
    _ctypes.frozen = sys.frozen

# Add some extra imports here, just to avoid putting them as "hidden imports"
# anywhere else - this script has the best idea about what it needs.
# (and hidden imports are currently disabled :)
#...none so far

# Patchup sys.argv for our DLL
#if sys.frozen=="dll" and not hasattr(sys, "argv"):
#    sys.argv = [win32api.GetModuleFileName(sys.frozendllhandle)]

# We assume that py2exe has magically set com_module_names
# to the module names that expose the COM objects we host.
# Note that here all the COM modules for the app are imported - hence any
# environment changes (such as sys.stderr redirection) will happen now.
try:
    com_module_names
except NameError:
    print "This script is designed to be run from inside py2exe % s" % str(details)
    sys.exit(1)
    
com_modules = []
for name in com_module_names:
    __import__(name)
    com_modules.append(sys.modules[name])

def get_classes(module):
    return [ob
            for ob in module.__dict__.values()
            if hasattr(ob, "_reg_progid_")
            ]

def DllRegisterServer():
    # Enumerate each module implementing an object
    from ctypes.com.register import register
    for mod in com_modules:
        # register each class
        register(*get_classes(mod))


def DllUnregisterServer():
    # Enumerate each module implementing an object
    from ctypes.com.register import unregister
    for mod in com_modules:
        # register each class
        unregister(*get_classes(mod))

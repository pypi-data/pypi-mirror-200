def __bootstrap__():
    global __bootstrap__, __loader__, __file__
    import sys, pkg_resources, importlib.util
    __file__ = pkg_resources.resource_filename(__name__, '4a0d29f3f35e06f65bf1__mypyc.cpython-310-x86_64-linux-gnu.so')
    __loader__ = None; del __bootstrap__, __loader__
    spec = importlib.util.spec_from_file_location(__name__,__file__)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
__bootstrap__()

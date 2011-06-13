from clojure.lang import RT, Compiler, Keyword
import java.io
import functools

def load_string(clojure_code):
    Compiler.load(java.io.StringReader(clojure_code))

def clojure(fn):
    try:
        clj_namespace = fn.__module__
    except AttributeError:
        clj_namespace = 'user'

    clojure_code ='(ns %s)\n%s' % (
        clj_namespace,
        fn.__doc__)
    load_string(clojure_code)

    clojure_fnc = RT.var(clj_namespace, fn.func_name)

    meta = clojure_fnc.meta()
    fn.__doc__ = meta.get(Keyword.intern('doc'))

    def aux(*args):
        return clojure_fnc.invoke(*args)
    functools.update_wrapper(aux, fn)

    return aux



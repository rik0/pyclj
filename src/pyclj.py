from clojure.lang import RT, Compiler, Keyword
import java.io
import functools

def clojure_compile_string(clojure_code):
    """Compile the clojure_code with clojure compiler
    """
    Compiler.load(java.io.StringReader(clojure_code))

def determine_clojure_namespace(fn):
    """Determines the appropriate clojure namespace from the original Python module
    """
    try:
        clj_namespace = fn.__module__
    except AttributeError:
        clj_namespace = 'user'
    return clj_namespace


def build_clojure_function_object(clj_namespace, fn):
    """Builds a clojure function from a python function with clojure code in the docs.
    """
    clojure_code = '(ns %s)\n%s' % (
        clj_namespace,
        fn.__doc__)
    clojure_compile_string(clojure_code)
    clojure_fnc = RT.var(clj_namespace, fn.func_name)
    return clojure_fnc

def get_docs(clojure_fnc):
    """Gets the docs from the clojure function object.
    """
    meta = clojure_fnc.meta()
    return meta.get(Keyword.intern('doc'))

def clojure(fn):
    """Decorator that substitutes an empty python function with clojure
     in the doc with a callable which delegates to the clojure function.
    """
    clj_namespace = determine_clojure_namespace(fn)
    clojure_fnc = build_clojure_function_object(clj_namespace, fn)

    fn.__doc__ = get_docs(clojure_fnc)

    def aux(*args):
        return clojure_fnc.invoke(*args)
    functools.update_wrapper(aux, fn)

    return aux



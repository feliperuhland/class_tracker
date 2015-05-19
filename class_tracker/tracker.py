# coding: utf-8

import sys


class TrackerException(Exception):
    def __init__(self, local_var, filename, line):
        self.local_var = local_var
        self.filename = filename
        self.line = line

    def __str__(self, local_var, filename, line):
        return repr('{} in {} near #{}'.format(self.local_var, self.filename, self.line))


def extract_class(class_tuple):
    new_class_list = []
    for clazz in class_tuple.split(','):
        index = clazz.rfind('.')
        mdl = clazz[:index]
        cls = clazz[index+1:]
        inst_mdl = __import__(mdl)
        inst_cls = getattr(inst_mdl, cls)
        new_class_list.append(inst_cls)
    return tuple(new_class_list)


def tracker_exception(class_list):
    class_list = extract_class(class_list)

    def tracker_wrap(f):
        def wrapper(*args, **kwargs):
            def trace_line_func(frame, event, arg):
                for local_var in frame.f_locals.keys():
                    if isinstance(frame.f_locals[local_var], class_list):
                        raise TrackerException(
                            frame.f_locals[local_var],
                            frame.f_code.co_filename,
                            frame.f_lineno
                        )
                return trace_line_func
            sys.settrace(trace_line_func)
            ret = f(*args, **kwargs)
            sys.settrace(None)
            return ret
        return wrapper
    return tracker_wrap

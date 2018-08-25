#   coding: utf-8
#   transformers reference

import logging
import functools

"""
        输入的node_map格式为：
        id          [int]
        key         [str]
        field       [str]
        label       [str] vak
        parent_id   [int]
        level       [int]
        children    [dict]
        is_leaf     [boolean]
        ext_data   [none or list or obj]
 """


def default_strategy(pnode, cnode, line_entity, extra_data):
    pass


strategies = {
    "default":default_strategy,
}


def strategy(group_name):
    """
    定义transformer的注解
    :param group_name:
    :return:
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'strategy'
        wrapper.__group__ = group_name.lower()
        return wrapper
    return decorator


def add_strategy(fn):
    """
    封装有注解的方法为transformer并添加到map中
    :param fn:
    :return:
    """
    method_group = getattr(fn, '__group__', None)
    if method_group is None:
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    strategies[method_group] = fn
    logging.info('add strategy %s %s => mapper' % (method_group, fn.__name__,))


def add_strategies(module_name):
    """
    加载transformers模块
    :param module_name:
    :return:
    """
    n = module_name.rfind('.')
    if n == (-1):
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n + 1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            method_group = getattr(fn, '__group__', None)
            if method_group:
                add_strategy(fn)


"""
加载transformers模块
"""
add_strategies("strategies")

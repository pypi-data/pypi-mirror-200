# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent import scope
from contrast.agent.assess.utils import is_tracked
from contrast.agent.assess.policy import string_propagation
from contrast.utils.decorators import fail_quietly


def contrast__cformat__modulo(format_str, args):
    with scope.propagation_scope():
        result = format_str % args

    if scope.in_scope() or scope.in_trigger_scope():
        return result

    _propagate_cformat(result, format_str, args)

    return result


@fail_quietly("failed to propagate through modulo in contrast__cformat__modulo")
def _propagate_cformat(result, format_str, args):
    propagation_func = None

    if isinstance(result, str):
        propagation_func = string_propagation.propagate_unicode_cformat
    elif isinstance(result, bytes):
        propagation_func = string_propagation.propagate_bytes_cformat
    elif isinstance(result, bytearray):
        # TODO: PYT-2709 - Update tests to verify bytearray is supported with and without funchook
        propagation_func = string_propagation.propagate_bytearray_cformat

    if propagation_func is None:
        return

    with scope.contrast_scope(), scope.propagation_scope():
        propagation_func(result, format_str, result, args, None)


def contrast__add(left, right):
    """
    This function replaces addition in the AST. We use double underscore to lower the
    probability of a name conflict.

    It is basically a pure-python translation of <type>_concat_new from str_concat.c.
    In the future, we should consider implementing as much of this in C as possible.
    """
    with scope.propagation_scope():
        result = left + right

    _propagate_add(left, right, result)

    return result


def contrast__append(target, value):
    orig_target = target
    with scope.propagation_scope():
        target += value

    _propagate_add(orig_target, value, target)

    return target


def contrast__fstring(*strings):
    # fstring formatting is equivalent to str.join
    return "".join(strings)


@fail_quietly("failed to propagate through addition in contrast__add")
def _propagate_add(left, right, result):
    propagation_func = None
    if isinstance(result, str):
        propagation_func = string_propagation.propagate_unicode_concat
    elif isinstance(result, bytes):
        propagation_func = string_propagation.propagate_bytes_concat
    elif isinstance(result, bytearray):
        propagation_func = string_propagation.propagate_bytearray_concat
    if propagation_func is None:
        return

    if len(result) < 2:
        return

    if scope.in_scope() or scope.in_trigger_scope():
        return

    if not (is_tracked(left) or is_tracked(right)):
        return

    with scope.contrast_scope(), scope.propagation_scope():
        propagation_func(result, left, result, (right,), {})


def populate_rewritten_functions(dest):
    for function in [
        contrast__add,
        contrast__append,
        contrast__fstring,
        contrast__cformat__modulo,
    ]:
        dest.setdefault(function.__name__, function)

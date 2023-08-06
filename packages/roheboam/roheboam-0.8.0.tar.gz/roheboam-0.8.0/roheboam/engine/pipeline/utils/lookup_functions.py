from tempfile import TemporaryDirectory


def return_boolean(boolean):
    return boolean


def return_negated_boolean(boolean):
    return not boolean


# def partially_construct(fn, **kwargs):
#     return partial(fn, **kwargs)


# def turn_first_arg_into_kwargs(fn):
#     def inner_fn(*args, **kwargs):
#         return fn(fn=kwargs["fn"], kwargs=args[0])

#     return inner_fn


# @turn_first_arg_into_kwargs
# def spread_arguments_before_call(fn, kwargs):
#     return fn(**kwargs)


# def function_composer(fns):
#     def wrapper(arg):
#         for fn in fns:
#             arg = fn(arg)
#         return arg

#     return wrapper


def create_temp_path():
    return TemporaryDirectory().name


lookup = {
    "return_boolean": return_boolean,
    "return_negated_boolean": return_negated_boolean,
    # "partially_construct": partially_construct,
    # "spread_arguments_before_call": spread_arguments_before_call,
    # "function_composer": function_composer,
    "create_temp_path": create_temp_path,
}

from jax import custom_vjp


def identity(function):
    wrapper = custom_vjp(function)

    def forward(*args, **kwargs):
        return function(*args, **kwargs), None

    def backward(_, gradient):
        return (gradient,)

    wrapper.defvjp(forward, backward)
    return wrapper

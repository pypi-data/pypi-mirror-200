from multipledispatch import dispatch
from jax.numpy import clip as clip_function
from jax import custom_vjp


@dispatch(object, object, object)
def clip(function, minimum, maximum):
    wrapper = custom_vjp(function)

    def forward(*args, **kwargs):
        return function(*args, **kwargs), None

    def backward(_, gradient):
        return (clip_function(gradient, minimum, maximum),)

    wrapper.defvjp(forward, backward)
    return wrapper


@dispatch(object, object)
def clip(function, maximum):
    return clip(function, -maximum, maximum)

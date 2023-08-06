# onionizer

[![PyPI - Version](https://img.shields.io/pypi/v/onionizer.svg)](https://pypi.org/project/onionizer)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/onionizer.svg)](https://pypi.org/project/onionizer)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)


## Introduction

Onionizer is a library that allows you to wrap a function with a list of middlewares. 

```python
import onionizer
new_func = onionizer.wrap_around(func, [middleware1, middleware2])
```
More complete example later.

## Motivation


Onionizer is inspired by the onion model of middlewares in web frameworks such as Django, Flask and FastAPI.

If you are into web developpement, you certainly found this pattern very convenient as you plug middlewares to your application to add features such as authentication, logging, etc.

**Why not generalize this pattern to any function ? That's what Onionizer does.**

Hopefully, it could nudge communities share code more easily when they are using extensively the same specific API. Yes, I am looking at you `openai.ChatCompletion.create`.

# Installation

```bash
pip install onionizer
```
no external dependencies

## Usage

```python
import onionizer
def func(x, y):
    return x + y

def middleware1(x, y):
    result = yield (x+1, y+1), {}  # yield the new arguments and keyword arguments ; obtain the result
    return result # Do nothing with the result

def middleware2(x, y):
    result = yield (x, y), {}  # arguments are not preprocessed by this middleware
    return result*2 # double the result

wrapped_func = onionizer.wrap_around(func, [middleware1, middleware2])
result = wrapped_func(0, 0)

assert result == 2
```

Tracing the execution layers by layers :
- `middleware1` is called with arguments `(0, 0)` ; it yields the new arguments `(1, 1)` and keyword arguments `{}` 
- `middleware2` is called with arguments `(1, 1)` ; it yields the new arguments `(1, 1)` and keyword arguments `{}` (unchanged)
- `wrapped_func` calls `func` with arguments `(1, 1)` which returns `2`
- `middleware2` returns `4`
- `middleware1` returns `4` (unchanged)

Alternatively, you can use the decorator syntax :
```python
@onionizer.decorate([middleware1, middleware2])
def func(x, y):
    return x + y
```

## Features

- support for normal function if you only want to preprocess arguments or postprocess results
- support for context managers out of the box. Use this to handle resources or exceptions (try/except around the yield statement wont work for the middlewares)
- simplified preprocessing of arguments using `PositionalArgs` and `KeywordArgs` to match your preferred style or onionizer.UNCHANGED (see below)


## WTF, did you reinvent decorators?

### Flexibilty is good, until it's not

Chances are, if asked to add behavior before and after a function, you would use decorators. 
And that's fine! Decorators are awesome and super flexible. But in the programming world, flexibility can also be a weakness. 

Onionizer middlewares are more constrained, but they are also more predictable. 
A middleware that do not share the exact same signature as the wrapped function will raise an error at wrapping time.
The coroutine syntax is also more explicit than the decorator syntax, once used to it, it is easier to 'wrap your head around it'

### Comparison with decorators

Let's take a look at the following example :

```python
import functools
def ensure_that_total_discount_is_acceptable(func):
    @functools.wraps(func)
    def wrapper(original_price, context):
        result = func(original_price, context)
        if original_price/result > 0.5:
            raise ValueError("Total discount is too high")
        return result
    return wrapper

@ensure_that_total_discount_is_acceptable
def discount_function(original_price, context):
    ...
```
Using onionizer, the same behavior can be achieved with the following code :
```python
import onionizer
def ensure_that_total_discount_is_acceptable(original_price, context):
    result = yield onionizer.UNCHANGED
    if original_price/result > 0.5:
        raise ValueError("Total discount is too high")
    return result

@onionizer.decorate([ensure_that_total_discount_is_acceptable])
def discount_function(original_price: int, context: dict) -> int:
    ...
```
It's more concise as there is no need to define and return a wrapper function (while keeping in mind to use `functools.wraps` to preserve the docstring and the signature of the wrapped function).
Yielding `onionizer.UNCHANGED` ensure the reader that the arguments are not modified by the middleware.
If there is an incompatibility of signatures, the middleware will raise an error at wrapping time, whereas the decorator syntax will fail at runtime one day you did not expect.

### Onion middlewares are nice to write, but I want to use it as classical decorators
If you don't want to fully commit to this new approach, you can stop midway and use our compatibility layer.
We got you covered !
```python
import onionizer

@onionizer.as_decorator
def ensure_that_total_discount_is_acceptable(original_price, context):
    result = yield onionizer.UNCHANGED
    if original_price/result > 0.5:
        raise ValueError("Total discount is too high")
    return result

@ensure_that_total_discount_is_acceptable
def discount_function(original_price: int, context: dict) -> int:
    ...
```
This is the perfect use case for mixing onionier middlewares with classical decorators.


## Advanced usage

### PositionalArgs and KeywordArgs

Onionizer provides two classes to simplify the preprocessing of arguments : `PositionalArgs`, `KeywordArgs`.

```python
import onionizer
def func(x, y):
    return x + y

def middleware1(x: int, y: int):
    result = yield onionizer.PositionalArgs(x + 1, y)
    return result

def middleware2(x: int, y: int):
    result = yield onionizer.KeywordArgs({'x': x, 'y': y + 1})
    return result
wrapped_func = onionizer.wrap_around(func, [middleware1, middleware2])
```

## License

`onionizer` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


## Roadmap
- Decorator
- ast parsing to check yield statement validity
- Library
- Support for onionizer.Result
- Raising exception
- logging mode

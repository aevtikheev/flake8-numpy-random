import ast
import pytest

from flake8_numpy_random import Plugin


def results(s):
    return {'{}:{}: {}'.format(*result) for result in Plugin(ast.parse(s)).run()}


@pytest.mark.parametrize(
    'code',
    (
        'import numpy\nnumpy.random()',
        'import os, numpy\nnumpy.random()',
        'import numpy as np\nnp.random()',
        'from numpy import random\nrandom()',
        'from numpy import random as rand\nrand()',
    ),
)
def test_numpy_random_call_prohibited(code):
    assert results(code) == {'2:0: NPR001 do not use numpy.random()'}


@pytest.mark.parametrize(
    'code',
    (
        '',
        'import numpy',
        'import random',
        'from random import random\nrandom()',
        'from random import random as rand\nrand()',
        'import numpy as np\nsomething.np.random()',
    ),
)
def test_correct_code(code):
    assert results(code) == set()

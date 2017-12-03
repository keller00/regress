import os
from regress import which, regress, VERSION, __all__


def test_check_regress_available():
    assert which('regress')

def test_version():
    assert VERSION

def test_all_variable():
    assert __all__


def test_simple_regression(tmpdir):
    testing_string = 'testing\n'
    input_file = tmpdir.join('in1')
    assert input_file.check() is False
    input_file.write(testing_string)
    output_file = tmpdir.join('out1')
    assert output_file.check() is False
    output_file.write(testing_string)
    assert tmpdir.strpath
    assert regress('cat', path=tmpdir.strpath) == []

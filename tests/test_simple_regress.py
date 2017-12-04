import random
from regress import regress, VERSION, __all__
from regress.regress import CommandNotFound, OutputNotFound

def randstring(length=10):
    valid_letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join((random.choice(valid_letters) for i in xrange(length)))

def test_version():
    assert VERSION


def test_all_variable():
    assert __all__


def test_exceptions():
    isinstance(CommandNotFound, Exception)
    isinstance(OutputNotFound, Exception)


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


def test_changed_prefix_regression(tmpdir):
    testing_string = 'testing\n'
    input_file = tmpdir.join('abc1')
    assert input_file.check() is False
    input_file.write(testing_string)
    output_file = tmpdir.join('asd1')
    assert output_file.check() is False
    output_file.write(testing_string)
    assert tmpdir.strpath
    assert regress('cat', in_prefix='abc', out_prefix='asd', path=tmpdir.strpath) == []


def test_command_not_found(tmpdir):
    testing_string = 'testing\n'
    input_file = tmpdir.join('in1')
    assert input_file.check() is False
    input_file.write(testing_string)
    output_file = tmpdir.join('asd1')
    assert output_file.check() is False
    output_file.write(testing_string)
    assert tmpdir.strpath
    try:
        assert regress('somethingnonexistent', in_prefix='abc', out_prefix='asd', path=tmpdir.strpath) == []
    except CommandNotFound:
        pass
    else:
        raise AssertionError


def test_miltiple_files(tmpdir):
    testing_string = 'testing\n'
    input_file = tmpdir.join('in1')
    assert input_file.check() is False
    input_file.write(testing_string)
    output_file = tmpdir.join('asd1')
    assert output_file.check() is False
    output_file.write(testing_string)
    assert tmpdir.strpath
    try:
        assert regress('somethingnonexistent', in_prefix='abc', out_prefix='asd', path=tmpdir.strpath) == []
    except CommandNotFound:
        pass
    else:
        raise AssertionError


def test_missing_output_warning(tmpdir):
    testing_string = 'testing\n'
    input_file = tmpdir.join('in1')
    assert input_file.check() is False
    input_file.write(testing_string)
    try:
        assert regress('cat', path=tmpdir.strpath) == []
    except OutputNotFound:
        raise AssertionError


def test_options(tmpdir):
    testing_string1 = '\t\ttesting\n'
    input_file1 = tmpdir.join('in1')
    assert input_file1.check() is False
    input_file1.write(testing_string1)
    output_file1 = tmpdir.join('out1')
    assert output_file1.check() is False
    output_file1.write('^I^Itesting\n')
    assert regress('cat', path=tmpdir.strpath, error=True, options=['-t']) == []


def test_multiple_tests(tmpdir):
    testing_string1 = randstring(50000)
    testing_string2 = randstring(500000)
    input_file1 = tmpdir.join('in1')
    assert input_file1.check() is False
    input_file1.write(testing_string1)
    input_file2 = tmpdir.join('in2')
    assert input_file2.check() is False
    input_file2.write(testing_string2)
    output_file1 = tmpdir.join('out1')
    assert output_file1.check() is False
    output_file1.write('   50000\n')
    output_file2 = tmpdir.join('out2')
    assert output_file2.check() is False
    output_file2.write('  500000\n')
    assert regress('wc', path=tmpdir.strpath, error=True, options=['-m']) == []

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
    r = regress('cat', path=tmpdir.strpath)
    print r
    assert r == []


def test_changed_prefix_regression(tmpdir):
    testing_string = 'testing\n'
    input_file = tmpdir.join('abc1')
    assert input_file.check() is False
    input_file.write(testing_string)
    output_file = tmpdir.join('asd1')
    assert output_file.check() is False
    output_file.write(testing_string)
    assert tmpdir.strpath
    r = regress('cat', in_prefix='abc', out_prefix='asd', path=tmpdir.strpath)
    print r
    assert r == []


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


def test_cat_options(tmpdir):
    testing_string1 = '\t\ttesting\n'
    input_file1 = tmpdir.join('in1')
    assert input_file1.check() is False
    input_file1.write(testing_string1)
    output_file1 = tmpdir.join('out1')
    assert output_file1.check() is False
    output_file1.write('^I^Itesting\n')
    r = regress('cat', path=tmpdir.strpath, error=True, options=['-t'])
    print r
    assert r == []


def test_awk_options(tmpdir):
    testing_string = 'a\tregress\tb'
    expected_output = 'regress\n'
    input_file1 = tmpdir.join('in1')
    assert input_file1.check() is False
    input_file1.write(testing_string)
    output_file1 = tmpdir.join('out1')
    assert output_file1.check() is False
    output_file1.write(expected_output)
    r = regress('awk', path=tmpdir.strpath, options=['-F', '\t', '{print $2}'])
    print r
    assert r == []


def test_one_fail(tmpdir):
    testing_string = 'testing\n'
    input_file1 = tmpdir.join('in1')
    assert input_file1.check() is False
    input_file1.write(testing_string)
    input_file2 = tmpdir.join('in2')
    assert input_file2.check() is False
    input_file2.write(testing_string)
    output_file1 = tmpdir.join('out1')
    assert output_file1.check() is False
    output_file1.write(testing_string)
    output_file2 = tmpdir.join('out2')
    assert output_file2.check() is False
    output_file2.write(testing_string + 'fail')
    r = regress('cat', path=tmpdir.strpath)
    print r
    assert len(r) == 1
    assert r[0][0].endswith('in2')

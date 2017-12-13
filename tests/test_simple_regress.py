from regress import regress, VERSION, __all__
from regress.regress import CommandNotFound, OutputNotFound


def test_version():
    """ Test that version variable is available """
    assert VERSION


def test_all_variable():
    """ Test if __all__ is available from regress """
    assert __all__


def test_exceptions():
    """ Simple exception inheritance test """
    isinstance(CommandNotFound, Exception)
    isinstance(OutputNotFound, Exception)


def test_simple_regression(tmpdir):
    """ Run simple regress test with cat and 1 input file """
    testing_string = 'testing\n'
    input_file = tmpdir.join('in1')
    assert not input_file.check()
    input_file.write(testing_string)
    output_file = tmpdir.join('out1')
    assert not output_file.check()
    output_file.write(testing_string)
    fails = regress('cat', path=tmpdir.strpath)
    print fails
    assert not fails


def test_changed_prefix_regression(tmpdir):
    """ Simple regress test with modified input and output prefixes """
    testing_string = 'testing\n'
    input_file = tmpdir.join('abc1')
    assert not input_file.check()
    input_file.write(testing_string)
    output_file = tmpdir.join('asd1')
    assert not output_file.check()
    output_file.write(testing_string)
    fails = regress('cat', in_prefix='abc', out_prefix='asd', path=tmpdir.strpath)
    print fails
    assert not fails


def test_command_not_found(tmpdir):
    """ Test command not found exception """
    testing_string = 'testing\n'
    input_file = tmpdir.join('in1')
    assert not input_file.check()
    input_file.write(testing_string)
    output_file = tmpdir.join('asd1')
    assert not output_file.check()
    output_file.write(testing_string)
    try:
        regress('somethingnonexistent', in_prefix='abc', out_prefix='asd', path=tmpdir.strpath)
        raise AssertionError
    except CommandNotFound:
        pass


def test_miltiple_files(tmpdir):
    """ Simple regress test with multiple input files """
    testing_string = 'testing\n'
    input_file = tmpdir.join('in1')
    assert not input_file.check()
    input_file.write(testing_string)
    output_file = tmpdir.join('asd1')
    assert not output_file.check()
    output_file.write(testing_string)
    try:
        regress('somethingnonexistent', in_prefix='abc', out_prefix='asd', path=tmpdir.strpath)
        raise AssertionError
    except CommandNotFound:
        pass


def test_missing_output_warning(tmpdir):
    """ Test missing output file exception """
    input_file = tmpdir.join('in1')
    assert not input_file.check()
    input_file.write('')
    try:
        regress('cat', path=tmpdir.strpath, error=True)
        raise AssertionError
    except OutputNotFound:
        pass


def test_cat_with_non_printing_options(tmpdir):
    """ Test regress passing one extra option/argument to cat """
    testing_string1 = '\t\ttesting\n'
    input_file1 = tmpdir.join('in1')
    assert not input_file1.check()
    input_file1.write(testing_string1)
    output_file1 = tmpdir.join('out1')
    assert not output_file1.check()
    output_file1.write('^I^Itesting\n')
    fails = regress('cat', path=tmpdir.strpath, error=True, options=['-t'])
    print fails
    assert not fails


def test_awk_with_second_column_options(tmpdir):
    """ Test regress passing multiple extra options/arguments to awk """
    testing_string = 'a\tregress\tb'
    expected_output = 'regress\n'
    input_file1 = tmpdir.join('in1')
    assert not input_file1.check()
    input_file1.write(testing_string)
    output_file1 = tmpdir.join('out1')
    assert not output_file1.check()
    output_file1.write(expected_output)
    fails = regress('awk', path=tmpdir.strpath, options=['-F', '\t', '{print $2}'])
    print fails
    assert not fails


def test_one_fail(tmpdir):
    """ Test regress failing 1/2 test and make sure the right one
    failed and the actual output is right """
    testing_string = 'testing\n'
    input_file1 = tmpdir.join('in1')
    assert not input_file1.check()
    input_file1.write(testing_string)
    input_file2 = tmpdir.join('in2')
    assert not input_file2.check()
    input_file2.write(testing_string)
    output_file1 = tmpdir.join('out1')
    assert not output_file1.check()
    output_file1.write(testing_string)
    output_file2 = tmpdir.join('out2')
    assert not output_file2.check()
    output_file2.write(testing_string + 'fail')
    fails = regress('cat', path=tmpdir.strpath)
    print fails
    assert len(fails) == 1
    assert fails[0][0].endswith('in2')
    assert fails[0][1] == testing_string

import pytest

from regress import regress, VERSION, __all__
from regress.regress import CommandNotFound, OutputNotFound
from .compat import on_windows


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
    testing_string = u'testing\n'
    input_file = tmpdir.join(u'in1')
    assert not input_file.check()
    input_file.write(testing_string)
    output_file = tmpdir.join(u'out1')
    assert not output_file.check()
    output_file.write(testing_string)
    fails = regress(u'Get-Content' if on_windows() else u'cat',
                    path=tmpdir.strpath)
    print(fails)
    assert not fails


def test_changed_prefix_regression(tmpdir):
    """ Simple regress test with modified input and output prefixes """
    testing_string = u'testing\n'
    input_file = tmpdir.join(u'abc1')
    assert not input_file.check()
    input_file.write(testing_string)
    output_file = tmpdir.join(u'asd1')
    assert not output_file.check()
    output_file.write(testing_string)
    fails = regress(u'Get-Content' if on_windows() else u'cat',
                    in_prefix=u'abc',
                    out_prefix=u'asd',
                    path=tmpdir.strpath)
    print(fails)
    assert not fails


def test_command_not_found(tmpdir):
    """ Test command not found exception """
    testing_string = u'testing\n'
    input_file = tmpdir.join(u'in1')
    assert not input_file.check()
    input_file.write(testing_string)
    output_file = tmpdir.join(u'asd1')
    assert not output_file.check()
    output_file.write(testing_string)
    try:
        regress(u'somethingnonexistent', in_prefix=u'abc', out_prefix=u'asd', path=tmpdir.strpath)
        raise AssertionError
    except CommandNotFound as err:
        assert(u'somethingnonexistent' in str(err))


def test_multiple_files(tmpdir):
    """ Simple regress test with multiple input files """
    testing_string = u'testing\n'
    input_file = tmpdir.join(u'in1')
    assert not input_file.check()
    input_file.write(testing_string)
    output_file = tmpdir.join(u'asd1')
    assert not output_file.check()
    output_file.write(testing_string)
    try:
        regress(u'somethingnonexistent', in_prefix=u'abc', out_prefix=u'asd', path=tmpdir.strpath)
        raise AssertionError
    except CommandNotFound:
        pass


def test_missing_output_warning(tmpdir):
    """ Test missing output file exception """
    input_file = tmpdir.join(u'in1')
    assert not input_file.check()
    input_file.write(u'')
    try:
        regress(u'Get-Content' if on_windows() else u'cat',
                path=tmpdir.strpath,
                error=True)
        raise AssertionError
    except OutputNotFound:
        pass


def test_cat_with_non_printing_options(tmpdir):
    """ Test regress passing one extra option/argument to cat """
    testing_string1 = u'\t\ttesting\n'
    input_file1 = tmpdir.join(u'in1')
    assert not input_file1.check()
    input_file1.write(testing_string1)
    output_file1 = tmpdir.join(u'out1')
    assert not output_file1.check()
    output_file1.write(u'^I^Itesting\n')
    fails = regress(u'Get-Content' if on_windows() else u'cat',
                    path=tmpdir.strpath,
                    error=True, options=[u'-t'])
    print(fails)
    assert not fails


@pytest.mark.skipif(on_windows(), reason="no awk alternative on Windows")
def test_awk_with_second_column_options(tmpdir):
    """ Test regress passing multiple extra options/arguments to awk """
    testing_string = u'a\tregress\tb'
    expected_output = u'regress\n'
    input_file1 = tmpdir.join(u'in1')
    assert not input_file1.check()
    input_file1.write(testing_string)
    output_file1 = tmpdir.join(u'out1')
    assert not output_file1.check()
    output_file1.write(expected_output)
    fails = regress(u'awk', path=tmpdir.strpath, options=[u'-F', u'\t', u'{print $2}'])
    print(fails)
    assert not fails


def test_one_fail(tmpdir):
    """ Test regress failing 1/2 test and make sure the right one
    failed and the actual output is right """
    testing_string = u'testing\n'
    input_file1 = tmpdir.join(u'in1')
    assert not input_file1.check()
    input_file1.write(testing_string)
    input_file2 = tmpdir.join(u'in2')
    assert not input_file2.check()
    input_file2.write(testing_string)
    output_file1 = tmpdir.join(u'out1')
    assert not output_file1.check()
    output_file1.write(testing_string)
    output_file2 = tmpdir.join(u'out2')
    assert not output_file2.check()
    output_file2.write(testing_string + u'fail')
    fails = regress(u'Get-Content' if on_windows() else u'cat',
                    path=tmpdir.strpath)
    print(fails)
    assert len(fails) == 1
    assert fails[0][0].endswith(u'in2')
    assert fails[0][1] == testing_string

from qtstrap.utils import Builder


def test_string_builder_basic():
    b = Builder()

    b += '1'
    with b:
        b << '2'
        with b:
            b << '3'
    b += '4'

    assert len(b.items) == 4
    assert b.items == [
        '1\n',
        '    2\n',
        '        3\n',
        '4\n',
    ]
    assert b.join() == '1\n    2\n        3\n4\n'


def test_string_builder_custom_output():
    output = []

    b = Builder(output.append)

    b += '1'
    with b:
        b << '2'
        with b:
            b << '3'

    assert len(output) == 3
    assert output == [
        '1\n',
        '    2\n',
        '        3\n',
    ]

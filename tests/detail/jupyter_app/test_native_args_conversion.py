from idact.detail.jupyter_app.native_args_conversion import \
    convert_native_args_from_command_line_to_dict


def test_convert_native_args_from_command_line_to_dict():
    convert = convert_native_args_from_command_line_to_dict

    assert convert(
        native_args=[['--arg1', '--arg2', '--arg3'],
                     ['value1', '123', 'None']]) == {'--arg1': 'value1',
                                                     '--arg2': '123',
                                                     '--arg3': None}

    assert convert(
        native_args=[['--arg1', '--arg2', '--arg1'],
                     ['value1', 'value2', 'value3']]) == {'--arg1': 'value3',
                                                          '--arg2': 'value2'}

    assert convert(
        native_args=[['--arg1', '--arg2', '--arg1'],
                     ['value1', 'value2', 'value3']]) == {'--arg1': 'value3',
                                                          '--arg2': 'value2'}

    assert convert(
        native_args=[['--arg1', '--arg2'],
                     ['value1', 'value2', 'value3']]) == {'--arg1': 'value1',
                                                          '--arg2': 'value2'}

    assert convert(
        native_args=[['--arg1', '--arg2', '--arg3'],
                     ['value1', 'value2']]) == {'--arg1': 'value1',
                                                '--arg2': 'value2'}

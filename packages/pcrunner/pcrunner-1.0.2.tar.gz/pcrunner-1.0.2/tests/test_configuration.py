# tests/test_configuration.py

from io import StringIO

from pcrunner.configuration import (
    read_check_commands,
    read_check_commands_txt,
    read_check_commands_yaml,
)


def test_read_check_commmands_txt_with_extra_lines():
    fd = StringIO(
        '''SERVICE|CHECK_01|check_dummy.py|0 OK -s 0
SERVICE|CHECK_02|check_dummy.py|1 WARNING -s 10

'''
    )
    assert read_check_commands_txt(fd) == [
        {
            'command': 'check_dummy.py 0 OK -s 0',
            'name': 'CHECK_01',
            'result_type': 'PROCESS_SERVICE_CHECK_RESULT',
        },
        {
            'command': 'check_dummy.py 1 WARNING -s 10',
            'name': 'CHECK_02',
            'result_type': 'PROCESS_SERVICE_CHECK_RESULT',
        },
    ]


def test_read_check_commmands_yaml():
    fd = StringIO(
        '''
- name: 'CHECK_01'
  command: 'check_dummy.py 0 OK -s 0'
  result_type: 'PROCESS_SERVICE_CHECK_RESULT'
- name: 'CHECK_02'
  command: 'check_dummy.py 1 WARNING -s 10'
  result_type: 'PROCESS_SERVICE_CHECK_RESULT'
'''
    )
    assert read_check_commands_yaml(fd) == [
        {
            'command': 'check_dummy.py 0 OK -s 0',
            'name': 'CHECK_01',
            'result_type': 'PROCESS_SERVICE_CHECK_RESULT',
        },
        {
            'command': 'check_dummy.py 1 WARNING -s 10',
            'name': 'CHECK_02',
            'result_type': 'PROCESS_SERVICE_CHECK_RESULT',
        },
    ]


def test_read_check_commands_returns_empyt_list():
    assert read_check_commands('/does/not/exists') == []

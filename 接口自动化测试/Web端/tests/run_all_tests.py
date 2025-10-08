

import pytest


def run_tests():
    pytest.main(['test_data_manage.py', 'test_device_manage.py', 'test_home_manage.py', 'test_home_page.py', 'test_system_manage.py'])


if __name__ == "__main__":
    run_tests()
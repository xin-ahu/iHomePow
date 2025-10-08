
# -*- coding: utf-8 -*-

import pytest


def run_tests():
    pytest.main(['test_home_info.py', 'test_home_data.py', 'test_device.py', 'test_data_statistics.py', 'test_mypage.py'])


if __name__ == "__main__":
    run_tests()




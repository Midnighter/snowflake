# -*- coding: utf-8 -*-


from snowflake import Snowflake


def test_main():
    assert isinstance(Snowflake(), object)


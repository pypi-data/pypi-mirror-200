#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `qcarchive_step` package."""

import pytest  # noqa: F401
import qcarchive_step  # noqa: F401


def test_construction():
    """Just create an object and test its type."""
    result = qcarchive_step.QCArchive()
    assert str(type(result)) == "<class 'qcarchive_step.qcarchive.QCArchive'>"

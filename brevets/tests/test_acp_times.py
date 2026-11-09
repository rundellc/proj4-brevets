# tests/test_acp_times.py

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import acp_times
import arrow

def test_open_time_start():
    """0km should open at start time"""
    open_time = acp_times.open_time(0, 200, "2024-01-01T00:00:00+00:00")
    expected = arrow.get("2024-01-01T00:00:00+00:00").isoformat()
    assert open_time == expected

def test_open_time_50km():
    """50km at 15km/h (34 km/h max): (50/34)*60 = 88.2 min"""
    open_time = acp_times.open_time(50, 200, "2024-01-01T00:00:00+00:00")
    expected = arrow.get("2024-01-01T01:28:14.117647+00:00").isoformat()
    assert open_time == expected

def test_close_time_50km():
    """50km at 15km/h min speed: (50/15)*60 = 200 min = 3:20"""
    close_time = acp_times.close_time(50, 200, "2024-01-01T00:00:00+00:00")
    expected = arrow.get("2024-01-01T03:20:00+00:00").isoformat()
    assert close_time == expected

def test_open_time_200km():
    """200km finish: (200/34)*60 = 352.9 minutes"""
    open_time = acp_times.open_time(200, 200, "2024-01-01T00:00:00+00:00")
    expected = arrow.get("2024-01-01T05:52:56.470588+00:00").isoformat()
    assert open_time == expected

def test_invalid_brevet_distance():
    """Should reject invalid brevet distances"""
    try:
        acp_times.open_time(100, 250, "2024-01-01T00:00:00+00:00")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_control_exceeds_brevet():
    """Should reject control distance > brevet distance"""
    try:
        acp_times.open_time(250, 200, "2024-01-01T00:00:00+00:00")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

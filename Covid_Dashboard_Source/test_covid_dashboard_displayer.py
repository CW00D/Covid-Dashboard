"""This module tests the covid_dashboard_displayer module"""

from covid_dashboard_displayer import caluclate_time_for_update
from covid_dashboard_displayer import create_new_update
from covid_dashboard_displayer import remove_updates
from covid_dashboard_displayer import restore_state

def test_caluclate_time_for_update():
    """
        Tests the calculate time for update function
    """
    data = caluclate_time_for_update("12:30")
    assert isinstance(data, int), "Expected integer"
    assert data>=0, "Expected positive integer"
    assert data<=86400, "Expected smaller than 86400"

def test_create_new_update():
    """
        Tests the create new update function
    """
    test_update = {"update_name":"Test_Update", "update_time":"12:30", "update_repeat":True, "covid_update":True, "news_update":True}
    create_new_update(test_update), "Create new update is broken"

def test_remove_updates():
    """
        Tests the remove updates function
    """
    try:
        remove_updates({"title":"Test_Update", "content":"Content", "repeat":True, "covid_update":True, "news_update":True})
    except ValueError:
        pass
    except:
        remove_updates({"title":"Test_Update", "content":"Content", "repeat":True, "covid_update":True, "news_update":True})

def test_restore_state():
    """
        Tests the restore state function
    """
    restore_state(), "Restore state is broken"

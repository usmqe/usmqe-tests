# -*- coding: utf8 -*-


def close_extra_windows(view):
    """
    Close all windows/tabs except for the very first one.
    """
    while len(view.browser.selenium.window_handles) > 1:
        view.browser.selenium.close()
        view.browser.selenium.switch_to.window(view.browser.selenium.window_handles[-1])


def bricks_displayed(view, bricks_count, part_id):
    """
    Return True if parent's bricks_count attribute equals "0"
    or the first brick's health is visible. Return False otherwise.
    column_number should be 0 for host bricks view and 1 for volume bricks view.
    """
    if bricks_count == "0":
        return True
    elif part_id is None:
        return len(view.bricks.row()[0].browser.elements(".//span[@uib-tooltip]")) == 1
    else:
        return len(view.volume_parts(part_id).bricks.row()[1].
                   browser.elements(".//span[@uib-tooltip]")) == 1

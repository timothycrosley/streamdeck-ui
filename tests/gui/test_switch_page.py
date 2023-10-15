from PySide6.QtCore import Qt
from PySide6.QtWidgets import QToolButton


def test_not_switch_to_invalid_page(qtbot, api_and_window, mocker):
    main_window, api = api_and_window

    # behave like the streamdeck is active
    api.reset_dimmer = mocker.MagicMock()
    api.reset_dimmer.return_value = False

    set_page_spy = mocker.spy(api, "set_page")
    get_pages_spy = mocker.spy(api, "get_pages")

    # select a deck button
    buttons = main_window.ui.pages.widget(0).deck_buttons.findChildren(QToolButton)
    qtbot.mouseClick(buttons[0], Qt.LeftButton)

    # write a non-existent switch_page
    tab = main_window.ui.button_states.widget(0)
    for child in tab.button_form.children():
        if child.objectName() == "switch_page":
            child.setValue(999)
    deck_id = tab.property("deck_id")
    page_id = tab.property("page_id")
    button_id = tab.property("button_id")

    # confirm that the state was set
    assert api.get_button_switch_page(deck_id, page_id, button_id) == 999

    # emulate a button press
    api.streamdeck_keys.key_pressed.emit(deck_id, button_id, True)

    # confirm the validation was called using get_pages
    get_pages_spy.assert_called_once()

    # confirm the page was not changed
    set_page_spy.assert_not_called()


def test_switch_to_valid_page(qtbot, api_and_window, mocker):
    main_window, api = api_and_window

    # behave like the streamdeck is active
    api.reset_dimmer = mocker.MagicMock()
    api.reset_dimmer.return_value = False

    set_page_spy = mocker.spy(api, "set_page")
    get_pages_spy = mocker.spy(api, "get_pages")

    # select a deck button
    buttons = main_window.ui.pages.widget(0).deck_buttons.findChildren(QToolButton)
    qtbot.mouseClick(buttons[0], Qt.LeftButton)

    # write a non-existent switch_page
    tab = main_window.ui.button_states.widget(0)
    for child in tab.button_form.children():
        if child.objectName() == "switch_page":
            child.setValue(1)
    deck_id = tab.property("deck_id")
    page_id = tab.property("page_id")
    button_id = tab.property("button_id")

    # confirm that the state was set
    assert api.get_button_switch_page(deck_id, page_id, button_id) == 1

    # emulate a button press
    api.streamdeck_keys.key_pressed.emit(deck_id, button_id, True)

    # confirm the validation was called using get_pages
    get_pages_spy.assert_called_once()

    # confirm the page was not changed
    set_page_spy.assert_called_once()

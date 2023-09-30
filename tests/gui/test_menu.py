def test_file_import(qtbot, api_and_window):
    """Test the file import menu item calls the underline logic."""
    main_window, api = api_and_window
    main_window.ui.actionImport.trigger()
    qtbot.waitUntil(api.import_config.assert_called_once)


def test_file_export(qtbot, api_and_window):
    """Test the file export menu item calls the underline logic."""
    main_window, api = api_and_window

    main_window.ui.actionExport.trigger()
    qtbot.waitUntil(api.export_config.assert_called_once)


def test_help_documentation(qtbot, mock_desktop_services_open_url, api_and_window):
    """Test the help documentation menu item calls the underline logic."""
    main_window, api = api_and_window
    main_window.ui.actionDocs.trigger()
    qtbot.waitUntil(mock_desktop_services_open_url.assert_called_once)


def test_help_github(qtbot, mock_desktop_services_open_url, api_and_window):
    """Test the help GitHub menu item calls the underline logic."""
    main_window, api = api_and_window
    main_window.ui.actionGithub.trigger()
    qtbot.waitUntil(mock_desktop_services_open_url.assert_called_once)


def test_help_about(qtbot, mock_message_box_about, api_and_window):
    """Test the help about menu item calls the underline logic."""
    main_window, api = api_and_window
    main_window.ui.actionAbout.trigger()
    qtbot.waitUntil(mock_message_box_about.assert_called_once)

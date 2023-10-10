from copy import deepcopy


def test_set_default_state__no_change(api_server, streamdeck_type, streamdeck_serial):
    default_state = deepcopy(api_server.state)
    api_server.set_default_state(streamdeck_serial, streamdeck_type)
    assert api_server.state == default_state


def test_set_default_state__set_type_config(api_server, streamdeck_type, streamdeck_serial):
    new_serial = "UNKNOWN_SERIAL"
    default_state = deepcopy(api_server.state)
    api_server.set_default_state(new_serial, streamdeck_type)
    assert new_serial != streamdeck_serial
    assert api_server.state != default_state
    assert api_server.state[new_serial] != api_server.state[streamdeck_serial]
    assert api_server.state[new_serial] == api_server.state[streamdeck_type]

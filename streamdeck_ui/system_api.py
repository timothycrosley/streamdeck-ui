import dbus


class SystemApi:

    def __init__(self):
        self.bus = dbus.SystemBus()

    def get_is_system_locked(self) -> bool:
        login1 = self.bus.get_object('org.freedesktop.login1',
                                 '/org/freedesktop/login1/session/auto')
        properties_interface = dbus.Interface(login1, 'org.freedesktop.DBus.Properties')
        session_properties = properties_interface.GetAll('org.freedesktop.login1.Session')
        system_is_locked = session_properties.get('LockedHint')

        return bool(system_is_locked)
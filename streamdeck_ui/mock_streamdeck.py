from StreamDeck.Devices import StreamDeck


class StreamDeckMock(StreamDeck.StreamDeck):
    """
    Represents a physically attached StreamDeck Original device.
    """

    KEY_COUNT = 24
    KEY_COLS = 6
    KEY_ROWS = 4

    KEY_PIXEL_WIDTH = 72
    KEY_PIXEL_HEIGHT = 72
    KEY_IMAGE_FORMAT = "BMP"
    KEY_FLIP = (True, True)
    KEY_ROTATION = 0

    DECK_TYPE = "Stream Deck Original"

    IMAGE_REPORT_LENGTH = 8191
    IMAGE_REPORT_HEADER_LENGTH = 16

    # fmt: off
    # 72 x 72 black BMP
    BLANK_KEY_IMAGE = [
        0x42, 0x4d, 0xf6, 0x3c, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x36, 0x00, 0x00, 0x00, 0x28, 0x00,
        0x00, 0x00, 0x48, 0x00, 0x00, 0x00, 0x48, 0x00,
        0x00, 0x00, 0x01, 0x00, 0x18, 0x00, 0x00, 0x00,
        0x00, 0x00, 0xc0, 0x3c, 0x00, 0x00, 0xc4, 0x0e,
        0x00, 0x00, 0xc4, 0x0e, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ] + [0] * (KEY_PIXEL_WIDTH * KEY_PIXEL_HEIGHT * 3)
    # fmt: on

    def _convert_key_id_origin(self, key):
        """
        Converts a key index from or to a origin at the physical top-left of
        the StreamDeck device.

        :param int key: Index of the button with either a device or top-left origin.

        :rtype: int
        :return: Key index converted to the opposite key origin (device or top-left).
        """

        key_col = key % self.KEY_COLS
        return (key - key_col) + ((self.KEY_COLS - 1) - key_col)

    def _read_key_states(self):
        """
        Reads the key states of the StreamDeck. This is used internally by
        :func:`~StreamDeck._read` to talk to the actual device.

        :rtype: list(bool)
        :return: Button states, with the origin at the top-left of the deck.
        """

        return None

    def __del__(self):
        """
        Delete handler for the StreamDeck, automatically closing the transport
        if it is currently open and terminating the transport reader thread.
        """
        pass

        # states = self.device.read(1 + self.KEY_COUNT)
        # if states is None:
        #     return None

        # states = states[1:]
        # return [bool(states[s]) for s in map(self._convert_key_id_origin, range(self.KEY_COUNT))]

    def open(self):
        """
        Opens the device for input/output. This must be called prior to setting
        or retrieving any device state.

        .. seealso:: See :func:`~StreamDeck.close` for the corresponding close method.
        """
        # self.device.open()
        # self._reset_key_stream()
        # self._setup_reader(self._read)

    def close(self):
        """
        Closes the device for input/output.

        .. seealso:: See :func:`~StreamDeck.open` for the corresponding open method.
        """
        pass

    def is_open(self):
        """
        Indicattes if the StreamDeck device is currently open and ready for use..

        :rtype: bool
        :return: `True` if the deck is open, `False` otherwise.
        """
        return True

    def connected(self):
        """
        Indicates if the physical StreamDeck device this instance is attached to
        is still connected to the host.

        :rtype: bool
        :return: `True` if the deck is still connected, `False` otherwise.
        """
        return True

    def id(self):
        """
        Retrieves the physical ID of the attached StreamDeck. This can be used
        to differentiate one StreamDeck from another.

        :rtype: str
        :return: Identifier for the attached device.
        """
        return "/dev/dummy"

    def _reset_key_stream(self):
        """
        Sends a blank key report to the StreamDeck, resetting the key image
        streamer in the device. This prevents previously started partial key
        writes that were not completed from corrupting images sent from this
        application.
        """

        payload = bytearray(self.IMAGE_REPORT_LENGTH)
        payload[0] = 0x02
        # self.device.write(payload)

    def reset(self):
        """
        Resets the StreamDeck, clearing all button images and showing the
        standby image.
        """

        payload = bytearray(17)
        payload[0:2] = [0x0B, 0x63]
        # self.device.write_feature(payload)

    def set_brightness(self, percent):
        """
        Sets the global screen brightness of the StreamDeck, across all the
        physical buttons.

        :param int/float percent: brightness percent, from [0-100] as an `int`,
                                  or normalized to [0.0-1.0] as a `float`.
        """

        print(f"Dummy brightness changed to: {percent}")
        if isinstance(percent, float):
            percent = int(100.0 * percent)

        percent = min(max(percent, 0), 100)

        payload = bytearray(17)
        payload[0:6] = [0x05, 0x55, 0xAA, 0xD1, 0x01, percent]
        # self.device.write_feature(payload)

    def get_serial_number(self):
        """
        Gets the serial number of the attached StreamDeck.

        :rtype: str
        :return: String containing the serial number of the attached device.
        """

        # serial = self.device.read_feature(0x03, 17)
        # return self._extract_string(serial[5:])
        return "FAKE"

    def get_firmware_version(self):
        """
        Gets the firmware version of the attached StreamDeck.

        :rtype: str
        :return: String containing the firmware version of the attached device.
        """

        # version = self.device.read_feature(0x04, 17)
        # return self._extract_string(version[5:])
        return "1.0"

    def set_key_image(self, key, image):
        """
        Sets the image of a button on the StreamDeck to the given image. The
        image being set should be in the correct format for the device, as an
        enumerable collection of bytes.

        .. seealso:: See :func:`~StreamDeck.get_key_image_format` method for
                     information on the image format accepted by the device.

        :param int key: Index of the button whose image is to be updated.
        :param enumerable image: Raw data of the image to set on the button.
                                 If `None`, the key will be cleared to a black
                                 color.
        """

    pass

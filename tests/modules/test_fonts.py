import json

from streamdeck_ui.modules.fonts import reorder_font_styles


def test_reorder():
    # fmt: off
    test_fonts_1 = {
        "Font1": {
            "Regular": "path_regular.ttf",
            "A": "path_A.ttf",
            "a": "path_a.ttf",
            "B": "path_B.ttf",
            "Italic": "path_italic.ttf"
        },
        "Font2": {
            "x": "path_x.ttf",
            "Bold": "path_bold.ttf",
            "Bold Italic": "path_bold_italic.ttf",
            "Italic": "path_italic.ttf"
        },
        "Font3": {
            "Regular": "path_regular.ttf",
            "Bold": "path_bold.ttf",
            "Italic": "path_italic.ttf",
            "Bold Italic": "path_bold_italic.ttf"
        }
    }
    expected_fonts_1 = {
        "Font1": {
            "Regular": "path_regular.ttf",
            "Italic": "path_italic.ttf",
            "A": "path_A.ttf",
            "B": "path_B.ttf",
            "a": "path_a.ttf"
        },
        "Font2": {
            "Bold": "path_bold.ttf",
            "Italic": "path_italic.ttf",
            "Bold Italic": "path_bold_italic.ttf",
            "x": "path_x.ttf"
        },
        "Font3": {
            "Regular": "path_regular.ttf",
            "Bold": "path_bold.ttf",
            "Italic": "path_italic.ttf",
            "Bold Italic": "path_bold_italic.ttf"
        }
    }
    # fmt: on
    test_fonts_1_sorted = reorder_font_styles(test_fonts_1)
    assert json.dumps(test_fonts_1_sorted) == json.dumps(expected_fonts_1)

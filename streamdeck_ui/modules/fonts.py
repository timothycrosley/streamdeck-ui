"""Adds support for handling system fonts in Linux"""
import os
import re
import subprocess  # nosec B404
from typing import Tuple

from PIL import ImageFont

from streamdeck_ui.config import DEFAULT_FONT, DEFAULT_FONT_SIZE, FONTS_FALLBACK_PATH

FONT_LANGUAGE = "en"  # Change this to your desired font language code
SHOW_ALL_LANGUAGES = False  # Set to True to show all languages


def get_fonts():
    """Populates a font dictionary in the form: font_dictionary[font_family][font_style] = font_file"""
    system_fonts_dict = get_system_fonts()
    fallback_fonts_dict = get_fallback_fonts()
    if len(system_fonts_dict) == 0:
        return reorder_font_styles(fallback_fonts_dict)
    else:
        # check if fallback/default fonts are in system fonts, if not add them
        for fallback_font_family in fallback_fonts_dict:
            if fallback_font_family in system_fonts_dict.keys():
                for fallback_font_style in fallback_fonts_dict[fallback_font_family].keys():
                    if fallback_font_style not in system_fonts_dict[fallback_font_family].keys():
                        fallback_font_file = fallback_fonts_dict[fallback_font_family][fallback_font_style]
                        system_fonts_dict[fallback_font_family][fallback_font_style] = fallback_font_file
            else:
                system_fonts_dict[fallback_font_family] = fallback_fonts_dict[fallback_font_family]
        return reorder_font_styles(system_fonts_dict)


def get_system_fonts():
    fonts_dict = {}
    try:
        fclist_locations = [
            "/usr/bin/fc-list",
            "/usr/sbin/fc-list",
            "/bin/fc-list",
            "/usr/local/sbin/fc-list",
            "/usr/local/bin/fc-list",
        ]
        fclist_path = None
        for file_path in fclist_locations:
            if os.path.exists(file_path):
                fclist_path = file_path
                break
        if fclist_path is None:
            raise FileNotFoundError
    except FileNotFoundError:
        print("The 'fc-list' command is not available on your system. Using fallback fonts.")
    else:
        # Construct the fc-list command with language and columns for family, style, and file information
        # including pixel size and then restricting len(font_data)==3 allows us to throw away some fonts that won't work with pillow
        arg_language = ":"
        if not SHOW_ALL_LANGUAGES:
            if is_valid_language_code(FONT_LANGUAGE):
                arg_language = ":lang=" + FONT_LANGUAGE
        fclist_command = [fclist_path, arg_language, "file", "family", "style", "pixelsize"]
        result = subprocess.run(fclist_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)  # nosec B603
        if result.returncode != 0:
            print("Error executing fc-list command: ", result.stderr)
            return fonts_dict
        # Split the output into lines
        lines = result.stdout.split("\n")
        # Extract the font family, style, and file information from each line
        for line in lines:
            if line.strip():
                font_data = line.split(":")
                # Every font has a file/family/style, since we also request pixel size in fc-list restricting len(font_data)==3
                # means we will throw away any fonts that specify a pixel size
                if len(font_data) == 3:
                    font_file = font_data[0].strip()
                    try:
                        ImageFont.truetype(font_file, DEFAULT_FONT_SIZE)
                    except OSError:
                        print("Pillow cannot render font... skipping: " + font_file)
                    else:
                        # Occasionally fc-list will return multiple font families/styles per font file (comma separated)
                        # Reversing font family and then taking the first item aligns best with my expectations given the font file name
                        font_family = font_data[1].strip().split(",")[::-1][0]
                        # Font style aligns best with my expectations if it is not reversed
                        font_style = font_data[2].strip().replace("style=", "").split(",")[0]
                        if font_family not in fonts_dict:
                            fonts_dict[font_family] = {font_style: font_file}
                        elif font_family in fonts_dict and font_style not in fonts_dict[font_family]:
                            fonts_dict[font_family][font_style] = font_file

        fonts_dict = dict(sorted(fonts_dict.items()))
    return fonts_dict


def get_fallback_fonts():
    """Populate a font dictionary with the fallback fonts if their file names are in the style: FontFamily-FontStyle.ttf"""
    fonts_dict = {}
    # Define a regular expression pattern to split the font style by camel case
    pattern = re.compile(r"(?<=[a-z])(?=[A-Z])")
    font_files = os.listdir(FONTS_FALLBACK_PATH)

    for font_file in font_files:
        if font_file.endswith((".ttf", ".otf")):
            parts = font_file.split("-")
            # Extract font name and style and add dictionary entry
            if len(parts) == 2:
                font_family, extension = parts
                font_style = extension.split(".")[0]
                # Split the font style by camel case and add spaces
                font_style_parts = pattern.split(font_style)
                font_style = " ".join(font_style_parts)

                if font_family not in fonts_dict:
                    fonts_dict[font_family] = {}
                fonts_dict[font_family][font_style] = os.path.join(FONTS_FALLBACK_PATH, font_file)
    return fonts_dict


def reorder_font_styles(fonts_dict):
    """Reorders the font styles in the desired order, with those not specified remaining at the end in alphabetical order"""
    desired_order = ["Regular", "Bold", "Italic", "Bold Italic"]
    for font_family, font_styles in fonts_dict.items():
        reordered = {
            font_style: fonts_dict[font_family][font_style] for font_style in desired_order if font_style in font_styles
        }
        for font_style, font_file in sorted(font_styles.items()):
            if font_style not in desired_order:
                reordered[font_style] = font_file
        fonts_dict[font_family] = reordered
    return fonts_dict


def is_valid_language_code(code):
    # Use a regular expression to check if the code is RFC-3066 compliant
    return re.match(r"^[a-zA-Z]{2}(-[a-zA-Z0-9]+)*$", code) is not None


def find_font_info(target_font_file: str) -> Tuple[str, str]:
    """Returns the font family and font style for a given font file path"""
    # The font file path is the font attribute that is stored in the .streamdeck_ui.json
    # we need the family/style for selecting the appropriate items in the combo boxes
    if target_font_file == "":
        target_font_file = DEFAULT_FONT
    for font_family, font_styles in FONTS_DICT.items():
        for font_style, font_file in font_styles.items():
            if font_file.endswith(target_font_file):
                return font_family, font_style
    return find_font_info(DEFAULT_FONT)


FONTS_DICT = get_fonts()
DEFAULT_FONT_FAMILY, DEFAULT_FONT_STYLE = find_font_info(DEFAULT_FONT)

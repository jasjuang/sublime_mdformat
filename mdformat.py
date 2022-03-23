#
# mdformat.py
# Autoformatter for Markdown files
#
# Written by Jason Juang,,,
# Copyright (c) 2022 Jason Juang,,,
#
# License: MIT
#

"""This module applies mdformat in sublime."""

import sublime
import sublime_plugin
import subprocess
import os

# Settings file locations.
settings_file = 'mdformat.sublime-settings'
custom_style_settings = 'mdformat_custom.sublime-settings'

st_encodings_trans = {
    "UTF-8": "utf-8",
    "UTF-8 with BOM": "utf-8-sig",
    "UTF-16 LE": "utf-16-le",
    "UTF-16 LE with BOM": "utf-16",
    "UTF-16 BE": "utf-16-be",
    "UTF-16 BE with BOM": "utf-16",
    "Western (Windows 1252)": "cp1252",
    "Western (ISO 8859-1)": "iso8859-1",
    "Western (ISO 8859-3)": "iso8859-3",
    "Western (ISO 8859-15)": "iso8859-15",
    "Western (Mac Roman)": "mac-roman",
    "DOS (CP 437)": "cp437",
    "Arabic (Windows 1256)": "cp1256",
    "Arabic (ISO 8859-6)": "iso8859-6",
    "Baltic (Windows 1257)": "cp1257",
    "Baltic (ISO 8859-4)": "iso8859-4",
    "Celtic (ISO 8859-14)": "iso8859-14",
    "Central European (Windows 1250)": "cp1250",
    "Central European (ISO 8859-2)": "iso8859-2",
    "Cyrillic (Windows 1251)": "cp1251",
    "Cyrillic (Windows 866)": "cp866",
    "Cyrillic (ISO 8859-5)": "iso8859-5",
    "Cyrillic (KOI8-R)": "koi8-r",
    "Cyrillic (KOI8-U)": "koi8-u",
    "Estonian (ISO 8859-13)": "iso8859-13",
    "Greek (Windows 1253)": "cp1253",
    "Greek (ISO 8859-7)": "iso8859-7",
    "Hebrew (Windows 1255)": "cp1255",
    "Hebrew (ISO 8859-8)": "iso8859-8",
    "Nordic (ISO 8859-10)": "iso8859-10",
    "Romanian (ISO 8859-16)": "iso8859-16",
    "Turkish (Windows 1254)": "cp1254",
    "Turkish (ISO 8859-9)": "iso8859-9",
    "Vietnamese (Windows 1258)":  "cp1258",
    "Hexadecimal": None,
    "Undefined": None
}


# Check if we are running on a Windows operating system
os_is_windows = os.name == 'nt'


# The default name of the mdformat executable
default_binary = 'mdformat.exe' if os_is_windows else 'mdformat'


def which(program):
    """http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python."""

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def set_path(path):
    """Set the path to the binary in the settings file."""

    settings = sublime.load_settings(settings_file)
    settings.set('binary', path)
    sublime.save_settings(settings_file)
    # Make sure the globals are updated.
    load_settings()


def update_path():
    """Display input panel to update the path."""

    load_settings()
    w = sublime.active_window()
    w.show_input_panel("Path to mdformat: ", binary, set_path, None, None)


def check_binary():
    """Check that the binary can be found and is executable."""

    # If we couldn't find the binary.
    if (which(binary) is None):
        # Try to guess the correct setting.
        if (which(default_binary) is not None):
            # Looks like mdformat is in the path, remember that.
            set_path(default_binary)
            return True
        # We suggest setting a new path using an input panel.
        msg = "The mdformat binary was not found. Set a new path?"
        if sublime.ok_cancel_dialog(msg):
            update_path()
            return True
        else:
            return False
    return True


def load_settings():
    """Load settings and put their values into global scope."""

    # We set these globals.
    global binary
    global format_on_save
    global style
    global wrap
    global number
    global end_of_line
    settings_global = sublime.load_settings(settings_file)
    settings_local = sublime.active_window(
    ).active_view().settings().get('MarkdownFormat', {})

    def load(name, default): return settings_local.get(
        name, settings_global.get(name, default))
    # Load settings, with defaults.
    binary = load('binary', default_binary)
    format_on_save = load('format_on_save', False)
    style = load('style', 'custom')
    wrap = load('wrap', 'keep')
    number = load('number', False)
    end_of_line = load('end_of_line', 'lf')


def is_supported(lang):
    """Check whether the file is Markdown related."""

    load_settings()
    return lang.endswith(('Markdown' + '.tmLanguage', 'Markdown' + '.sublime-syntax'))


class MdformatCommand(sublime_plugin.TextCommand):
    """Triggered when the user runs markdown format."""

    def run(self, edit):
        """Entry point for sublime to call this."""

        load_settings()

        if not check_binary():
            return

        # The below code has been taken and tweaked from llvm.
        encoding = st_encodings_trans[self.view.encoding()]
        if encoding is None:
            encoding = 'utf-8'

        if style == "custom":
            command = [binary,
                       '--wrap', wrap,
                       '--end-of-line', end_of_line]
            if number:
                command.append('--number')

            command.append(str(self.view.file_name()))
        else:
            command = [binary, str(self.view.file_name())]

        print(command)
        startupinfo = None
        if os_is_windows:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                             startupinfo=startupinfo)


class MdformatEventListener(sublime_plugin.EventListener):
    """Hook for on-save event, to allow application of mdformat on save."""

    def on_pre_save(self, view):
        """Check syntax and format on save prior step."""

        # Only do this for supported languages
        syntax = view.settings().get('syntax')
        if is_supported(syntax):
            # Ensure that settings are up to date.
            load_settings()
            if format_on_save:
                print("Auto-applying Markdown Format on save.")
                view.run_command("mdformat")


# Called from the UI to update the path in the settings.
class MdformatSetPathCommand(sublime_plugin.WindowCommand):
    """We can also update the path on the UI."""

    def run(self):
        """Update the path."""

        update_path()

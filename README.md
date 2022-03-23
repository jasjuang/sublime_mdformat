# Sublime Markdown Format

[![Build Status](https://travis-ci.com/jasjuang/sublime_mdformat.svg?branch=main)](https://travis-ci.com/jasjuang/sublime_mdformat)

## What it does

mdformat is a tool for formatting markdown files. This is a
package that allows you to run it easily from within Sublime Text.

## Installing

- This plugin is dependent on [mdformat](https://github.com/executablebooks/mdformat)

To install `mdformat`, do the following:

- Install [Python](http://python.org/download/) and [pip](http://www.pip-installer.org/en/latest/installing.html).

- Install `mdformat` by typing the following in a terminal:

  ```
  [sudo] pip install mdformat
  ```

- Set the path to the mdformat binaries. You can do this from within Sublime
  Text by choosing `Markdown Format - Set Path` from the command palette.  Hint:
  the path should look something like this `/usr/local/bin/mdformat`.
  If mdformat is in your system path, you shouldn't need to do anything.

## Use

- Default shortcut is `ctrl+shift+m`.
  This will apply mdformat to the selection.
- It is possible to run the formatter on every save to a file, change settings
  to `"format_on_save": true`.
- To change settings on a per-package basis, add them under `Markdown Format` key,
  example project.sublime-settings:
- To use style from a file (for example `.mdformat.toml`), change settings to `"style": "File"`. Otherwise `custom` style is used.

```json
{
  "folders": [],
  "settings": {
    "Markdown Format": {
      "style": "File",
      "format_on_save": true
    }
  }
}
```

## If You Liked This

- ... And want to contribute, PR's gladly accepted!

Please note that modifications should follow these coding guidelines:

- Indent is 4 spaces.
- Code should pass flake8 and pep257 linters.
- Vertical whitespace helps readability, don’t be afraid to use it.
- Please use descriptive variable names, no abbreviations unless they are very well known.

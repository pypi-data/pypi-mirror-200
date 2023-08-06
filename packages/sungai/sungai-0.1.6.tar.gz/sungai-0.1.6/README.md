# Sungai

![GitHub](https://img.shields.io/github/license/hugocartwright/sungai)![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/hugocartwright/sungai)![GitHub last commit](https://img.shields.io/github/last-commit/hugocartwright/sungai)
![PyPI](https://img.shields.io/pypi/v/sungai)![PyPI - Implementation](https://img.shields.io/pypi/implementation/sungai)![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sungai)![PyPI - Wheel](https://img.shields.io/pypi/wheel/sungai)![PyPI - Downloads](https://img.shields.io/pypi/dm/sungai)

Sungai is a tool for rating directories. It's great at giving pointers when cleaning up very messy directories.

## Installation

Install with ```pip install sungai```

## Usage

To run sungai on current directory (".")
```sungai .```

The target directory will get a rating between 0.0 and 1.0. The minimum score required for the target directory can also be set with the ```--min_score``` flag. The error count should be 0 for a pass.

```sungai <your_path_string_here> --min_score 1.0 --verbose```

Sungai lists directory paths in descending order of priority.

CAUTION: It is entirely up to the user to rearrange the contents of those directories. Or not.
Example actions include:
- moving them up to their parent directory
- rearranging their files
- grouping their directories into new ones
- ignoring sungai
- altogether deleting the given directories

### Ignore files or directories
An ignore file path can be specified to sungai. The given file should follow the .gitignore syntax.

```sungai <your_path_string_here> --ignore_config .sungai_ignore```


## Contributing
Feel free to drop an issue on the project's github page.

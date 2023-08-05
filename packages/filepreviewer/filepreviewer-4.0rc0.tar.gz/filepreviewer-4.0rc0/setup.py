# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['preview']

package_data = \
{'': ['*']}

install_requires = \
['pymsgbox>=1.0.9,<2.0.0', 'typer>=0.7.0,<0.8.0', 'watchdog>=2.2.1,<3.0.0']

entry_points = \
{'console_scripts': ['preview = preview.__main__:app']}

setup_kwargs = {
    'name': 'filepreviewer',
    'version': '4.0rc0',
    'description': '',
    'long_description': '# Preview\n\n`preview` is a tool for "previewing" files that require a compilatoin step, like LaTeX, Markdown, and more.\nIt works by managing a "build" step and a "view" step, so it can be used to live-preview many different types of files, and if you\nfiletype is not already supported, it is simple to add support for it.\n\n# Usage\n\nInstall with `pip`\n\n```\n$ pip install filepreviewer\n```\n\nto preview a file, just pass it to the `preview` command\n\n```\n$ preview file_to_preview.md\n```\n\n# How it works\n\n`preview` uses a handler to launch a view process in the background, and then run\nbuild process when the source file is changed. For example, the `just` handler can\nuse a justfile like this\n\n<!---begin\ntype = "file include"\nfilename = "doc/examples/justfile.md"\ncode-fence = true\ncode-fence-lang = "make"\n--->\n```make\nPREVIEW_INPUT_FILE := ""\nPREVIEW_TMPDIR:= ""\n\npreview-build:\n    pandoc {{PREVIEW_INPUT_FILE}} -o {{PREVIEW_TMPDIR}}/out.pdf\n\npreview-view:\n    zathura {{PREVIEW_TMPDIR}}/out.pdf\n\n```\n<!---\nend--->\nto preview Markdown files by compiling them to a PDF (using Pandoc) and opening then PDF with Zathura, which does automatic reload.\n\nYou can use any tool(s) you want to build and view your file. The only requirement is that view process _should block_. `preview` will launch it in the background and exit when it returns.\n\n# Examples\n\nTo preview a Gnuplot script you could use [sexpect](https://github.com/clarkwang/sexpect) to open gnuplot and load the script.\n\n<!---begin\ntype = "file include"\nfilename = "doc/examples/justfile.gnuplot"\ncode-fence = true\ncode-fence-lang = "make"\n--->\n```make\nPREVIEW_INPUT_FILE := ""\nPREVIEW_TMPDIR:= ""\n\npreview-build:\n    #! /bin/bash\n    if [[ -e preview-gnuplot.sock ]]\n    then\n      sexpect -sock preview-gnuplot.sock send \'load "{{PREVIEW_INPUT_FILE}}"\' -cr\n      sexpect -sock preview-gnuplot.sock expect\n    fi\n\npreview-view:\n    sexpect -sock preview-gnuplot.sock spawn gnuplot\n    just --justfile {{justfile()}} PREVIEW_INPUT_FILE={{PREVIEW_INPUT_FILE}} PREVIEW_TMPDIR={{PREVIEW_TMPDIR}} preview-build\n    zenity --info --no-markup --text="Click \'OK\' when you are done to close the preview."\n    sexpect -sock preview-gnuplot.sock send \'exit\' -cr\n    sexpect -sock preview-gnuplot.sock wait\n```\n<!---\nend--->\n\nThe use of [Zenity](https://help.gnome.org/users/zenity/stable/) here is\nrequired to keep the view process from returning immediatly, which would cause\npreview to terminate.\n\n# Handlers\n\nCurrently, Preview supports [`just`](https://help.gnome.org/users/zenity/stable/) and\nMake for handing the build and view steps.\n\n### Just handler\n\nTo use the just handler, create a file named `justfile.<file_extension>` that defines\na `preview-build` and `preview-view` recipe, as well as two variables named `PREVIEW_INPUT_FILE` and `PREVIEW_TMPDIR`. Preview will pass the name of the file being previewed, and the path to a temporary directory that is created for the hander to use.\n\n### Make handler\n\nTo use the make handler, create a file named `makefile.<file_extension>` that\ndefines the `preview-build` and `preview-view` targets. Preview will set two variables\nnamed `PREVIEW_INPUT_FILE` and `PREVIEW_TMPDIR` that contain the name of the file being previewed, and the path to a temporary directory that is created for the hander to use.\n',
    'author': 'CD Clark III',
    'author_email': 'clifton.clark@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

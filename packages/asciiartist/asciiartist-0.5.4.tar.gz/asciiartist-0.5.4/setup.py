# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asciiartist']

package_data = \
{'': ['*'], 'asciiartist': ['gen/*']}

install_requires = \
['matplotlib', 'scikit-image', 'tflite-runtime']

setup_kwargs = {
    'name': 'asciiartist',
    'version': '0.5.4',
    'description': "An ascii art generator that's actually good. Does edge detection and selects the most appropriate characters.",
    'long_description': '# Ascii Artist\n\nAn ascii art generator that\'s actually good. \nDoes edge detection and selects the most appropriate characters.\n\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/JuliaPoo/AsciiArtist/main/rsrc/skykid.jpg" alt = "Blue Tit">\n</p>\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/JuliaPoo/AsciiArtist/main//rsrc/bluetit.jpg" alt = "Blue Tit">\n</p>\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/JuliaPoo/AsciiArtist/main//rsrc/niko.jpg" alt = "Niko from oneshot!">\n</p>\n\n## Installing\n\n### Installing with pip:\n\n```\npip install asciiartist\n```\n\n### Installing from wheel:\n\nDownload the wheel file from this project\'s releases and run \n\n```\npip install <path/to/wheel>\n```\n\n## Quick Start\n\n```py\nfrom asciiartist import asciiartist, display_edges\nfrom PIL import Image\n\nimg = Image.open("niko.png")\n\nart, edges = asciiartist(\n    img, # The image!\n    30,  # Number of lines of the output ascii art\n    noise_reduction=2,  # Level of noise reduction (optional)\n    line_weight=1,      # Weight of the lines to draw (optional)\n    text_ratio=2.2      # Height/width ratio of each character (optional)\n)\n\nprint(art) # `art` is a string u can just print\n\n# v Display the result of edge detection. \n#   Good for finetuning params.\ndisplay_edges(edges)\n```\n\n## Build from Source\n\nRun the script `./model/model-gen.py` and build the wheel with `poetry build -f wheel`.\n\n## How it works\n\nRoughly, how _Ascii Artist_ generates the drawings:\n\n1. Run edge detection\n2. Segment the image for each char\n3. Pass each segment through a [CNN](https://en.wikipedia.org/wiki/Convolutional_neural_network) to get the most appropriate character.\n\nThe CNN is trained with distorted images of characters (in font consolas),\ncreated in a way that emulates the output of the edge detection.\n\n## Bye\n\n^-^\n\n```\n                                          __=E.L__      \n                                        >#-=@>@F* `<_   \n                                      _/`@o<FTFC@[_~_.__\n                                   _./`\\_`<__      @@7*`\n                              _,~``      *v `^L_  )(    \n                         _,~^C___ _    ````*@```````    \n                   __,;@"*\'`C` *@@_       _-V           \n               __,@\'^`CC)-[_L-----o,,}<@F--             \n    __,-Ec>C<4@\'C`\'`"-[_,/   _,L-L             ,"       \n -`````          ````                       _-\'         \n                        _   _           __~``           \n                        ``  "<`  _                      \n                              `(V\\_                     \n                                `V(<_                   \n                   _____,,~~<7oEE(@@_Eo@@Fo,            \n       ___,-~-^````               .-.__V)  ,_           \n```',
    'author': 'Julia',
    'author_email': 'julia.poo.poo.poo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JuliaPoo/AsciiArtist',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<=3.9',
}


setup(**setup_kwargs)

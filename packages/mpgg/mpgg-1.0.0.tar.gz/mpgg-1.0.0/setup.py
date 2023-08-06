# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mpgg']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=9.1.0,<10.0.0',
 'pyd2v>=1.3.0,<2.0.0',
 'pymediainfo>=6.0.1,<7.0.0',
 'pymp4>=1.2.0,<2.0.0',
 'vapoursynth>=50']

setup_kwargs = {
    'name': 'mpgg',
    'version': '1.0.0',
    'description': 'Streamlined MPEG-1 and MPEG-2 source loader and helper utility for VapourSynth',
    'long_description': '<p align="center">\n    <a href="https://github.com/rlaphoenix/mpgg">MPGG</a>\n    <br/>\n    <sup><em>Streamlined MPEG-1 and MPEG-2 source loader and helper utility for VapourSynth</em></sup>\n</p>\n\n<p align="center">\n    <a href="https://github.com/rlaphoenix/mpgg/actions/workflows/ci.yml">\n        <img src="https://github.com/rlaphoenix/mpgg/actions/workflows/ci.yml/badge.svg" alt="Build status">\n    </a>\n    <a href="https://python.org">\n        <img src="https://img.shields.io/badge/python-3.8%20%7C%7C%203.10-informational" alt="Python version">\n    </a>\n    <a href="https://vapoursynth.com">\n        <img src="https://img.shields.io/badge/vapoursynth-R58%2B-informational" alt="VapourSynth version">\n    </a>\n    <a href="https://deepsource.io/gh/rlaphoenix/mpgg/?ref=repository-badge">\n        <img src="https://deepsource.io/gh/rlaphoenix/mpgg.svg/?label=active+issues&token=9rxkTrTRXcRYIVl8HjRu2sYX" alt="DeepSource">\n    </a>\n</p>\n\n## Features\n\n- 🎥 Supports MPEG-1 and MPEG-2 Sources\n- 🧠 Understands Mixed-scan Sources\n- 🤖 VFR to CFR (Variable to Constant frame rate)\n- 🛠️ Automatic Frame-indexing using DGIndex\n- ⚙️ Zero-configuration\n- 🧩 Easy installation via PIP/PyPI\n- ❤️ Fully Open-Source! Pull Requests Welcome\n\n## Installation\n\n```shell\n$ pip install mpgg\n```\n\nVoilà 🎉! You now have the `mpgg` package installed, and you can now import it from a VapourSynth script.\n\n### Dependencies\n\nThe following is a list of software that needs to be installed manually. MPGG cannot install these automatically\non your behalf.\n\n#### Software\n\n- [MKVToolnix] (specifically mkvextract) for demuxing MPEG streams from MKV containers.\n- [DGIndex] for automatic frame-indexing of MPEG streams.\n\nMake sure you put them in your current working directory, in the installation directory, or put the directory path in\nyour `PATH` environment variable. If you do not do this then their binaries will not be able to be found.\n\n  [MKVToolNix]: <https://mkvtoolnix.download/downloads.html>\n  [DGIndex]: <https://rationalqm.us/dgmpgdec/dgmpgdec.html>\n\n#### VapourSynth Plugins\n\n- [d2vsource] for loading an indexed DGIndex project file.\n\nThese plugins may be installed using [vsrepo] on Windows, or from a package repository on Linux.\n\n  [d2vsource]: <https://github.com/dwbuiten/d2vsource>\n  [vsrepo]: <https://github.com/vapoursynth/vsrepo>\n\n## Usage\n\nThe following is an example of using MPGG to get a clean CFR Fully Progressive stream from an\nAnimated Mixed-scan VFR DVD-Video source.\n\n```python\nimport functools\n\nfrom mpgg import MPGG\nfrom havsfunc import QTGMC\n\n# load the source with verbose information printed\nmpg = MPGG(r"C:\\Users\\John\\Videos\\animated_dvd_video.mkv", verbose=True)\n\n# recover progressive frames where possible, and show which frames were recovered\nmpg.recover(verbose=True)\n\n# deinterlace any remaining interlaced frames with QTGMC, and show which frames were deinterlaced\nmpg.deinterlace(\n  kernel=functools.partial(QTGMC, Preset="Very Slow", FPSDivisor=2),\n  verbose=True\n)\n\n# convert VFR to CFR by duplicating frames in a pattern\nmpg.ceil()\n\n# get the final clip (you may use the clip in between actions as well)\nclip = mpg.clip\n\n# ...\n\nclip.set_output()\n```\n\nYou can also chain calls! This is the same script but chained,\n\n```python\nimport functools\n\nfrom mpgg import MPGG\nfrom havsfunc import QTGMC\n\n# load MPEG, recover progressive frames, deinterlace what\'s left, and finally VFR to CFR\nclip = MPGG(r"C:\\Users\\John\\Videos\\animated_dvd_video.mkv", verbose=True).\\\n  recover(verbose=True).\\\n  deinterlace(kernel=functools.partial(QTGMC, Preset="Very Slow", FPSDivisor=2), verbose=True).\\\n  ceil().\\\n  clip\n\n# ...\n\nclip.set_output()\n```\n\nThere are more methods not shown here. I recommend taking a look at the MPGG class for further\ninformation, methods, and more.\n\n> __Warning__ Do not copy/paste and re-use these examples. Read each method\'s doc-string information\n> as they each have their own warnings, tips, and flaws that you need to be aware of. For example,\n> recover() shouldn\'t be used on all MPEG sources, floor() shouldn\'t be used with recover(), you\n> may not want to use ceil() if you want to keep encoding as VFR, and such.\n\n## Terminology\n\n| Term           | Meaning                                                                        |\n|----------------|--------------------------------------------------------------------------------|\n| CFR            | Constant frame-rate, the source uses a set frame rate on playback              |\n| VFR            | Variable frame-rate, the source switches frame rate at least once on playback  |\n| Scan           | The technology used to show images on screens, i.e., Interlaced or Progressive |\n| Mixed-scan     | Source with both Progressive and Interlaced frames within the video data       |\n| Frame-indexing | Analyzing a source to index frame/field information for frame-serving          |\n\n## Contributors\n\n<a href="https://github.com/rlaphoenix"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/17136956?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt=""/></a>\n\n## License\n\n© 2021-2023 rlaphoenix — [GNU General Public License, Version 3.0](LICENSE)\n',
    'author': 'rlaphoenix',
    'author_email': 'rlaphoenix@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rlaphoenix/mpgg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

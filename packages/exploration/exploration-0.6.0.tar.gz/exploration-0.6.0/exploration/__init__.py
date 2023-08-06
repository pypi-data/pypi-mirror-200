"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2022-3-11
- Purpose: Represent & process exploration traces of discrete decision
    spaces.

Exploration contains sub-packages for dealing with exploration traces as
sequences of decision graphs (see `exploration.core`) and as journals
(see `exploration.journal`). See ../README.md (or
[https://pypi.org/project/exploration/](https://pypi.org/project/exploration/))
for project README.
"""

__version__ = "0.6.0"

# Imports define what's available when you do `import exploration`
from .core import *  # noqa
from . import core, graphs, display, journal, main  # noqa

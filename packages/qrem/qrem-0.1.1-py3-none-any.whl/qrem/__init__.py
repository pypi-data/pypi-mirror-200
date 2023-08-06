#ORGANIZATION - dont know what is the purpose of this file (MO) - (PP): important for defining initialization for packages/subpackages in python (think of every folder as a package/subpackage, when you import it __init__.py is run)


# [1] read version from installed package and provide in __version__ variable
from importlib.metadata import version
__version__ = version("qrem")


# [2] modules binding for top-level qrem package
# add here anything that should be accesible directly from "qrem.":
# example: if you want "import qrem.core.something.else" module  be available for users as "import qrem.else"
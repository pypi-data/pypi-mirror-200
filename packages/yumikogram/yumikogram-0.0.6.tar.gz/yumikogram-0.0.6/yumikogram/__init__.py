__version__ = "0.0.6"
__license__ = "GNU Lesser General Public License v3.0 (LGPL-3.0)"
__copyright__ = "Copyright (C) 2023-present yumiko-api <https://github.com/yumiko-api>"

from yumikogram.clients import Yumikogram

def yumiko_api():
  print(
     f'Yumikogram Successfully installed Current version of Yumikogram {__version__}' + "\n"
     f'Under {__license__}'
  )


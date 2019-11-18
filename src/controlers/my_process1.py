# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
#
# License: GNU Lesser General Public License v3.0 (LGPLv3)
from src.controlers import process_actions
from src.controlers.util import nebula_process


@nebula_process(process_actions.Process)
def external_function():
    print('hello world!')
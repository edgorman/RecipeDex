
import sys
from io import StringIO
from colorama import Fore

import pytest
from recipedex.log import Log


@pytest.mark.parametrize("verboseness,expected", [
    (
        0,
        [
            Fore.WHITE + "this is the message"
        ]
    ),
    (
        1,
        [
            Fore.LIGHTCYAN_EX + "[INFO]: this is the message",
            Fore.GREEN + "[SUCCESS]: this is the message",
            Fore.RED + "[ERROR]: this is the message",
            Fore.WHITE + "this is the message"
        ]
    )
])
def test_log(verboseness, expected):
    std_out = StringIO()
    sys.stdout = std_out

    Log.verboseness = verboseness
    Log.info("this is the message")
    Log.success("this is the message")
    Log.error("this is the message")
    Log.print("this is the message")

    sys.stdout = sys.__stdout__

    output_list = [o for o in std_out.getvalue().split("\n")[:-1]]
    assert len(output_list) == len([e for e in expected if len(e) > 0])

    for out, exp in zip(output_list, expected):
        assert out == exp

from pathlib import Path

import pytest

from solution import main, CHARSET

def test_output(capsys):
    for fn in Path('testcases/').glob('*-output.txt'):
        expected = fn.read_text()
        fn_base = fn.name[:-11]  # cut -output.txt
        with Path('testcases/' + fn_base + '.txt').open('r', encoding=CHARSET) as fh:
            main(fh)
        out, _ = capsys.readouterr()

        assert out == expected, f'Output doesn\'t match for test `{fn_base}`'

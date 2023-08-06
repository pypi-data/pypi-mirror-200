import pandas as pd

# This needs python3 -m pytest
# from utencilos.general import checkin

# This works with pytest
from src.utencilos.general import checkin


def test_checkin(capsys):
    start_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    output = (
        start_df.pipe(checkin, "before filtering")
        .loc[lambda x: x["a"] == 1]
        .pipe(checkin, "after filtering")
    )
    captured = capsys.readouterr()
    out_text = "(3, 2): before filtering\n(1, 2): after filtering\n"
    assert captured.out == out_text
    assert output.shape == (1, 2)

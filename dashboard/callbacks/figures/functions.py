from typing import Literal, Optional, Tuple


def define_mode_and_previous_mode(
    callback_trigger: str, previous_mode: Optional[Literal["all", "candlesticks", "close_line"]]
) -> Tuple[
    Optional[Literal["all", "candlesticks", "close_line"]], Optional[Literal["all", "candlesticks", "close_line"]]
]:
    mode: Optional[Literal["all", "candlesticks", "close_line"]]
    if callback_trigger == "all_mode":
        mode = "all"
    elif callback_trigger == "candlesticks_mode":
        mode = "candlesticks"
    elif callback_trigger == "close_line_mode":
        mode = "close_line"
    else:
        mode = None

    if previous_mode is None:
        mode = "all"
        previous_mode = "all"
    return mode, previous_mode

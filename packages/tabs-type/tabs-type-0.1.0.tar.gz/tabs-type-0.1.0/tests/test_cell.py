# import pytest

# from tabs_type.cell import Cell


# @pytest.mark.parametrize(
#     "cell1,cell2,expected",
#     [
#         (Cell("apple", "banana"), Cell("banana", "apple"), True),
#         (Cell("orange", "mango"), Cell("mango", "orange"), True),
#         (Cell("pineapple", "orange"), Cell("mango", "pineapple"), False),
#         (Cell("", ""), Cell("", ""), True),
#     ],
# )
# def test_is_co_cell(cell1: Cell, cell2: Cell, expected: bool):
#     result = cell1.is_co_cell(cell2)
#     assert (
#         result == expected
#     ), f"For cells {cell1} and {cell2}, expected {expected} but got {result}"


# @pytest.mark.parametrize(
#     "cell,expected",
#     [
#         (Cell("apple", "banana"), Cell("banana", "apple")),
#     ],
# )
# def test_reverse(cell: Cell, expected: bool):
#     result = Cell.reverse(cell)
#     assert result == expected


# @pytest.mark.parametrize(
#     "cell,expected",
#     [
#         (Cell("apple", "banana"), False),
#         (Cell("orange", "orange"), True),
#     ],
# )
# def test_is_inner(cell: Cell, expected: bool):
#     result = cell.is_inner()
#     assert result == expected


# @pytest.mark.parametrize(
#     "signal_id,expected",
#     [
#         ("[BTCUSDT,ETHUSDT,10]:PriceDiff", Cell("BTCUSDT", "ETHUSDT")),
#         ("[ETHUSDT,10]:PriceDiff", Cell("ETHUSDT", "ETHUSDT")),
#     ],
# )
# def test_from_signal_id(signal_id: str, expected: Cell):
#     result = Cell.from_signal_id(signal_id)
#     assert result == expected

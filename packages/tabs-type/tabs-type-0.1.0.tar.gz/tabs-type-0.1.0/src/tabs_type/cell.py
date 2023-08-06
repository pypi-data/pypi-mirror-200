# from __future__ import annotations

# from dataclasses import dataclass

# from tabs_settings.config.trading_pair import TradingPair


# @dataclass(frozen=True)
# class Cell:
#     trigger: TradingPair
#     target: TradingPair

#     @classmethod
#     def from_signal_id(cls, signal_id: str) -> Cell:
#         # cell-dependent signals are stored like [ETHUSDT,BTCUSDT,10000]:PriceDiff
#         # or [ETHUSDT,10000]:PriceDiff
#         trigger_target_str = signal_id.split(":")[0]
#         if len(trigger_target_str.split(",")) == 3:
#             trigger, target = list(map(str, trigger_target_str[1:-1].split(",")[:2]))
#         else:
#             trigger = trigger_target_str[1:-1].split(",")[0]
#             target = trigger
#         return cls(trigger, target)

#     @classmethod
#     def reverse(cls, cell: Cell) -> Cell:
#         return cls(cell.target, cell.trigger)

#     def is_co_cell(self, other: Cell) -> bool:
#         return self.trigger == other.target and self.target == other.trigger

#     def is_inner(self) -> bool:
#         return self.trigger == self.target

import pandas as pd
import numpy as np
from records import Records
from copy import copy

class Double7:
    def __init__(self, lookback: int):
        self.status = 1 # wait for entry 1 or made an entry -1
        self.lb = lookback
        self.pending_record = None
        self.records = []

    def _create_entries(self, entry_i: int, time_index: pd.DatetimeIndex, open: np.array, high: np.array, low: np.array, close: np.array):
        new_record = Records(entry_index=entry_i, entry_price=open[entry_i], entry_timestamp=time_index[entry_i], exit_index=-1, exit_price=np.nan, exit_timestamp=time_index[entry_i], percentage_change=np.nan)
        self.pending_record = new_record
    
    def _create_exites(self, exit_i: int, time_index: pd.DatetimeIndex, open: np.array, high: np.array, low: np.array, close: np.array):
        self.pending_record.exit_index = exit_i
        self.pending_record.exit_timestamp = time_index[exit_i]
        self.pending_record.exit_price = open[exit_i]
        self.pending_record.percentage_change = (self.pending_record.exit_price - self.pending_record.entry_price) / self.pending_record.entry_price * 100
        self.records.append(copy(self.pending_record))
        self.pending_record = None

    def update(self, i: int, time_index: pd.DatetimeIndex, open: np.array, high: np.array, low: np.array, close: np.array):
        if i < self.lb:
            return
        else:
            if self.pending_record == None:
                lookback_window = high[i-self.lb:i]
                max_index = np.argmax(lookback_window)
                if max_index == self.lb - 1:
                    self._create_entries(i, time_index, open, high, low, close)
            else:
                lookback_window = low[i-self.lb:i]
                min_index = np.argmin(lookback_window)
                if min_index == self.lb - 1:
                    self._create_exites(i, time_index, open, high, low, close)
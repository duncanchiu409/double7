import pandas as pd
import numpy as np
from dataclasses import dataclass

@dataclass
class Records:
    entry_index: int
    entry_price: float
    entry_timestamp: pd.Timestamp

    exit_index: int
    exit_price: float
    exit_timestamp: pd.Timestamp

    percentage_change: float
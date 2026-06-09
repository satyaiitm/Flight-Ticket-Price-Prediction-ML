import pandas as pd

import sys
from pathlib import Path

sys.path.append( str(Path(__file__).resolve().parent.parent))


from src.preprocessing import logical_imputer
from src.config import FLIGHT_DATA, CLEAN_FILGHT_DATA


df = pd.read_csv(FLIGHT_DATA)

clean_df = logical_imputer(df)

clean_df.to_csv(CLEAN_FILGHT_DATA)
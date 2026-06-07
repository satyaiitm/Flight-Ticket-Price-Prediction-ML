from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


FLIGHT_DATA = PROJECT_ROOT / "data" / "raw" / "flight_data.csv"
TEST_DATA = PROJECT_ROOT / "data" / "raw" / "test_data.csv"



CLEAN_FILGHT_DATA = PROJECT_ROOT / "data" / "processed" / "clean_flight_data.csv"
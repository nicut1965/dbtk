from datetime import datetime
import pandas as pd


def parse_excel_datetime(value):
    """
    Parseaza date/ora provenite din Excel sau CSV.
    Accepta:
      - datetime nativ
      - pandas Timestamp
      - string (24h sau AM/PM)
      - valori goale
    """

    # valori lipsa
    if value is None:
        return None

    if isinstance(value, float) and pd.isna(value):
        return None

    # deja datetime
    if isinstance(value, datetime):
        return value

    # pandas Timestamp
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()

    # string
    if isinstance(value, str):
        value = value.strip()

        if not value:
            return None

        formats = [
            "%m/%d/%Y %H:%M:%S",     # 01/31/2024 15:30:29
            "%m/%d/%Y %I:%M:%S %p",  # 12/22/2025 3:59:03 PM
            "%d/%m/%Y %H:%M:%S",     # 31/01/2024 15:30:29
            "%Y-%m-%d %H:%M:%S",     # 2024-01-31 15:30:29
            "%Y-%m-%d",              # 2024-01-31
            "%m/%d/%Y",              # 01/31/2024
            "%d/%m/%Y",              # 31/01/2024
        ]

        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        # fallback inteligent pandas (optional dar util)
        try:
            return pd.to_datetime(value, errors="raise").to_pydatetime()
        except Exception:
            pass

    raise ValueError(f"Format de data necunoscut: {value}")


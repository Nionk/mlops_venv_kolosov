import pandas as pd
from plt_temp import build_temperature_df


def test_build_temperature_df_structure_and_sorting():
    times = [
        "2026-05-01T02:00",
        "2026-05-01T00:00",
        "2026-05-01T03:00",
        "2026-05-01T01:00",
    ]
    temperatures = [12.5, 10.0, 14.0, 11.2]

    df = build_temperature_df(times, temperatures)

    assert list(df.columns) == ["time", "temperature_c"]

    assert len(df) == 4

    expected_times = pd.to_datetime([
        "2026-05-01T00:00",
        "2026-05-01T01:00",
        "2026-05-01T02:00",
        "2026-05-01T03:00",
    ])
    pd.testing.assert_series_equal(df["time"], pd.Series(expected_times, name="time"))

    expected_temps = [10.0, 11.2, 12.5, 14.0]
    assert df["temperature_c"].tolist() == expected_temps
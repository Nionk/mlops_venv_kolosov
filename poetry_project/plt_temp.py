import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://api.open-meteo.com/v1/forecast"
API_PARAMS = {
    "latitude": 55.75,
    "longitude": 37.61,
    "hourly": "temperature_2m",
}


def build_temperature_df(
    hours: list[str], temps: list[float], limit: int = 24
) -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "time": pd.to_datetime(hours[:limit]),
            "temperature_c": temps[:limit],
        }
    )
    df = df.sort_values("time").reset_index(drop=True)
    return df


def fetch_weather_data(
    url: str = API_URL, params: dict = API_PARAMS, timeout: int = 10
) -> dict:
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def main() -> None:
    data = fetch_weather_data()
    hourly = data["hourly"]

    hours = hourly["time"]
    temps = hourly["temperature_2m"]

    df = build_temperature_df(hours, temps, limit=24)

    df.to_csv("temperature_24h.csv", index=False)
    print("Сохранено в temperature_24h.csv")

    plt.figure(figsize=(10, 5))
    plt.plot(df["time"], df["temperature_c"], marker="o")
    plt.xticks(rotation=45)
    plt.title("Температура в Москве (24 часа)")
    plt.xlabel("Время")
    plt.ylabel("°C")
    plt.tight_layout()
    plt.savefig("temperature_24h.png")
    plt.close()
    print("График сохранен в temperature_24h.png")


if __name__ == "__main__":
    main()
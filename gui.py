import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime


def create_temperature_chart(forecast_data: list, parent_widget) -> FigureCanvasTkAgg:
    """
    Erstellt ein Temperatur-Diagramm und gibt ein tkinter-kompatibles Canvas zurück.
    forecast_data: Liste von Tageswetter-Dicts (von parse_forecast)
    parent_widget: tkinter-Frame in dem das Diagramm eingebettet wird
    """
    dates = [datetime.strptime(d["date"], "%Y-%m-%d") for d in forecast_data]
    temp_min = [d["temp_min"] for d in forecast_data]
    temp_max = [d["temp_max"] for d in forecast_data]

    fig, ax = plt.subplots(figsize=(7, 2.8), facecolor="#1a1a2e")
    ax.set_facecolor("#16213e")

    ax.plot(dates, temp_max, color="#e94560", linewidth=2.5, marker="o",
            markersize=6, label="Max °C", zorder=3)
    ax.plot(dates, temp_min, color="#0f3460", linewidth=2.5, marker="o",
            markersize=6, label="Min °C", zorder=3)
    ax.fill_between(dates, temp_min, temp_max, alpha=0.15, color="#e94560")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %d.%m"))
    ax.tick_params(colors="#a0a0c0", labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a2a4a")

    ax.set_title("Temperaturverlauf (5 Tage)", color="#c0c0e0",
                 fontsize=11, pad=10)
    ax.legend(facecolor="#1a1a2e", labelcolor="#c0c0e0", fontsize=9,
              framealpha=0.7)
    ax.grid(True, color="#2a2a4a", linestyle="--", linewidth=0.7, alpha=0.6)

    fig.tight_layout(pad=1.5)

    canvas = FigureCanvasTkAgg(fig, master=parent_widget)
    canvas.draw()
    return canvas

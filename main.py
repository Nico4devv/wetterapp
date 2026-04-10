import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests

from api import get_current_weather, get_forecast, parse_forecast
from storage import load_favorites, save_favorite, remove_favorite
from gui import create_temperature_chart


BG_DARK      = "#0d0d1a"
BG_CARD      = "#1a1a2e"
BG_CARD2     = "#16213e"
ACCENT       = "#e94560"
ACCENT2      = "#0f3460"
TEXT_MAIN    = "#e0e0f5"
TEXT_SUB     = "#8080b0"
FONT_TITLE   = ("Courier New", 22, "bold")
FONT_LABEL   = ("Courier New", 10)
FONT_SMALL   = ("Courier New", 9)
FONT_BIG     = ("Courier New", 38, "bold")

WEATHER_ICONS = {
    "01": "☀️", "02": "🌤️", "03": "☁️", "04": "☁️",
    "09": "🌧️", "10": "🌦️", "11": "⛈️", "13": "❄️", "50": "🌫️"
}


def icon_emoji(icon_code: str) -> str:
    return WEATHER_ICONS.get(icon_code[:2], "🌡️")



class WetterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🌦  WetterApp")
        self.geometry("820x700")
        self.resizable(False, False)
        self.configure(bg=BG_DARK)

        self.current_city = tk.StringVar()
        self.chart_canvas = None

        self._build_ui()
        self._refresh_favorites()

    # ── UI aufbauen ──────────────────────────────────────────────────────────
    def _build_ui(self):
        # Titel
        tk.Label(self, text="⛅  WETTER APP", font=FONT_TITLE,
                 bg=BG_DARK, fg=ACCENT).pack(pady=(18, 4))
        tk.Label(self, text="powered by OpenWeatherMap",
                 font=FONT_SMALL, bg=BG_DARK, fg=TEXT_SUB).pack()

        # Suchzeile
        search_frame = tk.Frame(self, bg=BG_DARK)
        search_frame.pack(pady=12)

        self.search_entry = tk.Entry(
            search_frame, textvariable=self.current_city,
            font=FONT_LABEL, bg=BG_CARD2, fg=TEXT_MAIN,
            insertbackground=TEXT_MAIN, relief="flat",
            width=28
        )
        self.search_entry.grid(row=0, column=0, ipady=8, padx=(0, 8))
        self.search_entry.bind("<Return>", lambda e: self._search())

        tk.Button(
            search_frame, text="Suchen", command=self._search,
            font=FONT_LABEL, bg=ACCENT, fg="white",
            activebackground="#c73652", relief="flat",
            cursor="hand2", padx=14
        ).grid(row=0, column=1)

        tk.Button(
            search_frame, text="★ Speichern", command=self._save_fav,
            font=FONT_LABEL, bg=ACCENT2, fg="white",
            activebackground="#0a2440", relief="flat",
            cursor="hand2", padx=10
        ).grid(row=0, column=2, padx=(8, 0))

        main_frame = tk.Frame(self, bg=BG_DARK)
        main_frame.pack(fill="both", expand=True, padx=16)

        self.weather_card = tk.Frame(main_frame, bg=BG_CARD,
                                     relief="flat", bd=0)
        self.weather_card.pack(side="left", fill="both", expand=True,
                               padx=(0, 10))

        self.lbl_city    = tk.Label(self.weather_card, text="—",
                                    font=("Courier New", 16, "bold"),
                                    bg=BG_CARD, fg=TEXT_MAIN)
        self.lbl_city.pack(pady=(16, 0))

        self.lbl_desc    = tk.Label(self.weather_card, text="",
                                    font=FONT_LABEL, bg=BG_CARD, fg=TEXT_SUB)
        self.lbl_desc.pack()

        self.lbl_temp    = tk.Label(self.weather_card, text="—°",
                                    font=FONT_BIG, bg=BG_CARD, fg=ACCENT)
        self.lbl_temp.pack(pady=(4, 0))

        self.lbl_emoji   = tk.Label(self.weather_card, text="",
                                    font=("Segoe UI Emoji", 36),
                                    bg=BG_CARD)
        self.lbl_emoji.pack()

        details_frame = tk.Frame(self.weather_card, bg=BG_CARD)
        details_frame.pack(pady=8)

        self.lbl_humidity = tk.Label(details_frame, text="💧 —%",
                                     font=FONT_LABEL, bg=BG_CARD, fg=TEXT_SUB)
        self.lbl_humidity.grid(row=0, column=0, padx=18)

        self.lbl_wind     = tk.Label(details_frame, text="💨 — m/s",
                                     font=FONT_LABEL, bg=BG_CARD, fg=TEXT_SUB)
        self.lbl_wind.grid(row=0, column=1, padx=18)

        self.lbl_feels    = tk.Label(details_frame, text="🌡️ Gefühlt —°",
                                     font=FONT_LABEL, bg=BG_CARD, fg=TEXT_SUB)
        self.lbl_feels.grid(row=0, column=2, padx=18)

        tk.Frame(self.weather_card, bg=ACCENT2, height=1).pack(
            fill="x", padx=16, pady=8)

        self.chart_frame = tk.Frame(self.weather_card, bg=BG_CARD)
        self.chart_frame.pack(fill="x", padx=8, pady=(0, 8))


        self.forecast_frame = tk.Frame(self.weather_card, bg=BG_CARD)
        self.forecast_frame.pack(fill="x", padx=12, pady=(0, 14))

        fav_card = tk.Frame(main_frame, bg=BG_CARD, width=160)
        fav_card.pack(side="right", fill="y")
        fav_card.pack_propagate(False)

        tk.Label(fav_card, text="★ Favoriten",
                 font=("Courier New", 11, "bold"),
                 bg=BG_CARD, fg=ACCENT).pack(pady=(14, 6))

        self.fav_listbox = tk.Listbox(
            fav_card, font=FONT_LABEL, bg=BG_CARD2,
            fg=TEXT_MAIN, selectbackground=ACCENT,
            relief="flat", bd=0, activestyle="none"
        )
        self.fav_listbox.pack(fill="both", expand=True, padx=8)
        self.fav_listbox.bind("<Double-Button-1>", self._load_fav)

        tk.Button(
            fav_card, text="🗑 Entfernen",
            command=self._remove_fav,
            font=FONT_SMALL, bg="#2a0a14", fg=TEXT_SUB,
            activebackground="#3a0a1a", relief="flat",
            cursor="hand2"
        ).pack(pady=8)


        self.status_var = tk.StringVar(value="Stadt eingeben und suchen …")
        tk.Label(self, textvariable=self.status_var,
                 font=FONT_SMALL, bg=BG_DARK, fg=TEXT_SUB).pack(pady=(4, 8))


    def _search(self):
        city = self.current_city.get().strip()
        if not city:
            return
        self.status_var.set(f"Lade Wetter für {city} …")
        threading.Thread(target=self._fetch_weather,
                         args=(city,), daemon=True).start()

    def _fetch_weather(self, city: str):
        try:
            current  = get_current_weather(city)
            forecast = get_forecast(city)
            daily    = parse_forecast(forecast)
            self.after(0, self._update_ui, current, daily)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                self.after(0, messagebox.showerror,
                           "Fehler", f"Stadt '{city}' nicht gefunden.")
            else:
                self.after(0, messagebox.showerror,
                           "API-Fehler", str(e))
            self.after(0, self.status_var.set, "Fehler beim Laden.")
        except Exception as e:
            self.after(0, messagebox.showerror, "Fehler", str(e))
            self.after(0, self.status_var.set, "Fehler beim Laden.")


    def _update_ui(self, current: dict, daily: list):
        name    = current["name"]
        country = current["sys"]["country"]
        temp    = current["main"]["temp"]
        feels   = current["main"]["feels_like"]
        hum     = current["main"]["humidity"]
        wind    = current["wind"]["speed"]
        desc    = current["weather"][0]["description"].capitalize()
        icon    = current["weather"][0]["icon"]

        self.lbl_city.config(text=f"{name}, {country}")
        self.lbl_desc.config(text=desc)
        self.lbl_temp.config(text=f"{temp:.1f}°C")
        self.lbl_emoji.config(text=icon_emoji(icon))
        self.lbl_humidity.config(text=f"💧 {hum}%")
        self.lbl_wind.config(text=f"💨 {wind} m/s")
        self.lbl_feels.config(text=f"🌡️ Gefühlt {feels:.1f}°C")

        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()
        canvas = create_temperature_chart(daily, self.chart_frame)
        canvas.get_tk_widget().pack(fill="x")
        self.chart_canvas = canvas

        for w in self.forecast_frame.winfo_children():
            w.destroy()

        for day in daily:
            col = tk.Frame(self.forecast_frame, bg=BG_CARD2, padx=8, pady=6)
            col.pack(side="left", expand=True, fill="x", padx=3)

            date_str = day["date"][5:]  # MM-DD
            tk.Label(col, text=date_str, font=FONT_SMALL,
                     bg=BG_CARD2, fg=TEXT_SUB).pack()
            tk.Label(col, text=icon_emoji(day["icon"]),
                     font=("Segoe UI Emoji", 18),
                     bg=BG_CARD2).pack()
            tk.Label(col, text=f"{day['temp_max']:.0f}°",
                     font=("Courier New", 11, "bold"),
                     bg=BG_CARD2, fg=ACCENT).pack()
            tk.Label(col, text=f"{day['temp_min']:.0f}°",
                     font=FONT_SMALL, bg=BG_CARD2, fg=TEXT_SUB).pack()

        self.status_var.set(
            f"Zuletzt aktualisiert: {name}, {country}")


    def _refresh_favorites(self):
        self.fav_listbox.delete(0, tk.END)
        for city in load_favorites():
            self.fav_listbox.insert(tk.END, city)

    def _save_fav(self):
        city = self.current_city.get().strip().title()
        if city:
            save_favorite(city)
            self._refresh_favorites()
            self.status_var.set(f"'{city}' zu Favoriten hinzugefügt.")

    def _load_fav(self, event=None):
        sel = self.fav_listbox.curselection()
        if sel:
            city = self.fav_listbox.get(sel[0])
            self.current_city.set(city)
            self._search()

    def _remove_fav(self):
        sel = self.fav_listbox.curselection()
        if sel:
            city = self.fav_listbox.get(sel[0])
            remove_favorite(city)
            self._refresh_favorites()
            self.status_var.set(f"'{city}' aus Favoriten entfernt.")



if __name__ == "__main__":
    app = WetterApp()
    app.mainloop()

# 🌦️ WetterApp

Eine Python-Desktop-Wetteranwendung mit GUI, Diagrammen und Favoritenspeicherung.

## Features

- 🌡️ Aktuelle Wetterdaten (Temperatur, Luftfeuchtigkeit, Wind, Gefühlte Temperatur)
- 📅 5-Tage-Vorhersage mit Icons
- 📊 Temperaturdiagramm (matplotlib)
- ⭐ Favoritenstädte speichern & schnell laden
- 🔒 API-Key sicher über `.env` Datei

## Screenshots

> GUI startet mit `python main.py`

## Installation

```bash
# 1. Repository klonen
git clone https://github.com/dein-name/wetter-app.git
cd wetter-app

# 2. Abhängigkeiten installieren
pip install -r requirements.txt

# 3. API-Key einrichten
cp .env.example .env
# .env öffnen und deinen Key von openweathermap.org eintragen

# 4. App starten
python main.py
```

## API-Key holen

1. Kostenlos registrieren auf [openweathermap.org](https://openweathermap.org/api)
2. Unter "API keys" einen Key erstellen
3. Key in die `.env` Datei eintragen

## Projektstruktur

```
wetter-app/
├── main.py          # GUI & App-Logik
├── api.py           # OpenWeatherMap API-Abfragen
├── chart.py         # Matplotlib Temperaturdiagramm
├── storage.py       # Favoriten (JSON)
├── requirements.txt
├── .env.example
└── README.md
```

## Technologien

| Library | Zweck |
|---|---|
| `tkinter` | GUI Framework |
| `requests` | HTTP / API-Abfragen |
| `matplotlib` | Temperaturdiagramm |
| `python-dotenv` | API-Key aus `.env` laden |

## Lizenz

MIT

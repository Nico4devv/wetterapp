import json
import os

FAVORITES_FILE = "favorites.json"


def load_favorites() -> list:
    """Lädt die gespeicherten Favoritenstädte."""
    if not os.path.exists(FAVORITES_FILE):
        return []
    with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_favorite(city: str) -> list:
    """Fügt eine Stadt zu den Favoriten hinzu (keine Duplikate)."""
    favorites = load_favorites()
    city = city.strip().title()
    if city not in favorites:
        favorites.append(city)
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(favorites, f, ensure_ascii=False, indent=2)
    return favorites


def remove_favorite(city: str) -> list:
    """Entfernt eine Stadt aus den Favoriten."""
    favorites = load_favorites()
    city = city.strip().title()
    if city in favorites:
        favorites.remove(city)
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(favorites, f, ensure_ascii=False, indent=2)
    return favorites

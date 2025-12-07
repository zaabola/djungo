from mcp.server.fastmcp import FastMCP
import os
import json

# Chemin absolu vers le dossier resources
FLIGHTS_PATH = os.path.join(os.path.dirname(__file__), "flights.json")

# Création du serveur
mcp = FastMCP(name="Aéroport Info")

def _load_flights():
    with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("flights", [])

# ──────────────────────────────────────────────────────────────
# EXPOSITION D'UNE RESOURCE (fichier JSON lisible par l'LLM)
# ──────────────────────────────────────────────────────────────
@mcp.resource("flights://today")
def flights_resource():
    with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
def find_flight(flight_number: str) -> str:
    """Trouve un vol par son numéro (ex: AF1234)"""
    flights = _load_flights()
    for flight in flights:
        if flight.get("flight_number", "").upper() == flight_number.upper():
            return f"""Avion
Vol {flight["flight_number"]} ({flight["airline"]})
{flight["departure_city"]} -> {flight["arrival_city"]}
Depart : {flight["departure_time"]} | Arrivee :
{flight["arrival_time"]}
Statut : {flight["status"]}
"""
    return f"Vol {flight_number} non trouve aujourd'hui."

@mcp.tool()
def flights_to(destination: str) -> str:
    """Liste tous les vols a destination d'une ville aujourd'hui."""
    flights = _load_flights()
    matches = [f for f in flights if destination.lower() in f["arrival_city"].lower()]
    if not matches:
        return f"Aucun vol trouve vers {destination.title()} aujourd'hui."
    result = f"Vols vers {destination.title()} ({len(matches)} trouve(s)) :\n\n"
    for f in matches:
        result += f"• {f['flight_number']} ({f['airline']}) -> {f['arrival_city']} a {f['arrival_time']} - {f['status']}\n"
    return result.strip()

# Lancement
if __name__ == "__main__":
    mcp.run(transport="stdio")  # pour VS Code Copilot
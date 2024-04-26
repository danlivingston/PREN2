def aktualisiereWuerfelPositionen(nachDrehung, farbenZuPosition):
    # Nach jeder Drehung müssen die Positionen der Würfel aktualisiert werden
    return {farbe: (position + nachDrehung) % 360 for farbe, position in farbenZuPosition.items()}

def berechneMagazinDrehungZuRelais(farbenZuPosition, zielFarbe, aktuelleMagazinPosition, zielRelais):
    relaisZuGrad = {1: 0, 2: 270, 3: 180, 4: 90}  # Anpassung der Relais Positionen
    zielPosition = farbenZuPosition[zielFarbe]
    relaisPosition = relaisZuGrad[zielRelais]

    # Berechne die notwendige Drehung
    drehung = (relaisPosition - zielPosition + 360) % 360

    # Aktualisiere die Positionen der Würfel nach der Drehung
    neueFarbenZuPosition = aktualisiereWuerfelPositionen(drehung, farbenZuPosition)
    return drehung, neueFarbenZuPosition

def relaisAktivieren(zielRelais):
    print(f"\tRelais {zielRelais} wird aktiviert, um den Würfel auszustoßen.")

def sortiereWuerfel(konfiguration):
    farbenZuPosition = {'blau': 0, 'rot': 120, 'gelb': 240}
    print("Beginne Sortiervorgang...\n")
    for position, farbe in sorted(konfiguration.items(), key=lambda x: int(x[0])):
        if farbe:  # Überspringe, wenn 'farbe' leer oder None ist
            zielRelais = ((int(position) - 1) % 4) + 1
            print(f"Position {position}, Farbe '{farbe}':")
            drehung, neueFarbenZuPosition = berechneMagazinDrehungZuRelais(farbenZuPosition, farbe, position, zielRelais)
            if drehung > 0:
                print(f"\tDas Magazin dreht sich um {drehung} Grad.")
            else:
                print("\tKeine Drehung erforderlich.")
            farbenZuPosition = neueFarbenZuPosition  # Aktualisiere die Positionen der Würfel
            relaisAktivieren(zielRelais)
        else:
            print(f"Position {position} hat keinen Würfel. Überspringen...")
    print("\nSortierung abgeschlossen. Alle Würfel sind entsprechend der Konfiguration sortiert.")

# Beispielkonfiguration, wobei einer der Einträge leer ist
konfiguration = {
    "1": "blau",
    "2": "",
    "3": "blau",
    "4": "gelb",
    "5": "rot",
    "6": "rot",
    "7": "blau",
    "8": "blau"
}

sortiereWuerfel(konfiguration)

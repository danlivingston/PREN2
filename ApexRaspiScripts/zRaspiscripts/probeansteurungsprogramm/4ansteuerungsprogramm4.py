import time

def schrittmotorDrehen(grad):
    grad = grad % 360  # Normalisierung auf 0-359 Grad
    if grad > 180:  # Wähle kürzesten Weg in eine Richtung
        grad -= 360
    if grad != 0:
        zeitProGrad = 1.2 / 360  # Zeit in Sekunden pro Grad
        drehZeit = abs(grad) * zeitProGrad  # Absolute Wert, da nur Vorwärtsbewegung
        print(f"\tSchrittmotor beginnt zu drehen um {abs(grad)} Grad vorwärts...")
        time.sleep(drehZeit)
        print(f"\tSchrittmotor hat die Drehung abgeschlossen. (Dauer: {drehZeit:.2f}s)")
    else:
        print("\tKeine Drehung erforderlich. Schrittmotor bleibt in Position.")

def aktualisiereWuerfelPositionen(nachDrehung, farbenZuPosition):
    return {color: (position + nachDrehung) % 360 for color, position in farbenZuPosition.items()}

def berechneMagazinDrehungZuRelais(farbenZuPosition, zielFarbe, aktuelleMagazinPosition, zielRelais):
    relaisZuGrad = {1: 0, 2: 90, 3: 180, 4: 270}
    zielPosition = farbenZuPosition[zielFarbe]
    relaisPosition = relaisZuGrad[zielRelais]
    drehung = (relaisPosition - zielPosition + 360) % 360
    if drehung > 180:  # Wähle kürzesten Weg in eine Richtung
        drehung -= 360
    neueFarbenZuPosition = aktualisiereWuerfelPositionen(drehung, farbenZuPosition)
    return drehung, neueFarbenZuPosition

def relaisAktivieren(zielRelais):
    print(f"\tRelais {zielRelais} wird aktiviert, um den Würfel auszustoßen...")
    time.sleep(0.5)  # Simuliere das Aktivieren des Relais
    print("\tWürfel wurde ausgestoßen.")

def sortiereWuerfel(konfiguration):
    startZeit = time.time()
    farbenZuPosition = {'blue': 0, 'red': 240, 'yellow': 120}
    print("Beginne Sortiervorgang...\n")
    for position, color in sorted(konfiguration.items(), key=lambda x: int(x[0])):
        if color:
            zielRelais = ((int(position) - 1) % 4) + 1
            print(f"Position {position}, Farbe '{color}':")
            drehung, neueFarbenZuPosition = berechneMagazinDrehungZuRelais(farbenZuPosition, color, position, zielRelais)
            schrittmotorDrehen(drehung)
            farbenZuPosition = neueFarbenZuPosition
            relaisAktivieren(zielRelais)
        else:
            print(f"Position {position} hat keinen Würfel. Überspringen...")
    endZeit = time.time()
    gesamtzeit = endZeit - startZeit
    print("\nSortierung abgeschlossen. Alle Würfel sind entsprechend der Konfiguration sortiert.")
    print(f"Gesamtzeit für den Sortiervorgang: {gesamtzeit:.2f} Sekunden.")

# Testkonfiguration
konfiguration = {
    "1": "blue",  
    "2": "yellow",
     "3": "blue",
    "4": "yellow",
    "5": "red",
    "6": "red",
    "7": "blue",
    "8": "blue"
}

sortiereWuerfel(konfiguration)


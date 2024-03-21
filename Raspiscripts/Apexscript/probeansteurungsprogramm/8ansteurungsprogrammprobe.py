import time

def schrittmotorDrehen(grad):
    if grad == 0 or grad == 360:
        print("\tKeine Drehung erforderlich. Schrittmotor bleibt in Position.")
        return

    modifizierterGrad = 360 - grad
    schritteProUmdrehung = 800
    modifizierterGrad = modifizierterGrad % 360
    schritte = int((modifizierterGrad / 360.0) * schritteProUmdrehung)

    if grad != 0:
        print(f"\tSchrittmotor beginnt zu drehen um {modifizierterGrad} Grad vorwärts... (simuliert {schritte} Schritte)")
        # Hier würde normalerweise die Drehung ausgeführt
        print("\tSimulierte Drehung abgeschlossen.")
    else:
        print("\tKeine Drehung erforderlich. Schrittmotor bleibt in Position.")

def aktualisiereWuerfelPositionen(nachDrehung, farbenZuPosition):
    return {color: (position + nachDrehung) % 360 for color, position in farbenZuPosition.items()}

def berechneMagazinDrehungZuRelais(farbenZuPosition, zielFarbe, aktuelleMagazinPosition, zielRelais):
    relaisZuGrad = {1: 0, 2: 270, 3: 180, 4: 90}
    zielPosition = farbenZuPosition[zielFarbe]
    relaisPosition = relaisZuGrad[zielRelais]
    drehung = (relaisPosition - zielPosition + 360) % 360
    neueFarbenZuPosition = aktualisiereWuerfelPositionen(drehung, farbenZuPosition)
    return drehung, neueFarbenZuPosition

def relaisAktivieren(zielRelais):
    print(f"\tRelais {zielRelais} wird aktiviert, um den Würfel auszustoßen... (simuliert)")
    # Hier würde normalerweise das Relais aktiviert
    print("\tSimulierte Aktion: Würfel ausgestoßen.")

def sortiereWuerfel(konfiguration):
    try:
        startZeit = time.time()
        farbenZuPosition = {'blue': 0, 'red': 120, 'yellow': 240}
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
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Testkonfiguration
konfiguration = {
    "1": "yellow",
    "2": "red",
    "3": "blue",
    "4": "blue",
    "5": "red",
    "6": "yellow",
    "7": "red",
    "8": "yellow"
}

sortiereWuerfel(konfiguration)

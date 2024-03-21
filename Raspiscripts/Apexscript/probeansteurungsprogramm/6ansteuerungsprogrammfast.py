import time

def schrittmotorDrehen(grad):
    # Überprüfung, ob grad gleich 0 oder 360 ist
    if grad == 0 or grad == 360:
        print("\tKeine Drehung erforderlich. Schrittmotor bleibt in Position.")
        return  # Frühe Rückkehr, um die Funktion zu beenden

    # Berechnung der modifizierten Drehung: 360 - ursprünglicher Gradwert, falls nicht 0 oder 360
    modifizierterGrad = 360 - grad

    zeitProGrad = 1.2 / 360  # Zeit in Sekunden pro Grad
    drehZeit = modifizierterGrad * zeitProGrad  # Gesamtzeit für die spezifizierte Drehung

    # Da grad niemals 0 oder 360 in diesem Block ist, entfällt die Überprüfung auf modifizierterGrad > 0
    print(f"\tSchrittmotor beginnt zu drehen um {modifizierterGrad} Grad...")
    time.sleep(drehZeit)  # Warte die berechnete Zeit
    print(f"\tSchrittmotor hat die Drehung abgeschlossen. (Dauer: {drehZeit:.2f}s)")
    
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
    print(f"\tRelais {zielRelais} wird aktiviert, um den Würfel auszustoßen...")
    time.sleep(0.5)  # Verzögerung von 0.5 Sekunden für das Relais
    print("\tWürfel wurde ausgestoßen.")

def sortiereWuerfel(konfiguration):
    startZeit = time.time()  # Startzeit erfassen
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
    endZeit = time.time()  # Endzeit erfassen
    gesamtzeit = endZeit - startZeit
    print("\nSortierung abgeschlossen. Alle Würfel sind entsprechend der Konfiguration sortiert.")
    print(f"Gesamtzeit für den Sortiervorgang: {gesamtzeit:.2f} Sekunden.")

# Hier ist die aktualisierte Konfiguration, die Sie verwenden können:
konfiguration = {
    "1": "blue",  
    "2": "yellow",
    "3": "red",
    "4": "red",
    "5": "",  
    "6": "yellow",
    "7": "red",
    "8": "yellow"
}

sortiereWuerfel(konfiguration)

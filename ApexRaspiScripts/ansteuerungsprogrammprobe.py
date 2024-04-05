import time
import os
import time
import subprocess

# Ermitteln des Basisverzeichnisses relativ zum aktuellen Skript
base_dir = os.path.dirname(os.path.abspath(__file__))

# Pfad für das zu startende Skript
first_script_path = os.path.join(base_dir, 'ansteuerungsvisual.py')


def schrittmotorDrehen(grad):
    zeitProGrad = 1.2 / 360  # Zeit in Sekunden pro Grad
    drehZeit = grad * zeitProGrad  # Gesamtzeit für die spezifizierte Drehung
    if grad > 0:
        print(f"\tSchrittmotor beginnt zu drehen um {grad} Grad...")
        time.sleep(drehZeit)  # Warte die berechnete Zeit
        print(f"\tSchrittmotor hat die Drehung abgeschlossen. (Dauer: {drehZeit:.2f}s)")
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
    print(f"\tRelais {zielRelais} wird aktiviert, um den Würfel auszustoßen...")
    time.sleep(0.5)  # Verzögerung von 0.5 Sekunden für das Relais
    print("\tWürfel wurde ausgestoßen.")

def sortiereWuerfel(konfiguration):
    # Starten des ersten Skripts
    first_script_process = subprocess.Popen(['python', first_script_path])
    
    try:
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
    finally:
        # Beenden des ersten Skripts, sobald das Hauptskript endet
        first_script_process.terminate()
        try:
            # Warten auf das Beenden des ersten Skripts (mit Timeout)
            first_script_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            # Erzwingen des Beendens, wenn das Skript nicht rechtzeitig endet
            first_script_process.kill()


#best case 
konfiguration = {
    "1": "blue",  
    "2": "yellow",   
    "3": "",
    "4": "blue", 
    "5": "red",  
    "6": "red",
    "7": "blue",
    "8": "yellow"  
}

sortiereWuerfel(konfiguration)

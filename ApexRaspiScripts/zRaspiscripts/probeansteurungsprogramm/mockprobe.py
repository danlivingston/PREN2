import time  # Dies muss am Anfang Ihres Skripts stehen

USE_MOCKS = True  # Setzen Sie dies auf False, wenn Sie mit echter Hardware arbeiten

if USE_MOCKS:
    class MockDRV8825:
        def __init__(self, dir_pin, step_pin, enable_pin, mode_pins):
            print(f"MockDRV8825 initialisiert mit dir_pin={dir_pin}, step_pin={step_pin}, enable_pin={enable_pin}, mode_pins={mode_pins}")

        def SetMicroStep(self, mode, step):
            print(f"SetMicroStep aufgerufen mit mode={mode}, step={step}")

        def TurnStep(self, Dir, steps, stepdelay):
            print(f"MockMotor dreht {Dir} um {steps} Schritte mit Verzögerung {stepdelay}")

        def Stop(self):
            print("MockMotor angehalten")

    class MockRelay:
        def __init__(self, relay_name):
            self.relay_name = relay_name
            print(f"MockRelay {self.relay_name} initialisiert")

        def on(self):
            print(f"MockRelay {self.relay_name} eingeschaltet")

        def off(self):
            print(f"MockRelay {self.relay_name} ausgeschaltet")

    DRV8825 = MockDRV8825
    Relay = MockRelay
else:
    from DRV8825 import DRV8825
    import PiRelay6
    class Relay:
        def __init__(self, relay_name):
            self.relay = PiRelay6.Relay(relay_name)

        def on(self):
            self.relay.on()

        def off(self):
            self.relay.off()

# Initialisierung des Schrittmotors
Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
Motor2.SetMicroStep('hardware', '1/4step')

r1 = Relay("RELAY1")
r4 = Relay("RELAY2")
r3 = Relay("RELAY3")
r2 = Relay("RELAY4")

def schrittmotorDrehen(grad):
    # Überprüfung, ob grad gleich 0 oder 360 ist
    if grad == 0 or grad == 360:
        print("\tKeine Drehung erforderlich. Schrittmotor bleibt in Position.")
        return  # Frühe Rückkehr, um die Funktion zu beenden
    
    modifizierterGrad = 360 - grad

    schritteProUmdrehung = 800  
    modifizierterGrad = modifizierterGrad % 360  
    schritte = int((modifizierterGrad / 360.0) * schritteProUmdrehung)  # Berechnet die erforderlichen Schritte basierend auf dem gewünschten Drehwinkel

    if grad != 0:
        print(f"\tSchrittmotor beginnt zu drehen um {modifizierterGrad} Grad vorwärts...")
        # Führt die Drehung aus, indem die berechnete Anzahl von Schritten an den Motor gesendet wird
        Motor2.TurnStep(Dir='forward', steps=schritte, stepdelay=0.0005)
        # Kurze Pause, um die Drehung abzuschließen, könnte je nach Anwendung angepasst werden
        time.sleep(0.1)
        print(f"\tSchrittmotor hat die Drehung abgeschlossen. ({schritte} Schritte)")
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
     # Definiere Verzögerungen
    verzogerung = 0.0005  # Verzögerung zwischen den Steps, aktuell nicht verwendet in dieser Funktion
    delay_hinten = 0.1  # Verzögerung nach dem Einschalten des Relais
    delay_vorne = 0.2  # Verzögerung nach dem Ausschalten des Relais

    print(f"\tRelais {zielRelais} wird aktiviert, um den Würfel auszustoßen...")
    if zielRelais == 1:
        r1.on()
        time.sleep(delay_hinten)  # Wartezeit direkt nach dem Einschalten
        r1.off()
        time.sleep(delay_vorne)  # Wartezeit direkt nach dem Ausschalten
    elif zielRelais == 2:
        r2.on()
        time.sleep(delay_hinten)
        r2.off()
        time.sleep(delay_vorne)
    elif zielRelais == 3:
        r3.on()
        time.sleep(delay_hinten)
        r3.off()
        time.sleep(delay_vorne)
    elif zielRelais == 4:
        r4.on()
        time.sleep(delay_hinten)
        r4.off()
        time.sleep(delay_vorne)
    print("\tWürfel wurde ausgestoßen.")

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
    "1": "red",  
    "2": "yellow",
    "3": "red",
    "4": "blue",
    "5": "",  
    "6": "yellow",
    "7": "",
    "8": "blue"
}


sortiereWuerfel(konfiguration)



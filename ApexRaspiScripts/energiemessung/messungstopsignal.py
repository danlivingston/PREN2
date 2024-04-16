import os

# Pfadkonfiguration
base_dir = os.path.dirname(os.path.abspath(__file__))
SIGNAL_FILE_PATH = os.path.join(base_dir, 'signal.txt')

# Dieses Skript schreibt ein 'stop'-Signal in eine Datei namens 'signal.txt'
def set_stop_signal():
    with open(SIGNAL_FILE_PATH, 'w') as file:
        file.write('stop')

if __name__ == "__main__":
    set_stop_signal()
    print("Stop-Signal gesetzt.")
    
    
    
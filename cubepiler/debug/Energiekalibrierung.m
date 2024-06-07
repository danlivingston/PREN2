clear all;
set(0, "defaultaxesfontsize", 24);  % Set default font size for axes labels

% Define the constants and data
Spannung = 23;  % Voltage in volts
Zeit = 30;      % Time in seconds
Strom = [0.1, 0.1979, 0.2977, 0.3972, 0.508, 0.808, 1.01, 1.32, 1.63, 2.1];  % Current in amperes
Energie_gemessen = [69.8,132.64, 197.45, 260.22, 332, 524.92, 661.23, 854.19, 1048.2, 1356.86];  % Measured energy in Ws


% Calculate the expected energy values
Energie_soll = Spannung * Zeit * Strom;


%Fehler Berechnen

Fehlerfaktor = Energie_soll / Energie_gemessen;

Fehlerfaktor_mean = mean(Fehlerfaktor)

Energie_korrigiert  = Energie_gemessen * Fehlerfaktor_mean;
% Plot the measured energy values
figure 1;
plot(Strom, Energie_gemessen, 'bo-', 'LineWidth', 1, 'MarkerSize', 4);
hold on;

# Plot the expected energy values
plot(Strom, Energie_soll, 'r*-', 'LineWidth', 1, 'MarkerSize', 4);

plot(Strom, Energie_korrigiert)
# Add labels and legend
xlabel('Strom (A)');
ylabel('Energie (Ws)');
title('Gemessene vs. Berechnete Energie');
legend('Gemessene Energie', 'Berechnete Energie', 'Location', 'NorthWest');

# Display the grid
grid on;

# Release the hold on the plot
hold off;



# Kalibriert
Strom_kalibriert = [0.1, 0.19, 0.29, 0.40, 0.49, 0.8, 1, 1.32, 1.54, 2.09];
Energie_gemessen_kalibriert = [74.13, 141.58, 210.37, 281.79, 342.53, 554.29, 688.45, 906.72, 1058.84, 1439.92];


% Calculate the expected energy values
Energie_soll_kalibriert = Spannung * Zeit * Strom_kalibriert;

% Plot the measured energy values
figure 2;
plot(Strom_kalibriert, Energie_gemessen_kalibriert, 'bo-', 'LineWidth', 1, 'MarkerSize', 4);
hold on;

# Plot the expected energy values
plot(Strom_kalibriert, Energie_soll_kalibriert, 'r*-', 'LineWidth', 1, 'MarkerSize', 4);


# Add labels and legend
xlabel('Strom (A)');
ylabel('Energie (Ws)');
title('Gemessene vs. Berechnete Energie');
legend('Gemessene Energie', 'Berechnete Energie', 'Location', 'NorthWest');


%Fehler Berechnen

Fehlerfaktor_kalibriert = Energie_soll_kalibriert / Energie_gemessen_kalibriert;

Fehlerfaktor_mean_kalibriert = mean(Fehlerfaktor_kalibriert)

# Display the grid
grid on;

# Release the hold on the plot
hold off;


# Set GPIO pin 4 to low
echo "4" >/sys/class/gpio/export
echo "out" >/sys/class/gpio/gpio4/direction
echo "0" >/sys/class/gpio/gpio4/value

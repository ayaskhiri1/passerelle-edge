@echo off
echo Démarrage des capteurs simulés...
echo.

start cmd /k "python sensors\mqtt_sensor.py"
timeout /t 2

start cmd /k "python sensors\http_sensor.py"
timeout /t 2

start cmd /k "python sensors\modbus_sensor.py"
timeout /t 2

echo Tous les capteurs sont démarrés!
pause
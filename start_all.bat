@echo off
echo ====================================
echo  PASSERELLE INTELLIGENTE - SYSTEME
echo ====================================
echo.

echo [1/5] Démarrage des capteurs simulés...
start cmd /k "python sensors\mqtt_sensor.py"
timeout /t 2
start cmd /k "python sensors\http_sensor.py"
timeout /t 2
start cmd /k "python sensors\modbus_sensor.py"
timeout /t 3

echo [2/5] Démarrage des clouds simulés...
start cmd /k "python clouds\fast_cloud.py"
timeout /t 2
start cmd /k "python clouds\slow_cloud.py"
timeout /t 2

echo [3/5] Démarrage du dashboard...
start cmd /k "python dashboard\app.py"
timeout /t 3

echo [4/5] Démarrage de la passerelle...
timeout /t 5
start cmd /k "python gateway\main.py"

echo [5/5] Ouverture du dashboard dans le navigateur...
timeout /t 3
start http://localhost:5000

echo.
echo ====================================
echo  Tous les services sont démarrés !
echo ====================================
echo.
echo Accès au dashboard: http://localhost:5000
echo.
pause
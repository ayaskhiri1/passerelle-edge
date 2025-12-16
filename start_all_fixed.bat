@echo off
echo ====================================
echo  PASSERELLE INTELLIGENTE - VERSION FIX
echo ====================================
echo.

echo [1/5] Nettoyage des anciens processus...
taskkill /f /im python.exe 2>nul
timeout /t 2

echo [2/5] Démarrage des capteurs...
start cmd /k "cd sensors && python http_sensor.py"
timeout /t 3
start cmd /k "cd sensors && python modbus_sensor.py"
timeout /t 3

echo [3/5] Démarrage des clouds...
start cmd /k "cd clouds && python fast_cloud.py"
timeout /t 3
start cmd /k "cd clouds && python slow_cloud.py"
timeout /t 3

echo [4/5] Démarrage du dashboard...
start cmd /k "cd dashboard && python app.py"
timeout /t 5

echo [5/5] Démarrage de la passerelle...
timeout /t 7
start cmd /k "python gateway/main.py"

echo.
echo ====================================
echo  SYSTEME PRÊT !
echo ====================================
echo.
echo 📊 Dashboard:    http://localhost:5000
echo ⚡ Fast Cloud:   http://localhost:8080/stats
echo 🐌 Slow Cloud:   http://localhost:8081
echo 📡 HTTP Sensor:  http://localhost:5001/data
echo.
timeout /t 3
start http://localhost:5000
@echo off
echo ====================================
echo  PASSERELLE INTELLIGENTE - DEMO
echo ====================================
echo.

echo [1/4] Démarrage des capteurs...
start cmd /k "cd sensors && python http_sensor.py"
timeout /t 2
start cmd /k "cd sensors && python modbus_sensor.py"
timeout /t 2

echo [2/4] Démarrage des clouds...
start cmd /k "cd clouds && python fast_cloud.py"
timeout /t 2
start cmd /k "cd clouds && python slow_cloud.py"
timeout /t 2

echo [3/4] Démarrage du dashboard...
start cmd /k "cd dashboard && python app.py"
timeout /t 3

echo [4/4] Démarrage de la passerelle...
timeout /t 5
start cmd /k "python gateway/main.py"

echo.
echo ====================================
echo  PRÊT !
echo ====================================
echo.
echo Dashboard: http://localhost:5000
echo Fast Cloud: http://localhost:8080/stats
echo.
echo Appuyez sur une touche pour ouvrir le dashboard...
pause
start http://localhost:5000
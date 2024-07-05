@echo off
REM Cambiar al directorio donde está tu entorno virtual de Python y el script
cd C:\Users\msaldarriaga\Desktop\Revision\vuelosBaratos

REM Activar el entorno virtual
call venv\Scripts\activate

REM Ejecutar el script de Python como un módulo
python -m scraper.main

# Proyecto I Análisis y Diseño
Módulo de Exportación e Importación de Datos del Panel de Control - DISAGRO


El proyecto se encuentra en la carpeta ***"modulo"***

***Comandos***

Levantar un entorno virtual
```
python -m venv .venv
o
py -m venv .venv
```

Acitvar el entorno virtual
```
Para PowerShell
.venv/Scripts/Activate.ps1

Para CMD
.venv/Scripts/Activate.bat
```

Para instalar la librerias del proyecto

```
pip install -r requirements.txt
```

Para levantar un servidor en python
```
flask --app <nombre de la carpeta> run
```
En este caso seria
```
flask --app main run
```

En caso de usar nuevas librerias externas agregarlas en el archivo ```requirements.txt```
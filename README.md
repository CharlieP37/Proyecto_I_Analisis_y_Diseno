# 1. Proyecto I Análisis y Diseño

Módulo de Exportación e Importación de Datos del Panel de Control - DISAGRO

El proyecto se encuentra en la carpeta ***"modulo"***

***Comandos***

Levantar un entorno virtual

```bash
python -m venv .venv
```

o

```bash
py -m venv .venv
```

Acitvar el entorno virtual

Para PowerShell

```bash
.venv/Scripts/Activate.ps1
```

Para CMD

```bash
.venv/Scripts/Activate.bat
```

Para instalar la librerias del proyecto

```bash
pip install -r requirements.txt
```

Para levantar un servidor en python

```bash
flask --app <nombre del archivo> run
```

En este caso seria

```bash
flask --app main run
```

En caso de usar nuevas librerias externas agregarlas en el archivo ```requirements.txt```

# Caja Chica - App de Contabilidad (Python + Kivy)

Aplicación móvil de contabilidad sencilla desarrollada con Python y Kivy.

## Funcionalidades

- **Saldo actual** en grande, se actualiza automáticamente
- **Registro de ingresos** (+) y **egresos** (-) con botones de colores
- **Historial de movimientos** con fecha, concepto y monto
- **Persistencia de datos** usando archivo JSON local
- **Diseño oscuro** moderno optimizado para móvil
- **Moneda en pesos argentinos** (ARS)

## Requisitos

- Python 3.8+
- Kivy

## Instalación (Desktop)

```bash
pip install kivy
python main.py
```

## Generar APK para Android

```bash
pip install buildozer cython setuptools
buildozer android debug
```

El APK se genera en la carpeta `bin/`.

## Estructura

```
caja-chica-python/
├── main.py           # Código principal de la app
├── buildozer.spec    # Configuración para generar APK
└── README.md
```

## Datos

Los movimientos se guardan en un archivo `caja_chica_data.json` que se crea automáticamente.

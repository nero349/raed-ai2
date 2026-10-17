
# RAED AI

Asistente personal de escritorio para Windows.

## Funciones actuales

- Interfaz oscura con detalles azules.
- Conversación mediante comandos básicos.
- Calculadora integrada.
- Guardado de notas en una base de datos SQLite local.
- Consulta de notas guardadas.
- Fecha y hora local.

## Requisitos

- Windows 10 o Windows 11.
- Python 3.10 o posterior.
- Tkinter y SQLite, incluidos normalmente con Python.

## Cómo iniciar

1. Descarga el repositorio desde GitHub usando Code > Download ZIP.
2. Extrae el archivo ZIP en una carpeta.
3. Instala Python 3 desde https://www.python.org/downloads/windows/
4. Durante la instalación, activa Add Python to PATH.
5. Abre la carpeta extraída.
6. Haz doble clic en start.bat.

## Uso

Escribe `ayuda` para consultar los comandos.

Ejemplos:

- `hola`
- `calcula 25 * (8 + 2)`
- `guardar nota: estudiar Python`
- `ver notas`
- `hora`

## Estado del proyecto

RAED AI se encuentra en una etapa inicial.
Todavía no incluye un modelo generativo ni búsqueda web integrada.

## Privacidad

Las notas se guardan localmente en `raed_memory.db`.
No introduzcas información sensible en equipos compartidos.

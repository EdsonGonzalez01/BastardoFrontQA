# Bastardo Front QA

Este repositorio contiene pruebas automatizadas end-to-end (E2E) para el frontend de Bastardo utilizando Pytest y Selenium.

## Requisitos Previos

- Python 3.12 o superior
- Google Chrome
- ChromeDriver (compatible con tu versión de Chrome)
- Node.js (para el servidor WebSocket)

## Instalación

1. Crear y activar un entorno virtual:
```bash
python -m venv .env
# En Windows:
.env\Scripts\activate
# En Linux/Mac:
source .env/bin/activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Configuración

Asegúrate de que:
1. El ChromeDriver está instalado y en tu PATH
2. El servidor WebSocket está ejecutándose en `localhost:3000`
3. El frontend de la aplicación está ejecutándose

## Ejecución de Pruebas

### Ejecutar todas las pruebas:
```bash
pytest
```

### Ejecutar pruebas con salida detallada:
```bash
pytest -v
```

### Ejecutar pruebas con prints en consola:
```bash
pytest -s
```

### Ejecutar un archivo de prueba específico:
```bash
pytest e2e/tests/test_new_room.py
```

### Ejecutar una prueba específica:
```bash
pytest e2e/tests/test_new_room.py::test_create_room_with_ws_simulation
```

## Estructura del Proyecto

```
├── conftest.py           # Configuración global de pytest
├── requirements.txt      # Dependencias del proyecto
└── e2e/
    ├── pages/           # Page Objects
    │   ├── lobby_page.py
    │   └── new_room_page.py
    └── tests/           # Archivos de prueba
        ├── test_lobby.py
        └── test_new_room.py
```

## Descripción de las Pruebas

### test_lobby.py
- `test_set_name_shows_welcome_and_options`: Verifica que el nombre del jugador se muestra correctamente
- `test_local_storage_after_set_name`: Verifica el almacenamiento local después de establecer el nombre
- `test_navigation_buttons`: Verifica la navegación entre páginas

### test_new_room.py
- `test_create_room_persists_room_id`: Verifica la persistencia del ID de sala
- `test_validation_errors_on_empty_fields`: Verifica validaciones de campos vacíos
- `test_create_room_with_ws_simulation`: Prueba la creación de sala con simulación WebSocket

## TODO Ejecución en CI/CD

Las pruebas están configuradas para ejecutarse en GitHub Actions. Ver el archivo `.github/workflows/pytest.yml` para más detalles.

Para ejecutar las pruebas en modo headless (sin interfaz gráfica):
```bash
pytest --headless
```

## Solución de Problemas

### Error de ChromeDriver
Si ves el error "Can not find chromedriver for currently installed chrome version":
1. Verifica tu versión de Chrome: `google-chrome --version`
2. Descarga el ChromeDriver correspondiente
3. Asegúrate de que ChromeDriver está en tu PATH

### Error de WebSocket
Si las pruebas fallan con errores de conexión WebSocket:
1. Verifica que el servidor WebSocket está ejecutándose en puerto 3000
2. Verifica que no hay firewalls bloqueando la conexión

## Contribución

1. Fork el repositorio
2. Crea una rama para tu feature: `git checkout -b feature/nueva-prueba`
3. Commit tus cambios: `git commit -am 'Añade nueva prueba'`
4. Push a la rama: `git push origin feature/nueva-prueba`
5. Crea un Pull Request

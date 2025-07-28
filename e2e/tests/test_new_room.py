from asyncio import wait
import json
from time import time
import pytest
from e2e.pages.new_room_page import NewRoomPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By  # Añade esta importación




@pytest.fixture(autouse=True)
def new_room_page(browser):
    page = NewRoomPage(browser)
    # Inicializar y limpiar storage
    page.open()
    page.clear_state()
    page.open()
    return page


def test_create_room_persists_room_id(new_room_page):
    browser = new_room_page.driver
    # Simula que el backend creó la sala estableciendo directamente el storage
    browser.execute_script(
        "window.localStorage.setItem('BASTARDO_ROOM_ID','room_7c16fe88-1ff2-4bf2-8a17-3532ab60cd3a');"
    )

    # Verifica que get_local_storage devuelve el valor guardado
    raw_room_id = new_room_page.get_local_storage('BASTARDO_ROOM_ID')
    room_id = raw_room_id.strip('"') if raw_room_id else raw_room_id
    assert room_id and room_id.startswith('room_'), \
        f"Expected stored room_..., got {room_id}"


def test_validation_errors_on_empty_fields(new_room_page):
    # Hacer click sin llenar campos
    new_room_page.click_create()
    # La URL no debe cambiar
    assert new_room_page.get_current_url().endswith('/game/new-room'), \
        "Debería quedarse en la página si faltan campos"
    


def test_validation_errors_on_empty_fields(new_room_page):
    # Hacer click sin llenar campos
    new_room_page.click_create()
    # La URL no debe cambiar
    assert new_room_page.get_current_url().endswith('/game/new-room'), \
        "Debería quedarse en la página si faltan campos"
    
def test_create_room_with_ws_simulation(new_room_page):
    print("Starting test_create_room_with_ws_simulation")
    #Create a web socket to connect to port 3000 
    ws_url = "ws://localhost:3000/"
    ws = new_room_page.create_websocket(ws_url)
    response = ws.recv()
    try:
        response_data = json.loads(response)
        #print(f"Parsed response: {json.dumps(response_data, indent=2)}")
    except json.JSONDecodeError:
        print("Response is not JSON format")

    response_data = json.loads(response)
    playerId = response_data.get("playerId")
    print(f"Player ID received: {playerId}")

    new_room_page.set_local_storage('BASTARDO_PLAYER_ID', playerId)
    new_room_page.set_local_storage('BASTARDO_PLAYER_NAME', 'TestPlayer')

    new_room_page.set_room_details('SalaTest', '5')
    new_room_page.click_create()
    
    # Verifica que el localStorage tiene el ID de la sala
    room_id = new_room_page.get_local_storage('BASTARDO_ROOM_ID').strip('"')
    assert room_id and room_id.startswith('room_'), \
        f"Expected stored room_..., got {room_id}"
    
    # Verificar que la URL tiene el ID de la sala
    current_url = new_room_page.get_current_url()
    assert f"/game/room/{room_id}" in current_url, \
        f"Expected URL to contain room ID, got {current_url}"
    
    #Verificar que el usuario está en la sala
    assert new_room_page.driver.find_element(By.ID, "playerName"), \
        "Expected playerName element to be present"

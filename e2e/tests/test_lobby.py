# e2e/tests/test_lobby.py
import pytest
from e2e.pages.lobby_page import LobbyPage

@pytest.fixture(autouse=True)
def lobby_page(browser):
    """
    Fixture que recibe el browser de conftest,
    abre la página, limpia localStorage y recarga antes de cada test.
    """
    page = LobbyPage(browser)

    # 1) Abre la página por primera vez
    page.open()

    # 2) Limpia localStorage
    page.clear_state()

    # 3) Recarga para partir con storage limpio
    page.open()

    return page


def test_set_name_shows_welcome_and_options(lobby_page):
    test_name = "Edson"
    lobby_page.set_name(test_name)

    welcome = lobby_page.get_welcome_text()
    assert test_name in welcome, "El label de bienvenida debe incluir el nombre"

    assert lobby_page.are_option_buttons_visible(), \
        "Los botones Find/Create Room deben ser visibles"


def test_local_storage_after_set_name(lobby_page):
    test_name = "Edson"
    lobby_page.set_name(test_name)

    # Validar localStorage (strip de comillas si existen)
    raw_player_id = lobby_page.get_local_storage("BASTARDO_PLAYER_ID")
    raw_player_name = lobby_page.get_local_storage("BASTARDO_PLAYER_NAME")
    # Elimina comillas alrededor si las hay
    player_id = raw_player_id.strip('"') if raw_player_id else raw_player_id
    player_name = raw_player_name.strip('"') if raw_player_name else raw_player_name

    assert player_id is not None and player_id.startswith("player_"), \
        f"Player ID incorrecto: {player_id}"
    assert player_name == test_name, \
        f"Player name en storage no coincide: {player_name}"


def test_navigation_buttons(lobby_page):
    # Setear nombre para habilitar botones
    lobby_page.set_name("TestUser")

    # Find Room redirige a /game/rooms
    lobby_page.click_find_room()
    assert "/game/rooms" in lobby_page.get_current_url(), \
        f"URL incorrecta después de Find Room: {lobby_page.get_current_url()}"
    
    # Volver al lobby, limpiar y recargar
    lobby_page.open()
    lobby_page.clear_state()
    lobby_page.open()
    lobby_page.set_name("TestUser")

    # Create Room redirige a /game/new-room
    lobby_page.click_create_room()
    assert "/game/new-room" in lobby_page.get_current_url(), \
        f"URL incorrecta después de Create Room: {lobby_page.get_current_url()}"
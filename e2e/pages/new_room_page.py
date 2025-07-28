from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from websocket import create_connection

class NewRoomPage:
    URL = "http://localhost:4200/game/new-room"

    def __init__(self, driver, timeout: int = 5):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        # Selectores
        self.room_name_input     = (By.CSS_SELECTOR, "app-input[placeholder='Enter room name'] input")
        self.capacity_input      = (By.CSS_SELECTOR, "app-input[placeholder='Enter room capacity'] input")
        self.create_room_button  = (By.CSS_SELECTOR, "app-button[label='Create Room'] button")

    def open(self):
        """Carga la página de creación de sala y espera los inputs"""
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self.room_name_input))

    def clear_state(self):
        """Limpia localStorage para aislar tests"""
        # Remueve claves usadas
        script = (
            "window.localStorage.removeItem('BASTARDO_PLAYER_ID');"
            "window.localStorage.removeItem('BASTARDO_PLAYER_NAME');"
            "window.localStorage.removeItem('BASTARDO_ROOM_ID');"
        )
        self.driver.execute_script(script)

    def set_room_details(self, name: str, capacity: str):
        """Llena los inputs de nombre y capacidad"""
        name_input = self.wait.until(EC.element_to_be_clickable(self.room_name_input))
        name_input.clear()
        name_input.send_keys(name)

        cap_input = self.wait.until(EC.element_to_be_clickable(self.capacity_input))
        cap_input.clear()
        cap_input.send_keys(capacity)

    def click_create(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.create_room_button))
        btn.click()

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_local_storage(self, key: str) -> str:
        return self.driver.execute_script(
            "return window.localStorage.getItem(arguments[0]);", key
        )
    
    def set_local_storage(self, key: str, value: str):
        """Establece un valor en localStorage"""
        self.driver.execute_script(
            "window.localStorage.setItem(arguments[0], arguments[1]);", key, f'"{value}"'
        )
    
    def create_websocket(self, url: str):
        """Crea un WebSocket para simular la conexión al backend"""
        ws = create_connection(url)
        return ws
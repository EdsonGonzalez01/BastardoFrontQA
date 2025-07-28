from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LobbyPage:
    URL = "http://localhost:4200"

    def __init__(self, driver, timeout: int = 5):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        # Selectores
        self.name_input      = (By.CSS_SELECTOR, ".lobby app-input input")
        self.set_name_btn    = (By.CSS_SELECTOR, ".lobby app-button[label='Set Name'] button")
        self.welcome_label   = (By.CSS_SELECTOR, ".lobby h2 label")
        self.find_room_btn   = (By.CSS_SELECTOR, ".options app-button[label='Find Room'] button")
        self.create_room_btn = (By.CSS_SELECTOR, ".options app-button[label='Create Room'] button")
        self.room_name_input     = (By.CSS_SELECTOR, "app-input[placeholder='Enter room name'] input")
        self.capacity_input      = (By.CSS_SELECTOR, "app-input[placeholder='Enter room capacity'] input")
        self.create_room_button  = (By.CSS_SELECTOR, "app-button[label='Create Room'] button")

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self.name_input))

    def clear_state(self):
        self.driver.execute_script("window.localStorage.clear();")

    def set_name(self, name: str):
        inp = self.wait.until(EC.element_to_be_clickable(self.name_input))
        inp.clear()
        inp.send_keys(name)
        btn = self.wait.until(EC.element_to_be_clickable(self.set_name_btn))
        btn.click()
        self.wait.until(EC.text_to_be_present_in_element(self.welcome_label, name))

    def get_welcome_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.welcome_label)).text

    def are_option_buttons_visible(self) -> bool:
        find_btn = self.wait.until(EC.visibility_of_element_located(self.find_room_btn))
        create_btn = self.wait.until(EC.visibility_of_element_located(self.create_room_btn))
        return find_btn.is_displayed() and create_btn.is_displayed()

    def get_local_storage(self, key: str) -> str:
        return self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)

    def click_find_room(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.find_room_btn))
        btn.click()

    def click_create_room(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.create_room_btn))
        btn.click()

    def get_current_url(self) -> str:
        return self.driver.current_url
    
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
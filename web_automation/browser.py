from time import sleep
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium import webdriver
from selenium.webdriver import Edge
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from utils.logger import logger
from utils.helpers import esperar_elemento, get_name_user_web
from utils.constants import *

def configBrowser():
    try:
        service = Service(EdgeChromiumDriverManager().install())
        option = webdriver.EdgeOptions()
        # option.add_argument("--headless")
        option.add_argument("--window-size=1366 ,768")
        driver = Edge(service=service, options=option)
        return driver
    except WebDriverException as e:
        logger.error(f'Error en la configuraicon de browser')

def go_to_portal(driver, url):
    if not url or not url.startswith("http"):
        logger.error(f"URL NO VÁLIDA O NO ENCONTRADA: {url}")
        raise ValueError(f"URL inválida: {url}")

    try:
        driver.get(url)
        logger.info("página cargada correctamente")
    except WebDriverException as e:
        logger.error(f"Error al cargar la paguina: {e}")


def login(driver, user):
    logger.debug(f"datos entrantes -> {driver}, {user}")
    try:
        email_input = esperar_elemento(driver, By.NAME, LOGIN_EMAIL_NAME, 3)
        password_input = esperar_elemento(driver, By.ID,LOGIN_PASSWORD_ID , 3)
        login_button = esperar_elemento(driver, By.CLASS_NAME, LOGIN_BUTTON_NAME, 3)

        if not all([email_input, password_input, login_button]):
            logger.error(
                "No se encontraron todos los elementos necesarios para el login"
            )
            return False

        email_input.send_keys(user[USER_EMAIL])
        password_input.send_keys(user[USER_PASSWORD])
        login_button.click()

        # Esperar breve antes de validar si se mostró un error
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.TAG_NAME, BODY_NAME))
        )

        # Validación de login fallido
        if driver.find_elements(By.CLASS_NAME,ALERT_CLASS):
            logger.warning("Credenciales inválidas.")
            return False
        # Validar si estan los elementos de cerrar session o la seccion de recibos tambien el nombre e usuario
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, XPATH_LOGOUT)
                )
            )
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        XPATH_LIST,
                    )
                )
            )

            logger.info(f"Login exitoso como: {get_name_user_web(driver)}")
            return True
        except TimeoutException:
            logger.warning(
                "No se encontró el enlace de cerrar sesión. Probable fallo de login."
            )
            return False

    except Exception as e:
        logger.error(f"Fallo login -> {e}")
        return False


def logout(driver):
    try:
        # Paso 1: Click para abrir el menú desplegable
        menu_toggle = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME,DROPDOWN_CLASS ))
        )
        menu_toggle.click()

        # Paso 2: Esperar y hacer clic en "Cerrar sesión"
        logout_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, XPATH_LOGOUT))
        )

        logger.info(f"Logout exitoso del usuario: {get_name_user_web(driver)}")
        logout_button.click()
        return True

    except Exception as e:
        logger.warning(f"No se pudo hacer logout: {e}")
        return False




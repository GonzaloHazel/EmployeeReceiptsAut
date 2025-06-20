from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import logger


def esperar_elemento(driver, by, value, timeout=10):
    """
    Espera hasta que un elemento esté presente en el DOM.

    :param driver: WebDriver de Selenium
    :param by: tipo de localizador (By.ID, By.NAME, etc)
    :param value: valor del localizador
    :param timeout: tiempo máximo de espera en segundos
    :return: el WebElement si se encuentra, None si no
    """
    try:
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))
    except TimeoutException:
        logger.warning(f"Elemento no encontrado: {by}={value} después de {timeout}s")
        return None


def get_name_user_web(driver):
    # Extraer nombre de usuario
    nombre_elemento = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "name"))
    )
    return nombre_elemento.text.strip()


def fetchall_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from utils.logger import logger
from utils.helpers import esperar_elemento, get_name_user_web
from utils.constants import *


def recipts_by_year(driver, year="2025"):
    try:
        recipts_secction = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    XPATH_LIST,
                )
            )
        )
        recipts_secction.click()
        header = esperar_elemento(driver, By.CLASS_NAME, "pane-header", 5)

        if header:
            logger.info("Se ingerso correctamente al panel de recibos!")
            select_element = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.ID,
                        "anio",
                    )
                )
            )
            select = Select(select_element)
            select.select_by_value(str(year))
            recipts_table = esperar_elemento(
                driver, By.CSS_SELECTOR, ".table-responsive table.table tbody", 5
            )
            recipts = recipts_table.find_elements(By.TAG_NAME, "tr")
            logger.info(f"total de datos encontrados -> {len(recipts)}")
            for recipt in recipts:
                uuid = recipt.find_element(By.NAME, "uuid")
                logger.info(f'uuid -> {uuid.get_attribute("value")}')

    except WebDriverException as e:
        logger.error(f"Error fallo en la busqueda de recibos: {e}")

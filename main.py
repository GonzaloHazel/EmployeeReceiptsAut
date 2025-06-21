from web_automation.browser import *
from database.db_manager import *
from utils.logger import logger
from dotenv import load_dotenv
import os

from web_automation.receipt_scraper import recipts_by_year


def main():
    logger.info("Inicio de ejecucion ok!")
    load_dotenv()
    try:
        driver = configBrowser()
        url = os.getenv("URL_")
        logger.info(f"Cargando url -> {url}")
        users = get_users()

        for user in users:
            go_to_portal(driver, url)
            success = login(driver, user)
            if success:
                recipts_by_year(driver)
                logout(driver)

    except Exception as e:
        logger.exception(f"Ocurrio un error critico: {e}")
    finally:
        driver.quit()  # quitas el navegador
        logger.info("Fin de la ejecucion")


if __name__ == "__main__":
    main()

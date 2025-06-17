from web_automation.browser import *
from database.db_manager import *
from utils.logger import logger
from dotenv import load_dotenv
import os


def main():
    logger.info("Inicio de ejecucion ok!")
    load_dotenv()
    try:
        driver = configBrowser()
        url = os.getenv("URL_")
        logger.info(f"Cargando url -> {url}")
        go_to_portal(driver, url)
        users = get_users()

        for user in users:
            success = login(driver, user)
            if success:
                recipts_by_year(driver)

    except Exception as e:
        logger.exception(f"Ocurrio un error critico: {e}")
    finally:
        driver.quit()  # quitas el navegador
        logger.info("Fin de la ejecucion")


if __name__ == "__main__":
    main()

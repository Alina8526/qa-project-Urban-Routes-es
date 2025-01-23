import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriv
import json
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import DesiredCapabilities
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""


    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code

#Cambios usando los tres selectores
class UrbanRoutesPage:
    from_field = (By.ID, 'from')  # Selector por ID
    to_field = (By.ID, 'to')  # Selector por ID
    tarifa_comfort_option = (By.ID, 'comfort')  # Selector por ID
    telefono_input = (By.ID, 'telefono')  # Selector por ID
    agregar_tarjeta_button = (By.ID, 'add-card-btn')  # Selector por ID
    cvv_input = (By.ID, 'code')  # Selector por ID
    mensaje_input = (By.CSS_SELECTOR, '#mensaje')  # Selector por CSS
    manta_checkbox = (By.CLASS_NAME, 'manta')  # Selector por ClassName
    pañuelos_checkbox = (By.XPATH, '//input[@id="pañuelos"]')  # Selector por XPath
    helados_input = (By.XPATH, '//*[@id="helados"]')  # Selector por XPath
    buscar_taxi_modal = (By.CSS_SELECTOR, '#buscar-taxi-modal')  # Selector por CSS
    info_conductor = (By.CLASS_NAME, 'info-conductor')  # Selector por ClassName

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def select_tarifa_comfort(self):
        self.driver.find_element(*self.tarifa_comfort_option).click()

    def fill_telefono(self, telefono):
        self.driver.find_element(*self.telefono_input).send_keys(telefono)

    def agregar_tarjeta(self, cvv):
        self.driver.find_element(*self.agregar_tarjeta_button).click()
        self.driver.find_element(*self.cvv_input).send_keys(cvv)
        # Simulamos que el campo pierde el foco
        self.driver.find_element(*self.cvv_input).send_keys(Keys.TAB)

    def write_mensaje(self, mensaje):
        self.driver.find_element(*self.mensaje_input).send_keys(mensaje)

    def pedir_manta_y_pañuelos(self):
        self.driver.find_element(*self.manta_checkbox).click()
        self.driver.find_element(*self.pañuelos_checkbox).click()

    def pedir_helados(self, cantidad):
        helados_input = self.driver.find_element(*self.helados_input)
        helados_input.send_keys(str(cantidad))
#Cambios
    def esperar_modal_taxi(self):
        # Espera inteligente en lugar de time.sleep
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.buscar_taxi_modal))
        return self.driver.find_element(*self.buscar_taxi_modal).is_displayed()

    def esperar_info_conductor(self):
        # Espera inteligente para la info del conductor
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.info_conductor))
        return self.driver.find_element(*self.info_conductor).is_displayed()



class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)
#Cambios
    def test_set_from(self):
        self.driver.get("URL_DE_TU_APLICACION")
        routes_page = UrbanRoutesPage(self.driver)
        address_from = "Calle Falsa 123"
        routes_page.set_from(address_from)
        assert routes_page.get_from() == address_from

    def test_set_to(self):
        self.driver.get("URL_DE_TU_APLICACION")
        routes_page = UrbanRoutesPage(self.driver)
        address_to = "Avenida Siempre Viva 456"
        routes_page.set_to(address_to)
        assert routes_page.get_to() == address_to

    def test_select_tarifa_comfort(self):
        self.driver.get("URL_DE_TU_APLICACION")
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_tarifa_comfort()
        # Verifica que la tarifa Comfort esté seleccionada correctamente (puedes verificar si el estado de un checkbox o un elemento cambia)
        comfort_selected = self.driver.find_element(*self.tarifa_comfort_option).is_selected()
        assert comfort_selected, "La tarifa Comfort no está seleccionada correctamente."

    def test_fill_telefono(self):
        self.driver.get("URL_DE_TU_APLICACION")
        routes_page = UrbanRoutesPage(self.driver)
        phone_number = "123456789"
        routes_page.fill_telefono(phone_number)
        # Verifica que el número de teléfono se haya ingresado correctamente
        entered_phone = routes_page.driver.find_element(*self.telefono_input).get_attribute("value")
        assert entered_phone == phone_number, f"El número de teléfono ingresado es {entered_phone}, debería ser {phone_number}."

    def test_agregar_tarjeta(self):
        self.driver.get("URL_DE_TU_APLICACION")
        routes_page = UrbanRoutesPage(self.driver)
        cvv_code = "123"
        routes_page.agregar_tarjeta(cvv_code)
        # Verifica si el campo de CVV perdió el enfoque correctamente (puedes verificar si el campo CVV ya no está enfocado)
        cvv_value = routes_page.driver.find_element(*self.cvv_input).get_attribute("value")
        assert cvv_value == cvv_code, f"El código CVV ingresado es {cvv_value}, debería ser {cvv_code}."

    def test_write_mensaje(self):
        self.driver.get("URL_DE_TU_APLICACION")
        routes_page = UrbanRoutesPage(self.driver)
        message = "Necesito un taxi urgente"
        routes_page.write_mensaje(message)
        # Verifica que el mensaje se haya escrito correctamente
        entered_message = routes_page.driver.find_element(*self.mensaje_input).get_attribute("value")
        assert entered_message == message, f"El mensaje ingresado es {entered_message}, debería ser {message}."

    def test_pedir_manta_y_pañuelos(self):
        self.driver.get("URL_DE_TU_APLICACION")
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.pedir_manta_y_pañuelos()
        # Verifica que los checkboxes de manta y pañuelos estén seleccionados
        manta_selected = self.driver.find_element(*self.manta_checkbox).is_selected()
        pañuelos_selected = self.driver.find_element(*self.pañuelos_checkbox).is_selected()
        assert manta_selected, "La manta no fue seleccionada."
        assert pañuelos_selected, "Los pañuelos no fueron seleccionados."

    def test_pedir_helados(self):
        self.driver.get("URL_DE_TU_APLICACION")
        routes_page = UrbanRoutesPage(self.driver)
        cantidad_helados = 2
        routes_page.pedir_helados(cantidad_helados)
        # Verifica que la cantidad de helados ingresada sea la correcta
        helados_quantity = routes_page.driver.find_element(*self.helados_input).get_attribute("value")
        assert helados_quantity == str(cantidad_helados), f"La cantidad de helados ingresada es {helados_quantity}, debería ser {cantidad_helados}."

    def test_esperar_modal_taxi(self):
        self.driver.get("URL_DE_TU_APLICACION")
        routes_page = UrbanRoutesPage(self.driver)
        assert routes_page.esperar_modal_taxi()

    def test_esperar_info_conductor(self):
        self.driver.get("URL_DE_TU_APLICACION")
        routes_page = UrbanRoutesPage(self.driver)
        assert routes_page.esperar_info_conductor()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
        
if __name__ == "__main__":
    unittest.main()
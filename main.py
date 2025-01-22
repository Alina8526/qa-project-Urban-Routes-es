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


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    tarifa_comfort_option = (By.ID, 'comfort')
    telefono_input = (By.ID, 'telefono')
    agregar_tarjeta_button = (By.ID, 'add-card-btn')
    cvv_input = (By.ID, 'code')  # Suponiendo que el campo CVV tiene id='code'
    mensaje_input = (By.ID, 'mensaje')
    manta_checkbox = (By.ID, 'manta')
    pañuelos_checkbox = (By.ID, 'pañuelos')
    helados_input = (By.ID, 'helados')
    buscar_taxi_modal = (By.ID, 'buscar-taxi-modal')
    info_conductor = (By.ID, 'info-conductor')

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

    def esperar_modal_taxi(self):
        time.sleep(2)  # Esperar a que aparezca el modal
        return self.driver.find_element(*self.buscar_taxi_modal).is_displayed()

    def esperar_info_conductor(self):
        time.sleep(2)  # Esperar a que se muestre la información del conductor
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

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        address_from = "Calle Falsa 123"
        address_to = "Avenida Siempre Viva 456"
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)

        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

        # Paso 2: Seleccionar tarifa Comfort
        routes_page.select_tarifa_comfort()

        # Paso 3: Rellenar número de teléfono
        phone_number = "123456789"
        routes_page.fill_telefono(phone_number)

        # Paso 4: Agregar tarjeta
        cvv_code = "123"  # Suponiendo que el código CVV es "123"
        routes_page.agregar_tarjeta(cvv_code)

        # Paso 5: Escribir mensaje
        message = "Necesito un taxi urgente"
        routes_page.write_mensaje(message)

        # Paso 6: Pedir manta y pañuelos
        routes_page.pedir_manta_y_pañuelos()

        # Paso 7: Pedir 2 helados
        routes_page.pedir_helados(2)

        # Paso 8: Esperar modal de búsqueda de taxi
        assert routes_page.esperar_modal_taxi()

        # Paso 9: Esperar información del conductor
        assert routes_page.esperar_info_conductor()




    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
        
if __name__ == "__main__":
    unittest.main()
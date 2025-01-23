Karla Alina Ramirez Valadez Proyecto Sprint 8

Urban Routes
Descripción del Proyecto
Urban Routes es una aplicación web que permite a los usuarios solicitar un taxi, configurar su viaje, seleccionar tarifas, agregar información de pago y solicitar elementos adicionales como mantas y helados. La aplicación está automatizada con pruebas de integración que cubren todo el proceso de solicitud de un taxi, desde la configuración de la dirección hasta la obtención de información del conductor.

Tecnologías y Técnicas Utilizadas
Python: El lenguaje de programación utilizado para escribir las pruebas automatizadas.

Para instalar Python en macOS, Windows y Linux, sigue estas instrucciones:
macOS:
Si usas Homebrew, puedes instalar Python con:
brew install python

También puedes descargarlo desde python.org y seguir las instrucciones de instalación.

Windows:
Ve a python.org, descarga el instalador de la última versión de Python y sigue las instrucciones. Asegúrate de marcar la opción "Add Python to PATH" durante la instalación.

Linux:
En distribuciones basadas en Debian/Ubuntu, puedes instalar Python con:
sudo apt update
sudo apt install python3
En Fedora o CentOS:
sudo dnf install python3

Selenium WebDriver: Para la automatización de las pruebas de la interfaz de usuario en navegadores web.

Para instalar Selenium, usa el siguiente comando en todos los sistemas operativos:
pip install selenium
unittest: Framework de pruebas unitarias en Python (incluido por defecto con Python). No es necesario instalarlo por separado, ya que viene con la instalación estándar de Python.

ChromeDriver: Para interactuar con el navegador Chrome. Necesitarás descargar el ChromeDriver compatible con tu versión de Chrome desde este enlace. A continuación, te indico cómo configurarlo según el sistema operativo:

macOS:
Descarga ChromeDriver desde el enlace anterior.
Mueve el archivo descargado a una carpeta en tu directorio, como ~/chromedriver/.
Si deseas, puedes agregar la ruta del ChromeDriver a tu variable de entorno:
export PATH=$PATH:/ruta/a/chromedriver/
Windows:
Descarga ChromeDriver desde el enlace anterior.
Extrae el archivo descargado y guarda chromedriver.exe en una carpeta de tu elección.
Agrega la ruta de esa carpeta a las variables de entorno del sistema.
Linux:
Descarga ChromeDriver desde el enlace anterior.
Extrae el archivo y mueve chromedriver a un directorio como /usr/local/bin/:
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

JSON: Para manejar las respuestas y el código de confirmación del teléfono. El módulo json es parte de la biblioteca estándar de Python, por lo que no es necesario instalarlo.

Instrucciones para Ejecutar las Pruebas
Instalar las dependencias: Si aún no tienes Selenium instalado, puedes hacerlo con el siguiente comando:
pip install selenium
Ejecutar las pruebas: Una vez que hayas instalado las dependencias necesarias, puedes ejecutar las pruebas con el siguiente comando:
pytest path/Alina8526/qa-project-Urban-Routes-es.py


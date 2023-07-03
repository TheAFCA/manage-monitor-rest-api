import requests
from mixer.backend.django import mixer
import unittest
from manage_monitor.django_apps.customer.models import Customer

class MiTestDeIntegracion(unittest.TestCase):
    def test_post_endpoint(self):
        url = 'http://localhost:8000/api/customers/add/'  # Reemplaza con la URL correcta de tu servidor

        # Datos de ejemplo para enviar en la solicitud POST
        customer_data = mixer.blend(Customer)

        # Realiza la solicitud POST al servidor
        response = requests.post(url, data=customer_data)

        import pdb
        pdb.set_trace()
        # Verifica el código de estado de la respuesta
        self.assertEqual(response.status_code, 201)  # Reemplaza con el código de estado esperado

        # Verifica los datos de respuesta si es necesario
        response_data = response.json()
        # ... verifica los datos de respuesta según tu caso de uso

if __name__ == '__main__':
    unittest.main()
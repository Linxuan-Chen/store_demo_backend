from locust import HttpUser, task, between
from random import randint


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    host = 'http://127.0.0.1:8000'

    @task(2)
    def view_products(self) -> None:
        self.client.get('/api/store/collections/', name='/api/store/collections/')

    @task(4)
    def view_a_product(self):
        self.client.get(f'/api/store/products/{randint(12, 13)}/',
                        name='/api/store/products/:id/')

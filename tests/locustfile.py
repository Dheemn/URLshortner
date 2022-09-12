from random import choice
import string
from time import sleep
from locust import HttpUser, task


def generate_random_links() -> str:
    end_list = ['.com', 'co.in', '.in', '.org', '.xyz', '.aero', '.ag',
                '.space', '.ai', '.beer', '.az', '.build', '.cafe', 'kitty']
    url = (''.join(choice(string.ascii_uppercase + string.ascii_lowercase
                          + string.digits) for i in range(10)))
    if choice([0, 1]):
        url = 'http://' + url
    url = url + choice(end_list)

    # This generates the paths in the url
    if choice([1, 100]) % 2:
        length = choice([0, 6])
        for i in range(length):
            path = (''.join(choice(string.ascii_uppercase +
                                   string.ascii_lowercase + string.digits)
                            for i in range(choice([2, 20]))))
            url = f'{url}/{path}'
        return url
    return url


class HelloWorldUser(HttpUser):

    @task
    def hello_world(self):
        self.client.get("/")

    @task
    def pass_urls(self):
        for i in range(10):
            url_data = generate_random_links()
            self.client.post("/new/", data={'url': url_data})
            sleep(1)

    @task
    def check_redirect_speed(self):
        pass

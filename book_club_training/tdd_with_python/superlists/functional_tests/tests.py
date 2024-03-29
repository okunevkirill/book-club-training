from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import os
import time

MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
    """Тест нового посетителя"""

    def setUp(self):
        """Установка"""
        self.browser = webdriver.Chrome()
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = f"http://{staging_server}"

    def tearDown(self):
        """Демонтаж"""
        time.sleep(3)
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """Подтверждение строки в таблице списка"""
        start_time = time.perf_counter()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.perf_counter() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        """Тест: можно начать список для одного пользователя"""

        # Эдит слышала про крутое новое онлайн-приложение со списком
        # неотложных дел. Она решает оценить его домашнюю страницу
        self.browser.get(self.live_server_url)

        # Она видит, что заголовок и шапка страницы
        # говорят о списках неотложных дел
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # Ей сразу же предлагается ввести элемент списка
        input_box = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(input_box.get_attribute("placeholder"), "Enter a to-do item")

        # Она набирает в текстовом поле "Купить павлиньи перья" (ее хобби –
        # вязание рыболовных мушек)
        input_box.send_keys("Купить павлиньи перья")

        # Когда она нажимает enter, страница обновляется, и теперь страница
        # содержит "1: Купить павлиньи перья" в качестве элемента списка
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        self.wait_for_row_in_list_table("1: Купить павлиньи перья")

        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент.
        # Она вводит "Сделать мушку из павлиньих перьев" (Эдит очень методична)
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Сделать мушку из павлиньих перьев")
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # Страница снова обновляется, и теперь показывает оба элемента ее списка
        self.wait_for_row_in_list_table("2: Сделать мушку из павлиньих перьев")
        self.wait_for_row_in_list_table("1: Купить павлиньи перья")
        # Удовлетворенная, она снова ложится спать.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """Тест: многочисленные пользователи могут начать списки по разным url"""
        # Эдит начинает новый список
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Купить павлиньи перья")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Купить павлиньи перья")
        # Она замечает, что ее список имеет уникальный URL-адрес
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # Теперь новый пользователь, Фрэнсис, приходит на сайт.
        # [*] Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
        # [*] информация от Эдит не прошла через данные cookie и пр.
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Фрэнсис посещает домашнюю страницу. Нет никаких признаков списка Эдит
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Купить павлиньи перья", page_text)
        self.assertNotIn("Сделать мушку", page_text)

        # Фрэнсис начинает новый список, вводя новый элемент. Он менее
        # интересен, чем список Эдит...
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Купить молоко")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Купить молоко")

        # Фрэнсис получает уникальный URL-адрес
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Опять-таки, нет ни следа от списка Эдит
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Купить павлиньи перья", page_text)
        self.assertIn("Купить молоко", page_text)

        # Удовлетворенные, они оба ложатся спать

    def test_layout_and_styling(self):
        """Тест макета и стилевого оформления"""
        # Эдит открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        canvas_x_offset = self.browser.execute_script(
            "return window.screenX + (window.outerWidth - "
            "window.innerWidth) / 2 - window.scrollX;"
        )

        # Она замечает, что поле ввода аккуратно центрировано
        input_box = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            input_box.location["x"] + canvas_x_offset + input_box.size["width"] / 2,
            512,
            delta=10,
        )

        # Она начинает новый список и видит, что поле ввода там тоже
        # аккуратно центрировано
        input_box.send_keys("testing")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: testing")
        input_box = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            input_box.location["x"] + canvas_x_offset + input_box.size["width"] / 2,
            512,
            delta=10,
        )

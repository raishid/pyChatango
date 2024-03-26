from playwright.sync_api import sync_playwright, Browser, Page
from .tempDir import temp_dir

"""
    pyChatango is a simple library to send messages to Chatango chatrooms
    :param chatango_link: link to the chatango chatroom
    :param login: Chatango username
    :param password: Password of the Chatango account
"""


class pyChatango:
    driver: Browser = None
    page: Page = None
    chatango_link: str = None
    chat_iframe = None
    credentials = None

    def __init__(self, chatango_link: str, login: str, password: str) -> None:
        print("Iniciando Navegador Playwright")
        self.chatango_link = chatango_link
        self._initChrome()
        self.credentials = {"login": login, "password": password}

    def _initChrome(self):
        args = ["--start-maximized", "--disable-blink-features=AutomationControlled"]
        args.append("--headless=new")
        self.driver = (
            sync_playwright()
            .start()
            .chromium.launch_persistent_context(
                user_data_dir=temp_dir(),
                channel="chrome",
                headless=False,
                no_viewport=True,
                args=args,
                ignore_default_args=["--enable-automation"],
            )
        )
        self.page = self.driver.pages[0]
        self.page.goto(self.chatango_link)
        self.page.wait_for_load_state("domcontentloaded")

        self.page.wait_for_timeout(3000)

        self.chat_iframe = self.page.wait_for_selector(
            "#flashcontent > iframe", timeout=5000
        ).content_frame()

    def _verify_login(self):
        if (
            self.chat_iframe.wait_for_selector(
                "#LOGIN", strict=False, state="attached", timeout=10000
            ).get_attribute("style")
            == "display: none;"
        ):
            return True

        return False

    def _login(self):
        self.chat_iframe.wait_for_selector("#LOGIN > div", timeout=10000).click()
        self.page.wait_for_timeout(3000)
        self.chat_iframe.wait_for_selector(
            ".login-dialog #full-username-input", timeout=10000
        ).fill(self.credentials["login"])
        self.page.wait_for_timeout(1000)
        self.chat_iframe.wait_for_selector(
            ".login-dialog #full-password-input", timeout=10000
        ).fill(self.credentials["password"])

        self.chat_iframe.wait_for_selector(
            ".login-dialog #full-loginbtn-wrapper > div", timeout=10000
        ).click()

        self.page.wait_for_timeout(3000)

        if (
            self.chat_iframe.wait_for_selector(
                "#LOGIN", strict=False, state="attached", timeout=10000
            ).get_attribute("style")
            == "display: none;"
        ):
            print("Login Exitoso")
            return

        Exception("Error en el Login")

    """
        Send a message to the chatroom
        :param message: Message to send
    """

    def chat(self, message: str):
        if not self._verify_login():
            self._login()

        self.chat_iframe.wait_for_selector("#input-field").fill(message)
        self.page.wait_for_timeout(1000)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(1000)

        print(f"Mensaje Enviado: {message}")

    def quit(self):
        self.driver.close()

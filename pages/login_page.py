class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error = page.locator("[data-test='error']")
        
    def open(self):
        self.page.goto("/")
        
    def login(self,user, password):
        self.username.fill(user)
        self.password.fill(password)
        self.login_button.click()
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
import sqlite3

# Definindo cores
primary_color = get_color_from_hex("#4CAF50")  # verde
secondary_color = get_color_from_hex("#FFC107")  # amarelo
background_color = get_color_from_hex("#FFFFFF")  # branco

Window.clearcolor = background_color

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            last_name TEXT NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            gender TEXT,
                            repeat_password TEXT)''')
        self.conn.commit()

    def register_user(self, name, last_name, email, password, gender, repeat_password):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''INSERT INTO users (name, last_name, email, password, gender, repeat_password) 
                              VALUES (?, ?, ?, ?, ?, ?)''', (name, last_name, email, password, gender, repeat_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login_user(self, email, password):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE email = ? AND password = ?''', (email, password))
        user = cursor.fetchone()
        return user

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=(30, 30, 30, 30))

        self.name_input = TextInput(hint_text="Nome", multiline=False, background_color=(1, 1, 1, 0.8))
        self.last_name_input = TextInput(hint_text="Sobrenome", multiline=False, background_color=(1, 1, 1, 0.8))
        self.email_input = TextInput(hint_text="E-mail", multiline=False, background_color=(1, 1, 1, 0.8))
        self.password_input = TextInput(hint_text="Senha", password=True, multiline=False, background_color=(1, 1, 1, 0.8))
        self.repeat_password_input = TextInput(hint_text="Repita a Senha", password=True, multiline=False, background_color=(1, 1, 1, 0.8))
        self.gender_input = TextInput(hint_text="Gênero", multiline=False, background_color=(1, 1, 1, 0.8))
        self.register_button = Button(text="Registrar", size_hint=(None, None), size=(100, 50), background_color=primary_color)
        self.register_button.bind(on_press=self.register_user)
        back_button = Button(text="Voltar", size_hint=(None, None), size=(100, 50), background_color=secondary_color)
        back_button.bind(on_press=self.go_back_to_login)

        layout.add_widget(Label(text="Registrar", font_size=36, color=(0, 0, 0, 1)))
        layout.add_widget(self.name_input)
        layout.add_widget(self.last_name_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.repeat_password_input)
        layout.add_widget(self.gender_input)
        layout.add_widget(self.register_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def register_user(self, instance):
        name = self.name_input.text
        last_name = self.last_name_input.text
        email = self.email_input.text
        password = self.password_input.text
        repeat_password = self.repeat_password_input.text
        gender = self.gender_input.text

        if password != repeat_password:
            self.show_popup("Erro", "As senhas não coincidem.")
            return

        db = Database()
        if db.register_user(name, last_name, email, password, gender, repeat_password):
            self.show_popup("Registro bem-sucedido", "Usuário registrado com sucesso!")
            self.go_back_to_login(None)
        else:
            self.show_popup("Erro", "E-mail já cadastrado.")

    def go_back_to_login(self, instance):
        self.parent.current = 'login'

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=(30, 30, 30, 30))

        self.email_input = TextInput(hint_text="E-mail", multiline=False, background_color=(1, 1, 1, 0.8))
        self.password_input = TextInput(hint_text="Senha", password=True, multiline=False, background_color=(1, 1, 1, 0.8))
        login_button = Button(text="Login", size_hint=(None, None), size=(100, 50), background_color=primary_color)
        login_button.bind(on_press=self.check_login)
        forgot_password_button = Button(text="Esqueci a senha", size_hint=(None, None), size=(150, 50), background_color=secondary_color)
        forgot_password_button.bind(on_press=self.go_to_forgot_password)
        register_button = Button(text="Registrar", size_hint=(None, None), size=(100, 50), background_color=secondary_color)
        register_button.bind(on_press=self.go_to_register)

        layout.add_widget(Label(text="Bem-vindo!", font_size=36, color=(0, 0, 0, 1)))
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.add_widget(forgot_password_button)
        layout.add_widget(register_button)

        self.add_widget(layout)

    def check_login(self, instance):
        email = self.email_input.text
        password = self.password_input.text

        db = Database()
        user = db.login_user(email, password)
        if user:
            print("Login bem-sucedido")
            print("Usuário:", user)
            self.parent.current = 'home'
        else:
            self.show_popup("Login Falhou", "Usuário ou senha incorretos.")

    def go_to_register(self, instance):
        self.parent.current = 'register'

    def go_to_forgot_password(self, instance):
        self.parent.current = 'forgot_password'

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()

class ForgotPasswordScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=(30, 30, 30, 30))

        self.email_input = TextInput(hint_text="E-mail", multiline=False, background_color=(1, 1, 1, 0.8))
        recover_button = Button(text="Recuperar", size_hint=(None, None), size=(100, 50), background_color=primary_color)
        recover_button.bind(on_press=self.recover_password)
        back_button = Button(text="Voltar", size_hint=(None, None), size=(100, 50), background_color=secondary_color)
        back_button.bind(on_press=self.go_back_to_login)

        layout.add_widget(Label(text="Esqueci a Senha", font_size=36, color=(0, 0, 0, 1)))
        layout.add_widget(self.email_input)
        layout.add_widget(recover_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def recover_password(self, instance):
        # Aqui você pode implementar a lógica de recuperação de senha via e-mail
        # Por enquanto, vamos apenas exibir uma mensagem
        self.show_popup("Recuperar Senha", "Instruções de recuperação de senha enviadas para o seu e-mail.")

    def go_back_to_login(self, instance):
        self.parent.current = 'login'

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        tabs = TabbedPanel(do_default_tab=False)
        cursos_tab = TabbedPanelHeader(text='Cursos')
        trilhas_tab = TabbedPanelHeader(text='Trilhas')
        comunidade_tab = TabbedPanelHeader(text='Comunidade')
        perguntas_tab = TabbedPanelHeader(text='Perguntas')
        artigos_tab = TabbedPanelHeader(text='Artigos')

        tabs.add_widget(cursos_tab)
        tabs.add_widget(trilhas_tab)
        tabs.add_widget(comunidade_tab)
        tabs.add_widget(perguntas_tab)
        tabs.add_widget(artigos_tab)

        layout.add_widget(tabs)

        # Adicione a área abaixo do TabbedPanel
        layout.add_widget(Label(text="Área com níveis: iniciante, intermediário e avançado"))

        self.add_widget(layout)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(ForgotPasswordScreen(name='forgot_password'))
        sm.add_widget(HomeScreen(name='home'))  # Adicionando a nova tela
        return sm

if __name__ == "__main__":
    MyApp().run()


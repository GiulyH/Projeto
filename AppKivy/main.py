from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

import pyrebase

# Configuração do Firebase
config = {
    "apiKey": "sua-api-key",
    "authDomain": "seu-auth-domain",
    "databaseURL": "sua-database-url",
    "projectId": "dados-1a530",
    "storageBucket": "seu-storage-bucket",
    "messagingSenderId": "seu-messaging-sender-id",
    "appId": "seu-app-id"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

class LoginScreen(Screen):
    ...
    def login(self, instance):
        username = self.username.text
        password = self.password.text
        try:
            user = auth.sign_in_with_email_and_password(username, password)
            # Usuário autenticado com sucesso
        except:
            # Falha na autenticação
            pass

    def signup(self, instance):
        self.manager.current = 'Signup'

class SignupScreen(Screen):
    ...
    def register(self, instance):
        name = self.name.text
        email = self.email.text
        dob = self.dob.text
        cpf = self.cpf.text
        try:
            user = auth.create_user_with_email_and_password(email, cpf)
            # Usuário criado com sucesso
        except:
            # Falha ao criar usuário
            pass
    ...


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        layout.add_widget(Label(text="Username"))
        self.username = TextInput(multiline=False)
        layout.add_widget(self.username)

        layout.add_widget(Label(text="Password"))
        self.password = TextInput(password=True, multiline=False)
        layout.add_widget(self.password)

        layout.add_widget(Button(text="Login", on_press=self.login))
        layout.add_widget(Button(text="Sign Up", on_press=self.signup))

    def login(self, instance):
        username = self.username.text
        password = self.password.text
        # Aqui você pode adicionar a lógica de autenticação com o banco de dados

    def signup(self, instance):
        self.manager.current = 'Signup'


class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super(SignupScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        layout.add_widget(Label(text="Name"))
        self.name = TextInput(multiline=False)
        layout.add_widget(self.name)

        layout.add_widget(Label(text="Email"))
        self.email = TextInput(multiline=False)
        layout.add_widget(self.email)

        layout.add_widget(Label(text="Date of Birth"))
        self.dob = TextInput(multiline=False)
        layout.add_widget(self.dob)

        layout.add_widget(Label(text="CPF"))
        self.cpf = TextInput(multiline=False)
        layout.add_widget(self.cpf)

        layout.add_widget(Button(text="Register", on_press=self.register))
        layout.add_widget(Button(text="Back", on_press=self.back))

    def register(self, instance):
        name = self.name.text
        email = self.email.text
        dob = self.dob.text
        cpf = self.cpf.text
        # Aqui você pode adicionar a lógica para registrar os detalhes do usuário no banco de dados

    def back(self, instance):
        self.manager.current = 'Login'


class ForgotPasswordScreen(Screen):
    def __init__(self, **kwargs):
        super(ForgotPasswordScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        layout.add_widget(Label(text="Enter your email"))
        self.email = TextInput(multiline=False)
        layout.add_widget(self.email)

        layout.add_widget(Button(text="Send Reset Email", on_press=self.send_reset_email))
        layout.add_widget(Button(text="Back", on_press=self.back))

    def send_reset_email(self, instance):
        email = self.email.text
        # Aqui você pode adicionar a lógica para enviar um e-mail de redefinição de senha

    def back(self, instance):
        self.manager.current = 'Login'


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='Login'))
        sm.add_widget(SignupScreen(name='Signup'))
        sm.add_widget(ForgotPasswordScreen(name='ForgotPassword'))
        return sm


if __name__ == '__main__':
    MyApp().run()

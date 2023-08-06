import os
import openai
from rich.traceback import Traceback
from rich.markdown import Markdown
from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

from terminal_chatgpt.spinner import Spinner

console = Console(color_system="256")
kb = KeyBindings()
session = PromptSession()


@kb.add('escape', 'enter')
def _(event):
    event.current_buffer.insert_text('\n')


@kb.add('enter')
def _(event):
    event.current_buffer.validate_and_handle()


def _get_api_key():
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        return api_key

    file_path = os.path.expanduser("~/.openai_api_key")
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            api_key = f.read().strip()
    else:
        console.print(Markdown(
            f"API key file at `{file_path}` not found! "
            f"If you have no idea what I'm talking about "
            f"check out the following page: https://platform.openai.com/account/api-keys"))
        api_key = input('Enter api key: ').strip()

        with open(file_path, "w") as f:
            f.write(api_key)
        console.print(Markdown(f"API key file has been saved at `{file_path}`"))
    return api_key


class Core:
    DEFAULT_SYSTEM_MESSAGE = "You are a helpful assistant. " \
                             "In markdown output always specify language. " \
                             "User can use `new` command to start conversation or chat, " \
                             "`exit` command to quit the conversation."

    BOT_EMOJI = '🤖'
    USER_EMOJI = '🙂'

    def _set_init_state(self):
        self.messages = [
            {
                "role": "system",
                "content": self.system_message
            }
        ]

    def __init__(self, system_message=None):
        openai.api_key = _get_api_key()
        self.system_message = system_message or self.DEFAULT_SYSTEM_MESSAGE
        self.first_prompt = None
        self._set_init_state()

    def _add_message(self, prompt: str) -> str:
        self.messages.append({'role': 'user', 'content': prompt})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
                n=1)
            response_message = response['choices'][0]['message']
        except Exception:
            self._exit_with_traceback()

        self.messages.append(response_message)
        return response_message.get('content')

    @staticmethod
    def _is_quit_prompt(prompt: str) -> bool:
        return prompt.strip().lower() in ['q', 'quit', 'exit', 'e', 'end', 'goodbye']

    @staticmethod
    def _is_empty_prompt(prompt: str) -> bool:
        return prompt.strip().lower() in ['', '\n']

    @staticmethod
    def _is_new_dialog(prompt: str) -> bool:
        return prompt.strip().lower() in ['clear', 'c', 'new']

    def _render_response(self, response):
        try:
            console.print(Markdown(f"{self.BOT_EMOJI}: {response}"), end='\n')
            print()
        except Exception:
            self._exit_with_traceback()

    @staticmethod
    def _clear_screen():
        os.system('clear')

    @staticmethod
    def _exit_with_traceback(exit_code=1):
        console.print(Traceback())
        exit(exit_code)

    def _ask_for_input(self):
        if self.first_prompt:
            users_prompt = self.first_prompt
            self.first_prompt = None
        else:
            users_prompt = session.prompt(
                message=f'{self.USER_EMOJI}: ',
                multiline=True,
                key_bindings=kb)
        return users_prompt

    @staticmethod
    def speak(text):
        os.system('osascript -e "say \\"{}\\" "'.format(text))

    def run(self, first_prompt=None):
        self.first_prompt = first_prompt
        while True:
            prompt = self._ask_for_input()

            if self._is_quit_prompt(prompt):
                exit(0)

            if self._is_empty_prompt(prompt):
                continue

            if self._is_new_dialog(prompt):
                self._clear_screen()
                self._set_init_state()
                continue

            print()
            with Spinner(f'{self.BOT_EMOJI} '):
                response = self._add_message(prompt)
            # self.speak(response)
            self._render_response(response)

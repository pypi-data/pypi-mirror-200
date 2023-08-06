from halo import Halo


class Spinner:
    def __init__(self, text=''):
        self.text = text
        self.spinner = Halo(text=text, spinner='dots', placement='right')

    def __enter__(self):
        self.spinner.start()
        return self.spinner

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.spinner.stop()

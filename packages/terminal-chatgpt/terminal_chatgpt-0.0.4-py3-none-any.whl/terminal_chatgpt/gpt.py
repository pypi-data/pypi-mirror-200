import click

from terminal_chatgpt.core import Core


@click.command()
@click.argument('first_prompt', nargs=-1)
@click.option('-s', '--system-message', help='Initial system message for gpt')
def gpt_entry_point(first_prompt, system_message):
    core = Core(system_message=system_message)
    first_prompt = ' '.join(first_prompt)
    core.run(first_prompt)


if __name__ == '__main__':
    gpt_entry_point()

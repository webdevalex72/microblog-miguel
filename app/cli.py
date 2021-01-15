import os
import click


"""
модуль app/cli.py, который реализует несколько команд быстрого 
доступа для управления языковыми переводами. В этом случае 
переменная current_app не работает, поскольку эти команды 
регистрируются при запуске, а не во время обработки запроса, 
который является единственным моментом, когда current_app 
может использоваться. Чтобы удалить ссылку на приложение 
в этом модуле, я прибегнул к другому трюку, который 
заключается в перемещении этих пользовательских команд 
внутри функции register(), которая принимает экземпляр app в качестве аргумента
---------------
Затем я вызвал эту функцию register() из microblog.py.
"""


def register(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass


    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d app/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')


    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d app/translations'):
            raise RuntimeError('compile command failed')


    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d app/translations -l ' + lang):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')
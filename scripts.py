from subprocess import run

def test():
    """
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover`
    """
    run(['python', '-m', 'unittest', 'discover'])

def dev():
    """
    Run project. Equivalent to:
    `poetry run python ./src/app.py`
    """
    run(['python', './src/app.py'])
import os


def path_normalizer(filepath: str):
    filepath = filepath.strip()
    if not filepath:
        return False
    if filepath in ('.', '..', '/', '\\'):
        return False

    if filepath.count('.') == 0:
        filepath += '.csv'

    if not filepath.endswith('.csv'):
        return False

    filepath = os.path.normpath(filepath)

    return filepath

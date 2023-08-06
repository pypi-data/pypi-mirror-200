def pyproject():
    return 'pyproject.toml'

def get_pyproject():
    with open(pyproject()) as file:
        return file.read()

def semantic_version_pattern():
    return r'version\s+=\s+"(\d+[.]\d+[.])(\d+)"'

def get_pyproject_version(text):
    return re.search(
        semantic_version_pattern(),
        text
    ).group(1, 2)

def update_pyproject_version():
    text = get_pyproject()
    version, patch = get_pyproject_version(text)
    write_file(
        filepath=pyproject(),
        data=re.sub(
            semantic_version_pattern(),
            f'version = "{version}{int(patch)+1}"',
            text
        )
    )
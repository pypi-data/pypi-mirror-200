from setuptools import setup, Extension

setup(
    # See pyproject.toml for most of the config metadata
    packages=['gopac'],
    ext_modules=[
        Extension(
            'gopac.extension.gopaccli',
            ['extension/src/gopaccli/gopaccli.go']
        ),
    ],
    build_golang_cli={'root': 'extension'},
)

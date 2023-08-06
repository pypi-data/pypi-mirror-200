from setuptools import setup

name = "types-flake8-simplify"
description = "Typing stubs for flake8-simplify"
long_description = '''
## Typing stubs for flake8-simplify

This is a PEP 561 type stub package for the `flake8-simplify` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`flake8-simplify`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/flake8-simplify. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `34018d6a2c9833de7c5718a70b5346245f583a73`.
'''.lstrip()

setup(name=name,
      version="0.20.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/flake8-simplify.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['flake8_simplify-stubs'],
      package_data={'flake8_simplify-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

# Python Encrypted File System

[![Made with Python](https://img.shields.io/badge/Python->=3.10-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")
[![Python package](https://github.com/joumaico/pyefs/actions/workflows/python-package.yml/badge.svg)](https://github.com/joumaico/pyefs/actions/workflows/python-package.yml)
[![Upload Python Package](https://github.com/joumaico/pyefs/actions/workflows/python-publish.yml/badge.svg)](https://github.com/joumaico/pyefs/actions/workflows/python-publish.yml)

PyEFS: A Python module for encrypting and decrypting files using the Fernet encryption algorithm.

## Installation

```console
$ pip install pyefs
```

## Usage

### Creating a new encryption key

To create a new encryption key, you can use the `generate_key()` method of the `SecureFile` class:

```python
from pyefs import SecureFile

key = SecureFile.generate_key()
```

### Encrypting a file

To encrypt a file, you can create a `SecureFile` object with the filename and encryption key, then call the `encrypt()` method:

```python
from pyefs import SecureFile

key = SecureFile.generate_key()

# create a file with some text
with open(filename, 'w') as f:
    f.write("This is a test file.")

# encrypt the file
sf = SecureFile(filename, key)
sf.encrypt()
```

By default, the `encrypt()` method reads the content of the file and overwrites it with the encrypted content. You can also provide a `bytes` object to encrypt and write to the file instead of the file's content:

```python
# encrypt a custom content
content = b"This is a custom content."
sf.encrypt(content)
```

### Decrypting a file

To decrypt a file, you can create a `SecureFile` object with the filename and encryption key, then call the `decrypt()` method:

```python
# decrypt the file
sf = SecureFile(filename, key)
sf.decrypt()
```

If the decryption fails, the `decrypt()` method returns `None`.

## Links
* PyPI Releases: https://pypi.org/project/pyefs
* Source Code: https://github.com/joumaico/pyefs

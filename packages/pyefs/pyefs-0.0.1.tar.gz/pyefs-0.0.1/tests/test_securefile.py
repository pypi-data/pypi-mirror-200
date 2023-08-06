from pyefs import SecureFile

import os


def test_encrypt_decrypt():
    filename = "testfile.txt"

    key = SecureFile.generate_key()

    # create a file with some text
    with open(filename, 'w') as f:
        f.write("This is a test file.")

    # encrypt the file and check if it's dencrypted
    sf = SecureFile(filename, key)
    sf.encrypt()
    assert os.path.getsize(filename) > 0
    assert sf.decrypt() == b"This is a test file."

    # clean up
    os.remove(filename)

from random import randbytes


class Encryptor:
    def __init__(self, book="book"):
        self.book = open(book, 'rb')

    def __del__(self):
        self.book.close()

    def encrypt_sym(self, sym: int):
        key = ord(self.book.read(1))
        return sym - key

    def encrypt_bytes(self, row: bytes, buffer=2, byteorder="little"):
        encrypted = []
        for sym in row:
            encrypted.append(self.encrypt_sym(sym=sym).to_bytes(buffer, byteorder, signed=True))
        return bytes().join(encrypted)


class Decryptor:
    def __init__(self, book="book"):
        self.book = open(book, 'rb')

    def __del__(self):
        self.book.close()

    def decrypt_sym(self, sym: int):
        key = ord(self.book.read(1))
        return key + sym

    def decrypt_bytes(self, row: bytes, buffer=2, byteorder="little"):
        decrypted = []
        for i in range(0, len(row), buffer):
            decrypted.append(self.decrypt_sym(int.from_bytes(row[i:i + 2], byteorder, signed=True)))
        return bytes(decrypted)


class Generator:
    def __init__(self, randomizer=randbytes):
        self.randomizer = randomizer

    def generate_book(self, filename: str, book_size: int, max_size_passing=104857600):
        with open(filename, 'wb') as book:
            full_passages = book_size // max_size_passing
            last_passage_len = book_size % max_size_passing
            for _ in range(full_passages):
                book.write(self.randomizer(max_size_passing))
            book.write(self.randomizer(last_passage_len))

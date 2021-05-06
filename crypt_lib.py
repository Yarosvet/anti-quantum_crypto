from random import randbytes


class Book:
    def __init__(self, book="book"):
        self.book = open(book, 'rb+')
        self.length = self.book.seek(0, 2)
        self.position = 0

    def __del__(self):
        self.book.close()

    def read(self):
        self.book.seek(self.position - 1, 2)
        self.position -= 1
        return self.book.read(1)

    def erase_end(self):
        self.book.truncate(self.length + self.position)
        self.book.flush()
        self.length = self.book.seek(0, 2)
        self.position = 0


class Encryptor(Book):
    def __init__(self, book="book"):
        super().__init__(book)

    def encrypt_sym(self, sym: int):
        key = ord(self.read())
        return sym - key

    def encrypt_bytes(self, row: bytes, buffer=2, byteorder="little"):
        encrypted = []
        for sym in row:
            encrypted.append(self.encrypt_sym(sym=sym).to_bytes(buffer, byteorder, signed=True))
        return bytes().join(encrypted)


class Decryptor(Book):
    def __init__(self, book="book"):
        super().__init__(book)

    def decrypt_sym(self, sym: int):
        key = ord(self.read())
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

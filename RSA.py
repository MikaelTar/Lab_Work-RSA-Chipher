import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog
import random
from math import gcd

class RSAApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RSA Encryption/Decryption")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        self.message_label = QLabel("Message:")
        self.message_input = QTextEdit()
        self.layout.addWidget(self.message_label)
        self.layout.addWidget(self.message_input)

        self.keys_layout = QHBoxLayout()
        self.public_key_label = QLabel("Public Key (n, e):")
        self.public_key_display = QLineEdit()
        self.keys_layout.addWidget(self.public_key_label)
        self.keys_layout.addWidget(self.public_key_display)

        self.private_key_label = QLabel("Private Key (n, d):")
        self.private_key_display = QLineEdit()
        self.keys_layout.addWidget(self.private_key_label)
        self.keys_layout.addWidget(self.private_key_display)

        self.layout.addLayout(self.keys_layout)

        self.generate_keys_button = QPushButton("Generate Keys")
        self.generate_keys_button.clicked.connect(self.generate_keys)
        self.layout.addWidget(self.generate_keys_button)

        self.encrypt_button = QPushButton("Encrypt")
        self.encrypt_button.clicked.connect(self.encrypt_message)
        self.layout.addWidget(self.encrypt_button)

        self.encrypted_label = QLabel("Encrypted Message:")
        self.encrypted_display = QLineEdit()
        self.layout.addWidget(self.encrypted_label)
        self.layout.addWidget(self.encrypted_display)

        self.decrypt_button = QPushButton("Decrypt")
        self.decrypt_button.clicked.connect(self.decrypt_message)
        self.layout.addWidget(self.decrypt_button)

        self.decrypted_label = QLabel("Decrypted Message:")
        self.decrypted_display = QTextEdit()
        self.layout.addWidget(self.decrypted_label)
        self.layout.addWidget(self.decrypted_display)

        self.central_widget.setLayout(self.layout)
        self.encrypted_string = []
        self.decrypted_string = []
        self.p = self.q = self.n = self.e = self.d = None

    def is_prime(self, num):
        if num < 2:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

    def generate_large_prime(self, bits=8):
        while True:
            num = random.getrandbits(bits)
            if self.is_prime(num):
                return num

    def generate_keys(self):
        p = self.generate_large_prime()
        q = self.generate_large_prime()
        n = p * q
        fi = (p - 1) * (q - 1)

        e = random.randint(2, fi - 1)
        while gcd(e, fi) != 1:
            e = random.randint(2, fi - 1)
        d = self.mod_inverse(e, fi)

        self.p = p
        self.q = q
        self.n = n
        self.e = e
        self.d = d

        self.public_key_display.setText(f"({self.n}, {self.e})")
        self.private_key_display.setText(f"({self.n}, {self.d})")

    def mod_inverse(self, a, m):
        g, x, y = self.extended_gcd(a, m)
        if g != 1:
            return None
        else:
            return x % m

    def extended_gcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.extended_gcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def encrypt_message(self):
        message = self.message_input.toPlainText()
        if not message:
            return
        if self.n is None or self.e is None:
            return
        m = 0
        self.encrypted_string = []
        for char in message:
            m = ord(char)
            c = pow(m, self.e)%self.n
            self.encrypted_string.append(str(c))
        self.encrypted_display.setText('|'.join(self.encrypted_string))

    def decrypt_message(self):
        if not self.encrypted_string:
            return
        if self.n is None or self.d is None:
            return
        self.decrypted_string = []
        for char in self.encrypted_string:
            char = int(char)
            m = chr(pow(char, self.d)%self.n)
            self.decrypted_string.append(m)
        self.decrypted_display.setPlainText(''.join(self.decrypted_string))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    rsa_app = RSAApp()
    rsa_app.show()
    sys.exit(app.exec_())
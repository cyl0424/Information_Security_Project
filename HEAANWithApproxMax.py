import os
import math
import numpy as np
import piheaan as heaan
from piheaan.math import sort, approx

class HEAANWithApproxMax:
    def __init__(self):
        self.parameters = heaan.ParameterPreset.FGb
        self.context = heaan.make_context(self.parameters)
        self.key_directory = "./keys"
        self.evaluator = None
        self.decryptor = None
        self.encryptor = None
        self.secret_key = None
        self.public_key = None
        self.log_slots = 15
        self.num_slots = 2 ** self.log_slots

        self.initialize()

    def initialize(self):
        heaan.make_bootstrappable(self.context)
        self.load_or_generate_keys()
        self.evaluator = heaan.HomEvaluator(self.context, self.public_key)
        self.decryptor = heaan.Decryptor(self.context)
        self.encryptor = heaan.Encryptor(self.context)

    def load_or_generate_keys(self):
        secret_key_path = os.path.join(self.key_directory, "secretkey.bin")
        public_key_path = os.path.join(self.key_directory, "public_key")

        if not os.path.exists(secret_key_path) or not os.path.exists(public_key_path):
            self.secret_key = heaan.SecretKey(self.context)
            key_generator = heaan.KeyGenerator(self.context, self.secret_key)
            key_generator.gen_common_keys()
            key_generator.save(self.key_directory)
        else:
            self.secret_key = heaan.SecretKey(self.context, secret_key_path)

        self.public_key = heaan.KeyPack(self.context, self.key_directory)
        self.public_key.load_enc_key()
        self.public_key.load_mult_key()

    def encrypt_message(self, message):
        ciphertext = heaan.Ciphertext(self.context)
        self.encryptor.encrypt(message, self.public_key, ciphertext)
        return ciphertext

    def decrypt_message(self, ciphertext):
        decrypted_message = heaan.Message(self.log_slots)
        self.decryptor.decrypt(ciphertext, self.secret_key, decrypted_message)
        return decrypted_message

    def create_n_values_msg(self, n):
        message = heaan.Message(self.log_slots)
        for i in range(self.num_slots):
            message[i] = n
        return self.encrypt_message(message)

    def define_c0(self, c, cs):
        temp_msg = self.sub_message(c, cs)
        print("temp_msg")
        print(temp_msg)
        return self.sign_message(temp_msg)

    def define_c_0_prime(self, c0):
        msg_one = self.create_n_values_msg(1)
        msg_half = self.create_n_values_msg(0.5)
        temp_res = self.add_message(c0, msg_one)
        return self.mult_message(temp_res, msg_half)

    def define_c1(self, c0):
        result_sum_all_slots = heaan.Ciphertext(self.context)
        self.evaluator.rot_sum([c0 for _ in range(self.num_slots)], [n for n in range(self.num_slots)], result_sum_all_slots)
        return result_sum_all_slots

    def broadcast_c1(self, c1):
        return self.create_n_values_msg(self.decrypt_message(c1)[0])


    def define_c_2(self, c1):
        msg_m = self.create_n_values_msg(1 / self.num_slots)
        temp_res = self.mult_message(c1, msg_m)
        return self.sign_message(temp_res)

    def calculate_cout(self, c_0_prime, c2):
        c_2_prime = self.define_c_0_prime(c2)
        c3 = self.sub_message(c_2_prime, self.create_n_values_msg(1))
        c4 = self.sub_message(c_0_prime, self.create_n_values_msg(1))
        c_2_prime_c4 = self.mult_message(c4, c_2_prime)
        c_0_prime_c3 = self.mult_message(c_0_prime, c3)

        negative_cout = self.add_message(c_2_prime_c4, c_0_prime_c3)

        result_negate = heaan.Ciphertext(self.context)
        self.evaluator.negate(negative_cout, result_negate)

        return result_negate

    def calculate_cout(self, c_0_prime, c2):
        c_2_prime = self.define_c_0_prime(c2)

        c3 = self.sub_message(c_2_prime, self.create_n_values_msg(1))
        c4 = self.sub_message(c_0_prime, self.create_n_values_msg(1))

        c_2_prime_c4 = self.mult_message(c4, c_2_prime)
        c_0_prime_c3 = self.mult_message(c_0_prime, c3)

        return self.sub_message(c_2_prime_c4, c_0_prime_c3)
    def calculate_ctmp(self, c2, i):
        c2_doubled = self.create_n_values_msg(2 * self.decrypt_message(c2)[0])
        return self.mult_message(c2_doubled, self.create_n_values_msg(0.5 ** i))

    def define_c_tmp(self, ciphertext, i):
        msg_one = self.create_n_values_msg(1)
        msg_two = self.create_n_values_msg(2)

        c2_twice = self.mult_message(ciphertext, msg_two)

        sub_one = self.sub_message(c2_twice, msg_one)

        msg_half = self.create_n_values_msg(0.5 ** i)

        result = self.mult_message(sub_one, msg_half)

        return result

    def update_cs(self, cs, ctmp):
        return self.add_message(cs, ctmp)

    def k_approx_max(self, c, k):

        i = 0

        cs = self.create_n_values_msg(0.5)

        while True:
            print("c")
            print(c)
            c0 = self.define_c0(c, cs)
            print("c0")
            print(c0)
            c_0_prime = self.define_c_0_prime(c0)
            print("c_0_prime")
            print(c_0_prime)
            c1 = self.define_c1(c0)
            print("c1")
            print(c1)
            c2 = self.define_c_2(c1)
            print("c2")
            print(c2)
            i += 1
            if i == k:
                cout = self.calculate_cout(c_0_prime, c2)
                print("cout")
                print(cout)
                return cout
            ctmp = self.define_c_tmp(c2, i)
            print("ctmp")
            print(ctmp)
            cs = self.update_cs(cs, ctmp)
            print("cs")
            print(cs)

    def add_message(self, ciphertext1, ciphertext2):
        result_add = heaan.Ciphertext(self.context)
        self.evaluator.add(ciphertext1, ciphertext2, result_add)
        return result_add

    def sub_message(self, ciphertext1, ciphertext2):
        result_sub = heaan.Ciphertext(self.context)
        self.evaluator.sub(ciphertext1, ciphertext2, result_sub)
        return result_sub

    def mult_message(self, ciphertext1, ciphertext2):
        result_mult = heaan.Ciphertext(self.context)
        self.evaluator.mult(ciphertext1, ciphertext2, result_mult)
        return result_mult

    def sign_message(self, ciphertext):
        result_sign = heaan.Ciphertext(self.context)
        approx.sign(self.evaluator, ciphertext, result_sign)
        return result_sign

    def send_data(self, matrix_data, n, s):
        self.n = n
        self.s = s
        split_matrixes = self.split_matrix(matrix_data, self.n, self.s)
        messages = []

        for i in range(len(split_matrixes)):
            message = heaan.Message(self.log_slots)
            for j, value in enumerate(split_matrixes[i]):
                message[j] = value
            messages.append(message)

        encrypt_messages = [self.encrypt_message(message=i) for i in messages]
        return encrypt_messages

    def split_matrix(self, matrix, n, s):
        h, w = matrix.shape
        padded_size = max(h, w)
        padded_matrix = np.full((padded_size, padded_size), 0.5)
        padded_matrix[:h, :w] = matrix
        self.log_slots = int(math.ceil(math.log(n ** 2, 2)))
        self.num_slots = 2 ** self.log_slots
        lists = []

        for i in range(0, padded_size - n + 1, s):
            for j in range(0, padded_size - n + 1, s):
                window = [padded_matrix[x][y] for x in range(i, i + n) for y in range(j, j + n)]
                if len(window) < self.num_slots:
                    window.extend([-0.5] * (self.num_slots - len(window)))
                lists.append(window)

        return lists

    def receive_data(self, encrypt_messages):
        max_elements = []
        for i in encrypt_messages:
            decrypt_message = self.decrypt_message(ciphertext=i)
            max_elements.append(decrypt_message[0])
        result = self.reshape_list_to_matrix(max_elements)
        return result

    def reshape_list_to_matrix(self, lst):
        n = len(lst)
        size = int(np.sqrt(n))
        if size * size != n:
            raise ValueError("리스트의 길이는 정확한 행렬 크기의 제곱이어야 합니다.")
        matrix = np.array(lst).reshape(size, size)
        return matrix


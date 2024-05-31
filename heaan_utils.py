# import psutil
import math, os
import numpy as np
import piheaan as heaan
from piheaan.math import sort, approx


class HEAAN:
    def __init__(self):
        # HEAAN 암호화 시스템 초기화
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

        # 윈도우 사이즈: n*n
        self.n = 2

        # stride: s
        self.s = 2

        self.i = 0

    def initialize(self):
        # HEAAN 암호화 시스템 초기화
        heaan.make_bootstrappable(self.context)

        # 키 로드 또는 생성
        self.load_or_generate_keys()

        # 암호화 관련 객체 초기화
        self.evaluator = heaan.HomEvaluator(self.context, self.public_key)
        self.decryptor = heaan.Decryptor(self.context)
        self.encryptor = heaan.Encryptor(self.context)

    def load_or_generate_keys(self):
        # 키가 존재하는지 확인하고, 없으면 생성하여 저장
        secret_key_path = os.path.join(self.key_directory, "secretkey.bin")
        public_key_path = os.path.join(self.key_directory, "public_key")

        if not os.path.exists(secret_key_path) or not os.path.exists(public_key_path):
            # 비밀 키 생성 및 저장
            self.secret_key = heaan.SecretKey(self.context)
            key_generator = heaan.KeyGenerator(self.context, self.secret_key)
            key_generator.gen_common_keys()
            key_generator.save(self.key_directory)
        else:
            # 이미 생성된 키 로드
            self.secret_key = heaan.SecretKey(self.context, secret_key_path)

        # 공개 키 로드
        self.public_key = heaan.KeyPack(self.context, self.key_directory)
        self.public_key.load_enc_key()
        self.public_key.load_mult_key()

    def encrypt_message(self, message):
        # 메시지 암호화
        ciphertext = heaan.Ciphertext(self.context)
        self.encryptor.encrypt(message, self.public_key, ciphertext)

        # 암호문 반환
        return ciphertext

    def decrypt_message(self, ciphertext):
        # 암호문 복호화
        decrypted_message = heaan.Message(self.log_slots)
        self.decryptor.decrypt(ciphertext, self.secret_key, decrypted_message)

        # 복호화된 메시지 반환
        return decrypted_message

    # 윈도우 사이즈에 맞춰서 log_slots 조정
    def calculate_send_log_slots(self, n):
        log_value = math.log(n ** 2, 2)

        # 로그 값에 가장 가까운 정수로 올림
        rounded_log = math.ceil(log_value)

        # send_log_slots 값을 결정
        send_log_slots = max(2, min(rounded_log, 15))
        self.log_slots = send_log_slots
        return send_log_slots

    # log_slots에 맞춰서 num_slots 조정
    def set_num_slots(self, log_slots):
        self.num_slots = 2 ** log_slots
        return 2 ** log_slots

    # 메시지를 암호화하여 서버측으로 보내는걸 가정하고 구현한 함수
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

        print(f"messages: {messages}")
        encrypt_messages = [self.encrypt_message(message=i) for i in messages]
        return encrypt_messages

    # 암호화한 데이터 내림차순 정렬
    def sort_encrypt_messages(self, encrypt_messages):
        # 정렬된 암호문을 담기 위한 list
        sorted_messages = []

        # list에 담긴 암호문을 각각 정렬 (piheaan의 내장함수 사용)
        for i in encrypt_messages:
            ciphertext_out_sort = heaan.Ciphertext(self.context)
            sort.sort(self.evaluator, i, ciphertext_out_sort, self.num_slots, False)

            sorted_messages.append(ciphertext_out_sort)

        # print(f"sort: {sorted_messages}\n")

        # 정렬된 암호문 list 반환
        return sorted_messages

    # Approximating Max Function을 이용해서 최댓값 찾기
    def max_encrypt_messages(self, encrypt_messages):
        # 정렬된 암호문을 담기 위한 list
        sorted_messages = []

        # list에 담긴 암호문을 각각 정렬 (자체구현 함수 사용)
        for i in encrypt_messages:
            ciphertext_out_sort = self.approx_max(i, 2)
            sorted_messages.append(ciphertext_out_sort)

        print(f"sort: {sorted_messages}\n")

        # 정렬된 암호문 list 반환
        return sorted_messages

    def split_matrix(self, matrix, n, s):
        # 입력 행렬의 크기
        h, w = len(matrix), len(matrix[0])

        # Determine the padding required for height and width
        padded_size = max(h, w)
        padded_matrix = np.full((padded_size, padded_size), 255.0)  # Fill with padding value 255

        # Copy original matrix into the padded matrix
        padded_matrix[:h, :w] = matrix

        # print(f"padded_matrix: {padded_matrix}\n")

        # 윈도우 사이즈에 맞춰 log_slots, num_slots 값 변경
        self.calculate_send_log_slots(n)
        self.set_num_slots(self.log_slots)

        # max값을 찾기위해 비교해야하는 수의 집합들을 담을 list
        lists = []

        # max값을 찾기위해 비교해야하는 수의 집합으로 matrix 분할
        for i in range(0, padded_size - n + 1, s):
            for j in range(0, padded_size - n + 1, s):
                window = [padded_matrix[x][y] for x in range(i, i + n) for y in range(j, j + n)]

                # 데이터의 길이가 num_slots보다 작을 경우 sort 함수 사용이 가능한 수 중 가장 작은 수인 -0.5를 padding으로 추가
                if len(window) < self.num_slots:
                    window.extend([0.0] * (self.num_slots - len(window)))

                lists.append(window)

        # print(f"split: {lists}\n")
        return lists

    # max_pooling을 위한 정렬이 진행된 암호문을 받아 처리할 함수
    def receive_data(self, encrypt_messages):
        # 각 window 범위 내 수 중 최댓값을 담을 list
        max_elements = []

        # 각 암호문을 복호화하여 0번째 인덱스의 값을 max_elements에 추가
        for i in encrypt_messages:
            decrypt_message = self.decrypt_message(ciphertext=i)
            max_elements.append(decrypt_message[0])

        # list 형태의 최댓값을 max_pooling 결과로 변환하기 위해 reshape 진행
        result = self.reshape_list_to_matrix(max_elements)
        # print(f"max_pooling_result: {result}\n")

        return result

    # 최댓값의 개수가 제곱수일 경우 행렬로 변환하도록 하는 함수
    def reshape_list_to_matrix(self, lst):
        n = len(lst)
        size = int(np.sqrt(n))  # 리스트 길이의 제곱근을 구해서 변환할 행렬의 크기 결정

        if size * size != n:
            raise ValueError("리스트의 길이는 정확한 행렬 크기의 제곱이어야 합니다.")

        # 입력 리스트를 행렬로 변환
        matrix = np.array(lst).reshape(size, size)

        return matrix

    def add_message(self, ciphertext1, ciphertext2):
        # 두 ciphertext 간의 덧셈 연산 후 반환
        result_add = heaan.Ciphertext(self.context)
        self.evaluator.add(ciphertext1, ciphertext2, result_add)
        return result_add

    def sub_message(self, ciphertext1, ciphertext2):
        # 두 ciphertext 간의 뺄셈 연산 후 반환
        result_sub = heaan.Ciphertext(self.context)
        self.evaluator.sub(ciphertext1, ciphertext2, result_sub)
        return result_sub

    def mult_message(self, ciphertext1, ciphertext2):
        # 두 ciphertext 간의 곱셈 연산 후 반환
        result_mult = heaan.Ciphertext(self.context)
        self.evaluator.mult(ciphertext1, ciphertext2, result_mult)
        return result_mult

    def sign_message(self, ciphertext):
        # ciphertext의 부호에 따라 -1, 0, 1로 slot 값을 반환
        result_sign = heaan.Ciphertext(self.context)
        approx.sign(self.evaluator, ciphertext, result_sign)
        return result_sign

    def negate_message(self, ciphertext):
        # ciphertext의 부호를 반대로 변경
        result_negate = heaan.Ciphertext(self.context)
        self.evaluator.negate(ciphertext, result_negate)
        return result_negate

    def create_n_values_msg(self, n, log_slots):
        # 모든 slot 값이 n인 message 반환
        num_slots = 2 ** log_slots
        data = [n] * num_slots
        message = heaan.Message(log_slots)
        for i in range(num_slots):
            message[i] = data[i]
        return message

    def define_c_s(self):
        msg_half = self.create_n_values_msg(0.5, self.log_slots)
        result = self.encrypt_message(msg_half)

        return result

    def define_c1(self, ciphertext):
        # Ciphertext의 모든 slot 값을 더하고, 해당 값을 모든 slot에 넣음
        result_sum_all_slots = heaan.Ciphertext(self.context)
        self.evaluator.rot_sum([ciphertext for _ in range(self.num_slots)],
                               [n for n in range(self.num_slots)], result_sum_all_slots)
        return result_sum_all_slots

    def define_c0(self, ciphertext, ciphertext_s):
        temp_msg = self.sub_message(ciphertext, ciphertext_s)
        result = self.sign_message(temp_msg)

        return result

    # It is used for defining c_0_prime and c_2_prime
    def define_c_prime(self, ciphertext_0):
        msg_one = self.create_n_values_msg(1, self.log_slots)
        msg_half = self.create_n_values_msg(0.5, self.log_slots)
        temp_res = self.add_message(ciphertext_0, msg_one)
        result = self.mult_message(temp_res, msg_half)

        return result

    def define_c_2(self, ciphertext_1):
        self.bootstrap_cipher(ciphertext_1)
        msg_m = self.create_n_values_msg((1 / (self.num_slots)), self.log_slots)
        temp_res = self.mult_message(ciphertext_1, msg_m)

        result = self.sign_message(temp_res)

        return result

    def increase_i(self):
        self.i += 1

    def define_cipher_sub_one(self, ciphertext):
        msg_one = self.create_n_values_msg(1, self.log_slots)
        result = self.sub_message(ciphertext, msg_one)

        return result

    def define_c_out(self, ciphertext4, ciphertext2_prime, ciphertext0_prime, ciphertext3):
        mult_c4_c2_prime = self.mult_message(ciphertext4, ciphertext2_prime)
        mult_c0_prime_c3 = self.mult_message(ciphertext0_prime, ciphertext3)

        add_two_mult = self.add_message(mult_c4_c2_prime, mult_c0_prime_c3)

        result = self.negate_message(add_two_mult)

        return result

    def define_c_tmp(self, ciphertext):
        self.bootstrap_cipher(ciphertext)

        msg_one = self.create_n_values_msg(1, self.log_slots)
        msg_two = self.create_n_values_msg(2, self.log_slots)

        c2_twice = self.mult_message(ciphertext, msg_two)

        sub_one = self.sub_message(c2_twice, msg_one)

        msg_half = self.create_n_values_msg(0.5 ** self.i, self.log_slots)

        result = self.mult_message(sub_one, msg_half)

        return result

    def redefine_c_s(self, ciphertext_s, ciphertext_tmp):
        add_ciphers = self.add_message(ciphertext_s, ciphertext_tmp)

        return add_ciphers

    def bootstrap_cipher(self, ciphertext):
        self.evaluator.bootstrap(ciphertext, ciphertext)

    def approx_max(self, c, k):
        print(f"c: {c}")
        self.i = 0

        c_s = self.define_c_s()
        print(f"c_s: {c_s}")

        while True:
            print(f"i: {self.i}, k: {k}")

            c_0 = self.define_c0(c, c_s)
            print(f"c_0: {c_0}")

            c_0_prime = self.define_c_prime(c_0)
            print(f"c_0_prime: {c_0_prime}")

            c_1 = self.define_c1(c_0)
            print(f"c_1: {c_1}")

            c_2 = self.define_c_2(c_1)
            print(f"c_2: {c_2}")

            self.increase_i()

            if self.i == k:
                c_2_prime = self.define_c_prime(c_2)
                print(f"c_2_prime: {c_2_prime}")

                c_3 = self.define_cipher_sub_one(c_2_prime)
                print(f"c_3: {c_3}")
                c_4 = self.define_cipher_sub_one(c_0_prime)
                print(f"c_4: {c_4}")

                c_out = self.define_c_out(c_4, c_2_prime, c_0_prime, c_3)
                print(f"c_out: {c_out}")

                return c_out

            c_tmp = self.define_c_tmp(c_2)
            print(f"c_tmp: {c_tmp}")
            c_s = self.redefine_c_s(c_s, c_tmp)
            print(f"c_s: {c_s}")
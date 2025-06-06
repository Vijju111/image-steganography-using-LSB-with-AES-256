from PIL import Image
import numpy as np
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
import os

def calculate_capacity(image_stream):
    with Image.open(image_stream) as img:
        width, height = img.size
        return (width * height * 3) // 8 - 48  # 48 bytes metadata

def embed_data(image_stream, message, password):
    salt = os.urandom(16)
    iv = os.urandom(16)

    key = PBKDF2(password.encode(), salt, dkLen=32, count=100000)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))

    data_package = salt + iv + encrypted
    binary_data = ''.join(f"{byte:08b}" for byte in data_package)

    img = Image.open(image_stream).convert('RGB')
    img_array = np.array(img)
    width, height = img.size

    if len(binary_data) + 64 > (width * height * 3):
        raise ValueError(f"Message too large. Max: {(width*height*3-64)//8 - 48} bytes")

    binary_data += '11111111' * 8

    data_index = 0
    for row in img_array:
        for pixel in row:
            for channel in range(3):
                if data_index < len(binary_data):
                    pixel[channel] = (pixel[channel] & 0xFE) | int(binary_data[data_index])
                    data_index += 1
    return Image.fromarray(img_array)

def extract_data(image_stream, password):
    img = Image.open(image_stream).convert('RGB')
    img_array = np.array(img)

    binary_stream = []
    for row in img_array:
        for pixel in row:
            for channel in range(3):
                binary_stream.append(str(pixel[channel] & 1))

    full_data = ''.join(binary_stream)
    end_index = full_data.find('11111111' * 8)
    if end_index == -1:
        raise ValueError("No hidden message found")

    data_bytes = bytes(int(full_data[i:i+8], 2) for i in range(0, end_index, 8))

    salt, iv, encrypted = data_bytes[:16], data_bytes[16:32], data_bytes[32:]

    key = PBKDF2(password.encode(), salt, dkLen=32, count=100000)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    try:
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        return decrypted.decode('utf-8')
    except:
        raise ValueError("Decryption failed - wrong password")
from Crypto.Cipher import DES3
from PIL import Image

filename = "a.bmp"
filename_out = "tux_encrypted"
format = "BMP"
key = "aaaaaabbbbbbccccccdddddd"
IV =b'11112222'

def pad(data):
    return data + b"\x00" * (16 - len(data) % 16)

def convert_to_RGB(data):
    r, g, b = tuple(map(lambda d: [data[i] for i in range(0, len(data)) if i % 3 == d], [0, 1, 2]))

    # print(r)


    pixels = tuple(zip(r, g, b))
    return pixels

def process_image(filename,outfilename):
    # Opens image and converts it to RGB format for PIL
    im = Image.open(filename)
    data = im.convert("RGB").tobytes()
    original = len(data)
    mn=des3_cbc_encrypt(key, pad(data))[:original]
    print("okkkkkkkkkkkkkkkkkkk")
    new = convert_to_RGB(mn)
    print(im.size)
    im2 = Image.new("RGBA", im.size)
    im2.putdata(new)
    im2.save(outfilename, format)

def dec_process_image(filename,filedec):
    im=Image.open(filename)
    data=im.convert("RGB").tobytes()
    original=len(data)
    mn=des3_cbc_decrypt(key,pad(data))[:len(data)]
    new=convert_to_RGB(mn)
    im2=Image.new(im.mode,im.size)
    im2.putdata(new)
    im2.save(filedec,format)




def des3_cbc_encrypt(key, data, mode=DES3.MODE_CBC):
    des = DES3.new(key, mode, IV=IV)
    new_data = des.encrypt(data)
    return new_data

def des3_cbc_decrypt(key,data, mode=DES3.MODE_CBC):
    des=DES3.new(key,mode, IV=IV)
    new_data=des.decrypt(data)
    return new_data


# def des3_ecb_encrypt(key, data, mode=DES3.MODE_ECB):
#     des = DES3.new(key.encode("utf8"), mode)
#     new_data = des.encrypt(data)
#     return new_data
#
# def des3_ecb_decrypt(key, data, mode=DES3.MODE_ECB):
#     des=DES3.new(key.encode("utf8"),mode)
#     new_data=des.decrypt(data)
#     return new_dataaas

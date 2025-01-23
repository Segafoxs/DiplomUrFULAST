import gostcrypto
import secrets
import string

if __name__ == '__main__':
    private_key = bytearray([
        0x7a, 0x92, 0x9a, 0xde, 0x78, 0x9b, 0xb9, 0xbe, 0x10, 0xed, 0x35, 0x9d, 0xd3, 0x9a, 0x72, 0xc1,
        0x1b, 0x60, 0x96, 0x1f, 0x49, 0x39, 0x7e, 0xee, 0x1d, 0x19, 0xce, 0x98, 0x91, 0xec, 0x3b, 0x28,
    ])



    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(32))
    print(password)
    #private_key = bytearray("test", encoding="utf-8")
    private_key = bytearray(password, encoding="utf-8")
    print(len(str(private_key)))
    print(private_key.decode())

    sign_obj = gostcrypto.gostsignature.new(gostcrypto.gostsignature.MODE_256,
                                            gostcrypto.gostsignature.CURVES_R_1323565_1_024_2019[
                                                'id-tc26-gost-3410-2012-256-paramSetB'])
    file_path = '19.docx'
    buffer_size = 128

    hash_obj = gostcrypto.gosthash.new('streebog256')

    with open(file_path, 'rb') as file:
        hash_obj.update(file.read())
        # buffer = file.read(buffer_size)
        # while len(buffer) > 0:

            # buffer = file.read(buffer_size)
    digest = hash_obj.digest()
    print(hash_obj.hexdigest())

    signature = sign_obj.sign(private_key, digest)
    print(signature)
    print(signature)

    sign_obj = gostcrypto.gostsignature.new(gostcrypto.gostsignature.MODE_256,
                                            gostcrypto.gostsignature.CURVES_R_1323565_1_024_2019[
                                                'id-tc26-gost-3410-2012-256-paramSetB'])

    #генерация публичного ключа
    public_key = sign_obj.public_key_generate(private_key)

    #верификация подписи
    if sign_obj.verify(public_key, digest, signature):
        print('Signature is correct')
    else:
        print('Signature is not correct')

# Мы создаем модель где храним приватный ключ для каждого сотрудника и проверяем его акктуальность и просроченость
# Приватный ключ мы создаем сами  для каждого сотрудника и "выдаем" ему ключ
# Пользователь может скачать документ и посмотреть
# Подписать документ с помощью своего приватного ключа(ввод в интрефейсе)
# Мы сохраняем информацию о подписи хэш сумма файла (блокчейн) и саму версию файла на minio
# Minio хранит файлы (может разные версии)
# Просмотр истории подписаний для конкретного файла
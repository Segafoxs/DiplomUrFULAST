import gostcrypto

def generate_signature(data, private_key: str) -> (bytearray, bytearray):
    sign_obj = gostcrypto.gostsignature.new(
        gostcrypto.gostsignature.MODE_256,
        gostcrypto.gostsignature.CURVES_R_1323565_1_024_2019[
            'id-tc26-gost-3410-2012-256-paramSetB'])

    buffer_size = 128

    hash_obj = gostcrypto.gosthash.new('streebog256')
    hash_obj.update(data)
    # buffer = data.read(buffer_size)
    # while len(buffer) > 0:
    #
    #     buffer = data.read(buffer_size)

    digest = hash_obj.digest()
    primary_key_b = bytearray(private_key, encoding="utf-8")
    signature = sign_obj.sign(primary_key_b, digest)

    public_key = sign_obj.public_key_generate(primary_key_b)

    return digest, signature, public_key


def check_signature(private_key, digest, signature) -> bool:
    sign_obj = gostcrypto.gostsignature.new(gostcrypto.gostsignature.MODE_256,
                                            gostcrypto.gostsignature.CURVES_R_1323565_1_024_2019[
                                                'id-tc26-gost-3410-2012-256-paramSetB'])

    primary_key_b = bytearray(private_key, encoding="utf-8")
    public_key = sign_obj.public_key_generate(primary_key_b)

    return sign_obj.verify(public_key, digest, signature)
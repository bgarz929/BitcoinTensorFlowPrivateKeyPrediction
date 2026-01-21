import tensorflow as tf
import numpy as np
import hashlib
import converter

# ================= CONFIG =================
bitsP2PKH = 160
model_file = "prediction.keras"

# contoh HASH160 (20 bytes = 160 bit)
public_key = "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798"
# =========================================


# ---------- Base58 ----------
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def base58_encode(b: bytes) -> str:
    num = int.from_bytes(b, 'big')
    result = ""
    while num > 0:
        num, rem = divmod(num, 58)
        result = ALPHABET[rem] + result

    # leading zero bytes → leading '1'
    pad = 0
    for byte in b:
        if byte == 0:
            pad += 1
        else:
            break
    return "1" * pad + result


def base58check_encode(payload: bytes) -> str:
    checksum = hashlib.sha256(
        hashlib.sha256(payload).digest()
    ).digest()[:4]
    return base58_encode(payload + checksum)


def privatekey_hex_to_wif_compressed(hex_key: str) -> str:
    privkey_bytes = bytes.fromhex(hex_key)
    if len(privkey_bytes) != 32:
        raise ValueError("Private key must be 32 bytes")

    payload = b'\x80' + privkey_bytes + b'\x01'  # mainnet + compressed
    return base58check_encode(payload)


def main():
    # ---- load model ----
    model = tf.keras.models.load_model(model_file)

    # ---- convert public key hash ----
    public_key_bytes = bytes.fromhex(public_key)
    public_key_int = converter.intFromBytes(public_key_bytes)

    bit_array = converter.convert_to_binary_arrays(
        [public_key_int],
        bitsP2PKH
    )

    bit_array = np.asarray(bit_array, dtype=np.float32)

    if bit_array.shape != (1, bitsP2PKH):
        raise ValueError(f"Invalid input shape {bit_array.shape}")

    # ---- predict ----
    prediction = model.predict(bit_array, verbose=0)

    # ---- NN output → private key HEX ----
    private_key_hex = converter.float_array_to_hex(
        prediction[0],
        64
    )

    # ---- convert to WIF compressed ----
    wif_compressed = privatekey_hex_to_wif_compressed(private_key_hex)

    print("Predicted Private Key (HEX):")
    print(private_key_hex)
    print("\nWIF (Compressed):")
    print(wif_compressed)


if __name__ == "__main__":
    main()

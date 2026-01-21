import tensorflow as tf
import numpy as np
import converter

# ================= CONFIG =================
bitsP2PKH = 160
model_file = "prediction.keras"

# contoh HASH160 (20 bytes = 160 bit)
public_key = "e954123abe469e5d293167aac708da1943e48481"
# =========================================


def main():
    # ---- load model ----
    model = tf.keras.models.load_model(model_file)

    # ---- convert hex public key to int ----
    public_key_bytes = bytes.fromhex(public_key)
    public_key_int = converter.intFromBytes(public_key_bytes)

    # ---- convert int to binary array (SAMA DENGAN TRAINING) ----
    bit_array = converter.convert_to_binary_arrays(
        [public_key_int],
        bitsP2PKH
    )

    # ---- IMPORTANT FIX: convert to numpy float32 ----
    bit_array = np.asarray(bit_array, dtype=np.float32)

    # ---- safety check ----
    if bit_array.ndim != 2 or bit_array.shape[1] != bitsP2PKH:
        raise ValueError(
            f"Invalid input shape {bit_array.shape}, expected (batch, {bitsP2PKH})"
        )

    # ---- predict ----
    prediction = model.predict(bit_array, verbose=0)

    # ---- convert output to hex private key ----
    possible_secret = converter.float_array_to_hex(prediction[0], 64)

    print("Predicted private key (hex):")
    print(possible_secret)


if __name__ == "__main__":
    main()


from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()


secret_key = 'xbglVHmv8O9kUFSzzVzL73Vlag2asQ6IwNzcMjgW7eY' # Not a good practice, but it's just a demo


password_file_path = "/path/to/password/file.txt"
encryption_key = os.environ.get('JWT_ENCRYPTION_KEY').encode()
encryption_cipher = Fernet(encryption_key)

def encrypt_payload(payload: dict) -> bytes:
    payload_str = str(payload).encode()
    encrypted_payload = encryption_cipher.encrypt(payload_str)
    return encrypted_payload

def decrypt_payload(encrypted_payload: bytes) -> dict:
    decrypted_payload_str = encryption_cipher.decrypt(encrypted_payload).decode()
    return decrypted_payload_str

def generate_token(user_id) -> str:
    dt = datetime.utcnow() + timedelta(hours=72)
    encrypted_payload = {
        "user_id": str(encrypt_payload(user_id)),
        "exp": dt
    }
    token: str = encode(
        payload=encrypted_payload,  # Encode the encrypted payload instead of the original payload
        key=secret_key, 
        algorithm="HS256",
    )
    return token

def verify_token(token: str) -> dict:
    try:
        encrypted_payload = decode(token, key=secret_key, algorithms=['HS256'])
        binary = encrypted_payload['user_id'][2:-1].encode()

        data:dict = {
            'user_id': decrypt_payload(binary),
            'exp': encrypted_payload['exp']
        }  # Decrypt the encrypted payload
        print(data)
        return {'code': 'token_valid', 'data': data} 
    except ExpiredSignatureError:
        return {'code': 'token_expired'}
    except InvalidTokenError:
        return {'code': 'invalid_token'}
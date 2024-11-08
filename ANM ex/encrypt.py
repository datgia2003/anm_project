import custom_library

def encrypt_message(message, public_key):
    segment_size = custom_library.get_segment_size(public_key['n'])
    encrypted_segments = []

    while message:
        segment = message[:segment_size]
        message = message[segment_size:]
        segment = int.from_bytes(segment.encode('utf-8'), byteorder='big')
        encrypted_segment = custom_library.modular_exponentiation(segment, public_key['e'], public_key['n'])
        encrypted_segments.append(encrypted_segment)
    
    return encrypted_segments

def encrypt_file(data_file_path, public_key, encrypted_file_path):
    with open(data_file_path, 'rb') as data_file:
        with open(encrypted_file_path, 'w', encoding='utf-8') as encrypted_file:
            from os import stat
            encrypted_file.write(str(stat(data_file_path).st_size) + '\n')
            
            segment_size = custom_library.get_segment_size(public_key['n'])

            while segment := data_file.read(segment_size):
                segment = int.from_bytes(segment, byteorder='big')
                encrypted_segment = custom_library.modular_exponentiation(segment, public_key['e'], public_key['n'])
                encrypted_file.write(str(encrypted_segment) + '\n')

    return encrypted_file_path

if __name__ == "__main__":
    data_file_path = 'data.txt'
    public_key_path = 'result/public_key.json'
    encrypted_file_path = 'result/encrypted_data.txt'

    import json
    with open(public_key_path, 'r', encoding='utf-8') as f:
        public_key = json.loads(f.read())

    encrypt_file(data_file_path, public_key, encrypted_file_path)
    print('done.')

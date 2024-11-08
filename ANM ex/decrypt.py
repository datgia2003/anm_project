import custom_library

def decrypt_message(encrypted_segments, private_key):
    decrypted_message = ''

    for segment in encrypted_segments:
        decrypted_segment = custom_library.modular_exponentiation(segment, private_key['d'], private_key['n'])
        decrypted_message += decrypted_segment.to_bytes((decrypted_segment.bit_length() + 7) // 8, byteorder='big').decode('utf-8')
    
    return decrypted_message

def decrypt_file(encrypted_file_path, private_key, decrypted_file_path):
    with open(encrypted_file_path, 'r', encoding='utf-8') as encrypted_file:
        with open(decrypted_file_path, 'wb') as decrypted_file:
            original_data_file_size = int(encrypted_file.readline().strip())
            remain_data_to_read = original_data_file_size

            segment_size = custom_library.get_segment_size(private_key['n'])

            while segment := encrypted_file.readline().strip():
                segment = int(segment)
                segment = custom_library.modular_exponentiation(segment, private_key['d'], private_key['n'])
                remain_data_to_read -= segment_size
                if remain_data_to_read <= 0:
                    remain_data_to_read += segment_size
                    segment_bytes = segment.to_bytes(remain_data_to_read, byteorder='big')
                    decrypted_file.write(segment_bytes)
                    break
                else:
                    segment_bytes = segment.to_bytes(segment_size, byteorder='big')
                    decrypted_file.write(segment_bytes)
    return decrypted_file_path

if __name__ == "__main__":
    encrypted_file_path = 'result/encrypted_data.txt'
    private_key_path = 'result/private_key.json'
    decrypted_file_path = 'result/decrypted_data.txt'

    import json
    with open(private_key_path, 'r', encoding='utf-8') as f:
        private_key = json.loads(f.read())

    decrypt_file(encrypted_file_path, private_key, decrypted_file_path)
    print('done.')

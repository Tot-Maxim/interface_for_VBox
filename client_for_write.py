path_to_file = 'temp.txt'


def write_data(data):
    with open(path_to_file, 'a+b') as temp_file:
        temp_file.write(data)
        temp_file.write(b'\n')
        print(f'Write data: {data}')

    with open(path_to_file, 'rb') as temp_file:
        content = temp_file.read()
        print(f'READ Data: {content}')


while True:
    for i in range(100):
        data = bytes([i])
        write_data(data)
        # data_in_int = int.from_bytes(data, byteorder='big', signed=True)
        # print(data_in_int)


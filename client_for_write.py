data_1 = b'123'
data_2 = b'456'
data_3 = b'789'
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
        data = i
        write_data(bytes(data))

    #data = input('Ведите данные: ')
    #if data == '':
    #    break

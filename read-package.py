path_to_temp = '/media/sf_FilePack/from_host.docx'
path_to_temp2 ='/media/sf_FilePack/from_virtual.docx'
#path_to_data = 'data.txt'


def read_packet(path_to_temp: str):
    with open(path_to_temp, 'rb+') as temp_file:  # Открываем temp_file в режиме чтения-записи-бинарный
        content = temp_file.read()  # Читаем содержимое temp_file

        index = content.find(b'\t0t')  # Находим индекс первого вхождения символа \n
        if index != -1:  # Если \n найден
            data = content[:index]  # Извлекаем данные до первого символа \n
            content = content[index + 3:]  # Обновляем content после первого символа \n

            #with open(path_to_data, 'wb') as data_file:
            #    data_file.write(data)
            print(f'Write to {path_to_temp} data: {data}')

            temp_file.seek(0)
            temp_file.truncate()
            temp_file.write(content)


while True:
    read_packet(path_to_temp)
    read_packet(path_to_temp2)

import os
import tempfile
import time
class AtomicWrite():
    def __init__(self, path, mode='w', encoding='utf-8'):
        self.path = path
        self.mode = mode if mode == 'wb' else 'w'
        self.encoding = encoding

    def __enter__(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            mode=self.mode,
            encoding=self.encoding if self.mode != 'wb' else None,  # Исправлено здесь
            delete=False
        )
        return self.temp_file

    def __exit__(self, exc_type, exc_message, traceback):
        self.temp_file.close()
        if exc_type is None:
            os.rename(self.temp_file.name, self.path)
        else:
            os.unlink(self.temp_file.name)

items = ['one', 'two', 'three']
data_to_write = '\n'.join(items)
with AtomicWrite('data_file.txt', 'wb') as file:
    file.write(data_to_write.encode('utf-8'))
    time.sleep(1)
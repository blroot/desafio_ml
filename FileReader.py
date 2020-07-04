import string
import random


class FileReader:
    def __init__(self, config, parser_factory):
        self.file_name = ''.join(random.choice(string.ascii_letters) for i in range(10))
        self.chunk_size = int(config['file_reader']['chunk_size'])
        self.file_path = config['file_reader']['file_path']
        self.reader = parser_factory.get_parser(config['file_reader']['type'])

    def upload(self, request):
        with open(self.file_path + self.file_name, "bw") as f:
            while True:
                chunk = request.stream.read(int(self.chunk_size))
                if len(chunk) == 0:
                    return
                f.write(chunk)

    def read_line(self):
        with open(self.file_path + self.file_name, "r") as f:
            reader = self.reader(f)
            for row in reader:
                yield row

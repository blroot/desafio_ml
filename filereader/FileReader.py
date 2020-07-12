from flask import current_app as app
import os


class FileReader:
    def __init__(self, parser_factory, record_format, file_name):
        self.file_name = file_name
        self.file_path = app.config.get("FILE_PATH")
        self.parser = parser_factory.get_parser(app.config.get("FILE_TYPE"))
        self.record_format = record_format

    """
    def upload(self, request):
        file = request.files['file']
        file.save(self.file_path + self.file_name)

        with open(self.file_path + self.file_name, "bw") as f:
            while True:
                chunk = request.stream.read(int(self.chunk_size))
                if len(chunk) == 0:
                    return
                f.write(chunk)
    """

    def read_line(self):
        with open(self.file_path + self.file_name, "r") as f:
            reader = self.parser.reader(f)
            for row in reader:
                yield self.parser.build_record(row, self.record_format)

    def remove_file(self):
        os.remove(self.file_path + self.file_name)

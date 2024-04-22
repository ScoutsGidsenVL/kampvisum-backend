"""scouts_auth.inuits.files.file_utils."""
import tempfile


class FileUtils:
    @staticmethod
    def get_temp_file(filename: str):
        return "%s/%s" % (tempfile.gettempdir(), filename)

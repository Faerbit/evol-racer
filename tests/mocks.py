import mock
import builtins

class mock_open():

    def __init__(self, read_data):
        self.read_data = read_data

    def __enter__(self):
        self.context = mock.patch.object(
                builtins, "open", mock.mock_open(read_data=self.read_data))
        self.context.__enter__().return_value.__iter__.return_value = self.read_data.split("\n")
        return self.context.__enter__()

    def __exit__(self, *args):
        self.context.__exit__(*args)


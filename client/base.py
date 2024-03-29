import numpy as np

from utility.tokenize import remove_htmltags, remove_special_character, \
    tokenize
from utility.utils import save_text_to_file, read_text_from_file
from utility.config import init_config

Settings = init_config()
output_setting = Settings.get('OUTPUT')


class Client:
    raw: str = None
    """
    raw field, the raw data from client request
    """

    content: str = None
    """
    content field, the plaintext strip html tags or special characters
    """

    tokens: list = None
    """
    tokens field, a list include all tokens from content.
    """

    vector = None
    """
    vector matrix, an array of features values.
    """

    url = None  # client request base url

    filename_raw = 'raw.txt'
    filename_content = 'content.txt'
    filename_output = 'output.txt'

    def __init__(self, *args, logger=None, save=False, force_update=False):
        global Settings
        self._logger = logger
        self.is_save: bool = save
        self.force_update: bool = force_update
        self.url = getattr(Settings, self.__class__.__name__)['url']

    def run(self):
        raise NotImplementedError

    def get_raw(self):
        raise NotImplementedError

    def save(self):
        # the data item should include three information.
        # data_item = (`file_path`, `file_name`, `file_content`)
        data_list = [
            (
                output_setting.get('q1_path', '.'),
                self.filename_raw,
                self.raw.decode()
            ),
            (
                output_setting.get('q1_path', '.'),
                self.filename_content,
                self.content
            ),
            (
                output_setting.get('q1_path', '.'),
                self.filename_output,
                '\n'.join(self.tokens)
            ),
            (
                output_setting.get('q2_path', '.'),
                self.filename_output,
                str('\n'.join([str(["{:.3}".format(n) for n in l]) for l in
                               self.vector.tolist()]))
            )
        ]

        for p, n, c in data_list:
            if c:
                save_text_to_file(p, n, c)

    def read_raw_from_file(self):
        try:
            return read_text_from_file(
                output_setting.get('q1_path', '.'),
                self.filename_raw
            )
        except Exception as e:
            self._logger.error("can't read raw from file: %s" % e)
            return None

    @staticmethod
    def get_tokens(html: str) -> (str, list):
        text = remove_htmltags(html)  # strip http tags
        plaintext = remove_special_character(text)  # strip http tags
        return plaintext, tokenize(plaintext)

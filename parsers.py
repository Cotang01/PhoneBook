import configparser
import json
import logging
import configargparse
from typing import Dict


class IniConfigParse:
    """ A class for parsing configuration from an INI files. """
    def __init__(self):
        parser = configargparse.ArgParser()
        parser.add_argument('-c, --config', default='config.ini',
                            is_config_file=True,
                            help='Path to file config.ini')
        parser.add_argument('--log_config',
                            default={
                                "level": logging.INFO,
                                "format": "%(asctime)s %(levelname)s %(message)s",
                                "filename": "logger.log"},
                            help='Configuration parameters for logging')
        parser.add_argument('--lang',
                            default={
                                "eng": "view_text_lines_ENG.py",
                                "ru": "view_text_lines_RU.py"},
                            help='App localization')

        args = parser.parse_args()

        self.log_config = json.loads(args.log_config)
        self.lang = json.loads(args.lang)


class IniLocalizationParser:
    @staticmethod
    def read_properties_file(file_path: str) -> Dict:
        """ Get dict with localization data. """
        config = configparser.ConfigParser(allow_no_value=True)
        with open(file_path, 'r', encoding='UTF-8') as f:
            config.read_string(f'[localization]\n' + f.read())
        # return dict(config.__dict__['_sections']['localization'])
        return dict(config.__dict__['_sections']['localization'])

import argparse
import sys

class SupportAction(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest,
                 default=False,
                 required=False,
                 help=None,
                 deprecated=False):
        super(SupportAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            const=True,
            deprecated=deprecated,
            required=required,
            help=help,
            default=default)

    def __call__(self, parser, namespace, values, option_strings=None):
        setattr(namespace, self.dest, self.const)
        namespace.handler_class.display_support()
        parser.exit()


class ErrorHandlingParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n\n' % message)
        self.print_help()
        sys.exit(2)

def format_min_dec(value, min_decimals):
    string = str(value)
    if "." not in string:
        return string + "." + "0" * min_decimals
    else:
        whole, dec = string.split(".")
        if len(dec) >= min_decimals:
            return string
        else:
            return string + "0" * min_decimals


def align_by_decimal(string, size, dec_pos):
    string = string.strip()

    if "." not in string:
        raise RuntimeError("ERROR: No decimal found in string. Cannot align")

    strlen = len(string)

    if size <= strlen:
        return string

    whole, dec = string.split(".")

    room_left = dec_pos - len(whole)
    room_right = size - dec_pos - 1 - len(dec)

    if room_left < 0:
        return string
    if room_right < 0:
        return string


    return " " * room_left + string + " " * room_right

from os import getcwd

from wwwpy import Config


# if main it does not detect the 'user folder' correctly


def quickstart():
    print(getcwd())
    Config().quickstart()


if __name__ == '__main__':
    quickstart()

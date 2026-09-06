"""CAPSM Stage-1 rebuild - verified download and integrity reporting."""

from capsm.data.download import run as download_run
from capsm.data.integrity import run as integrity_run


def main():
    download_run()
    integrity_run()


if __name__ == "__main__":
    main()

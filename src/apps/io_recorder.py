import os

from uaos import App


class IoRecorder(App):
    optional = ['Apify']

    def __init__(self):
        super().__init__()
        if hasattr(os, "dupterm"):
            pass

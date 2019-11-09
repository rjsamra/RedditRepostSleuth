import json

from redditrepostsleuth.core.model.imagematch import ImageMatch
from redditrepostsleuth.core.model.imagerepostwrapper import ImageRepostWrapper


class ImageMatchJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ImageMatch):
            return o.to_dict()

class ImageRepostWrapperEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ImageRepostWrapper):
            return o.to_dict()
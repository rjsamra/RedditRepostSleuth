from redditrepostsleuth.core.model.search_times import SearchTimes


class ImageSearchTimes(SearchTimes):
    """
    Class to dynamically start and stop perf_counts with variable names
    """
    def __init__(self):
        super().__init__()
        self.pre_annoy_filter_time: float = float(0)
        self.index_search_time: float = float(0)
        self.meme_filter_time: float = float(0)
        self.meme_detection_time: float = float(0)
        self.set_match_post_time: float = float(0)
        self.remove_duplicate_time: float = float(0)
        self.set_match_hamming: float = float(0)
        self.image_search_api_time: float = float(0)
        self.filter_removed_posts_time: float = float(0)
        self.filter_deleted_posts_time: float = float(0)
        self.set_meme_hash_time: float = float(0)
        self.set_closest_meme_hash_time: float = float(0)
        self.distance_filter_time: float = float(0)
        self.get_closest_match_time: float = float(0)

    def to_dict(self):
        return {**{
            'pre_annoy_filter_time': self.pre_annoy_filter_time,
            'index_search_time': self.index_search_time,
            'meme_filter_time': self.meme_filter_time,
            'meme_detection_time': self.meme_detection_time,
            'set_match_post_time': self.set_match_post_time,
            'remove_duplicate_time': self.remove_duplicate_time,
            'set_match_hamming': self.set_match_hamming,
            'image_search_api_time': self.image_search_api_time,
            'filter_removed_posts_time': self.filter_removed_posts_time,
            'filter_deleted_posts_time': self.filter_deleted_posts_time,
            'image_search_api_time': self.image_search_api_time,
            'set_meme_hash_time': self.set_meme_hash_time,
            'set_closest_meme_hash_time': self.set_closest_meme_hash_time,
            'distance_filter_time': self.distance_filter_time,
            'get_closest_match_time': self.get_closest_match_time

        }, **super().to_dict()}


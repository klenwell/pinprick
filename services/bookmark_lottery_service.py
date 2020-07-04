import random
from math import ceil
from services.bookmark_service import BookmarkService


def choose_randomly_distributed_bookmarks(count):
    """For given count, will break bookmarks into groups evenly divided by and
    return one random bookmark from each group.
    """
    selected_bookmarks = []

    pinboard = BookmarkService()
    bookmarks = sorted(pinboard.bookmarks, key=lambda b: b.created_at)
    bookmark_pools = shard_list(bookmarks, count)

    for bookmark_pool in bookmark_pools:
        bookmark = random.choice(bookmark_pool)
        selected_bookmarks.append(bookmark)

    return selected_bookmarks


def shard_list(seq, num_shards):
    """"""
    avg_shard_size = ceil(len(seq) / num_shards)

    # Yield successive n-sized chunks from lst.
    # https://stackoverflow.com/a/312464/1093087
    for i in range(0, len(seq), avg_shard_size):
        yield seq[i:i + avg_shard_size]

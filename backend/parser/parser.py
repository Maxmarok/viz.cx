"""VIZ Blockchain to MongoDB parser"""
from typing import NoReturn
from time import sleep
from helpers.mongo import get_last_blocknum, save_block
from helpers.viz import get_last_block_in_chain, get_ops_in_block
from parser.posts import fetch_new_updates


def start_parsing() -> NoReturn:
    """Parse VIZ Blockchain blocks to MongoDB."""
    try:
        last_blocknum_in_bd = get_last_blocknum()
        print("Last block in db: {}".format(last_blocknum_in_bd))
    except IndexError:
        print("Blocks not found in current MongoDB collection. Start from 1.")
        last_blocknum_in_bd = 0
    while True:
        try:
            last_blocknum_in_bkchn = get_last_block_in_chain()
            if last_blocknum_in_bkchn - last_blocknum_in_bd > 1:
                for _ in range(last_blocknum_in_bd + 1, last_blocknum_in_bkchn):
                    save_block(get_ops_in_block(_, False))
                    last_blocknum_in_bd = _
                    if last_blocknum_in_bd % 100 == 0:
                        print("Saved block {}".format(last_blocknum_in_bd))
            else:
                fetch_new_updates()
                sleep(3)
        except Exception as e:
            print("Parsing error: {}. Restart in 10 seconds.".format(str(e)))
            sleep(10)
            print("Restarting...")

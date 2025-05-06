import logging
from src.cracker.hash_cracker import crack_hash_with_mp
from src.cracker.crack_time import  get_crack_stats

from config.config import USER_INFO

from src.cracker.serialization import serialize_card

from src.cracker.stats import visual_crack_stats


def main():
    cores_stats = []
    time_stats = []
    for stat in get_crack_stats("140495200b351b7f18a46e3796f2875ebdf0023568933ef3b99efb285af3f06b","2301", "547905"):
        cores_stats.append(stat["cores"])
        time_stats.append(stat["crack_time"])
    
    visual_crack_stats(cores_stats, time_stats)

if __name__ == "__main__":
    main()

import json
import logging

logger = logging.getLogger(__name__)


class ItemsExporter:
    def __init__(self):
        self.mapping = {}
        with open('export/mappings/items_statistics.json') as f:
            self.mapping = json.load(f)

    def parse_single_item(self, item):
        # parses from "name_of_item: stat+0.1 stat2-0.2" to (name_of_item, [(stat1, 0.1), (stat2, 0.2)])
        item_name, stats_str = item.split(": ")
        stats = stats_str.split(" ")
        parsed_stats = []
        for stat in stats:
            if '+' in stat:
                stat_name, stat_value = stat.split("+")
                parsed_stats.append((self.mapping[stat_name], float(stat_value[:-1])))
            elif '-' in stat:
                stat_name, stat_value = stat.split("-")
                parsed_stats.append((self.mapping[stat_name], -float(stat_value[:-1])))
            else:
                logger.error(f"Could not parse stat {stat} - unknown operator?")
                raise Exception
        return item_name, parsed_stats

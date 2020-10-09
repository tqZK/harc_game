import json
import logging
logging.basicConfig(format='%(message)s')



class ItemsExporter:
    def __init__(self):
        self.mapping = {}
        with open('export/mappings/items_statistics.json') as f:
            self.mapping = json.load(f)

    def parse_single_item(self, item):
        # parses from "name_of_item: stat+1% stat2-2%" to (name_of_item, [(stat1, 0.01), (stat2, 0.02)])
        item_name, stats_str = item.split(": ")
        parsed_stats = []
        stats = stats_str.split(" ")
        if stats_str:
            for stat in stats:
                if '+' in stat:
                    stat_name, stat_value = stat.split("+")
                    real_stat_value = float(stat_value[:-1]) / 100 if stat_value.endswith("%") else float(stat_value)
                    parsed_stats.append((self.mapping[stat_name], real_stat_value))
                elif '-' in stat:
                    stat_name, stat_value = stat.split("-")
                    real_stat_value = float(stat_value[:-1]) / 100 if stat_value.endswith("%") else float(stat_value)
                    parsed_stats.append((self.mapping[stat_name], -real_stat_value))
                else:
                    logging.error(f"Could not parse stat '{stat}' in item '{item}' - unknown operator?")
                    raise Exception
        return item_name, parsed_stats


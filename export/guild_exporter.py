import csv
import json
from game.config import BASE_TAX_RATE


class GuildExporter:

    def __init__(self):
        self.mapping = {}
        with open('export/mappings/guild.json') as f:
            self.mapping = json.load(f)

    def export_guild_tsv(self, filename):
        guild_stats = {}
        all_guild_stats = self.read_tsv_file(filename)
        only_guild_stats = {"tax_rate": all_guild_stats["tax_rate"]}
        del all_guild_stats["tax_rate"]
        return only_guild_stats, all_guild_stats

    def read_tsv_file(self, filename):
        data = {}
        with open(filename) as tsvfile:
            reader = csv.reader(tsvfile, dialect='excel-tab')
            for row in reader:
                if row[0] in self.mapping:
                    data.update(self.parse_stat(row))
        return data

    def parse_stat(self, row):
        stat_name = self.mapping[row[0]]
        stat_value = row[1]
        parsed_stat_value = 0
        if stat_name == "tax_rate":
            if stat_value == "?":
                parsed_stat_value = BASE_TAX_RATE
            elif stat_value.endswith("%"):
                parsed_stat_value = float(stat_value[:-1]) / 100
            else:
                raise Exception("Tax rate should be in % form")
        else:
            parsed_stat_value = float(stat_value[:-1]) / 100
        return {stat_name: parsed_stat_value}

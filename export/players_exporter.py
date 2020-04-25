import csv
import json

from game.player import Player


class PlayersExporter:
    def __init__(self):
        self.mapping = {}
        with open('export/mappings/player.json') as f:
            self.mapping = json.load(f)

    def export_players_tsv(self, filename):
        data = self.read_tsv_file(filename)

        data = self.remove_empty_lines(data)

        # TODO: validate file

        players = []
        for row in data:
            print(row)
            players.append(Player(**row))

        # TODO: validate players (calculated stats)

        # TODO: return players
        return []

    def read_tsv_file(self, filename):
        data = []
        with open(filename) as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            reader.fieldnames = [self.mapping[field] for field in reader.fieldnames]
            for row in reader:
                data.append(dict(row))
        return data

    def remove_empty_lines(self, data):
        data_cleared = []
        for row in data:
            if row['player_id'] and row['name'] and row['initials']:
                data_cleared.append(row)
        return data_cleared

    def validate_player_with_data(self):
        # TODO: validate lvl
        # TODO: validate exp
        # TODO: validate dmg
        # TODO: validate cumulative_gold
        # TODO: validate max life points


        pass

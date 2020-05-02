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

        players = []
        for row in data:
            print(row)
            player = Player(**row)
            # self.validate_player_with_data(player, row)
            players.append(player)

        return players

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

    def validate_player_with_data(self, player, row):
        for attr_name, attr in zip(
            ["lvl", "exp", "dmg", "cumulative_gold", "max_life_points"],
            [player.lvl, player.dmg, player.cumulative_gold, player.max_life_points]
        ):
            assert row[attr_name] == attr, f"Player {player.player_id} {attr_name} {attr} is not equal to exported {attr_name} {row[attr_name]}"

        # TODO: check for present bag - if not, then other_2 should be empty

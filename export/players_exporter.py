import csv
import json

from game.player import Player
from export.items_exporter import ItemsExporter


class PlayersExporter:
    def __init__(self):
        self.mapping = {}
        with open('export/mappings/player.json') as f:
            self.mapping = json.load(f)
        self.items_exporter = ItemsExporter()

    def export_players_tsv(self, filename):
        data = self.read_tsv_file(filename)
        data = self.remove_empty_lines(data)

        players = []
        for row in data:
            row_cleared = {k: v for k, v in row.items() if v != "" and v != "-"}
            self.parse_player_items(row_cleared)
            # TODO: parse "tak" etc. to True
            # TODO: parse str to int etc.
            print(row_cleared)
            player = Player(**row_cleared)
            print(player)
            self.validate_player_with_data(player, row)
            players.append(player)
            print('------')

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

    def parse_player_items(self, player_data):
        item_places = ["helmet", "armor", "hand_1", "hand_2", "other_1", "other_2"]
        for item_place in item_places:
            if item_place in player_data:
                item = player_data[item_place]
                parsed_item = self.items_exporter.parse_single_item(item)
                player_data[item_place] = parsed_item

    def validate_player_with_data(self, player, row):
        for attr_name in ["lvl", "exp", "dmg", "cumulative_gold", "max_life_points"]:
            value = getattr(player, attr_name)
            # TODO: change it after parsing types
            exported = type(value)(row[attr_name])
            assert exported == value, \
                f"Player {player.player_id} {attr_name} {value} is not equal to exported {attr_name} {exported}"

        # TODO: check for present bag - if not, then other_2 should be empty
        # TODO: validate buffs

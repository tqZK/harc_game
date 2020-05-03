from export.players_exporter import PlayersExporter

if __name__ == '__main__':
    exporter = PlayersExporter()
    exported_data = exporter.export_players_tsv('examples/player_stats.tsv')
    print(exported_data)

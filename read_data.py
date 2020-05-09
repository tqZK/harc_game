from export.players_exporter import PlayersExporter
from export.guild_exporter import GuildExporter

if __name__ == '__main__':
    guild_exporter = GuildExporter()
    guild_stats, guild_stats_for_player = guild_exporter.export_guild_tsv('examples/guild_stats.tsv')
    print(guild_stats)
    print(guild_stats_for_player)

    exporter = PlayersExporter(buffs_from_guild=guild_stats_for_player)
    exported_data = exporter.export_players_tsv('examples/players_stats.tsv')
    print(exported_data)

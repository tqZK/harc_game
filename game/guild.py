class Guild:
    def __init__(self):
        self.players = []
        self.gold = 0

    @property
    def strenght(self):
        return sum([player.strenght for player in self.players])

    def __str__(self):
        return f"Gildia:\t" \
               f"sila={self.strenght}\t" \
               f"zloto={self.gold}\t"

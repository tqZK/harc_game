class Monster:
    def __init__(self, monster_id, strength, life_points, first_attack_chance):
        self.monster_id = monster_id
        self._life_points = life_points
        self.strenght = strength
        self.first_attack_chance = first_attack_chance

    @property
    def life_points(self):
        return self._life_points

    @life_points.setter
    def life_points(self, value):
        self._life_points = max(0, value)

    @property
    def alive(self):
        return bool(self.life_points > 0)

    def __str__(self):
        return f"Nieosłonięty {self.monster_id}:\t" \
               f"punkty_zycia={self.life_points}\t" \
               f"sila={self.strenght}".expandtabs(8)

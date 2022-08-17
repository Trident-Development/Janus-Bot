from random import randint


class Colors:
    def __init__(self):
        self.color_list = [0x36A64F, 0x288BA8, 0x746AB0, 0xE83845, 0xFFCE30, 0xE389B9]

    def random_color(self):
        return self.color_list[randint(0, len(self.color_list) - 1)]

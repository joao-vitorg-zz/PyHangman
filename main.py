#!/usr/bin/python3
# -*- coding: utf-8 -*-

from json import load, dump, decoder
from random import choice


class Hangman(object):
    def __init__(self):
        while True:
            self.letters = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'
            self.word = self.random_word()
            self.mask = '*' * len(self.word)
            self.level = 0

            self.banner()
            self.name = input(' ╚Name> ')[:8]
            if self.name == 'quit':
                break

            self.main()

    @staticmethod
    def banner():
        print('''
 ╔═══════════════════════════════════════════════════════════════════════════════════════════╗
 ║                                                                                           ║
 ║    ▄█    █▄       ▄████████ ███▄▄▄▄      ▄██████▄    ▄▄▄▄███▄▄▄▄      ▄████████ ███▄▄▄▄   ║
 ║   ███    ███     ███    ███ ███▀▀▀██▄   ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███ ███▀▀▀██▄ ║
 ║   ███    ███     ███    ███ ███   ███   ███    █▀  ███   ███   ███   ███    ███ ███   ███ ║
 ║  ▄███▄▄▄▄███▄▄   ███    ███ ███   ███  ▄███        ███   ███   ███   ███    ███ ███   ███ ║
 ║ ▀▀███▀▀▀▀███▀  ▀███████████ ███   ███ ▀▀███ ████▄  ███   ███   ███ ▀███████████ ███   ███ ║
 ║   ███    ███     ███    ███ ███   ███   ███    ███ ███   ███   ███   ███    ███ ███   ███ ║
 ║   ███    ███     ███    ███ ███   ███   ███    ███ ███   ███   ███   ███    ███ ███   ███ ║
 ║   ███    █▀      ███    █▀   ▀█   █▀    ████████▀   ▀█   ███   █▀    ███    █▀   ▀█   █▀  ║
 ║                                                                                           ║
 ╠═══════════════════════════════════════════════════════════════════════════════════════════╝
 ║ type "quit" to exit.''')

    def main(self):
        while self.level < 9:
            self.print()

            letter = input(' ╚> ').upper()
            if letter == 'QUIT':
                break

            self.check_word(letter)
            if self.mask == self.word:
                self.reg_score(self.name)
                self.final('WON')
                break
        else:
            self.final('LOSE')

    def print(self):
        letters = self.formatted_letters()
        body = self.get_body()

        print('')
        print(" ╔═══════════════════════════════╗")
        print(" ║{:^31}║".format('HANGMAN'))
        print(" ╠═════╤═════╦═══════════════════╣")
        print(" ║{:^11}║{:^19}║".format(body[0], letters[0]))
        print(" ║{:^11}║{:^19}║".format(body[1], letters[2]))
        print(" ║{:^11}║{:^19}║".format(body[2], letters[1]))
        print(" ║{:^11}╠═══════════════════╣".format(body[3]))
        print(" ║{:^11}║{:^19}║".format(body[4], self.mask))
        print(" ╠═══════════╩═══════════════════╝")

    def final(self, mode):
        try:
            with open('files/score.json') as f:
                score = list(load(f).items())
        except decoder.JSONDecodeError:
            score = []

        print('')
        print(" ╔════════════════╗")
        print(" ║{:^16}║".format('YOU ' + mode))
        print(" ╠════════════════╣")
        print(" ║{:^16}║".format(self.word))
        print(" ╠══════════╤═════╣")
        for name, points in score[:4]:
            print(" ║ %-8s │ %-4s║" % (name, points))
        print(" ╚══════════╧═════╝")
        input()

    def reg_score(self, name):
        with open('files/score.json', 'r+') as f:
            points = 9 - self.level + len(self.word)
            try:
                json = load(f)
            except decoder.JSONDecodeError:
                json = {}

            if name in json:
                json[name] += points
            else:
                json[name] = points
            f.seek(0)

            json = sorted(json.items(), key=lambda x: x[1], reverse=True)
            dump(dict(json), f, indent=1)

    def get_body(self):
        return (
            ('', '', '', '', ''),
            ('O', '  ', '', '', ''),
            ('O', '/ ', '', '', ''),
            ('O', '/|', '', '', ''),
            ('O', '/|\\', '', '', ''),
            ('O', '/|\\', '´ | `', '', ''),
            ('O', '/|\\', '´ | `', '/  ', ''),
            ('O', '/|\\', '´ | `', '/ \\', ''),
            ('O', '/|\\', '´ | `', '/ \\', '°   °')
        )[self.level]

    @staticmethod
    def random_word():
        with open('files/wordlist.txt') as f:
            return choice(f.read().splitlines()).upper()

    def formatted_letters(self):
        return [self.letters[x:y] for x, y in ((0, 17), (17, 36), (36, 51))]

    def check_word(self, letter):
        if letter in self.letters and letter != '':
            if letter in self.word:
                for index, x in enumerate(self.word):
                    if x in letter:
                        self.mask = self.mask[:index] + self.word[index] + self.mask[index + 1:]
            else:
                self.level += 1
            self.letters = self.letters.replace(letter, ' ')


if __name__ == '__main__':
    Hangman()

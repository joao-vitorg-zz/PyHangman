from json import load, dump
from random import choice


class Hangman:
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
        print(f" ╔{'═' * 31}╗")
        print(f" ║{'HANGMAN':^31}║")
        print(f" ╠═════╤═════╦{'═' * 19}╣")
        print(f" ║{body[0]:^11}║{letters[0]:^19}║")
        print(f" ║{body[1]:^11}║{letters[1]:^19}║")
        print(f" ║{body[2]:^11}║{letters[2]:^19}║")
        print(f" ║{body[3]:^11}╠{'═' * 19}╣")
        print(f" ║{body[4]:^11}║{self.mask:^19}║")
        print(f" ╠{'═' * 11}╩{'═' * 19}╝")

    def final(self, mode):
        with open('files/score.json', 'r') as f:
            score = sorted(load(f).items(), key=lambda x: x[1], reverse=True)

        print('')
        print(f" ╔{'═' * 16}╗")
        print(f" ║{'YOU ' + mode:^16}║")
        print(f" ╠{'═' * 16}╣")
        print(f" ║{self.word:^16}║")
        print(" ╠══════════╤═════╣")
        for name, points in score[:4]:
            print(f" ║ {name:<8} │ {points:<4}║")
        print(" ╚══════════╧═════╝")
        input('')

    def reg_score(self, name):
        with open('files/score.json', 'r+') as f:
            points = 9 - self.level + len(self.word)
            json = load(f)

            if name in json:
                json[name] += points
            else:
                json[name] = points
            f.seek(0)
            dump(json, f, indent=1)

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

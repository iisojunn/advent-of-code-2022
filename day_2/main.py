import sys
from enum import Enum

ROCK = "ROCK"
PAPER = "PAPER"
SCISSORS = "SCISSORS"


class OpponentChoices(Enum):
    ROCK = "A"
    PAPER = "B"
    SCISSORS = "C"


class MyChoices(Enum):
    ROCK = "X"
    PAPER = "Y"
    SCISSORS = "Z"


CHOICE_SCORE = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3,
}


class MatchScore(Enum):
    WIN = 6
    TIE = 3
    LOSE = 0


MATCH_SCORE = {
    (ROCK, PAPER): MatchScore.WIN,
    (PAPER, SCISSORS): MatchScore.WIN,
    (SCISSORS, ROCK): MatchScore.WIN,
    (ROCK, ROCK): MatchScore.TIE,
    (PAPER, PAPER): MatchScore.TIE,
    (SCISSORS, SCISSORS): MatchScore.TIE,
    (PAPER, ROCK): MatchScore.LOSE,
    (SCISSORS, PAPER): MatchScore.LOSE,
    (ROCK, SCISSORS): MatchScore.LOSE,
}


def main():
    score = 0
    for opponent_choice, my_choice in strategy_guide(sys.argv[1]):
        score += MATCH_SCORE[(opponent_choice.name, my_choice.name)].value
        score += CHOICE_SCORE[my_choice.name]
    print(score)


def strategy_guide(file_name):
    with open(file_name) as file:
        for line in file.readlines():
            opponent, me = line.strip().split(" ")
            yield OpponentChoices(opponent), MyChoices(me)


if __name__ == '__main__':
    main()

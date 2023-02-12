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


class MatchResult(Enum):
    WIN = "WIN"
    TIE = "TIE"
    LOSE = "LOSE"


ROUND_TARGET = {
    "X": MatchResult.LOSE,
    "Y": MatchResult.TIE,
    "Z": MatchResult.WIN,
}

MATCH_SCORE = {
    MatchResult.WIN: 6,
    MatchResult.TIE: 3,
    MatchResult.LOSE: 0,
}

MATCH_RESULT = {
    (ROCK, PAPER): MatchResult.WIN,
    (PAPER, SCISSORS): MatchResult.WIN,
    (SCISSORS, ROCK): MatchResult.WIN,
    (ROCK, ROCK): MatchResult.TIE,
    (PAPER, PAPER): MatchResult.TIE,
    (SCISSORS, SCISSORS): MatchResult.TIE,
    (PAPER, ROCK): MatchResult.LOSE,
    (SCISSORS, PAPER): MatchResult.LOSE,
    (ROCK, SCISSORS): MatchResult.LOSE,
}

REQUIRED_CHOICE = {
    (ROCK, MatchResult.WIN): PAPER,
    (ROCK, MatchResult.TIE): ROCK,
    (ROCK, MatchResult.LOSE): SCISSORS,
    (PAPER, MatchResult.WIN): SCISSORS,
    (PAPER, MatchResult.TIE): PAPER,
    (PAPER, MatchResult.LOSE): ROCK,
    (SCISSORS, MatchResult.WIN): ROCK,
    (SCISSORS, MatchResult.TIE): SCISSORS,
    (SCISSORS, MatchResult.LOSE): PAPER,

}


def main():
    file_name = sys.argv[1]

    score = 0
    for opponent_choice, my_choice in strategy_guide_a(file_name):
        score += MATCH_SCORE[MATCH_RESULT[(opponent_choice.name, my_choice.name)]]
        score += CHOICE_SCORE[my_choice.name]
    print(score)

    score2 = 0
    for opponent_choice, target in strategy_guide_b(file_name):
        score2 += MATCH_SCORE[target]
        score2 += CHOICE_SCORE[REQUIRED_CHOICE[(opponent_choice.name, target)]]
    print(score2)


def raw_data(file_name):
    with open(file_name) as file:
        for line in file.readlines():
            yield line.strip().split(" ")


def strategy_guide_a(file_name):
    for opponent, me in raw_data(file_name):
        yield OpponentChoices(opponent), MyChoices(me)


def strategy_guide_b(file_name):
    for opponent, target in raw_data(file_name):
        yield OpponentChoices(opponent), ROUND_TARGET[target]


if __name__ == '__main__':
    main()

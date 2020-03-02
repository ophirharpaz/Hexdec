import click
import signal
import sys
import time
from random import choice, randint


DEFAULT_UPPER_LIMIT = 0x100
DEC, HEX, MIX = 'd2x', 'x2d', 'both'
AVERAGE_TIME = 0
ITERATIONS = 0


def welcome():
    print("""
     __________
    | ________ |
    ||12345678||
    |''''''''''|
    |[M|#|C][-]| HexDec - Become a Hexa(decimal) Pro!
    |[7|8|9][+]| Author: Ophir Harpaz (@ophirharpaz)
    |[4|5|6][x]| ascii art by hjw
    |[1|2|3][%]|
    |[.|O|:][=]|
    |==========|
    
    Set the game properties using:
    - the maximal number that will show up;
    - the game mode (d2x for decimal to hexa, x2d for the opposite direction, or both)
    """)


@click.command()
@click.option('--max-number',
              type=click.IntRange(1, sys.maxsize),
              prompt='Choose a maximal number',
              default=DEFAULT_UPPER_LIMIT)
@click.option('--game-mode',
              type=click.Choice((HEX, DEC, MIX), case_sensitive=False),
              prompt=True,
              default=HEX)
def play(max_number, game_mode):
    signal.signal(signal.SIGINT, signal_handler)
    global AVERAGE_TIME, ITERATIONS  # I use globals so that signal_handler can access the values from all stack-frames
    click.echo('To stop the game, type Ctrl+C')

    # Game loop
    while True:
        if MIX == game_mode:
            user_succeeded, response_time = play_round(max_number, hex_to_dec=choice([True, False]))
        elif DEC == game_mode:
            user_succeeded, response_time = play_round(max_number, hex_to_dec=False)
        else:
            user_succeeded, response_time = play_round(max_number, hex_to_dec=True)
        ITERATIONS += 1
        AVERAGE_TIME = (AVERAGE_TIME * (ITERATIONS - 1) + response_time) / ITERATIONS
        if not user_succeeded:
            click.echo('Oops, you got that last one wrong...')
            say_goodbye()
            return


def play_round(max_number, hex_to_dec):
    n = randint(0, max_number)
    n_for_display = hex(n) if hex_to_dec else n
    t = time.time()
    while True:
        try:
            input_num = input('* {} = '.format(n_for_display)).replace('0x', '')
            response_time = time.time() - t
            converted = int(input_num, 10 if hex_to_dec else 16)
            break
        except ValueError:
            click.echo('invalid value, try again:')
    return converted == n, response_time


def say_goodbye():
    click.echo('\nYou played {0} iterations '
               'and your average response time was {1:.3f} seconds. '
               'Come back again! :)'.format(ITERATIONS, AVERAGE_TIME))


def signal_handler(sig, frame):
    """
    Exit gracefully in case of a Ctrl+C event.
    """
    say_goodbye()
    sys.exit(0)


if __name__ == '__main__':
    if sys.version_info.major < 3:
        print('Use Python3 and later :)')
        sys.exit(0)
    welcome()
    play()

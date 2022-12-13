from Game import *

if __name__ == '__main__':
    game = SeaBattle(10)
    game.init()
    step_game = 0
    while game:
        if step_game % 2 == 0:
            game.human_go()
        else:
            game.computer_go()

        step_game += 1

    if game.is_human_win:
        print("Поздравляем! Вы победили!")
    elif game.is_computer_win:
        print("Все получится, со временем")
    else:
        print("Ничья.")
# Kuba

## Description

![directions](https://user-images.githubusercontent.com/32501313/117386394-b08b1180-ae9b-11eb-9779-9bbd8531c91d.PNG)

## Setup and Usage

Here's a very simple example of how your `KubaGame` class could be used by the autograder or a TA:
```
game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
game.get_marble_count() #returns (8,8,13)
game.get_captured('PlayerA') #returns 0
game.get_current_turn() #returns 'PlayerB' because PlayerA has just played.
game.get_winner() #returns None
game.make_move('PlayerA', (6,5), 'F')
game.make_move('PlayerA', (6,5), 'L') #Cannot make this move
game.get_marble((5,5)) #returns 'W'
```

## TODO

Expand README.
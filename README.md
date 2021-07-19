# Phazed Game and Player

* plays a card game called 'Phazed'
## [Live Demo]()
* hosted on repl.it

## About Phazed, the game
* A card game based off games like [Phase 10](https://en.wikipedia.org/wiki/Phase_10) and [Rummy](https://en.wikipedia.org/wiki/Rummy)
* Details about the game can be found in [`gamespec.pdf`](gamespec.pdf)

## Installation
> if you do not intend on ammending the code, you might want to use the [Live Demo](#live-demo) instead

## Playing the Game with `game.py`
* Default Settings
* Custom Settings
  > can be changed by entering `No` when asked ` → Use default settings? [Yes/No]:`
  * Normal/Bonus game
  * Number of Players (2 to 4 players)
  * Automatic Card Handling
* inputs are not case sensative

## Normal Bot 0, `normalbot0.py`
### Arguments
|Argument/Param|Description|
|---|--|
|`player_id`|integer between 0 and 3 inclusive, indicating the ID of the player attempting the play|
|`table`|4-element list representing the table; which has the phase plays for each of Players 0-3|
|`turn_history`|list of all turns in the hand to date|
|`phase_status`|a 4-element list indicating the phases that each of Players 0-3|
|`hand`|list of cards in the current player's hand|
|`discard`|the top card of the discard stack|
* Returns:
  * a 2-tuple consisting of the type of play and the cards being played

## Bonus Bot 0, `bonusbot0.py`

## How to Add Bots
* Normal Bots have to be named `normalbot#`
    and Bonus Bots have to be named `bonusbot#` where # is a number betweeen
    0 and 3 inclusive as there can only be a maximum of 4 bots playing at a 
    time.

<sub>`player.py` placed 11th out of 438 players submitted to a subject-cohort-wide tournament and `player-bonus.py` placed 2nd out of 266 other players submitted to a bonus tournament. </sub>

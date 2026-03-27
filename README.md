# PyBadge-Snake
This is the game snake coded for a PyBadge LC. I coded this in CircuitPython version 10.0.3. The version of CircuitPython used is a slightly modified version for slight efficiency increase and fixed [stage and ugame](https://github.com/python-ugame/circuitpython-stage) library's. I origonaly was planning on using [Stage](https://github.com/python-ugame/circuitpython-stage) which is why I contacted adafruit to get them to get it fixed and added it to my circuit python.

# Features
This snake game features lots of options. There are 9 backgrounds, 11 customizable snake colors, 10 speed options, shadows, and a face which are all customizable through the built in settings menu which you can access by pressing the select button.

## Backgrounds
This game has 9 great colors including:
| Color    | Background | Color    | Background |
| -------- | ---------- | -------- | ---------- |
| ☀️Day    | ![day]    | ⭐️Night  | ![night]   |
| ❄️Snow   | ![snow]   | 🌋Lava   | ![lava]    |
| 🌵Desert | ![desert] | 🌳Forest | ![forest]  |
| 🌊Sea    | ![sea]    | 👽Space  | ![space]   |
| 🐍Basic  | ![basic]  |          |            |

## Snake Colors
| Color      | Preview       | Color     | Preview      |
| ---------- | ------------- | --------- | ------------ |
| Red        | ![red]        | Pure Blue | ![pure_blue] |
| Orange     | ![orange]     | Blue      | ![blue]      |
| Yellow     | ![yellow]     | Purple    | ![purple]    |
| Pure Green | ![pure_green] | Pink      | ![pink]      |
| Green      | ![green]      | Black     | ![black]     |
| White      | ![white]      |           |              |

## Speed
There are 10 diffrent speed options with varing levels of difficulty. there is anything from speed 1 which is easy to ten which is very fast. It is toggleable from within the settings menu and defults to 5.
This snake game features a shadow that is under the snake. It is toggleable from within the settings menu and defults to True.
## Face
This snake game features a face that changes the way it is looking based on the direction you move. It is toggleable from within the settings menu and defults to True.

[day]:   ./github/background_day.png 
[night]: ./github/background_night.png
[snow]:  ./github/background_snow.png
[lava]:  ./github/background_lava.png
[desert]:./github/background_desert.png
[forest]:./github/background_forest.png
[sea]:   ./github/background_sea.png
[space]: ./github/background_space.png
[basic]: ./github/background_basic.png

[red]:       ./github/snake_red.png          
[orange]:    ./github/snake_orange.png
[yellow]:    ./github/snake_yellow.png
[pure_green]:./github/snake_pure_green.png
[green]:     ./github/snake_green.png
[pure_blue]: ./github/snake_pure_blue.png
[blue]:      ./github/snake_blue.png
[purple]:    ./github/snake_purple.png
[pink]:      ./github/snake_pink.png
[white]:     ./github/snake_white.png
[black]:     ./github/snake_black.png

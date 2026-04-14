# PyBadge-Snake
This is the game snake coded for a PyBadge LC. I coded this in CircuitPython version 10.0.3. The version of CircuitPython used is a slightly modified version for slight efficiency increase and fixed [stage and ugame](https://github.com/python-ugame/circuitpython-stage) library's. I originally was planning on using [Stage](https://github.com/python-ugame/circuitpython-stage) which is why I contacted adafruit to get them to get it fixed and added it to my circuit python.

# Features
This snake game features lots of options. There are 9 backgrounds, 11 customizable snake colors, 10 speed options, shadows, and a face which are all customizable through the built in settings menu which you can access by pressing the select button. When you hold the B button when resetting or plugging in or turning on it puts in to PyBadge mode where the settings and high score are saved after each round. in the terminal when plugged in it prints out a log for debugging:
```
code.py output:
Total    Load      Memory  Section
119.0ms  119.0ms   113152  Load Modules
119.3ms  0.2ms     112672  Initializing the Display
235.1ms  115.8ms   95648   Font Load
295.4ms  60.3ms    92528   Initialize Speaker
296.1ms  0.7ms     90976   Button Setup
296.3ms  0.1ms     90560   Initialize Read/Write to "settings.json"
[... 29 lines of logs ...]
527.1ms  16.1ms    67072   Game Settings
538.5ms  11.4ms    68624   Garbage Collection
1033.7ms 495.2ms   68192   Enable Display
1045.0ms 11.4ms    68624   Garbage Collection
```

## Backgrounds
This game has 9 great color themes including:
| Color    | Background | Color    | Background |
| -------- | ---------- | -------- | ---------- |
| ☀️Day    | ![day]    | ⭐️Night  | ![night]   |
| ❄️Snow   | ![snow]   | 🌋Lava   | ![lava]    |
| 🌵Desert | ![desert] | 🌳Forest | ![forest]  |
| 🌊Sea    | ![sea]    | 👽Space  | ![space]   |
| 🐍Basic  | ![basic]  |          |            |

## Snake Colors
There are 11 diffrent colors for the snake:
| Color      | Preview       | Color     | Preview      |
| ---------- | ------------- | --------- | ------------ |
| Red        | ![red]        | Pure Blue | ![pure_blue] |
| Orange     | ![orange]     | Blue      | ![blue]      |
| Yellow     | ![yellow]     | Purple    | ![purple]    |
| Pure Green | ![pure_green] | Pink      | ![pink]      |
| Green      | ![green]      | Black     | ![black]     |
| White      | ![white]      |           |              |

## Speed
There are 10 different speed options with varying levels of difficulty. there is anything from speed 1 which is easy to ten which is very fast. It is toggleable from within the settings menu and is one of the settings that auto loads from the settings.json.
## Shadow
This snake game features a shadow that is under the snake. It is toggleable from within the settings menu and is one of the settings that auto loads from the settings.json.
## Face
This snake game features a face that changes the way it is looking based on the direction you move. It is toggleable from within the settings menu and is one of the settings that auto loads from the settings.json.
## Settings
The setting are all stored in a settings file called <code>settings.json</code> formatted like this:
```jsonc
{
  "high_score": 27, //The high score as a integer
  "shadow": false,  //The status of the shadow as a boolean
  "head": true,     //The status of the head as a boolean
  "bg_idx": 0,	    //The index for the color theme. A number of value 0-8 for the 9 backgrounds
  "snake_idx": 0,   //The index for the snake color. A number of value 0-10 for the 11 backgrounds
  "speed": 5        //The speed of the snake as a positive integer
}
```
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
# Design

## Game Hierarchy

```
Game
├── Screen
│   ├── Layers
│   │   ├── LayerN - array or sprite group? 
│   │   └── ...
│   └── render()
│       └── Calls each sprite's draw() function and passes a "transform" such as the camera
├── Camera
│   └── apply((x, y))
│       ├── offset() # Calculated with target_sprite
│       ├── scale() # TODO
│       └── returns transformed sprite position 
└── States
    ├── Menus
    │   └── Main Menu
    │       └── Components
    │           ├── Buttons
    │           │   └── on/off with tweening
    │           └── Sliders
    └── Main Game
        ├── Level Data
        ├── Sprites
        ├── Colliders
        ├── Player
        ├── Collision detection
        └── Pause Screen
```

[Edit Here](https://tree.nathanfriend.io/?s=(%27opIns!(%27fancy!true~fullPatFtYilingSlasFrootDot!true)~K(%27K%27Game3ULVRLVN%20-ZrYy%20orWgroup%3F%205...0rHdAQ5Call7each94%227dYw2funcI6and%20passe7a%20%5C%27E%5C%279uchZ7thjcamAa3CamAa0apply%7B%7Bx%2C%20y%7D%7D5offsetJCalculabd8arget_s45scaleJTODO5return7EedWposiI63Stabs0MHuRkMHu5*CompXHtR**ButtXR***X%2Foff8weHing5**SlidAs0kGame5Level%20Data5S4RCollidARPlV5Collisio6debcIn5PausjU3%27)~vAsiX!%271%27)*%20%2003*2Q%203%5Cn*4prib50*6n%207s%208%20with%20t9%20sAerEtYnsformFh!false~HenItioJ2%23%20Ksource!Q%7B%7DRs5UScreH0VayAW94%20XonYraZ%20abteje%20kMai6%01kjbZYXWVURQKJIHFEA987654320*)


Example Game Sprite class declaration (using custom sprite)

```python

class EvilSnake(src.Sprite):
    """The most evil of evil snakes
    """

    def __init__(self, game, **kwargs):
        super().__init__(game.enemy, game.screen.layer12) # Sprite type and Render layer
        self.animation = src.Animator(asset("snake/snake_animated.png"))
        self.init_physics()
    
    def init_physics():
        ...
```

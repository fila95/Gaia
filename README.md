# Advanced-User-Interfaces
Advanced User Interfaces Course Repository

## Configuration

### Actions:
Actions are composed as follows:
``` json
{
	"parseIdentifier": "START",
	"attributes": {}
}
```

Other two *OPTIONAL* attributes can be specified:
``` json
{
	"parseIdentifier": "START",
	"attributes": {},
	"identifier": "__ID__",
	"timeout": 10
}
```

`identifier` m if specified, sets an identifier for that action so that can be used to the Skip Action.
`timeout` if specified (in seconds), kills the action after a certain amount of time.

#### StartAction
An action that identifies the game's start point.
Start and End actions should be used ONLY in the mail loadable action file!
``` json
{
	"parseIdentifier": "START",
	"attributes": {}
}
```

###### Available Attributes
No attributes are needed.

---

#### End Action
An action that identifies the game has reached the end.
Start and End actions should be used ONLY in the mail loadable action file!
``` json
{
	"parseIdentifier": "END",
	"attributes": {}
}
```

###### Available Attributes
No attributes are needed.

---

#### Restart Action
An action that restarts the entire action hierarchy!
``` json
{
	"parseIdentifier": "RESTART",
	"attributes": {}
}
```

###### Available Attributes
No attributes are needed.

---

#### Play Animation Action
An action that plays an animation on the dots!
If no timeout is specified in the action's definition the action starts and ends immediately so make sure to set the `stops_at_end` key accordingly to your needs!
``` json
{
	"parseIdentifier": "PLAY_ANIMATION",
	"attributes": {
		"animation": "RAINBOW_CYCLE",
		"animation_affect_dots": true,
		"stops_at_end": true
	}
}
```

###### Available Attributes

| Parameter 	| Type       	| Description 	|
|-----------	|------------	|-------------	|
| animation | `required` 	| animation should be one of: `RAINBOW`, `RAINBOW_CYCLE`, `THEATER_CHASE_RAINBOW`|
| animation_affect_dots | `optional` 	| wether animation animates the single leds or the entire dot |
| stops_at_end | `required` 	| when action finishes set `true` if the animation should stop, otherwise set `false`|

---

#### Dynamic Load Action
An action that loads other actions from file and appends them after itself. Then goes directly to the next one.
``` json
{
	"parseIdentifier": "DYNAMIC_LOAD",
	"attributes": {
		"paths": [
			"config/blabla.action.json"
		]
	}
}
```

###### Available Attributes

| Parameter 	| Type       	| Description 	|
|-----------	|------------	|-------------	|
| paths | `required` 	| array of strings identifying one file each|


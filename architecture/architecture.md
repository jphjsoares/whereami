#Architecture explanation

This file explains various endpoints that are in the architecture.drawio file

/map/newbyregion -> select n different locations in a given (default) region
/map/newworld -> select n different locations in the world
/map/createcustom -> a user is able to create a custom game (chooses different locations)
/game/createnewgame -> user selects the map, privacy and only the creator is allowed to invite player

|Endpoint           | Explanation                  		                      					   |
|-------------------|------------------------------------------------------------------------------|
|/map/newbyregion   |select n different locations in a given (default) region	  				   |
|/map/newworld      |select n different locations in the world                   				   |
|/map/createcustom  |a user is able to create a custom game (chooses different locations)		   |
|/game/createnewgame|user selects the map, privacy and only the creator is allowed to invite player|
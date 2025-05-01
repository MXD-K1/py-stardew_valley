# Py-StarDew Valley - Learning Project

This project is inspired by the [Clear Code YouTube tutorial](https://www.youtube.com/watch?v=T4IX36sP_0c) 
on creating a Stardew Valley-inspired game using Python and Pygame. It serves as a learning exercise to explore 
game development concepts, Python programming, and Pygame functionalities.

## Version
**Current Version**: 1.0.0  
(*This version reflects the initial release of the learning project.*)

## Features
- **Farming mechanics**.
- **Day and night cycle**.
- **Weather effects**.
- **Merchant interactions**.
- **Tile-based map and sprite animations**.
- **Saving Mechanism:** progress is automatically saved when the player sleeps, ensuring a seamless experience
and preventing data loss. Players can resume their game from their last rest point.

## Purpose
The primary goal of this project is to:
1. Learn and practice Python programming.
2. Understand game development principles.
3. Explore Pygame for creating 2D games.

## To-do List
1. Add seasons to the game.
2. Add a visible inventory for the player.
3. Money will be visible all time.
4. More items will be added to the game.
5. Enhance plants and soil logic.
6. Add sav for the time.

## Playing guide
- To move use arrows.
- To sleep go to the bed and press Enter.
- To use a tool press space key.
- To change a tool press q.
- To change the seed use e key.
- To plant a seed press left ctrl.
- To trade with the merchant press Enter.
- To end trading press Escape key.
- To buy or sell something press space.

## Problems
1. For unknown reason some the _sprites_ might not appear in the screen. As a temporary solution I sorted the
*sprite groups*.
2. If long time was spent in the game without sleeping, the display gets weird.

## How to Run
1. Clone this repository to your local machine.
2. Ensure Python is installed (Python version >= 3.6 is required).  
   *You can verify your Python version with:*
   ```bash
   python --version
   ```
3. Install the required dependencies:
   ```bash
   pip install pygame, pytmx
   ```
4. Run the main script:
   ```bash
   python main.py
   ```
   
OR simply you can run the [EXE file](EXE/Py-stardew%20vally.exe).

## Resources
- **YouTube Tutorial**: [Creating a Stardew Valley-inspired game in Python](https://www.youtube.com/watch?v=T4IX36sP_0c)
- by Clear Code.
- **GitHub Repository**: [PyDew Valley](https://github.com/clear-code-projects/PyDew-Valley) 
- for code and resources in the game.

## Contributing
Contributions to this project are welcome and encouraged!
Whether it's improving the code, fixing problems,  suggesting new features, or sharing ideas,
feel free to get involved.
    
---
*To contribute:* 
- Fork the project.
- Make your changes.
- Create a pull request!

## Acknowledgments
Special thanks to **_Clear Code_** for providing an excellent tutorial and resources to guide this learning journey.

## License
This project is open-source and available under the MIT License. Feel free to use, modify, and distribute the code,
provided proper attribution is given. For more information see the included [license](LICENSE).
   

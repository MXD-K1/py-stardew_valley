# Py-StarDew Valley - Learning Project

This project is inspired by the [Clear Code YouTube tutorial](https://www.youtube.com/watch?v=T4IX36sP_0c) 
on creating a Stardew Valley-inspired game using Python and Pygame. It serves as a learning exercise to explore 
game development concepts, Python programming, and Pygame functionalities.

## Version
**Current Version**: 1.0.2  
*When the game reach version 1.1.0, it will be ready for playing!*.

## What's New:
- Fixed some bugs:
  1. EXE and the source files are working now.
  2. Money appears all the time.
  3. Settings are being added
  
## Features
- **Farming mechanics**.
- **Day and night cycle**.
- **Weather effects**.
- **Merchant interactions**.
- **Tile-based map and sprite animations**.
- **Saving Mechanism:** progress is automatically saved when the player sleeps, ensuring a seamless experience and 
preventing data loss. Players can resume their game from their last rest point.

## Purpose
The primary goal of this project is to:
1. Learn and practice Python programming.
2. Understand game development principles.
3. Explore Pygame for creating 2D games.
4. Understand and explore Tiled for making tile-based games.

## To-do List
1. [ ] Add seasons to the game.
2. [ ] Add a visible inventory for the player. (In progress)
3. [x] Money will be visible all time.
4. [ ] More items will be added to the game.
5. [ ] Enhance plants and soil logic.
6. [ ] Change saving mechanism to save at any time. (In progress)
7. [ ] Add settings to the game. (In progress)
8. [ ] Save the time and the state of the trees in the game.


## Playing Guide
- To move use arrows.
- To sleep go to the bed and press Enter.
- To use a tool press space key.
- To change a tool press q.
- To change the seed use e key.
- To plant a seed press left ctrl.
- To trade with the merchant press Enter.
- To end trading press Escape key.
- To buy or sell something press space.
- To switch between items in the inventory use a and d keys.
- To select a tool from the inventory press Enter.

## Problems
1. For unknown reason some the _sprites_ might not appear in the screen. As a temporary solution I sorted the
*sprite groups*.
2. If long time was spent in the game without sleeping, the display gets weird.  (In progress)

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
4. If you are not in code file write this into the terminal:
    ```bash
   cd code
   ```
5. Run the main script:
   ```bash
   python main.py
   ```
   
OR simply you can run the [EXE file](EXE/Py-stardew%20vally.exe).

## Resources
- **YouTube Tutorial**: [Creating a Stardew Valley-inspired game in Python](https://www.youtube.com/watch?v=T4IX36sP_0c)
by Clear Code.
- **GitHub Repository**: [PyDew Valley](https://github.com/clear-code-projects/PyDew-Valley) 
- for code and resources in the game.
- **Asset packs**:
  - https://cupnooble.itch.io/sprout-lands-asset-pack
  - https://cupnooble.itch.io/sprout-lands-ui-pack

## Contributing
Contributions to this project are welcome and encouraged!
Whether it's improving the code, fixing problems, suggesting new features, or sharing ideas, feel free to get involved.
    
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

## Contact 
For any questions, issues, or feedback, don't hesitate to open an issue on GitHub or email me at hmdoonwork71@gmail.com.
   

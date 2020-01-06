# Search/Pathfinding Visualization

## Overview
I created this project mainly to practice my Python and search algorithm skills and create a visualization tool to help see how different search techniques work. I got the idea from YouTube and thought I would have a go at creating something similar. 

### Instructions
I included a requirements.txt for dependencies and versions. I had to use PyGame 2.0.0.dev6 because anything earlier didn't work with MacOS. 

- Run main.py
- Select grid size and search algorithm
- Select start and goal row/col Note: row/col values change based on grid size chosen
- Confirm your selection and the grid will appear
- Click and hold left mouse to add walls to the grid
- Press SPACEBAR to start the visualization 

## Approach

Some notes on my approach and issues I came across.

**Tools used:** 
- Tkinter: To create a window with different options for the user to select which search technique and grid size to use.
- Pygame: Generates the actual visualization of the search algorithm in progress 

### Choice for Visualization
In hindsight I don't know if Pygame was the best choice to create the visualization. Maybe Matlab or something else would have been better but I didn't have experience with any GUI libraries so I figured I'd try out PyGame and see how it went. All things considered, I'm happy with how it turned out.

### Threads
One of the main issues I had was how to separate the visualization and the actual algorithm. I could have merged the algorithms inside the main game loop that created the visuals but that seemed a little tedious and felt like a bad approach to the problem. And once the PyGame loop is running (i.e. making the grid show up)no other code will run. 

I decided to try Python's Threading library and it worked well aside from a few hiccups with PyGame. I initially tried to have PyGame's game loop split off in a separate thread but I quickly discovered PyGame isn't threadsafe and it's better to handle the game-loop in the main thread. I ended up making the search algorithm run as a separate thread.

### Tkinter
I wanted to have an interface to choose options about the grid and which algorithm to use. Since tkinter is included with Python it seemed like the logical choice.

One of the hurdles I had with this was setting up a way to limit the indices available to choose from for the start/goal cells. I wanted to have different grid sizes so these values had to change based on that grid size was chosen.

I thought the easiest way to do this would be a paging window system so the indices could update based on the selections made in the previous window. I also wanted to allow the option to return and change selections from previous windows. It turns out this was a little more complicated to achieve than I thought it would be, but luckily there are some excellent tutorials on StackOverflow for how to do this. Link below.

### PyGame 
Creating the grid in PyGame was one the easier parts of this project. It was fairly simple to generate a grid window with the draw.line method in PyGame. The only slightly tricky thing was converting locations on the PyGame grid to indices in the matrix used in the search algorithm.

### Features to Implement
Some of the things that I would like to improve or implement:
- Implement another window to start the search algorithm after walls have been added instead of having to press spacebar
- Add the ability remove walls after they have been added
- Add a way to increase the weight of cells to see how A-star reacts to an increased weight in certain cells
- Implement Dijkstra's after above bullet point

### Resources/Helpful Websites
Some great resources that I found along the way that helped me out a lot.

Excellent tutorial on A-Star and how to implement. Also many other helpful guides on other topics  
https://www.redblobgames.com/pathfinding/a-star/introduction.html  

Guide on creating stackable tkinter frames. My window.py is basically this just tweaked for my needs  
https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter


### Conclusion
I had a lot of fun with this project and definitely learned a lot along the way. Although I was familiar with BFS and DFS I didn't have as much knowledge on A-Star and this project definitely gave me a better understanding of how it works. Hopefully this inspires someone else to try something similar! 


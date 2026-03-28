# Traffic-Navigation-Simulator
AI-based traffic navigation simulator using BFS, DFS, A, and Greedy algorithms with interactive visualization.

##  Overview
The Traffic Navigation Simulator is an AI-based project that finds the optimal path between a start and end point on a grid using the A* algorithm. It simulates real-world navigation by considering obstacles and traffic conditions.

The project supports both:
- GUI-based visualization using Tkinter
- CLI-based execution for automated evaluation

##  Features
- A* pathfinding algorithm  
- Obstacle avoidance  
- Traffic-aware routing  
- Dual interface (GUI + CLI)  
- Command-line execution support  

##  Project Structure
Traffic_Simulator/
├── app.py
├── cli.py
├── README.md

##  Requirements
- Python 3.x
- Tkinter (pre-installed with Python)

##  How to Run

### CLI Mode 
python cli.py

### GUI Mode
python app.py

##  Algorithm Used
The project uses the A* (A-Star) algorithm, which combines actual path cost and heuristic estimation (Manhattan distance) to find the shortest path efficiently.

## Output
- PATH → sequence of coordinates
- STEPS → number of steps taken
- TOTAL COST → cost including traffic

## Note
The CLI version is designed for automated evaluation and runs without user input.

##  Future Enhancements
- Real-time traffic updates  
- Multiple algorithm support (BFS, UCS)  
- Dynamic grid input  

### Project Report
[View Project Report (Google Docs)](https://docs.google.com/document/d/1B61d3MUliVfx2qD1ZTwrh-SK5EnPUuoKdxVBoJml4IU/edit?tab=t.0)

##  Author
Faleha Karim 
VIT University

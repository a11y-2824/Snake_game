#!/usr/bin/env python3
"""
Terminal Snake Game
A classic Snake game that runs in the terminal using only Python built-in libraries.
Use WASD or arrow keys to control the snake.
"""

import random
import time
import sys
import os
import msvcrt  # Windows-specific module for keyboard input

class SnakeGame:
    def __init__(self, width=40, height=20):
        self.width = width
        self.height = height
        self.snake = [(width // 2, height // 2)]
        self.direction = (1, 0)  # Start moving right
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        
    def generate_food(self):
        """Generate food at a random position not occupied by the snake"""
        while True:
            food = (random.randint(1, self.width - 2), random.randint(1, self.height - 2))
            if food not in self.snake:
                return food
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw(self):
        """Draw the game board"""
        self.clear_screen()
        
        # Create the game board
        board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Draw borders
        for x in range(self.width):
            board[0][x] = '#'
            board[self.height - 1][x] = '#'
        for y in range(self.height):
            board[y][0] = '#'
            board[y][self.width - 1] = '#'
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            if i == 0:  # Head
                board[y][x] = '@'
            else:  # Body
                board[y][x] = '*'
        
        # Draw food
        fx, fy = self.food
        board[fy][fx] = '$'
        
        # Print the board
        for row in board:
            print(''.join(row))
        
        print(f"Score: {self.score}")
        print("Controls: W/A/S/D or Arrow Keys to move, Q to quit")
    
    def get_input(self):
        """Get keyboard input (Windows-specific using msvcrt)"""
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\xe0':  # Arrow key prefix
                key = msvcrt.getch()
                if key == b'H':  # Up arrow
                    return 'w'
                elif key == b'P':  # Down arrow
                    return 's'
                elif key == b'K':  # Left arrow
                    return 'a'
                elif key == b'M':  # Right arrow
                    return 'd'
            else:
                return key.decode('utf-8').lower()
        return None
    
    def update_direction(self, key):
        """Update snake direction based on input"""
        directions = {
            'w': (0, -1),  # Up
            's': (0, 1),   # Down
            'a': (-1, 0),  # Left
            'd': (1, 0)    # Right
        }
        
        if key in directions:
            new_direction = directions[key]
            # Prevent snake from going backwards into itself
            if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
                self.direction = new_direction
    
    def move_snake(self):
        """Move the snake in the current direction"""
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check for collisions with walls
        if (new_head[0] <= 0 or new_head[0] >= self.width - 1 or
            new_head[1] <= 0 or new_head[1] >= self.height - 1):
            self.game_over = True
            return
        
        # Check for collision with self
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def run(self):
        """Main game loop"""
        print("Welcome to Terminal Snake!")
        print("Press any key to start...")
        msvcrt.getch()
        
        while not self.game_over:
            self.draw()
            
            # Get input with timeout
            start_time = time.time()
            key = None
            while time.time() - start_time < 0.2:  # 200ms timeout
                key = self.get_input()
                if key:
                    break
                time.sleep(0.01)
            
            if key == 'q':
                break
            
            if key:
                self.update_direction(key)
            
            self.move_snake()
        
        # Game over screen
        self.clear_screen()
        print("Game Over!")
        print(f"Final Score: {self.score}")
        print("Press any key to exit...")
        msvcrt.getch()

def main():
    """Main function to start the game"""
    try:
        game = SnakeGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Make sure you're running this on Windows with Python 3.x")

if __name__ == "__main__":
    main()

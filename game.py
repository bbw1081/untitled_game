import pygame

class Game():
    """A class to handle all of the high-level game functions"""
    def __init__(self):
        """Initialize the game"""
        pass

    def update(self):
        """Update the game"""
        self.check_collisions()

    def draw(self):
        """draw the HUD"""
        pass

    def check_collisions(self):
        """Check for collisions that affect gameplay"""
        pass

    def check_round_completion(self):
        """Check to see if the player has completed the round"""
        pass

    def check_game_over(self):
        """Check to see if the player has died"""
        pass

    def start_next_round(self):
        """Start the next round of the game"""
        pass

    def main_menu(self):
        """Display the main menu"""
        pass

    def death_screen(self):
        """Display the death screen"""
        pass

    def intermission_screen(self):
        """Display the screen that will be shown between rounds"""
        pass

    def reset_game(self):
        """Completley reset the game"""
        pass

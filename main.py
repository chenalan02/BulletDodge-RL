from game import Map

if __name__ == "__main__":
    game = Map("black.jpg", FPS=200)
    game.addAI( (0,0), speed=0.5, cooldown= 50, movementFactor=25)
    done = False

    while not done:
        done = game.update()
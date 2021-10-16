from game import Map

if __name__ == "__main__":
    game = Map(FPS=150)
    game.addHardcodedAI( (0,0), speed=0.5, cooldown= 50, movementFactor=25)
    game_done = False

    while not game_done:
        game.move()
        nextState, reward, done = game.update()
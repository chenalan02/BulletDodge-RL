from game import Map

if __name__ == "__main__":
    game = Map("grassy_field.jpg", userPlaying=True)
    game.addAI( (0,0), cooldown= 100, movementFactor=50)
    game.all_find_enemies()
    done = False

    while not done:
        done = game.update()
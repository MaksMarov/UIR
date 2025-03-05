import pygame
from simulation import Simulation
from renderer import Renderer
from data_tool import save_simulation_results_csv

def run():
    pygame.init()

    FPS = 60
    clock = pygame.time.Clock()

    simulation = Simulation()
    renderer = Renderer(simulation.grid)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation.toggle_pause()

        if simulation.update():
            save_simulation_results_csv(len(simulation.grid.dead_people), len(simulation.grid.survived_people), simulation.timer)
            break

        renderer.render(people=simulation.grid.people)
    
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    
run()
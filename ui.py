import pygame
import pygame.freetype
from pygame.locals import *
from assets.constants.constants import Constants
from classes.sudoku.sudoku import Sudoku
from classes.logging.logger import Logger
from classes.difficulty.difficulty import Difficulty


pygame.mixer.init()
pygame.init()

pygame.display.set_caption(Constants.GAME_TITLE)
pygame.display.set_icon(pygame.image.load(Constants.FAVICON))


screen = pygame.display.set_mode(
    [Constants.SCREEN_WIDTH,
     Constants.SCREEN_HEIGHT]
)
sudoku=Sudoku()
selected_difficulty= Difficulty.EASY
logger = Logger()
MARGINS=50
TILE_SIZE=50
NUMBER_MARGIN=20 

def draw_button(screen, image_path, position, title, max_size=(100, 100), font_size=24):
    button = pygame.image.load(image_path)
    original_size = button.get_size()
    aspect_ratio = original_size[0] / original_size[1]
    new_width = min(max_size[0], original_size[0])
    new_height = min(max_size[1], original_size[1])

    if original_size[0] > max_size[0] or original_size[1] > max_size[1]:
        if aspect_ratio >= 1:
            new_height = int(new_width / aspect_ratio)
        else:
            new_width = int(new_height * aspect_ratio)

    button = pygame.transform.scale(button, (new_width, new_height))

    screen.blit(button, position)

    font = pygame.font.Font(None, font_size)
    text_surf = font.render(title, True, (0, 0, 0))
    text_rect = text_surf.get_rect(
        center=(position[0] + new_width // 2, position[1] - new_height // 4))

    screen.blit(text_surf, text_rect)

    return button.get_rect(topleft=position)


def draw_value(screen, value, position):
    font = pygame.freetype.SysFont("Arial", 24)
    font.render_to(screen, position, str(value), (0, 0, 0))


def splash_screen():
    running = True

    background = pygame.image.load(Constants.SPLASH_SCREEN_BACKGROUND)
    background = pygame.transform.scale(
        background, (Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    screen.blit(background, (0, 0))

    play_button_image = pygame.image.load(Constants.PLAY_BUTTON)
    play_button_size = play_button_image.get_size()
    play_button_scaled = pygame.transform.scale(
        play_button_image, (play_button_size[0] // 1.5, play_button_size[1] // 1.5))
    play_button_rect = play_button_scaled.get_rect(center=(
        Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT - Constants.SCREEN_HEIGHT // 5))
    screen.blit(play_button_scaled, play_button_rect.topleft)

    font_path = pygame.freetype.match_font("Consolas")
    font_size = 80
    font = pygame.freetype.Font(font_path, font_size)
    font_color = (255, 255, 255)
    text_animation_counter = 0
    increase = True

    pygame.mixer.music.load(Constants.MUSIC_PATH)
    pygame.mixer.music.set_volume(Constants.DEFAULT_VOLUME)
    pygame.mixer.music.play(-1)

    while running:
        mouse_pos = pygame.mouse.get_pos()

        if play_button_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN and play_button_rect.collidepoint(event.pos):
                pygame.mixer.music.stop()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                running = False

        if increase:
            text_animation_counter += 1
            if text_animation_counter > 10:
                increase = False
        else:
            text_animation_counter -= 1
            if text_animation_counter < -10:
                increase = True

        font_size = max(100 + text_animation_counter * 2, 80)
        font.size = font_size
        title_surface, title_rect = font.render("Sudoku", font_color)
        title_rect.center = (Constants.SCREEN_WIDTH // 2,
                             Constants.SCREEN_HEIGHT // 5)

        screen.blit(background, (0, 0))
        screen.blit(play_button_scaled, play_button_rect.topleft)
        screen.blit(title_surface, title_rect)

        pygame.display.flip()
        pygame.time.wait(50)


def draw_sudoku_grid(screen):
    grid_origin = (50, 50)
    grid_size = 450
    cell_size = grid_size // 9
    line_color = (0, 0, 0)

    for i in range(10):
        line_width = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, line_color, (grid_origin[0] + i * cell_size, grid_origin[1]),
                         (grid_origin[0] + i * cell_size, grid_origin[1] + grid_size), line_width)
        pygame.draw.line(screen, line_color, (grid_origin[0], grid_origin[1] + i * cell_size),
                         (grid_origin[0] + grid_size, grid_origin[1] + i * cell_size), line_width)


def draw_sudoku_screen():
    screen.fill((255, 255, 255))

    background = pygame.image.load(Constants.SUDOKU_SCREEN_BACKGROUND)
    background = pygame.transform.scale(
        background, (Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    screen.blit(background, (0, 0))

    hint_button_rect = draw_button(
        screen, Constants.HINT_BUTTON,
        (600, 100), "Indices", max_size=(100, 100)
    )

    refresh_button_rect = draw_button(
        screen, Constants.REFRESH_BUTTON,
        (600, 275), "Nouvelle partie", max_size=(100, 100)
    )

    difficulty_button_rects = draw_difficulty_buttons(
        screen, 520, 400)

    draw_sudoku_grid(screen)

    draw_numbers(screen)

    return refresh_button_rect, hint_button_rect, difficulty_button_rects


def draw_difficulty_buttons(screen, start_x, start_y):
    colors = [(0, 255, 0), (255, 255, 0), (255, 100, 0)]
    titles = ["Facile", "Intermédiaire", "Avancé"]
    rects = []

    x = start_x
    for i, (title, color) in enumerate(zip(titles, colors)):
        rect = draw_colored_button(
            screen, (x, start_y), title, color, padding=(10, 5))
        rects.append(rect)
        x += rect.width + Constants.BUTTON_SPACING

    return rects


def draw_colored_button(screen, position, title, color, padding=(10, 5)):
    font = pygame.font.Font(None, 20)
    text_surf = font.render(title, True, (0, 0, 0))
    text_size = text_surf.get_size()

    button_width = text_size[0] + 2 * padding[0]
    button_height = text_size[1] + 2 * padding[1]
    button_size = (button_width, button_height)

    button_rect = pygame.Rect(position, button_size)
    pygame.draw.rect(screen, color, button_rect)

    text_rect = text_surf.get_rect(center=button_rect.center)

    screen.blit(text_surf, text_rect)

    return button_rect


def draw_numbers(screen):
    """
    TODO: 4.3. Affichage d'un chiffre à l'écran au sein d'une case
    """
    # TODO: 4.3. Affichage d'un chiffre à l'écran au sein d'une case
    #on veut iterer sur chacune des positions de notre sudoku
    for i in range(9):
        for j in range(9):
            value = sudoku._board[i][j]
            if value != 0:
                x_pos= i * TILE_SIZE + MARGINS + NUMBER_MARGIN #va permettre daller dans la case que l'on veut
                y_pos= j * TILE_SIZE + MARGINS + NUMBER_MARGIN
                draw_value(screen, value, (x_pos, y_pos)) 
def draw_selected_tile(screen, selected_tile):
    if selected_tile != None:
        x, y = selected_tile
        x_pos= x * TILE_SIZE + MARGINS 
        y_pos= y * TILE_SIZE + MARGINS 
        pygame.draw.rect(screen,(255,105,180),(x_pos,y_pos,TILE_SIZE,TILE_SIZE),4) 

def get_clicked_tile(x, y):
    #retourne none si la position du clique ne correspond pas a une case a linterieur du Sudoku
    #On ajoute cette fonction pour lutiliser dans le main 
    sudoku_start = MARGINS
    sudoku_end = MARGINS + 9 * TILE_SIZE
    if sudoku_start <= x <= sudoku_end and sudoku_start <= y <= sudoku_end: #Permet de sassurer quon est dans la postion de la grille par rapport aux marges
        row = (x - MARGINS)// TILE_SIZE
        col = (y - MARGINS) // TILE_SIZE
        return (row,col)
    else:
        return None
  
def afficher_message_fin(screen, message):
    font = pygame.font.Font(None, 48)  
    text_surface = font.render(message, True, (255, 0, 0)) 
    text_rect = text_surface.get_rect(center=(Constants.SCREEN_WIDTH / 2, Constants.SCREEN_HEIGHT / 2))
    screen.blit(text_surface, text_rect)

def draw_chances(screen,chances):
    font=pygame.font.Font(None,27)
    text=font.render(f"Attention, il ne te reste que {chances} chance(s)",True,(2,8,0))
    screen.blit(text,(5,5))

def afficher_indices(screen, indices, row, col):
    font = pygame.font.SysFont('Arial', 28)
    couleur = (75, 0, 130)
    if indices:
        message = f"Indice : Le(s) chiffre(s) {', '.join(str(i) for i in indices)} peuvent être ajoutés dans cette case."
    else:
        message = "Aucun chiffre ne peut être ajouté dans cette case."
    text_surface = font.render(message, True, couleur)
    x_position = Constants.SCREEN_WIDTH - text_surface.get_width() - 40
    y_position = Constants.SCREEN_HEIGHT - text_surface.get_height() - 20
    screen.blit(text_surface, (x_position, y_position))
    pygame.display.flip()

def main():
    global sudoku, selected_tile,selected_difficulty
    try:
        splash_screen() #affiche la page initiale
    except Exception as e:
        logger.log(f"Erreur lors de l'affichage d'écran: {str(e)}","critical")
    logger.log("La partie est commencé.", "info")
    try:
        sudoku.generate_view_board(selected_difficulty) #Initialise le board selon le niveau de difficulte 
        logger.log("Grille générée","debug")
    except Exception as e:
        logger.log(f"Erreur lors de la generation de la grille: {str(e)}", "critical" )
    try:
        refresh_button_rect, hint_button_rect, difficulty_button_rects = draw_sudoku_screen() 
    except Exception as e:
        logger.log(f"Erreur lors du dessin de l'écran.: {str(e)}","critical")
    running = True
    chances = 3
    clicked_tile = None
    Joue = True
    try:
        draw_chances(screen,chances)
    except Exception as e:
        logger.log(f"Erreur lors de l'affichage de chances: {str(e)}","critical")
    logger.log(f"Lancement du jeu réussi","debug")
    selected_difficulty = Difficulty.EASY
    logger.log(f"La difficulté initiale a été initialisé à {selected_difficulty}","debug")
    while running:
        try:
            mouse_pos = pygame.mouse.get_pos()
        except Exception as e:
            logger.log(f"Erreur lors de la dectection de la position de la sourie","critical")

        over_any_button = any(rect.collidepoint(mouse_pos) for rect in difficulty_button_rects) or refresh_button_rect.collidepoint(
            mouse_pos) or hint_button_rect.collidepoint(mouse_pos)
        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_HAND if over_any_button else pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            elif event.type == MOUSEBUTTONDOWN:
                # TODO 4.3. Réinitialisation du jeu
                logger.log("Clic de la souris détecté","debug")
                x,y = event.pos
                clicked_outside = True 
                if refresh_button_rect.collidepoint(event.pos):
                    logger.log("L'utilisateur a démarré une nouvelle partie.","info")
                    logger.log("Clic du bouton refresh détecté","debug")
                    logger.log(f"La nouvelle difficulté est {selected_difficulty}","info")
                    sudoku.generate_view_board(selected_difficulty)
                    selected_tile = None
                    chances = 3
                    logger.log("Les chances ont été réinitialisées à 3","debug")
                    Joue = True
                    clicked_outside = False
                    draw_sudoku_screen()
                    draw_chances(screen,chances)
                # TODO 4.3. Indices
                elif hint_button_rect.collidepoint(event.pos) and Joue:
                    try:
                        if clicked_tile is not None:
                            row, col = clicked_tile
                            indices = sudoku.Indice(row, col) 
                            logger.log("Clic du bouton d'indice détecté","debug")
                            logger.log(f"L'utilisateur a demandé un indice.", "info")
                            if indices:
                                afficher_indices(screen, indices, row, col)
                                logger.log(f"Indice : Le(s) chiffre(s) {', '.join(str(i) for i in indices)} peuvent être ajoutés à la ligne {row+1}, colonne {col + 1}.", "info")   
                                logger.log("Un indice a été généré avec succès","debug")
                            else: 
                                logger.log("Aucun indice disponible: {str(e)}.", "critical") 
                                afficher_indices(screen, indices, row, col)   
                        clicked_outside = False
                    except Exception as e: 
                        logger.log(f"Erreur dans la demande d'indice: {str(e)}.","critical")         
                
                    logger.log(f"Nouvelle difficulté sélectionnée: {selected_difficulty}.", "info")
                    clicked_outside = False
                # Difficulty buttons
                else:
                    x,y = event.pos
                    clicked_tile= get_clicked_tile(x, y)
                    if clicked_tile != None and Joue:
                        row, col = clicked_tile
                        clicked_tile= get_clicked_tile(x, y)
                        logger.log(f"L'utilisateur a selectionne {(col+1,row+1)}","info")
                        selected_tile = clicked_tile
                        row,col = clicked_tile
                        if sudoku._board[row][col] == 0: #permet de cliquer seulement si la case est vide 
                            selected_tile = clicked_tile
                            draw_sudoku_screen()
                            draw_selected_tile(screen,selected_tile)
                        else:
                            selected_tile = None
                        clicked_outside = False 
                if clicked_outside:
                    try:
                        logger.log(" Clic en dehors des zones interactives.", "debug")
                        for i, rect in enumerate(difficulty_button_rects):
                            if rect.collidepoint(event.pos):
                                logger.log(f" Le niveau de difficulté est: {selected_difficulty}.", "info")
                                # TODO 4.3. Difficultés
                                if i == 0:
                                    selected_difficulty = Difficulty.EASY

                                elif i == 1:
                                    selected_difficulty = Difficulty.INTERMEDIATE

                                elif i == 2: 
                                    selected_difficulty = Difficulty.ADVANCED
                                logger.log("Changement de difficulté effectué avec succès.", "debug")
                                break
                    except Exception as e:
                        logger.log(f"Erreur lors du changement de difficulté: {str(e)}. ","critical")
            elif event.type == KEYDOWN:
                # TODO 4.3. Insertion d'une case à la suite de l'appui du clavier (0-9)
                if event.unicode in '0123456789' and Joue:
                    logger.log(f"L'utilisateur a cliqué sur {event.unicode}", "info")
                    if selected_tile:  
                        row, col = selected_tile
                        num = int(event.unicode)
                        if num == 0:
                            sudoku._board[row][col] = 0
                        elif sudoku.is_valid(row, col, num):  
                            sudoku._board[row][col] = num
                            logger.log(f"Placement du chiffre {num} réussi.", "info")
                            if sudoku.Board_Complete():
                                logger.log(f"La grille a été completé", "info")
                                afficher_message_fin(screen, "Vous avez gagné !")
                                logger.log("Le message de victoire a été généré avec succès.","debug")
                                logger.log(f"L'utilisateur a gagné !","info")
                                pygame.display.flip()
                                pygame.time.delay(4000)
                                Joue = False
            
                        else:
                            chances -= 1
                            logger.log(f"Mauvaise entrée. Chances restantes: {chances}", "critical")
                            if chances <= 0:
                                afficher_message_fin(screen, "Vous avez perdu. Plus de chances.")
                                logger.log("Le message de défaite a été généré avec succès.","debug")
                                logger.log(f"Les chances sont épuisées: {str(e)}.", "critical")
                                pygame.display.flip()
                                Joue= False
                                break

                        draw_sudoku_screen()
        
            if not clicked_tile:
                draw_sudoku_screen()
                draw_numbers(screen) 

            if clicked_tile is not None:
                draw_selected_tile(screen, selected_tile)
                pygame.display.flip()
                pygame.display.update()

            if not running:
                break
            draw_chances(screen,chances)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()


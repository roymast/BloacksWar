# This file is for displaying the first page
# The page contains background image and button to continue

from pages.Page import *


class FirstPage(Page):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.start = False
        self.first_page_background = pygame.image.load("pics/first page.png")
        self.rect = self.first_page_background.get_rect(topleft=(WINDOW_WIDTH/3+50, 300))

    def goToPage(self):
        while not self.start:
            self.handleUserInputs()
            self.displayPage()

    def displayPage(self):
        """
        func to display the page
        :return: None
        """
        self.screen.blit(self.first_page_background, (0, 0))
        self.screen.blit(PygameConstans.START_GAME_IMG.value[IMG_INDEX], self.rect)
        pygame.display.update()

    def handleUserInputs(self):
        """
        func to handle inputs of the user
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame(self.screen, None)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.start = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start = True

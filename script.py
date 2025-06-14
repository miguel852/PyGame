import pygame
import random
import sys
import time

pygame.init()

# Configurações iniciais
info = pygame.display.Info()
largura, altura = info.current_w, info.current_h
tela = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)
pygame.display.set_caption("Cogulandia Matuê")
relogio = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (34, 177, 76)
VERMELHO = (255, 0, 0)
AZUL = (0, 162, 232)
ROXO = (128, 0, 128)
CINZA = (100, 100, 100)

# Sons (substitua pelos seus caminhos corretos)
pygame.mixer.music.load(r"C:\Users\aluno\PyCharmMiscProject\.venv\audios\som_gorila.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

som_beck = pygame.mixer.Sound(r"C:\Users\aluno\PyCharmMiscProject\.venv\audios\som_gorila.mp3")
som_gorila = pygame.mixer.Sound(r"C:\Users\aluno\PyCharmMiscProject\.venv\audios\som_gorila.mp3")
som_dano = pygame.mixer.Sound(r"C:\Users\aluno\PyCharmMiscProject\.venv\audios\som_gorila.mp3")

# Sprites
fundo = pygame.image.load(r"C:\Users\aluno\PyCharmMiscProject\imagens\fundo.jpg")
fundo = pygame.transform.scale(fundo, (largura, altura))

sprite_barco = pygame.image.load(r"C:\Users\aluno\PyCharmMiscProject\imagens\barco.png")
sprite_barco = pygame.transform.scale(sprite_barco, (80, 80))

sprite_tesouro = pygame.image.load(r"C:\Users\aluno\PyCharmMiscProject\imagens\tesouro.png")
sprite_tesouro = pygame.transform.scale(sprite_tesouro, (50, 50))

sprite_bomba = pygame.image.load(r"C:\Users\aluno\PyCharmMiscProject\imagens\bomba.png")
sprite_bomba = pygame.transform.scale(sprite_bomba, (50, 50))

sprite_gorila = pygame.image.load(r"C:\Users\aluno\PyCharmMiscProject\imagens\gorila_roxo.png")
sprite_gorila = pygame.transform.scale(sprite_gorila, (60, 60))

# Botões
botao_largura = 120
botao_altura = 40

botao_sair = pygame.Rect(largura - botao_largura - 10, 10, botao_largura, botao_altura)
botao_reiniciar = pygame.Rect(largura - botao_largura - 10, 60, botao_largura, botao_altura)

def desenhar_botoes():
    fonte = pygame.font.SysFont(None, 30)

    pygame.draw.rect(tela, VERDE, botao_reiniciar)
    texto_reiniciar = fonte.render("Reiniciar", True, BRANCO)
    texto_rect = texto_reiniciar.get_rect(center=botao_reiniciar.center)
    tela.blit(texto_reiniciar, texto_rect)

    pygame.draw.rect(tela, VERMELHO, botao_sair)
    texto_sair = fonte.render("Sair", True, BRANCO)
    texto_rect2 = texto_sair.get_rect(center=botao_sair.center)
    tela.blit(texto_sair, texto_rect2)

# Classe do barco
class Barco:
    def __init__(self):
        self.x = largura // 2
        self.y = altura - 150
        self.velocidade_base = 8
        self.velocidade = self.velocidade_base
        self.piscando = False
        self.tempo_piscando = 0
        self.aura_roxa = False

    def mover(self, tecla):
        if tecla[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidade
        if tecla[pygame.K_RIGHT] and self.x < largura - 80:
            self.x += self.velocidade

    def desenhar(self):
        if self.aura_roxa and (time.time() % 0.4 > 0.2):
            pygame.draw.ellipse(tela, ROXO, (self.x - 5, self.y - 5, 90, 90), 4)
        elif self.piscando and (time.time() % 0.3 > 0.15):
            pygame.draw.ellipse(tela, VERMELHO, (self.x - 5, self.y - 5, 90, 90), 4)
        else:
            pygame.draw.ellipse(tela, AZUL, (self.x - 5, self.y - 5, 90, 90), 4)
        tela.blit(sprite_barco, (self.x, self.y))

    def tomar_dano(self):
        self.piscando = True
        self.tempo_piscando = time.time()

    def atualizar(self):
        if self.piscando and time.time() - self.tempo_piscando > 1.5:
            self.piscando = False

# Classe dos itens
class Item:
    def __init__(self, tipo=None):
        self.tipo = tipo if tipo else random.choice(["tesouro", "bomba"])
        self.x = random.randint(0, largura - 50)
        self.y = -50
        self.velocidade = random.randint(5, 9)

    def mover(self, nivel, dificuldade):
        self.y += self.velocidade + (nivel - 1) * 2 + dificuldade

    def desenhar(self):
        if self.tipo == "tesouro":
            tela.blit(sprite_tesouro, (self.x, self.y))
        elif self.tipo == "bomba":
            tela.blit(sprite_bomba, (self.x, self.y))
        elif self.tipo == "gorila":
            tela.blit(sprite_gorila, (self.x, self.y))

# Colisão
def colidiu(item, barco):
    barco_rect = pygame.Rect(barco.x, barco.y, 80, 80)
    item_rect = pygame.Rect(item.x, item.y, 50, 50)
    return barco_rect.colliderect(item_rect)

# Porto e Barras
def desenhar_porto(pontos, energia):
    pygame.draw.rect(tela, ROXO, (0, altura - 70, largura, 70))
    fonte = pygame.font.SysFont(None, 30)
    texto = fonte.render("Farmácia da Fumaça 🌿💊", True, BRANCO)
    tela.blit(texto, (10, altura - 50))

    progresso = pontos % 50
    pygame.draw.rect(tela, CINZA, (10, altura - 30, largura - 20, 20))
    pygame.draw.rect(tela, VERDE, (10, altura - 30, (largura - 20) * (progresso / 50), 20))

    pygame.draw.rect(tela, CINZA, (10, 10, 300, 15))
    pygame.draw.rect(tela, AZUL, (10, 10, 300 * (energia / 100), 15))
    texto_ice = fonte.render("Barra de ICE 🧊", True, AZUL)
    tela.blit(texto_ice, (320, 8))

# Game Over
def game_over(pontuacao, tempo, nivel):
    fonte = pygame.font.SysFont(None, 80)
    texto = fonte.render("GAME OVER", True, VERMELHO)
    tela.blit(texto, (largura // 2 - 200, altura // 2 - 150))

    fonte2 = pygame.font.SysFont(None, 50)
    texto_pontos = fonte2.render(f"Pontos: {pontuacao}", True, VERMELHO)
    texto_tempo = fonte2.render(f"Tempo: {int(tempo)}s", True, VERMELHO)
    texto_nivel = fonte2.render(f"Nível: {nivel}", True, VERMELHO)

    tela.blit(texto_pontos, (largura // 2 - 100, altura // 2 - 50))
    tela.blit(texto_tempo, (largura // 2 - 100, altura // 2))
    tela.blit(texto_nivel, (largura // 2 - 100, altura // 2 + 50))

    desenhar_botoes()
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    esperando = False
                    main()
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_sair.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()
                if botao_reiniciar.collidepoint(evento.pos):
                    esperando = False
                    main()

# Loop Principal
def main():
    barco = Barco()
    itens = []
    pontuacao = 0
    nivel = 1
    dificuldade = 0
    erros = 0
    energia = 100
    ice_infinito = False
    invencivel = False
    tempo_bonus = 0
    fonte = pygame.font.SysFont(None, 40)
    inicio_tempo = time.time()

    rodando = True
    while rodando:
        relogio.tick(60)
        tela.blit(fundo, (0, 0))

        tempo_atual = time.time()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_sair.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()
                if botao_reiniciar.collidepoint(evento.pos):
                    main()
                    return

        teclas = pygame.key.get_pressed()

        if (teclas[pygame.K_SPACE] and energia > 0) or ice_infinito:
            barco.velocidade = barco.velocidade_base * 2
            if not ice_infinito:
                energia -= 0.8
                if energia < 0:
                    energia = 0
        elif energia <= 0:
            barco.velocidade = barco.velocidade_base * 0.5
        else:
            barco.velocidade = barco.velocidade_base

        barco.mover(teclas)
        barco.atualizar()
        barco.desenhar()

        desenhar_porto(pontuacao, energia)

        nivel = pontuacao // 50 + 1
        dificuldade = (pontuacao // 20) * 1.5

        if random.randint(1, max(5, 30 - int(dificuldade * 2))) == 1:
            itens.append(Item())

        if random.randint(1, 500) == 1:
            itens.append(Item("gorila"))

        for item in itens[:]:
            item.mover(nivel, dificuldade)
            item.desenhar()

            if colidiu(item, barco):
                if item.tipo == "bomba":
                    if not invencivel:
                        erros += 1
                        barco.tomar_dano()
                        som_dano.play()
                        if erros >= 3:
                            game_over(pontuacao, time.time() - inicio_tempo, nivel)
                            rodando = False
                    itens.remove(item)

                elif item.tipo == "tesouro":
                    if invencivel:
                        pontuacao += 1
                    else:
                        pontuacao += 5
                    itens.remove(item)
                    energia += 10
                    som_beck.play()
                    if energia > 100:
                        energia = 100

                elif item.tipo == "gorila":
                    ice_infinito = True
                    invencivel = True
                    barco.aura_roxa = True
                    tempo_bonus = tempo_atual + 6
                    som_gorila.play()
                    itens.remove(item)
                    if erros > 0:
                        erros -= 1  # Ganha uma vida

            elif item.y > altura:
                itens.remove(item)

        if tempo_atual > tempo_bonus and tempo_bonus != 0:
            ice_infinito = False
            invencivel = False
            barco.aura_roxa = False
            tempo_bonus = 0

        tempo_jogo = time.time() - inicio_tempo
        texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, VERMELHO)
        texto_tempo = fonte.render(f"Tempo: {int(tempo_jogo)}s", True, VERMELHO)
        texto_nivel = fonte.render(f"Nível: {nivel}", True, VERMELHO)
        texto_erros = fonte.render(f"Cogumelos: {erros}/3", True, VERMELHO)

        tela.blit(texto_pontos, (10, 35))
        tela.blit(texto_tempo, (10, 70))
        tela.blit(texto_nivel, (10, 105))
        tela.blit(texto_erros, (10, 140))

        desenhar_botoes()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

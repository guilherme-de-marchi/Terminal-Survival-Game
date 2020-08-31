# Created by: Guilherme-de-Marchi
# Current version: Alpha 1.0.1
# License: MIT License
# GitHub: https://github.com/Guilherme-De-Marchi/Terminal-Survival-Game
# '''if you make any improvement scans of the code and 
# want to contribute to the game, send on my github'''

from msvcrt import kbhit, getwch
from curses import *
from random import randint

class Jogador():
    def __init__(self, mundo, vida: int, fome: int):
        self.TAMANHO_INVENTARIO = 5
        self.LIMITE_BLOCOS_ESPACO_INVENTARIO = 99
        self.mundo = mundo
        self.vida = vida
        self.fome = fome
        self.esta_se_movendo = 0
        self.caindo = 0
        self.inventario = {espaco: {0: 0} for espaco in range(self.TAMANHO_INVENTARIO)}
        self.espaco_inventario = 0
        self.ponteiro = (0, 1)
        self.direcoes = {
            'a': -1,
            'd': 1,
        }
        self.direcoes_ponteiro = {
            1: (1, -1),
            2: (1, 0),
            3: (1, 1),
            4: (0, -1),
            6: (0, 1),
            7: (-1, -1),
            8: (-1, 0),
            9: (-1, 1)
        }

    def posicao(self) -> tuple:
        for y in range(len(self.mundo.mundo)):
            for x in range(len(self.mundo.mundo[y])):
                if self.mundo.mundo[y][x] == 1: return (y, x)

    def mover_ponteiro(self, entrada: int):
        self.ponteiro = self.direcoes_ponteiro.get(entrada) or self.ponteiro

    def mover(self, direcao: int):
        pos = self.posicao()

        if self.mundo.mundo[pos[0]][pos[1]+direcao] != 0:
            if self.mundo.mundo[pos[0]-1][pos[1]+direcao] == 0:
                if self.mundo.mundo[pos[0]-1][pos[1]] == 0:
                    self.mundo.mundo[pos[0]][pos[1]] = 0
                    self.mundo.mundo[pos[0]-1][pos[1]+direcao] = 1
                    self.esta_se_movendo += 1

        elif self.mundo.mundo[pos[0]][pos[1]+direcao] == 0:
            self.mundo.mundo[pos[0]][pos[1]] = 0
            self.mundo.mundo[pos[0]][pos[1]+direcao] = 1
            self.esta_se_movendo += 1

        if self.posicao()[1] in [8, len(self.mundo.mundo[0]) - 9]:
            self.mundo.gerar_area(direcao)

    def ficar_com_fome(self):
        if self.esta_se_movendo >= 10:
            self.fome -= 1
            self.esta_se_movendo = 0
            return 1
        return 0

    def cair(self) -> bool:
        pos = self.posicao()
        if self.mundo.mundo[pos[0]+1][pos[1]] == 0:
            self.mundo.mundo[pos[0]][pos[1]] = 0
            self.mundo.mundo[pos[0]+1][pos[1]] = 1
            self.caindo += 1
            self.esta_se_movendo += 1
            return True

        if self.caindo > 2:
            self.vida -= self.caindo - 2
            self.caindo = 0
            return True

        self.caindo = 0
        return False

    def mudar_espaco_inventario(self, entrada: str):
        if entrada == '+': 
            if self.espaco_inventario < self.TAMANHO_INVENTARIO - 1:
                self.espaco_inventario += 1
            else:
                self.espaco_inventario = 0
        elif entrada == '-':
            if self.espaco_inventario > 0:
                self.espaco_inventario -= 1
            else:
                self.espaco_inventario = self.TAMANHO_INVENTARIO - 1

    def quebrar_bloco(self):

        bloco = self.mundo.mundo[self.posicao()[0] + self.ponteiro[0]][self.posicao()[1] + self.ponteiro[1]]
        for espaco in self.inventario:
            if list(self.inventario[espaco].keys())[0] == bloco and self.inventario[espaco][bloco] < self.LIMITE_BLOCOS_ESPACO_INVENTARIO:
                self.inventario[espaco][bloco] += 1
                break
            elif list(self.inventario[espaco].keys())[0] == 0:
                self.inventario[espaco] = {bloco: 1}
                break

        self.esta_se_movendo += 1

        self.mundo.mundo[self.posicao()[0] + self.ponteiro[0]][self.posicao()[1] + self.ponteiro[1]] = 0

    def colocar_bloco(self):
        bloco = list(self.inventario[self.espaco_inventario].keys())[0]
        if self.inventario[self.espaco_inventario][bloco] > 0:
            
            if self.mundo.mundo[self.posicao()[0] + self.ponteiro[0]][self.posicao()[1] + self.ponteiro[1]] == 0:
                self.mundo.mundo[self.posicao()[0] + self.ponteiro[0]][self.posicao()[1] + self.ponteiro[1]] = bloco
            
            elif self.ponteiro == (1, 0):
                self.mundo.mundo[self.posicao()[0] - self.ponteiro[0]][self.posicao()[1] + self.ponteiro[1]] = 1
                self.mundo.mundo[self.posicao()[0] + self.ponteiro[0]][self.posicao()[1] + self.ponteiro[1]] = bloco

            self.inventario[self.espaco_inventario][bloco] -= 1
            if self.inventario[self.espaco_inventario][bloco] == 0: self.inventario[self.espaco_inventario] = {0: 0}

        self.esta_se_movendo += 1

class Mundo():
    def __init__(self):
        self.CAMADA_MAX = 30
        self.CAMADA_CARVAO = self.CAMADA_MAX/2
        self.altura_arvore = 4
        self.configs = {
            'camada_chao_max': 10,
            'camada_chao_min': self.CAMADA_MAX - 3,
        }

        self.mundo = [[0 for x in range(15)] for y in range(self.CAMADA_MAX)]
        self.alt = randint(self.configs['camada_chao_max'], self.configs['camada_chao_min'])

        for x in range(15):
            for y in range(self.CAMADA_MAX):
                if y == self.alt: self.mundo[y][x] = 3
                elif y > self.alt: self.mundo[y][x] = 6 if randint(1, 20) == 1 and y >= self.CAMADA_CARVAO else 2
            self.alt += randint(-1, 1)

        for y in range(len(self.mundo)):
            for x in range(len(self.mundo[y])):
                if self.mundo[y][x] == 3 and x == 7: 
                    self.mundo[y-1][x] = 1
                    break

    def gerar_area(self, direcao: int):
        if direcao == 1:
            for i in range(15):
                self.alt += randint(-1, 1)
                for y in range(len(self.mundo)):
                    if y == self.alt: 
                        self.mundo[y].append(3)
                    elif y > self.alt: 
                        if randint(1, 20) == 1 and y >= self.CAMADA_CARVAO:
                            self.mundo[y].append(6)
                        else:
                            self.mundo[y].append(2)
                    else:
                        self.mundo[y].append(0)

            for x in range(len(self.mundo[0]) - 16, len(self.mundo[0])):
                if randint(0, 15) == 1:
                    for y in range(len(self.mundo)):
                        if self.mundo[y][x] == 3:
                            alt = y - 1
                            break
                    for i in range(self.altura_arvore):
                        self.mundo[alt - i][x] = 4
                    self.mundo[alt - self.altura_arvore][x] = 5
                    break

        elif direcao == -1:
            for i in range(15):
                for y in range(len(self.mundo)):
                    if self.mundo[y][0] == 3: 
                        self.alt2 = y + randint(-1, 1)

                for y in range(len(self.mundo)):
                    if y == self.alt2: 
                        self.mundo[y].insert(0, 3)
                    elif y > self.alt2: 
                        if randint(1, 20) == 1 and y >= self.CAMADA_CARVAO:
                            self.mundo[y].insert(0, 6)
                        else:
                            self.mundo[y].insert(0, 2)
                    else:
                        self.mundo[y].insert(0, 0)

            for x in range(0, 15):
                if randint(0, 15) == 1:
                    for y in range(len(self.mundo)):
                        if self.mundo[y][x] == 3:
                            alt = y - 1
                            break
                    for i in range(self.altura_arvore):
                        self.mundo[alt - i][x] = 4
                    self.mundo[alt - 4][x] = 5
                    break
                    

def mostrar_tela(janela, objetos: dict, mundo, jogador, tela: str):
    janela.clear()
    janela.move(0, 0)

    if tela == 'jogo':

        janela.addstr('\n')
        janela.addstr('█'*jogador.vida, color_pair(7))
        janela.addstr('\n')
        janela.addstr('█'*jogador.fome, color_pair(9))

        for y in range(len(mundo.mundo)):
            janela.addstr('\n')

            for x in range(jogador.posicao()[1] - 7, jogador.posicao()[1] + 8):
                janela.addstr('██', color_pair(objetos[mundo.mundo[y][x]]))

        janela.addstr('\n\nInventário:\n')
        janela.addstr('    ' * jogador.espaco_inventario + ' V')
        janela.addstr('\n')

        for i in range(jogador.TAMANHO_INVENTARIO):

            janela.addstr(' ██ ', color_pair(objetos[list(jogador.inventario[i].keys())[0]]))

        janela.addstr('\n')
        for i in range(jogador.TAMANHO_INVENTARIO):

            janela.addstr('{: ^4}'.format(jogador.inventario[i][list(jogador.inventario[i].keys())[0]]))
        
        janela.addstr(f'\nTamanho do mundo: {len(mundo.mundo[0])}')
    
    elif tela == 'morte':

        janela.addstr('\n')
        janela.addstr('Você morreu!', color_pair(7))

    janela.refresh()

janela = initscr()
echo(False)
curs_set(0)

start_color()
init_pair(1, 112, 0)  # VERDE 1
init_pair(2, 117, 0)  # AZUL
init_pair(3, 224, 0)  # COR-DE-PELE
init_pair(4, 246, 0)  # CINZA
init_pair(5, 94, 0)   # MARROM
init_pair(6, 34, 0)   # VERDE 2
init_pair(7, 196, 0)  # VERMELHO
init_pair(8, 238, 0)  # CINZA ESCURO
init_pair(9, 14, 0)   # AMARELO

objetos = {
    0: 2, # AR
    1: 3, # JOGADOR
    2: 4, # PEDRA
    3: 1, # GRAMA
    4: 5, # MADEIRA
    5: 6, # FOLHA
    6: 8, # CARVÃO
}

mundo = Mundo()

jogador = Jogador(mundo, 10, 20)

mostrar_tela(janela, objetos, mundo, jogador, 'jogo')

while True:
    
    if jogador.vida <= 0:
        mostrar_tela(janela, objetos, mundo, jogador, 'morte')
        napms(5000)
        exit()

    if jogador.fome <= 0:
        jogador.vida -= 1
        mostrar_tela(janela, objetos, mundo, jogador, 'jogo')

    if jogador.cair():
        mostrar_tela(janela, objetos, mundo, jogador, 'jogo')

    if jogador.ficar_com_fome():
        mostrar_tela(janela, objetos, mundo, jogador, 'jogo')

    if kbhit():

        entrada = getwch()

        if entrada.isnumeric():
            jogador.mover_ponteiro(int(entrada))
            continue

        if entrada.lower() == 'q':
            jogador.quebrar_bloco()
            mostrar_tela(janela, objetos, mundo, jogador, 'jogo')
            continue

        if entrada.lower() == 'e':
            jogador.colocar_bloco()
            mostrar_tela(janela, objetos, mundo, jogador, 'jogo')
            continue

        if entrada in ['+', '-']:
            jogador.mudar_espaco_inventario(entrada)
            mostrar_tela(janela, objetos, mundo, jogador, 'jogo')
            continue

        jogador.mover(jogador.direcoes.get(entrada.lower()))
        mostrar_tela(janela, objetos, mundo, jogador, 'jogo')

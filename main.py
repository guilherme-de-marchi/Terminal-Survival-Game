# Created by: Guilherme-de-Marchi
# Encoding: UTF8
# Current version: Alpha 1.0.3
# License: MIT License
# GitHub: https://github.com/Guilherme-De-Marchi/Terminal-Survival-Game
# '''if you make any improvement scans of the code and 
# want to contribute to the game, send on my github'''

from msvcrt import kbhit, getwch
from curses import *
from random import random, randint, seed

class Jogador():

    def __init__( self, mundo, vida: int, fome: int, tamanho_inventario: int, limite_blocos_inventario_selecionado: int ):

        self.TAMANHO_INVENTARIO = tamanho_inventario
        self.LIMITE_BLOCOS_inventario_selecionado = limite_blocos_inventario_selecionado

        self.mundo = mundo

        self.vida = vida
        self.fome = fome
        
        self.inventario = {espaco: {0: 0} for espaco in range( self.TAMANHO_INVENTARIO )}

        self.inventario_selecionado = 0
        self.acumulo_movimento = 0
        self.acumulo_queda = 0
        self.ponteiro = (0, 1)
        
        self.direcoes_ponteiro = {
            #   y   x
            1: (1, -1),
            2: (1, 0),
            3: (1, 1),
            4: (0, -1),
            6: (0, 1),
            7: (-1, -1),
            8: (-1, 0),
            9: (-1, 1)
        }

        self.colocar_jogador_no_mundo()

    def posicao( self ) -> tuple:

        for y in range( len( self.mundo.mundo ) ):

            for x in range( len( self.mundo.mundo[y] ) ):

                if self.mundo.mundo[ y ][ x ] == 1:
        
                    return ( y, x )

    def mover_ponteiro( self, entrada: int ):

        self.ponteiro = self.direcoes_ponteiro.get( entrada ) or self.ponteiro

    def mover_jogador( self, direcao: int ):

        posicao = self.posicao()

        if direcao == 0: return

        if self.mundo.mundo[ posicao[ 0 ] ][ posicao[ 1 ] + direcao ] == 0:

            self.mundo.mundo[ posicao[ 0 ] ][ posicao[ 1 ]] = 0
            self.mundo.mundo[ posicao[ 0 ] ][ posicao[ 1 ] + direcao ] = 1
            self.acumulo_movimento += 1

        elif self.mundo.mundo[ posicao[ 0 ] - 1 ][ posicao[ 1 ] + direcao ] == 0 and self.mundo.mundo[ posicao[ 0 ] - 1 ][ posicao[ 1 ] ] == 0:

            self.mundo.mundo[ posicao[ 0 ] ][ posicao[ 1 ] ] = 0
            self.mundo.mundo[ posicao[ 0 ] - 1 ][ posicao[ 1 ] + direcao ] = 1
            self.acumulo_movimento += 1

        elif self.mundo.mundo[ posicao[ 0 ] + 1 ][ posicao[ 1 ] + direcao ] == 0 and self.mundo.mundo[ posicao[ 0 ] ][ posicao[ 1 ] + direcao ] == 0:

            self.mundo.mundo[ posicao[ 0 ] ][ posicao[ 1 ] ] = 0
            self.mundo.mundo[ posicao[ 0 ] + 1 ][ posicao[ 1 ] + direcao ] = 1
            self.acumulo_movimento += 1

        else: return

        if self.posicao()[ 1 ] in [ 6, len( self.mundo.mundo[ 0 ] ) - 7 ]:

            self.mundo.gerar_conjunto( direcao )

    def diminuindo_fome( self ) -> bool:

        if self.acumulo_movimento == 10:

            return True

        return False

    def caindo( self ) -> bool:

        posicao = self.posicao()

        if self.mundo.mundo[ posicao[ 0 ] + 1 ][ posicao[ 1 ] ] == 0:

            self.mundo.mundo[ posicao[ 0 ] ][ posicao[ 1 ] ] = 0
            self.mundo.mundo[ posicao[ 0 ] + 1 ][ posicao[ 1 ] ] = 1
            self.acumulo_queda += 1

            return True

        self.acumulo_queda = 0

        return False

    def diminuir_fome( self ):

        self.fome -= 1
        self.acumulo_movimento = 0

    def levar_dano_queda( self ):

        if self.acumulo_queda >= 3:

            self.vida -= self.acumulo_queda - self.acumulo_queda

    def mudar_inventario_selecionado( self, entrada: str ):

        if entrada == '+':

            self.inventario_selecionado = self.inventario_selecionado + 1 if self.inventario_selecionado < self.TAMANHO_INVENTARIO - 1 else 0

        elif entrada == '-':

            self.inventario_selecionado = self.inventario_selecionado - 1 if self.inventario_selecionado > 0 else self.TAMANHO_INVENTARIO - 1

    def quebrar_bloco( self ):

        posicao = self.posicao()

        bloco = self.mundo.mundo[ posicao[ 0 ] + self.ponteiro[ 0 ] ][ posicao[ 1 ] + self.ponteiro[ 1 ] ]

        if bloco == 0: return

        self.mundo.mundo[ posicao[ 0 ] + self.ponteiro[ 0 ] ][ posicao[ 1 ] + self.ponteiro[ 1 ] ] = 0

        for espaco in self.inventario:

            if list( self.inventario[ espaco ].keys() )[ 0 ] == bloco and self.inventario[ espaco ][ bloco ] < self.LIMITE_BLOCOS_inventario_selecionado:
                
                self.inventario[ espaco ][ bloco ] += 1
                break

            elif list( self.inventario[ espaco ].keys() )[ 0 ] == 0:

                self.inventario[ espaco ] = { bloco: 1 }
                break

        self.acumulo_movimento += 1

    def colocar_bloco( self ):

        posicao = self.posicao()

        bloco = list( self.inventario[ self.inventario_selecionado ].keys() )[ 0 ]

        if self.inventario[ self.inventario_selecionado ][ bloco ] != 0:
            
            if self.mundo.mundo[ posicao[ 0 ] + self.ponteiro[ 0 ] ][ posicao[ 1 ] + self.ponteiro[ 1 ] ] == 0:

                self.mundo.mundo[ posicao[ 0 ] + self.ponteiro[ 0 ] ][ posicao[ 1 ] + self.ponteiro[ 1 ] ] = bloco
            
            elif self.ponteiro == (1, 0):

                self.mundo.mundo[ posicao[ 0 ] ][ posicao[ 1 ] ] = bloco
                self.mundo.mundo[ posicao[ 0 ] - 1 ][ posicao[ 1 ] ] = 1

            self.inventario[ self.inventario_selecionado ][ bloco ] -= 1

            if self.inventario[ self.inventario_selecionado ][ bloco ] == 0: 
                
                self.inventario[ self.inventario_selecionado ] = { 0: 0 }

            self.acumulo_movimento += 1

    def colocar_jogador_no_mundo( self ):

        for y in range( len( self.mundo.mundo ) ):

            if self.mundo.mundo[ y ][ int( len( self.mundo.mundo[ 0 ] ) / 2 ) ] == 3: 
                
                self.mundo.mundo[ y - 1 ][ int( len( self.mundo.mundo[ 0 ] ) / 2 ) ] = 1

class Mundo():

    def __init__( self ):

        self.PROFUNDIDADE_MUNDO = 20
        self.LARGURA_CONJUNTO_MUNDO = 15

        self.PEDRA = { 'camada_minima': self.PROFUNDIDADE_MUNDO - 7, 'camada_maxima': self.PROFUNDIDADE_MUNDO - 2 }
        self.CARVAO = { 'camada_minima': self.PEDRA[ 'camada_minima' ], 'camada_maxima': self.PROFUNDIDADE_MUNDO - 2 }

        self.ARVORE = { 'altura_minima': 3, 'altura_maxima': 5 }

        self.mundo = [ [] for y in range( self.PROFUNDIDADE_MUNDO ) ]
        
        self.gerar_conjunto( 1 )
        self.gerar_conjunto( -1 )
        self.gerar_conjunto( 1 )

    def gerar_conjunto( self, direcao: int ):       

        altura_coluna, bloco = 0, 0

        for i in range( self.LARGURA_CONJUNTO_MUNDO ):

            for y in range( self.PROFUNDIDADE_MUNDO ):

                try:

                    if self.mundo[ y ][ len( self.mundo[ 0 ] ) - 1 if direcao == 1 else 0 ] == 2:

                        altura_coluna = y + randint( -1, 1 )

                        if altura_coluna < self.PEDRA[ 'camada_minima' ]: altura_coluna = self.PEDRA[ 'camada_minima' ]

                        elif altura_coluna > self.PEDRA[ 'camada_maxima' ]: altura_coluna = self.PEDRA[ 'camada_maxima' ]

                        break
                    
                except IndexError:

                    altura_coluna = randint( self.PEDRA[ 'camada_minima' ], self.PEDRA[ 'camada_maxima' ] )
                    break

            for y in range( self.PROFUNDIDADE_MUNDO ):

                if y < altura_coluna - 1: bloco = 0

                elif y == altura_coluna - 1: bloco = 3

                elif y > altura_coluna + 2 and randint( 1, 10 ) == 1 and y >= self.CARVAO[ 'camada_minima' ] and y <= self.CARVAO[ 'camada_maxima' ]: bloco = 6

                else: bloco = 2

                if direcao == 1: self.mundo[ y ].append( bloco )

                else: self.mundo[ y ].insert( 0, bloco )

            if altura_coluna - ( self.ARVORE[ 'altura_maxima' ] + 1 ) >= 0:

                if randint( 1, 20 ) == 1:

                    x = 0 if direcao == -1 else -1

                    altura_arvore = randint( self.ARVORE[ 'altura_minima' ], self.ARVORE[ 'altura_maxima' ] )

                    for y in range( self.PROFUNDIDADE_MUNDO ):

                        if y == altura_coluna - ( altura_arvore + 1 ): self.mundo[ y ][ x ] = 5

                        elif y > altura_coluna - ( altura_arvore + 1 ) and y < altura_coluna - 1: self.mundo[ y ][ x ] = 4

def mostrar_jogo( janela, mundo, jogador, objetos: dict ):

    janela.clear()

    janela.addstr( '\n' )

    janela.addstr( '█' * jogador.vida, color_pair( 7 ) )

    janela.addstr( '\n' )

    janela.addstr( '█' * jogador.fome, color_pair( 9 ) )

    for y in range( len( mundo.mundo ) ):

        janela.addstr( '\n' )

        for x in range( jogador.posicao()[ 1 ] - 6, jogador.posicao()[ 1 ] + 7 ):

            janela.addstr( '██' , color_pair( objetos[ mundo.mundo[ y ][ x ] ] ) )

    janela.addstr( '\n' )

    janela.addstr( '    ' * jogador.inventario_selecionado + ' --\n' )

    for i in range( jogador.TAMANHO_INVENTARIO ):

        janela.addstr( ' ██ ', color_pair( objetos[ list( jogador.inventario[ i ].keys() )[ 0 ] ] ) )

    janela.addstr( '\n' )

    for i in range( jogador.TAMANHO_INVENTARIO ):

        janela.addstr( '{: ^4}'.format( jogador.inventario[ i ][ list( jogador.inventario[ i ].keys() )[ 0 ] ] ) )
    
    janela.refresh()

def mostrar_aviso_morte( janela, aviso: str ):

    janela.clear()

    janela.addstr( f'\n{ aviso }', color_pair( 7 ) )

    janela.refresh()

janela = initscr()

echo( False )
curs_set( 0 )

start_color()

init_pair( 1, 112, 0 )  # VERDE 1
init_pair( 2, 117, 0 )  # AZUL
init_pair( 3, 224, 0 )  # COR-DE-PELE
init_pair( 4, 246, 0 )  # CINZA
init_pair( 5, 94, 0 )   # MARROM
init_pair( 6, 34, 0 )   # VERDE 2
init_pair( 7, 196, 0 )  # VERMELHO
init_pair( 8, 238, 0 )  # CINZA ESCURO
init_pair( 9, 14, 0 )   # AMARELO

objetos = {
    0: 2,    # AR
    1: 3,    # JOGADOR
    2: 4,    # PEDRA
    3: 1,    # GRAMA
    4: 5,    # MADEIRA
    5: 6,    # FOLHA
    6: 8,    # CARVÃO
}

mundo = Mundo()

jogador = Jogador( mundo, 10, 20, 6, 10 )

mostrar_jogo( janela, mundo, jogador, objetos )

while True:
    
    if jogador.vida <= 0:

        mostrar_aviso_morte( janela, 'Você morreu de fome!' if jogador.fome <= 0 else 'Você morreu!' )

        napms(5000)
        exit()

    if jogador.fome <= 0:

        jogador.vida -= 1

        mostrar_jogo( janela, mundo, jogador, objetos )

    if jogador.caindo():

        jogador.levar_dano_queda()

        mostrar_jogo( janela, mundo, jogador, objetos )

    if jogador.diminuindo_fome():

        jogador.diminuir_fome()

        mostrar_jogo( janela, mundo, jogador, objetos )

    if kbhit():

        entrada = getwch()

        if entrada.isnumeric():

            jogador.mover_ponteiro( int( entrada ) )

        elif entrada.lower() == 'q':

            jogador.quebrar_bloco()

        elif entrada.lower() == 'e':

            jogador.colocar_bloco()

        elif entrada in [ '+', '-' ]:

            jogador.mudar_inventario_selecionado( entrada )

        else: jogador.mover_jogador( -1 if entrada.lower() == 'a' else 1 if entrada.lower() == 'd' else 0 )
        
        mostrar_jogo( janela, mundo, jogador, objetos )

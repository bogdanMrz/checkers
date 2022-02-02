import time
import string
import random
import pygame, sys
import tkinter as tk
from tkinter import *



alfabet = string.ascii_lowercase
pygame.init()
pygame.mouse.set_cursor(*pygame.cursors.arrow)

w_gr = 80
h_gr = 80
class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 8
    NR_LINII = 8
    SIMBOLURI_JUC = ['n', 'a']  
    JMIN = None  # 'n'
    JMAX = None  # 'a'
    GOL = '#'
    W_GR = w_gr
    H_GR = h_gr
    ECRAN=pygame.display.set_mode(size=((NR_COLOANE+2)*W_GR,(NR_LINII+2)*H_GR))
    font = pygame.font.SysFont('Arial',W_GR)

    x = {juc:pygame.transform.scale(pygame.image.load(juc+'.png'), (h_gr,w_gr)) for juc in SIMBOLURI_JUC}
    y = {juc.upper():pygame.transform.scale(pygame.image.load(juc.upper()+'.png'), (h_gr,w_gr)) for juc in SIMBOLURI_JUC}

    IMG_JUC = {
        **x, **y
        }
    
    def __init__(self, tabla=None):
        
        if tabla != None:
            self.matr = tabla
            return

        self.matr = []
        
        impar = []
        par = []

        for i in range(self.NR_COLOANE):
            if i%2 == 0:
                par.append(self.GOL)
                impar.append(self.SIMBOLURI_JUC[1])
            else:
                par.append(self.SIMBOLURI_JUC[1])
                impar.append(self.GOL)

        for i in range((self.NR_LINII-2)//2):
            if i%2 == 0:
                self.matr.append(par)
            else:
                self.matr.append(impar)

        liber = []
        for i in range(self.NR_COLOANE):
            liber.append(self.GOL)
        self.matr.append(liber)
        self.matr.append(liber)

        impar = []
        par = []

        for i in range(self.NR_COLOANE):
            if i%2 == 0:
                impar.append(self.GOL)
                par.append(self.SIMBOLURI_JUC[0])
            else:
                impar.append(self.SIMBOLURI_JUC[0])
                par.append(self.GOL)

        for i in range((self.NR_LINII-2)//2):
            if i%2 == 0:
                self.matr.append(par)
            else:
                self.matr.append(impar)


    def poate_muta(self, semn, i, j):
        if self.matr[i][j].islower():
            if j + 1 < Joc.NR_COLOANE and self.matr[i+semn][j+1] == Joc.GOL:
                return True
            if 0 <= j - 1 and self.matr[i+semn][j-1] == Joc.GOL:
                return True
            if 0 <= i + 2 * semn < Joc.NR_LINII and j + 2 < Joc.NR_COLOANE and self.matr[i+2*semn][j+2] == Joc.GOL and self.matr[i+semn][j+1] not in [Joc.GOL, self.matr[i][j], self.matr[i][j].upper()]:
                return True
            if 0 <= i + 2 * semn < Joc.NR_LINII and  0 <= j - 2 and self.matr[i+2*semn][j-2] == Joc.GOL and self.matr[i+semn][j-1] not in [Joc.GOL, self.matr[i][j], self.matr[i][j].upper()]:
                return True
        if self.matr[i][j].isupper():
            for semn in [-1,1]:
                if 0 <= i + semn < Joc.NR_LINII and 0 <= j + semn < Joc.NR_COLOANE and self.matr[i+semn][j+semn] == Joc.GOL:
                    return True
                if 0 <= i + semn < Joc.NR_LINII and 0 <= j - semn < Joc.NR_COLOANE and self.matr[i+semn][j-semn] == Joc.GOL:
                    return True
                if 0 <= j + 2 * semn < Joc.NR_COLOANE and self.matr[i+2*semn][j+2*semn] == Joc.GOL and self.matr[i+semn][j+semn] not in [Joc.GOL, self.matr[i][j], self.matr[i][j].lower()]:
                    return True
                if 0 <= j - 2 * semn < Joc.NR_COLOANE and self.matr[i+2*semn][j-2*semn] == Joc.GOL and self.matr[i+semn][j-semn] not in [Joc.GOL, self.matr[i][j], self.matr[i][j].lower()]:
                    return True
        
        return False

    def final(self, jucator):
        # returnam simbolul jucatorului pierzator daca 
        # nu mai are piese/nu poate muta
        # ori 'False' daca nu s-a terminat jocul

        if jucator == Joc.SIMBOLURI_JUC[1]:
            semn = 1
        else:
            semn = -1
        
        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE):
                if self.matr[i][j].lower() == jucator and self.poate_muta(semn, i, j):
                    return False


        return jucator





    def copie_matr(self):
        matr = []
        for linie in self.matr:
            matr.append(linie.copy())
        
        return matr

    def mutare(self, jucator, i, j, l_mutari, prima_miscare=True):

        if jucator == Joc.SIMBOLURI_JUC[1]:
            semn = 1
            destinatie = Joc.NR_LINII - 1
        else:
            semn = -1
            destinatie = 0

        
        if prima_miscare and j + 1 < Joc.NR_COLOANE and self.matr[i+semn][j+1] == Joc.GOL:
            if i + semn == destinatie:
                matr = self.copie_matr()
                matr[i+semn][j+1] = jucator.upper()
                matr[i][j] = Joc.GOL

                l_mutari.append(Joc(matr))
            else:
                matr = self.copie_matr()
                matr[i+semn][j+1] = jucator
                matr[i][j] = Joc.GOL

                l_mutari.append(Joc(matr))

        if prima_miscare and 0 <= j - 1 and self.matr[i+semn][j-1] == Joc.GOL:
            if i + semn == destinatie:
                matr = self.copie_matr()
                matr[i+semn][j-1] = jucator.upper()
                matr[i][j] = Joc.GOL

                l_mutari.append(Joc(matr))
            else:
                matr = self.copie_matr()
                matr[i+semn][j-1] = jucator
                matr[i][j] = Joc.GOL

                l_mutari.append(Joc(matr))
        
        recursie = False

        if  j + 2 < Joc.NR_COLOANE  and 0 <= i + 2 * semn < Joc.NR_LINII and self.matr[i+semn][j+1] not in [Joc.GOL, jucator, jucator.upper()] and self.matr[i+2*semn][j+2] == Joc.GOL:
            recursie = True
            if (i + 2 * semn) == destinatie:

                matr = self.copie_matr()

                matr[i][j] = Joc.GOL
                matr[i+semn][j+1] = Joc.GOL
                matr[i+2*semn][j+2] = jucator.upper()

                aux = Joc(matr)
                aux.mutare_rege(jucator,i+2*semn,j+2,l_mutari,prima_miscare=False)

            else:
                matr = self.copie_matr()

                matr[i][j] = Joc.GOL
                matr[i+semn][j+1] = Joc.GOL
                matr[i+2*semn][j+2] = jucator
                

                aux = Joc(matr)
                aux.mutare(jucator,i+2*semn,j+2,l_mutari,prima_miscare=False)

        if 0 <= j - 2 and 0 <= i + 2 * semn < Joc.NR_LINII and self.matr[i+semn][j-1] not in [Joc.GOL, jucator, jucator.upper()] and self.matr[i+2*semn][j-2] == Joc.GOL:
            recursie = True
            if (i + 2 * semn) == destinatie:
                matr = self.copie_matr()

                matr[i][j] = Joc.GOL
                matr[i+semn][j-1] = Joc.GOL
                matr[i+2*semn][j-2] = jucator.upper()

                aux = Joc(matr)
                aux.mutare_rege(jucator,i+2*semn,j-2,l_mutari,prima_miscare=False)

            else:
                matr = self.copie_matr()

                matr[i][j] = Joc.GOL
                matr[i+semn][j-1] = Joc.GOL
                matr[i+2*semn][j-2] = jucator
                

                aux = Joc(matr)
                aux.mutare(jucator,i+2*semn,j-2,l_mutari,prima_miscare=False)

        if not prima_miscare and not recursie:
            l_mutari.append(self)



    def mutare_rege(self, jucator, i, j, l_mutari, prima_miscare=True):
        if prima_miscare:
            for semn in [-1,1]:
                if 0 <= i+semn < Joc.NR_LINII and 0 <= j+semn < Joc.NR_COLOANE and self.matr[i+semn][j+semn] == Joc.GOL:
                    matr = self.copie_matr()
                    matr[i][j] = Joc.GOL
                    matr[i+semn][j+semn] = jucator.upper()

                    l_mutari.append(Joc(matr))
                
                if 0 <= i+semn < Joc.NR_LINII and 0 <= j-semn < Joc.NR_COLOANE and self.matr[i+semn][j-semn] == Joc.GOL:
                    matr = self.copie_matr()
                    matr[i][j] = Joc.GOL
                    matr[i+semn][j-semn] = jucator.upper()
        
                    l_mutari.append(Joc(matr))
        
        recursie = False
        for semn in [-1, 1]:
            if 0 <= i+2*semn < Joc.NR_LINII and 0 <= j+2*semn < Joc.NR_COLOANE and self.matr[i+2*semn][j+2*semn] == Joc.GOL and self.matr[i+semn][j+semn] not in [Joc.GOL, jucator, jucator.upper()]:
                recursie = True
                
                matr = self.copie_matr()
                matr[i][j] = Joc.GOL
                matr[i+semn][j+semn] = Joc.GOL
                matr[i+2*semn][j+2*semn] = jucator.upper()

                aux = Joc(matr)
                aux.mutare_rege(jucator,i+2*semn,j+2*semn,l_mutari,False)


            if 0 <= i+2*semn < Joc.NR_LINII and 0 <= j-2*semn < Joc.NR_COLOANE and self.matr[i+2*semn][j-2*semn] == Joc.GOL and self.matr[i+semn][j-semn]not in [Joc.GOL, jucator, jucator.upper()]:
                recursie = True

                matr = self.copie_matr()
                matr[i][j] = Joc.GOL
                matr[i+semn][j-semn] = Joc.GOL
                matr[i+2*semn][j-2*semn] = jucator.upper()

                aux = Joc(matr)
                aux.mutare_rege(jucator,i+2*semn,j-2*semn,l_mutari,False)

        if not recursie and not prima_miscare:
            l_mutari.append(self)         


    def mutari(self, jucator):
        l_mutari=[]
        for i in range(Joc.NR_LINII):
            for j in range(Joc.NR_COLOANE):
                if self.matr[i][j] == jucator: 
                    self.mutare(jucator,i,j,l_mutari)
                elif self.matr[i][j] == jucator.upper():
                    self.mutare_rege(jucator,i,j,l_mutari)
                    
        return l_mutari




    def fct_euristica(self):
        '''
        Piesele normale valoareaza 3 puncte,
        pe cand "regii" valoreaza 5 puncte.
        Se face diferenta intre culori si 
        pr urma se adauga o valoare random pentru a
        departaja pozitiile egale si a face ca algoritmul 
        sa nu fie in totaliate deterministica, adica
        pe o pozitia poate juca mutari diferite pentru fiecare
        rulare, dar la fel de bune.
        '''

        scor = 0

        for linie in self.matr:
            for pozitie in linie:
                if pozitie == Joc.JMAX:
                    scor += 3
                elif pozitie == Joc.JMAX.upper():
                    scor += 5
                elif pozitie == Joc.JMIN:
                    scor -= 3
                elif pozitie == Joc.JMIN.upper():
                    scor -= 5
        

        scor *= 10
        scor += random.randint(0,9)

        return scor
       
    def fct_euristica1(self):
        '''
        Similar cu cealalta euristica numai ca apreciaza si
        cat de multe mutari mai poate face un jucator si
        cat de aproape sunt piesel sale de a devenii regi.
        '''
        scor = 0
        promovare = 0
        nr_miscari = 0        

        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE):
                if self.matr[i][j] == Joc.JMAX:
                    scor += 3
                    if self.poate_muta(1,i,j):
                        nr_miscari += 1
                    promovare += (self.NR_LINII - i)

                elif self.matr[i][j] == Joc.JMAX.upper():
                    scor += 5
                    if self.poate_muta(1,i,j):
                        nr_miscari += 1
                elif self.matr[i][j] == Joc.JMIN:
                    scor -= 3
                    if self.poate_muta(-1,i,j):
                        nr_miscari -= 1
                    promovare += i
                elif self.matr[i][j] == Joc.JMIN.upper():
                    scor -= 5
                    if self.poate_muta(-1,i,j):
                        nr_miscari -= 1


        return scor*(10**6) + nr_miscari*(10**4) + promovare*100 + random.randint(0,9)


    def estimeaza_scor(self, jucator, adancime):
        t_final = self.final(jucator)
        if t_final == Joc.JMAX :
            return (-(9*10**10)-adancime)
        elif t_final == Joc.JMIN:
            return (+(9*10**10)+adancime)
        else:
            return self.fct_euristica()


    def __str__(self):
        sir = '   '
        for i in range(self.NR_COLOANE):
            sir = sir + alfabet[i] + ' '

        sir += '\n   '
        for i in range(self.NR_COLOANE):
            sir += '--'
        sir += '\n'

        for i in range(self.NR_LINII):
            sir += str(i+1) + ' |'
            for j in range(self.NR_COLOANE):
                sir += self.matr[i][j] + ' '

            sir += '|'
            sir += str(i+1)
            sir += '\n'


        sir += '   '

        for i in range(self.NR_COLOANE):
            sir += '--'
        
        sir += '\n   '
        for i in range(self.NR_COLOANE):
            sir = sir + alfabet[i] + ' '
        sir += '\n'

        return sir

    def genereaza_grid(self):
        for i in range(1,self.NR_LINII+1):
            patr = pygame.Rect(0, i*self.H_GR, self.W_GR, self.H_GR)
            pygame.draw.rect(self.ECRAN, (102,102,0), patr)
            self.ECRAN.blit(self.font.render(str(i), True, (255,0,0)), patr)

            patr = pygame.Rect((self.NR_COLOANE+1)*self.W_GR, i*self.H_GR, self.W_GR, self.H_GR)
            pygame.draw.rect(self.ECRAN, (102,102,0), patr)
            self.ECRAN.blit(self.font.render(str(i), True, (255,0,0)), patr)
      
        for j in range(1,self.NR_COLOANE+1):
            patr = pygame.Rect(j*self.W_GR, 0, self.W_GR, self.H_GR)
            pygame.draw.rect(self.ECRAN, (102,102,0), patr)
            self.ECRAN.blit(self.font.render(alfabet[j-1], True, (255,0,0)), patr)

            patr = pygame.Rect(j*self.W_GR, (self.NR_LINII+1)*self.H_GR, self.W_GR, self.H_GR)
            pygame.draw.rect(self.ECRAN, (102,102,0), patr)
            self.ECRAN.blit(self.font.render(alfabet[j-1], True, (255,0,0)), patr)


        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE):
                patr = pygame.Rect((j+1)*(self.W_GR), (i+1)*(self.H_GR), self.W_GR, self.H_GR)
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.ECRAN, (222,184,135), patr)
                else:
                    pygame.draw.rect(self.ECRAN, (139,69,19), patr)
                
                if self.matr[i][j].lower() in self.SIMBOLURI_JUC:
                    self.ECRAN.blit(self.IMG_JUC[self.matr[i][j]],((j+1)*self.W_GR,(i+1)*self.H_GR))
                
        pygame.display.flip()

class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu
    configuratiile posibile in urma mutarii unui jucator
    """

    ADANCIME_MAX = None

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        #adancimea in arborele de stari
        self.adancime=adancime

        #scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor=scor

        #lista de mutari posibile din starea curenta
        self.mutari_posibile=[]

        #cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa=None

    def jucator_opus(self):
        if self.j_curent==Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari(self):
        l_mutari=self.tabla_joc.mutari(self.j_curent)
        juc_opus=self.jucator_opus()
        l_stari_mutari=[Stare(mutare, juc_opus, self.adancime-1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari


    def __str__(self):
        sir= str(self.tabla_joc) + "(Juc curent: "+self.j_curent+")\n"
        return sir




def alpha_beta(alpha, beta, stare):
    jucator = stare.j_curent

    if stare.adancime==0 or stare.tabla_joc.final(jucator) :
        stare.scor = stare.tabla_joc.estimeaza_scor(jucator,stare.adancime)
        return stare

    if alpha >= beta:
        return stare #este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX :
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            #calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if(alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN :
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if(beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break
    

    stare.scor = stare.stare_aleasa.scor
    
    return stare



def afis_daca_final(stare_curenta):
    jucator = stare_curenta.j_curent
    final = stare_curenta.tabla_joc.final(jucator)
    if(final):
        return True

    return False








def dif(window_dif, entry):
    difficulty = None
    difficulty = entry.get()
    if difficulty.isdigit():
        difficulty = int(difficulty)
        if 1 <= difficulty <= 6:
            Stare.ADANCIME_MAX = difficulty
            window_dif.destroy()
        else:
            difficulty = None






def color(window_color, color):
    Joc.JMIN = color

    [s1, s2] = Joc.SIMBOLURI_JUC.copy()
    Joc.JMAX = s1 if Joc.JMIN == s2 else s2
    if Joc.JMAX == s1:
        Joc.SIMBOLURI_JUC = [s2,s1]
    window_color.destroy()




def main():
    window_dif = tk.Tk()
    label = tk.Label(text='Choose difficulty 1-6')
    label.pack()

    entry = tk.Entry()
    entry.pack()

    button = tk.Button(
        text="Send",
        command=lambda: dif(window_dif, entry)
    )

    button.pack()

    window_dif.mainloop()

    if not Stare.ADANCIME_MAX:
        return



    window_color = tk.Tk()
    [s1, s2] = Joc.SIMBOLURI_JUC.copy()
    frame = tk.Frame(
                master=window_color,
                relief=tk.RAISED,
                borderwidth=1
            )

    frame.grid(row=0, column=0, padx=10, pady=5)
    button = tk.Button(master=frame, text='Black', command=lambda:color(window_color,s1))
    button.pack()


    frame = tk.Frame(
                master=window_color,
                relief=tk.RAISED,
                borderwidth=1
            )

    frame.grid(row=0, column=1, padx=10, pady=5)
    button = tk.Button(master=frame, text='White', command=lambda:color(window_color, s2))
    button.pack()
    window_color.mainloop()
    if not Joc.JMIN:
        return

    pygame.display.set_caption('Dame')

    tabla_curenta = Joc()
    stare_curenta = Stare(tabla_curenta, Joc.SIMBOLURI_JUC[0], Stare.ADANCIME_MAX)
    
    prima_mutare = True

    while True :
        stare_curenta.tabla_joc.genereaza_grid()
        if (afis_daca_final(stare_curenta)):
            pygame.quit()
            sys.exit()
            break

        if (stare_curenta.j_curent == Joc.JMIN):
            #muta jucatorul
            raspuns_valid=False
            if prima_mutare and Joc.JMAX == s1:
                prima_mutare = False
                stare_curenta.j_curent = stare_curenta.jucator_opus()
                continue

            while not raspuns_valid:
                t_inainte=int(round(time.time() * 1000))

                linie = -1
                coloana = -1
         
                while (linie, coloana) == (-1, -1):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            coloana, linie = event.pos
                            linie = linie // stare_curenta.tabla_joc.W_GR - 1
                            coloana = coloana // stare_curenta.tabla_joc.H_GR - 1
                    
                if 0 <= linie < Joc.NR_LINII and 0 <= coloana < Joc.NR_COLOANE:
                    if stare_curenta.tabla_joc.matr[linie][coloana] == stare_curenta.j_curent:
                        rege = False
                    
                    elif stare_curenta.tabla_joc.matr[linie][coloana] == stare_curenta.j_curent.upper():
                        rege = True

                    else:
                        continue

                else:
                    continue

                
                l_mutari = []
                if rege:
                    stare_curenta.tabla_joc.mutare_rege(stare_curenta.j_curent,linie,coloana,l_mutari)
                else:
                    stare_curenta.tabla_joc.mutare(stare_curenta.j_curent,linie,coloana,l_mutari)
                

                linie1, coloana1 = -1, -1
            
                while (linie1, coloana1) == (-1,-1):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            coloana1, linie1 = event.pos
                            linie1 = linie1 // stare_curenta.tabla_joc.W_GR - 1
                            coloana1 = coloana1 // stare_curenta.tabla_joc.H_GR - 1
                    
                if 0 <= linie1 < Joc.NR_LINII and 0 <= coloana1 < Joc.NR_COLOANE:

                    for mutare in l_mutari:
                        if mutare.matr[linie1][coloana1] == stare_curenta.j_curent.lower() or mutare.matr[linie1][coloana1] == stare_curenta.j_curent.upper():
                            aux = mutare
                            raspuns_valid = True
                       
          
            stare_curenta.tabla_joc = aux

            stare_curenta.j_curent = stare_curenta.jucator_opus()
            stare_curenta.tabla_joc.genereaza_grid()

        #--------------------------------
        else: #jucatorul e JMAX (calculatorul)
        #Mutare calculator
            stare_actualizata = alpha_beta(-5000, 5000, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
           
            #S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()
            #stare_curenta.tabla_joc.genereaza_grid()


if __name__ == "__main__" :    
    main()
    
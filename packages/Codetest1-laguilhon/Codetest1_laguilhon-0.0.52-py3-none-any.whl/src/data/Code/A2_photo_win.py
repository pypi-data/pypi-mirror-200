from tkinter import *
from tkinter import ttk
import  tkinter as tk
from tkinter.messagebox import *



from PIL import ImageTk, Image

#classes
import Algo_main_CelebA_vf as a
import  image_celeba as imc

import A2_loading_win as l
import A3_export_data_win as e


    #####     FENETRES avec PHOTOS    ######
class photo_win:

    def __init__(self, string_titre):
        self.win = Tk()
        self.width= self.win.winfo_screenwidth()
        self.height= self.win.winfo_screenheight()
        self.win.geometry("%dx%d" % (self.width, self.height))
        self.win.title(string_titre)

        self.text=tk.StringVar()
        self.text.set("Choississez une ou plusieurs images qui correspondent en cliquant dessus.")
        self.label = ttk.Label( self.win, textvariable=self.text)
        self.label.pack(pady=10)

        self.label2 = ttk.Label(self.win, text="Si aucune image ne correspond ou que vous souhaitez recommencer, vous pouvez appuyez sur ce bouton pour obtenir 5 nouvelles photos de la base de données: " )
        self.label2.pack()
        end_button = Button(self.win, text="Ré-initialiser", command=self.reinitialise)
        end_button.pack()

        
        self.L_photos=[]
        self.L_photos=a.initialisation_Liste_5_premiers()

        self.can_im = Canvas(self.win,bg='white',height=400,width=self.width)
        self.can_im.pack(pady=100)

        self.can_text = Canvas(self.win,height=600,width=self.width)
        self.can_text.pack()

        self.chosen_number=[]
        self.iteration =0
         ### pas utilisé ?
    
        #celeba
        self.mise_a_j_img()

        self.win.mainloop()
    
    def mise_a_j_img(self):
        # Créer les boutons avec les images
        #doit rajouter master=self.win pour éviter problemes avec ma
        #pour éviter le pyimage doesn't exite sur la creation du bouton
        self.im1=ImageTk.PhotoImage(self.L_photos[0].im, master=self.win)
        self.im2=ImageTk.PhotoImage(self.L_photos[1].im, master=self.win)
        self.im3=ImageTk.PhotoImage(self.L_photos[2].im, master=self.win)
        self.im4=ImageTk.PhotoImage(self.L_photos[3].im, master=self.win)
        self.im5=ImageTk.PhotoImage(self.L_photos[4].im, master=self.win)

        self.b1 = tk.Button(self.can_im, image=self.im1, command=lambda: self.choice(0))
        self.b1.pack(side = LEFT, padx=10)

        self.b2 = tk.Button(self.can_im, image=self.im2, highlightcolor="green", highlightthickness=3, activebackground='green', command=lambda: self.choice(1))
        self.b2.pack(side = LEFT, padx=10)

        self.b3 = tk.Button(self.can_im, image=self.im3, highlightcolor="green", highlightthickness=3, activebackground='green', command=lambda: self.choice(2))
        self.b3.pack(side = LEFT, padx=10)
    
        self.b4 = tk.Button(self.can_im, image=self.im4, highlightcolor="green", highlightthickness=3, activebackground='green', command=lambda: self.choice(3))
        self.b4.pack(side = LEFT, padx=10)

        self.b5 = tk.Button(self.can_im, image=self.im5, highlightcolor="green", highlightthickness=3, activebackground='green', command=lambda: self.choice(4))
        self.b5.pack(side = LEFT, padx=10)
        self.chosen_number=[]

    def reinitialise(self):
        for c in self.can_im.winfo_children():
           c.destroy() 

        for c in self.can_text.winfo_children():
           c.destroy() 
        t="Images réinitialisées. Choississez une image (ou plusieurs) qui correspond(ent) le plus en cliquant dessus"
        self.text.set(t)
        self.chosen_number=[]
        self.L_photos=a.initialisation_Liste_5_premiers()
        self.mise_a_j_img()


    def close_win(self):
        self.win.destroy()

    def choice(self, number) :
        if number in self.chosen_number :
            self.chosen_number.remove(number)
        else :
            self.chosen_number.append(number)
        
        for c in self.can_text.winfo_children():
           c.destroy()

        chosen_str=""
        for i in self.chosen_number :
            chosen_str += str(i+1) + ", "

        if len(self.chosen_number)==1 :
            texte_avec_numero=str("Vous avez choisi l'image : "+ chosen_str + ". Voulez vous : ")
            self.label = ttk.Label(self.can_text, text=texte_avec_numero )
            self.label.pack(pady=20)
            end_button = Button(self.can_text, text="Générer d'autres photos à partir de celle choisie", command=self.generate_image)
            end_button.pack(pady=20)
            end_button = Button(self.can_text, text="Valider cette photo comme photo finale", command=self.validate)
            end_button.pack()
        if len(self.chosen_number)>1 :
            texte_avec_numero=str("Vous avez choisi les images : "+ chosen_str + ". Voulez vous : ")
            self.label = ttk.Label(self.can_text, text=texte_avec_numero )
            self.label.pack(pady=20)
            end_button = Button(self.can_text, text="Générer d'autres photos à partir de celles choisies", command=self.generate_image)
            end_button.pack(pady=20)
    

        #l.loading_window()

    def generate_image(self):
        self.iteration+=1
        #algo génétique avec liste des image numero self.a de la liste initiale    et   genere nouvelle liste :
        self.L_photos=a.generate_5_new_photos(self.L_photos, self.chosen_number,  self.iteration)

        t="Choississez à nouveau l'image qui correspond le plus en cliquant dessus (itération : " + str(self.iteration) + " )"
        self.text.set(t)
        
        for c in self.can_im.winfo_children():
           c.destroy() 

        for c in self.can_text.winfo_children():
           c.destroy() 

        self.mise_a_j_img()
        

    def validate(self) :
        choice_final=askokcancel(title="Confirmation de validation", message="Etes-vous sur de vouloir choisir cette photo comme photo finale ? ")
        if choice_final :
            self.close_win()

            # à modif
            chosen_photo=self.L_photos[self.chosen_number[0]].im
            e.export_data_win(chosen_photo)



 #####    MAIN    ######

#photo_win("test mise en commun")
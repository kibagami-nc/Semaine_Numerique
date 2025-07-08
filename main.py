import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
import threading

class PopUpGame:
    def __init__(self):
        self.score = 0
        self.windows_to_close = 10  # Nombre de fenêtres à fermer
        self.closed_windows = 0
        self.game_active = False
        self.popup_windows = []
        self.main_window = None
        
    def start_game(self):
        """Démarre le jeu principal"""
        self.main_window = tk.Tk()
        self.main_window.title("Jeu Pop-Up - Fermez toutes les fenêtres!")
        self.main_window.geometry("400x300")
        self.main_window.configure(bg="#2c3e50")
        
        # Interface principale
        title_label = tk.Label(
            self.main_window, 
            text="JEU POP-UP", 
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title_label.pack(pady=20)
        
        instruction_label = tk.Label(
            self.main_window,
            text=f"Fermez {self.windows_to_close} fenêtres pop-up le plus vite possible!",
            font=("Arial", 12),
            fg="white",
            bg="#2c3e50",
            wraplength=350
        )
        instruction_label.pack(pady=10)
        
        self.score_label = tk.Label(
            self.main_window,
            text=f"Fenêtres fermées: {self.closed_windows}/{self.windows_to_close}",
            font=("Arial", 14),
            fg="#3498db",
            bg="#2c3e50"
        )
        self.score_label.pack(pady=10)
        
        start_button = tk.Button(
            self.main_window,
            text="COMMENCER LE JEU",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white",
            command=self.begin_popup_phase,
            relief="raised",
            bd=3
        )
        start_button.pack(pady=20)
        
        quit_button = tk.Button(
            self.main_window,
            text="Quitter",
            font=("Arial", 12),
            bg="#95a5a6",
            fg="white",
            command=self.main_window.quit
        )
        quit_button.pack(pady=10)
        
        self.main_window.mainloop()
    
    def begin_popup_phase(self):
        """Commence la phase des pop-ups"""
        self.game_active = True
        self.closed_windows = 0
        self.update_score()
        
        # Démarrer la création de pop-ups en arrière-plan
        threading.Thread(target=self.create_popup_sequence, daemon=True).start()
    
    def create_popup_sequence(self):
        """Crée une séquence de fenêtres pop-up"""
        for i in range(self.windows_to_close):
            if not self.game_active:
                break
                
            # Attendre un délai aléatoire entre chaque pop-up
            time.sleep(random.uniform(0.5, 2.0))
            
            # Créer une nouvelle fenêtre pop-up
            self.create_popup_window(i)
    
    def create_popup_window(self, window_id):
        """Crée une fenêtre pop-up individuelle"""
        popup = tk.Toplevel()
        popup.title(f"Pop-up #{window_id + 1}")
        popup.geometry("250x150")
        popup.configure(bg="#e67e22")
        
        # Position aléatoire sur l'écran
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        popup.geometry(f"250x150+{x}+{y}")
        
        # Contenu de la fenêtre
        messages = [
            "FERMEZ-MOI!",
            "Pop-up gênant!",
            "Cliquez pour fermer",
            "Fenêtre intrusive",
            "Supprimez-moi!",
            "Pop-up malveillant",
            "Fermez cette fenêtre!",
            "Publicité non désirée"
        ]
        
        label = tk.Label(
            popup,
            text=random.choice(messages),
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#e67e22"
        )
        label.pack(pady=20)
        
        close_button = tk.Button(
            popup,
            text="✖ FERMER",
            font=("Arial", 10, "bold"),
            bg="#c0392b",
            fg="white",
            command=lambda: self.close_popup(popup),
            relief="raised",
            bd=2
        )
        close_button.pack(pady=10)
        
        # Empêcher la fermeture par la croix rouge (forcer l'utilisation du bouton)
        popup.protocol("WM_DELETE_WINDOW", lambda: self.close_popup(popup))
        
        # Rendre la fenêtre toujours au premier plan
        popup.attributes("-topmost", True)
        popup.focus_force()
        
        self.popup_windows.append(popup)
    
    def close_popup(self, popup_window):
        """Ferme une fenêtre pop-up et met à jour le score"""
        if popup_window in self.popup_windows:
            popup_window.destroy()
            self.popup_windows.remove(popup_window)
            self.closed_windows += 1
            self.update_score()
            
            # Vérifier si toutes les fenêtres sont fermées
            if self.closed_windows >= self.windows_to_close:
                self.end_game()
    
    def update_score(self):
        """Met à jour l'affichage du score"""
        if hasattr(self, 'score_label'):
            self.score_label.config(
                text=f"Fenêtres fermées: {self.closed_windows}/{self.windows_to_close}"
            )
    
    def end_game(self):
        """Termine le jeu et lance la fenêtre de mot de passe"""
        self.game_active = False
        
        # Fermer toutes les fenêtres restantes
        for popup in self.popup_windows[:]:
            popup.destroy()
        self.popup_windows.clear()
        
        # Afficher message de victoire
        messagebox.showinfo(
            "Félicitations!", 
            f"Bravo! Vous avez fermé toutes les {self.windows_to_close} fenêtres!\n\n"
            "Maintenant, vous devez entrer le mot de passe secret..."
        )
        
        # Lancer la fenêtre de mot de passe
        self.show_password_window()
    
    def show_password_window(self):
        """Affiche la fenêtre finale pour entrer le mot de passe"""
        # Créer la fenêtre de mot de passe
        password_window = tk.Toplevel(self.main_window)
        password_window.title("Mot de passe requis")
        password_window.geometry("400x300")
        password_window.configure(bg="#34495e")
        password_window.resizable(False, False)
        
        # Centrer la fenêtre sur l'écran
        password_window.update_idletasks()
        width = password_window.winfo_width()
        height = password_window.winfo_height()
        x = (password_window.winfo_screenwidth() // 2) - (width // 2)
        y = (password_window.winfo_screenheight() // 2) - (height // 2)
        password_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Configuration de la fenêtre
        password_window.transient(self.main_window)
        password_window.grab_set()  # Rendre la fenêtre modale
        password_window.focus_set()  # Donner le focus à la fenêtre
        
        # Interface de la fenêtre de mot de passe
        title_label = tk.Label(
            password_window,
            text="🔒 ACCÈS SÉCURISÉ",
            font=("Arial", 18, "bold"),
            fg="#ecf0f1",
            bg="#34495e"
        )
        title_label.pack(pady=20)
        
        instruction_label = tk.Label(
            password_window,
            text="Entrez le mot de passe secret pour terminer le jeu:",
            font=("Arial", 12),
            fg="#bdc3c7",
            bg="#34495e",
            wraplength=350
        )
        instruction_label.pack(pady=10)
        
        # Zone de saisie du mot de passe
        password_frame = tk.Frame(password_window, bg="#34495e")
        password_frame.pack(pady=20)
        
        password_label = tk.Label(
            password_frame,
            text="Mot de passe:",
            font=("Arial", 12),
            fg="#ecf0f1",
            bg="#34495e"
        )
        password_label.pack()
        
        self.password_entry = tk.Entry(
            password_frame,
            font=("Arial", 14),
            width=20,
            show="*",  # Masquer le texte saisi
            relief="ridge",
            bd=2
        )
        self.password_entry.pack(pady=5)
        
        # S'assurer que le champ de saisie reçoit le focus
        password_window.after(100, lambda: self.password_entry.focus_set())
        
        # Boutons
        button_frame = tk.Frame(password_window, bg="#34495e")
        button_frame.pack(pady=20)
        
        validate_button = tk.Button(
            button_frame,
            text="VALIDER",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            command=lambda: self.validate_password(password_window),
            relief="raised",
            bd=3,
            padx=20
        )
        validate_button.pack(side=tk.LEFT, padx=10)
        
        hint_button = tk.Button(
            button_frame,
            text="INDICE",
            font=("Arial", 12),
            bg="#f39c12",
            fg="white",
            command=self.show_password_hint,
            relief="raised",
            bd=3,
            padx=20
        )
        hint_button.pack(side=tk.LEFT, padx=10)
        
        # Permettre la validation avec la touche Entrée
        password_window.bind('<Return>', lambda event: self.validate_password(password_window))
        
        # Empêcher la fermeture de la fenêtre sans mot de passe
        password_window.protocol("WM_DELETE_WINDOW", lambda: self.confirm_exit(password_window))
        
        return password_window
    
    def validate_password(self, password_window):
        """Valide le mot de passe saisi"""
        # Liste des différents mots de passe possibles
        différents_mots_de_passe = [
            "POPUP2025", "POPUP2024", "POPUP2023", "POPUP2022", "POPUP2021", "POPUP2020",
        ]
        
        # Mot de passe choisi aléatoirement dans la liste
        correct_password = random.choice(différents_mots_de_passe)  # Mot de passe secret
        entered_password = self.password_entry.get().upper()
        
        if entered_password == correct_password:
            # Mot de passe correct
            password_window.destroy()
            self.show_victory_screen()
        else:
            # Mot de passe incorrect
            messagebox.showerror(
                "Mot de passe incorrect",
                "Le mot de passe saisi est incorrect.\n\nEssayez encore ou utilisez l'indice."
            )
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
    
    def show_password_hint(self):
        """Affiche un indice pour le mot de passe"""
        messagebox.showinfo(
            "💡 Indice",
            "Le mot de passe est composé de :\n\n"
            "• Le nom du jeu (en majuscules)\n"
            "• Suivi de l'année actuelle\n\n"
            "Exemple: MOTDEPASSE2024"
        )
    
    def show_victory_screen(self):
        """Affiche l'écran de victoire final"""
        victory_window = tk.Toplevel(self.main_window)
        victory_window.title("🎉 VICTOIRE!")
        victory_window.geometry("500x400")
        victory_window.configure(bg="#2ecc71")
        victory_window.resizable(False, False)
        
        # Centrer la fenêtre
        victory_window.transient(self.main_window)
        victory_window.grab_set()  # Rendre la fenêtre modale
        
        # Contenu de l'écran de victoire
        title_label = tk.Label(
            victory_window,
            text="🎊 FÉLICITATIONS! 🎊",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#2ecc71"
        )
        title_label.pack(pady=30)
        
        message_label = tk.Label(
            victory_window,
            text="Vous avez réussi à :\n\n"
                 f"✓ Fermer {self.windows_to_close} fenêtres pop-up\n"
                 "✓ Trouver le mot de passe secret\n"
                 "✓ Terminer le jeu avec succès!",
            font=("Arial", 14),
            fg="white",
            bg="#2ecc71",
            justify="left"
        )
        message_label.pack(pady=20)
        
        score_label = tk.Label(
            victory_window,
            text=f"🏆 Score final: {self.closed_windows}/{self.windows_to_close} fenêtres fermées",
            font=("Arial", 16, "bold"),
            fg="#f1c40f",
            bg="#2ecc71"
        )
        score_label.pack(pady=20)
        
        # Boutons finaux
        button_frame = tk.Frame(victory_window, bg="#2ecc71")
        button_frame.pack(pady=30)
        
        restart_button = tk.Button(
            button_frame,
            text="🔄 REJOUER",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            command=lambda: self.restart_game(victory_window),
            relief="raised",
            bd=3,
            padx=20
        )
        restart_button.pack(side=tk.LEFT, padx=15)
        
        quit_button = tk.Button(
            button_frame,
            text="🚪 QUITTER",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            command=self.quit_game,
            relief="raised",
            bd=3,
            padx=20
        )
        quit_button.pack(side=tk.LEFT, padx=15)
    
    def restart_game(self, victory_window):
        """Redémarre le jeu"""
        victory_window.destroy()
        
        # Fermer toutes les fenêtres existantes
        for popup in self.popup_windows[:]:
            try:
                popup.destroy()
            except:
                pass
        self.popup_windows.clear()
        
        if self.main_window:
            self.main_window.destroy()
        
        # Créer une nouvelle instance du jeu
        new_game = PopUpGame()
        new_game.start_game()
    
    def confirm_exit(self, window):
        """Confirme la sortie du jeu"""
        if messagebox.askyesno("Confirmer", "Êtes-vous sûr de vouloir quitter le jeu?"):
            window.destroy()
            self.quit_game()
    
    def quit_game(self):
        """Quitte complètement le jeu"""
        # Arrêter le jeu
        self.game_active = False
        
        # Fermer toutes les fenêtres pop-up
        for popup in self.popup_windows[:]:
            try:
                popup.destroy()
            except:
                pass
        self.popup_windows.clear()
        
        # Fermer la fenêtre principale
        if self.main_window:
            try:
                self.main_window.quit()
                self.main_window.destroy()
            except:
                pass

def main():
    """Fonction principale pour lancer le jeu"""
    print("🎮 Démarrage du jeu Pop-Up...")
    game = PopUpGame()
    game.start_game()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time

import threading
import os
class PopUpGame: # rename demande d'amie pour faire comme dans la mission GTA ?
    def __init__(self):
        self.score = 0
        self.time_limit = 30  # Durée du jeu en secondes (remis à 30 sec)
        self.time_remaining = 30 # Temps qu'il reste pour le jeu (remis à 30 sec)
        self.closed_windows = 0
        self.game_active = False
        self.popup_windows = []
        self.main_window = None
        self.start_time = None
        self.popup_delay = 1.0  # Délai initial entre les pop-ups (plus rapide)
        self.min_delay = 0.15  # Délai minimum entre les pop-ups (plus rapide)
        
    def start_game(self):
        """Démarre le jeu principal"""
        self.main_window = tk.Tk()
        self.main_window.title("Jeu Pop-Up - Défi Chronomètre!")
        self.main_window.geometry("400x300")
        self.main_window.configure(bg="#2c3e50")
        # self.main_window.attributes("-fullscreen", True)  # Plein écran supprimé

        # Interface principale, page pour start le jeu
        title_label = tk.Label(
            self.main_window, 
            text="POP-UP", 
            font=("Arial", 25, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title_label.pack(pady=20)
        
        instruction_label = tk.Label( # deuxième ligne d'instruction
            self.main_window,
            text=f"Fermez le maximum de fenêtres en {self.time_limit} secondes!",
            font=("Arial", 12),
            fg="white",
            bg="#2c3e50",
            wraplength=350
        )
        instruction_label.pack(pady=10)
        
        self.score_label = tk.Label( # Affichage du score (3ème ligne)
            self.main_window,
            text=f"Score: {self.closed_windows} fenêtres fermées",
            font=("Arial", 14),
            fg="#3498db",
            bg="#2c3e50"
        )
        self.score_label.pack(pady=5)
        
        self.time_label = tk.Label( # Affichage du temps restant
            self.main_window,
            text=f"Temps restant: {self.time_remaining}s",
            font=("Arial", 14),
            fg="#e74c3c",
            bg="#2c3e50"
        )
        self.time_label.pack(pady=5)
        
        start_button = tk.Button( # Bouton pour commencer le jeu
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
        
        quit_button = tk.Button( # Bouton pour quitter le jeu
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
        self.start_time = time.time()
        self.time_remaining = self.time_limit
        self.popup_delay = 2.0  # Reset du délai initial
        self.update_score()
        
        # Démarrer le timer du jeu
        threading.Thread(target=self.game_timer, daemon=True).start()
        # Démarrer la création de pop-ups en arrière-plan
        threading.Thread(target=self.create_popup_sequence, daemon=True).start()
    
    def game_timer(self):
        """Gère le timer du jeu"""
        while self.game_active and self.time_remaining > 0:
            time.sleep(0.1)  # Mise à jour toutes les 100ms
            if self.game_active:
                elapsed_time = time.time() - self.start_time
                self.time_remaining = max(0, self.time_limit - elapsed_time)
                self.update_time_display()
        
        if self.game_active:  # Le temps est écoulé
            self.end_game()
    
    def create_popup_sequence(self):
        """Crée une séquence continue de fenêtres pop-up"""
        popup_id = 0
        while self.game_active and self.time_remaining > 0:
            # Créer une nouvelle fenêtre pop-up
            self.create_popup_window(popup_id)
            popup_id += 1
            
            # Attendre selon le délai actuel
            time.sleep(self.popup_delay)
            
            # Réduire progressivement le délai basé sur le score
            speed_factor = min(self.closed_windows * 0.05, 0.8)  # Max 80% de réduction
            self.popup_delay = max(self.min_delay, 2.0 - (2.0 * speed_factor))
    
    def create_popup_window(self, window_id):
        """Crée une fenêtre pop-up individuelle avec une image du dossier img (GIF ou PNG uniquement)"""
        popup = tk.Toplevel()
        popup.title(f"Pop-up #{window_id + 1}")
        popup.configure(bg="#e67e22")
        popup.resizable(False, False)  # Empêche le plein écran et le redimensionnement

        # Charger une image GIF ou PNG du dossier img
        img_folder = os.path.join(os.path.dirname(__file__), "img")
        img_files = [f for f in os.listdir(img_folder) if f.lower().endswith((".gif", ".png"))]
        if img_files:
            img_path = os.path.join(img_folder, random.choice(img_files))
            img_tk = tk.PhotoImage(file=img_path)
            # Réduire l'image à 50% puis zoom aléatoire entre 1x et 2x
            img_small = img_tk.subsample(2, 2)
            zoom_factor = random.randint(1, 2)
            img_zoomed = img_small.zoom(zoom_factor, zoom_factor)
            img_width = img_zoomed.width()
            img_height = img_zoomed.height()
            img_label = tk.Label(popup, image=img_zoomed, bg="#e67e22")
            img_label.image = img_zoomed  # garder une référence
            img_label.pack(pady=5)
            # Adapter la taille de la fenêtre à l'image zoomée
            popup.geometry(f"{img_width}x{img_height}")
        else:
            img_label = tk.Label(popup, text="Aucune image trouvée", bg="#e67e22")
            img_label.pack(pady=5)
            popup.geometry("120x60")

        # Position aléatoire sur l'écran
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        popup.geometry(f"+{x}+{y}")

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
            font=("Arial", 10, "bold"),
            fg="white",
            bg="#e67e22"
        )
        label.pack(pady=5)
        
        close_button = tk.Button(
            popup,
            text="✖ FERMER",
            font=("Arial", 9, "bold"),
            bg="#c0392b",
            fg="white",
            command=lambda: self.close_popup(popup),
            relief="raised",
            bd=2
        )
        close_button.pack(pady=5)
        
        popup.protocol("WM_DELETE_WINDOW", lambda: self.close_popup(popup))
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
    
    def update_score(self):
        """Met à jour l'affichage du score"""
        if hasattr(self, 'score_label'):
            self.score_label.config(
                text=f"Score: {self.closed_windows} fenêtres fermées"
            )
    
    def update_time_display(self):
        """Met à jour l'affichage du temps restant"""
        if hasattr(self, 'time_label'):
            self.time_label.config(
                text=f"Temps restant: {int(self.time_remaining)}s"
            )
    
    def end_game(self):
        """Termine le jeu et lance la fenêtre de mot de passe"""
        self.game_active = False
        
        # Fermer toutes les fenêtres restantes
        for popup in self.popup_windows[:]:
            popup.destroy()
        self.popup_windows.clear()
        
        # Afficher message de victoire avec le score
        messagebox.showinfo(
            "Temps écoulé!", 
            f"Bravo! Votre score final est de {self.closed_windows} fenêtres fermées!\n\n"
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
                 f"✓ Fermer {self.closed_windows} fenêtres pop-up en {self.time_limit} secondes\n"
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
            text=f"🏆 Score final: {self.closed_windows} fenêtres fermées",
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
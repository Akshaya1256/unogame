import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
import pygame
class StartWindow:
    def __init__(self, root):
        self.root = root
        self.play_background_music()
        self.root.title("UNO Card Game")
        self.label = tk.Label(root, text="Welcome to UNO Card Game", font=(18),fg='black',bg='yellow')
        self.label.pack(pady=20)
        self.load_and_display_image()
        self.num_players_label = tk.Label(root, text="Enter the number of players:",font=14,fg='blue',bg='yellow',width=25,height=2)
        self.num_players_label.pack()
        self.num_players_entry = tk.Entry(root,width=20)
        self.num_players_entry.pack()
        self.start_button = tk.Button(root, text="START GAME", command=self.start_game,fg='red',bg='yellow',font=30,width=25,height=3)
        self.start_button.pack()
        #self.load_and_display_image()

    def play_background_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load('C:\\Users\\Chinnu\\Desktop\\python project\\cards\\Komiku_-_04_-_Skate.mp3')
        pygame.mixer.music.play(-1)  

    def stop_background_music(self):
        pygame.mixer.music.stop()

    def load_and_display_image(self):
        image_path = 'C:\\Users\\Chinnu\\Desktop\\python project\\cards\\cards_gif.gif'
        original_image = Image.open(image_path)
        width = 400  
        height = 500  
        resized_image = original_image.resize((width, height))
        photo = ImageTk.PhotoImage(resized_image)
        self.image_label = tk.Label(self.root, image=photo)
        self.image_label.image = photo
        self.image_label.pack()

    def start_game(self):
        num_players = int(self.num_players_entry.get())
        self.root.destroy()  
        self.stop_background_music()
        self.game_window = tk.Tk()
        self.game = UnoGame(self.game_window, num_players)
        self.game_window.configure(bg='green')
        self.game_window.mainloop()

class UnoGame:
    def __init__(self, root, num_players):
        self.root = root
        self.root.title("UNO Card Game")
        self.num_players = num_players
        self.num_cards = 7  
        self.player_hands = []
        self.discard_pile = []
        self.deck = self.create_deck()
        self.shuffle_deck()
        self.create_players()
        self.current_player = 1
        self.direction = 1
        self.load_card_images()
        self.create_widgets()
        self.discard_pile.append(self.deck.pop())
        self.can_draw_card = True
        self.is_turn_over = True 
        self.update_display()

    def create_deck(self):
        suits = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
        ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
        deck = [f"{rank} of {suit}" for suit in suits for rank in ranks]
        return deck

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def create_players(self):
        for i in range(self.num_players):
            hand = []
            for j in range(self.num_cards):
                card = self.deck.pop()
                hand.append(card)
            self.player_hands.append(hand)

    def load_card_images(self):
        self.card_images = {}
        for suit in ['Hearts', 'Spades', 'Diamonds', 'Clubs']:
            for rank in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']:
                card = f"{rank} of {suit}"
                image_name = f"{rank} of {suit}.png"
                image_path = os.path.join("cards", image_name)
                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    image = image.resize((100, 150), Image.LANCZOS)
                    self.card_images[card] = ImageTk.PhotoImage(image)
                else:
                    print(f"Image not found for {card}")

    def create_widgets(self):
        self.discard_label = tk.Label(self.root, text="Top Card on Discard Pile:", font=('Helvetica', 16))
        self.discard_label.pack(pady=10)
        self.top_card_label = tk.Label(self.root, image=None)
        self.top_card_label.pack()
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(pady=10)
        self.current_player_label = tk.Label(self.root, text=f"Current Player: Player {self.current_player + 1}", font=('Helvetica', 16))
        self.current_player_label.pack(pady=10)
        self.play_btn = tk.Button(self.root, text="Play Card", command=self.play_card)
        self.play_btn.pack()
        self.draw_btn = tk.Button(self.root, text="Draw Card", command=self.draw_card)
        self.draw_btn.pack()
        self.quit=tk.Button(self.root,text="Quit Game",command=self.quit_game)
        self.quit.pack()
        self.update_display()

    def quit_game(self):
        self.root.destroy()

    def update_display(self):
        self.update_top_card_display()
        self.update_current_player_label()
        self.update_player_hand_display()

    def update_top_card_display(self):
        if not self.discard_pile:
            self.top_card_label.config(text="No Card on Discard Pile")
            return
        top_card = self.discard_pile[-1]
        card_image = self.card_images.get(top_card)
        if card_image:
            self.top_card_label.config(image=card_image)
            self.top_card_label.image = card_image
        else:
            self.top_card_label.config(text="No Card on Discard Pile")

    def update_current_player_label(self):
        self.current_player_label.config(text=f"Current Player: Player {self.current_player + 1}")

    def update_player_hand_display(self):
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        for i, card in enumerate(self.player_hands[self.current_player]):
            card_image = self.card_images.get(card)
            if card_image:
                card_button = tk.Button(self.player_frame, image=card_image, command=lambda i=i: self.play_card(i))
                card_button.image = card_image
                card_button.pack(side=tk.LEFT, padx=2)

    def play_card(self, card_index):
        if self.player_hands[self.current_player]:
            card = self.player_hands[self.current_player].pop(card_index)
            if not self.discard_pile:
                self.discard_pile.append(card)
            else:
                top_card = self.discard_pile[-1]
                if self.is_valid_play(card, top_card):
                    self.discard_pile.append(card)
                    self.is_turn_over = True  
                else:
                    self.player_hands[self.current_player].append(card)
                    messagebox.showerror("Invalid Play", "The selected card does not match the top card.")
                    return  
            self.next_turn()
        else:
            messagebox.showinfo("No Cards to Play", "You don't have any cards to play!")

    
    def draw_card(self):
        if self.can_draw_card:
            card = self.deck.pop(0)
            top_card = self.discard_pile[-1]
            self.player_hands[self.current_player].append(card)
            self.can_draw_card = False
            self.update_player_hand_display() 
            self.is_turn_over = True 
            self.next_turn()
            if len(self.deck)==0:
                messagebox.showinfo("deck is empty")
                #self.root.destroy()

        else:
            messagebox.showinfo("Draw Card", "You can draw only once in a round!")
                           
    def next_turn(self):
        if self.is_turn_over:  
            winner_index = self.check_winner()
            if winner_index is not None:
                self.show_winner_message(winner_index)
                self.root.destroy() 
            else:
                self.is_turn_over = False  
                self.can_draw_card = True
                self.current_player = (self.current_player + self.direction) % self.num_players
                self.update_display()

    def is_valid_play(self, card, top_card):
        card_rank, card_suit = card.split()[0], card.split()[2]
        top_card_rank, top_card_suit = top_card.split()[0], top_card.split()[2]
        return card_rank == top_card_rank or card_suit == top_card_suit
    
    def check_winner(self):
        for i, hand in enumerate(self.player_hands):
            if len(hand) == 0:
                return i  
        return None

    def show_winner_message(self, winner_index):
        player_number = winner_index + 1
        messagebox.showinfo("Winner", f"Player {player_number} winss!!")

def main():
    root = tk.Tk()
    start_window = StartWindow(root)
    root.config(bg='green')
    root.mainloop()

if __name__ == "__main__":
   main()
import random
from tkinter import *
from pandas import *
from tkinter import messagebox
import random

BACKGROUND_COLOR = "#B1DDC6"


# ------------ CHOOSING A RANDOM WORD ----------- #

def choose_random_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(data_dict)
    card_canvas.itemconfig(lang_text, text="German", fill="black")
    card_canvas.itemconfig(word_text, text=current_card["German"], fill="black")
    card_canvas.itemconfig(card_img, image=card_front_img)
    flip_timer = window.after(3000, func=change_card)


def change_card():
    card_canvas.itemconfig(lang_text, text="Turkish", fill="white")
    card_canvas.itemconfig(word_text, text=current_card["Turkish"], fill="white")
    card_canvas.itemconfig(card_img, image=card_back_img)


def remove_card():
    data_dict.remove(current_card)
    choose_random_word()
    data_frame = DataFrame(data_dict)
    data_frame.to_csv('./data/words_to_learn.csv', index=False)
    if len(data_dict) == 0:
        messagebox.showinfo(title="Congrats", message="You have completed all the words!")
        window.destroy()


# ------------- UI ------------- #
window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=change_card)

# Flash Card Canvas
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_img = card_canvas.create_image(400, 263, image=card_front_img)
lang_text = card_canvas.create_text(400, 150, text="German", font=("Ariel", 40, "italic"))
word_text = card_canvas.create_text(400, 263, text="Word", font=("Ariel", 40, "bold"))
card_canvas.grid(row=0, column=0, columnspan=2)

# Buttons
# Right Button
right_img = PhotoImage(file="./images/right.png")
grn_btn = Button(image=right_img, command=remove_card)
grn_btn.config(highlightthickness=0)
grn_btn.grid(row=1, column=1)
# Wrong Button
wrong_img = PhotoImage(file="./images/wrong.png")
red_btn = Button(image=wrong_img, command=choose_random_word)
red_btn.config(highlightthickness=0)
red_btn.grid(row=1, column=0)

# --------- GETTING THE DATA FROM CSV FILE --------- #

current_card = {}
words_to_learn = []
data_file = ""
try:
    data_file = read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    data_file = read_csv("./data/french_words.csv")
finally:
    data_file.dropna(inplace=True)
    data_dict = data_file.to_dict(orient="records")
    choose_random_word()

window.mainloop()

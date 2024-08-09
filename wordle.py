from tkinter import *
from tkinter import messagebox
from random import randrange
import requests

BUTTONS: list[str] = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D',
                      'Delete',
                      'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M',
                      'Submit']

URL: str = "https://api.dictionaryapi.dev/api/v2/entries/en/"


def wordsData() -> list[str]:
    with open("words.txt", "r") as file:
        return [line.strip() for line in file]


WORDS_TO_GUESS: list[str] = wordsData()


class Wordle(Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("WORDLE")
        self.iconbitmap("icon.ico")
        self.geometry("629x600")
        self.resizable(False, False)

        self.bottomFrame: Frame = Frame(self)
        self.bottomFrame.pack(side=BOTTOM)
        self.topFrame: Frame = Frame(self)
        self.topFrame.pack(side=TOP, pady=30)

        self.labels: list[Label] = []
        self.labels_to_restart: list[Label] = []

        self.counter: int = 0

        self.can_input: bool = True

        self.word_to_guess: str = WORDS_TO_GUESS[randrange(len(WORDS_TO_GUESS))].upper()
        self.entered_word: str = ""

        for i in range(30):
            label: Label = Label(self.topFrame, text="", bg="white", width=9, height=4)
            self.labels.append(label)
            self.labels_to_restart.append(label)

        for i, label in enumerate(self.labels):
            row, col = divmod(i, 5)
            label.grid(row=row, column=col, padx=5, pady=5)

        for i in range(28):
            self.button: Button = Button(self.bottomFrame, text=BUTTONS[i], justify=CENTER, width=5, height=2,
                                         command=lambda ind=i: self.buttonCommand(BUTTONS[ind]))
            self.button.grid(row=(0 if i < 14 else 1), column=(i if i < 14 else i - 14))

    def buttonCommand(self, letter: str) -> None:
        if letter == 'Delete':
            self.deleteCommand()

        elif letter == 'Submit':
            self.submitCommand()

        else:
            self.letterCommand(letter)

    def deleteCommand(self) -> None:
        self.counter -= 1
        self.entered_word = self.entered_word[:-1]
        self.labels[self.counter].config(text="")

        if self.counter < 0:
            self.counter = 0

        self.can_input = True

    def submitCommand(self) -> None:
        if self.counter % 5 != 0 or self.counter == 0:
            messagebox.showinfo("Message", "Not enough letters!")
        else:
            if not self.isWordValid():
                messagebox.showinfo("Message", "Such word does not exist!")
            else:
                self.checkWithWordToGuess()
                self.labels = self.labels[self.counter:]
                self.counter = 0
                self.can_input = True

                if not self.playerWin() and self.outOfTries():
                    self.quitOrRestart("lost")

                self.entered_word = ""

    def letterCommand(self, letter: str) -> None:
        if self.can_input:
            self.labels[self.counter].config(text=letter)
            self.entered_word += letter
            self.counter += 1

            if self.counter == 5:
                self.can_input = False

    def isWordValid(self) -> bool:
        return requests.get(URL + self.entered_word).status_code != 404

    def checkWithWordToGuess(self) -> None:
        self.highlightWord()

        if self.playerWin():
            self.quitOrRestart("won")

    def highlightWord(self) -> None:
        for i in range(5):
            if self.entered_word[i] == self.word_to_guess[i]:
                self.labels[i].config(bg="green")
            elif self.entered_word[i] in self.word_to_guess:
                self.labels[i].config(bg="yellow")
            else:
                self.labels[i].config(bg="gray")

    def quitOrRestart(self, result: str) -> None:
        answer: bool = messagebox.askyesno("Message", f"You {result}! The word was {self.word_to_guess.title()}. "
                                                      f"Do you want to play again?")
        if answer:
            self.restartGame()
        else:
            self.quitGame()

    def playerWin(self) -> bool:
        return self.entered_word == self.word_to_guess

    def outOfTries(self) -> bool:
        return len(self.labels) == 0

    def restartGame(self) -> None:
        self.word_to_guess = WORDS_TO_GUESS[randrange(len(WORDS_TO_GUESS))].upper()
        self.entered_word = ""
        self.counter = 0
        self.can_input = True
        self.labels = self.labels_to_restart.copy()

        for label in self.labels:
            label.config(text="", bg="white")

    def quitGame(self) -> None:
        self.destroy()


def main() -> None:
    app: Wordle = Wordle()
    app.mainloop()


if __name__ == "__main__":
    main()

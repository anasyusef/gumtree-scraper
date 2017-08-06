#!/usr/bin/python


"""Copyright® Anas Yousef 2017"""


from tkinter import *
import tkinter.messagebox as box
import GumtreeScraper


class App:

    def __init__(self, master):
        frame = Frame(master)

        self.separate_x = 5
        self.separate_y = 2

        self.search_label = Label(frame, text="Search")
        self.search_entry = Entry(frame, text="Search")

        self.location_label = Label(frame, text="Postcode (optional)")
        self.location_entry = Entry(frame, text="Postcode (optional)")

        self.num_pages_label = Label(frame, text="Number of pages (default 1)")
        self.num_pages_entry = Entry(frame, text="Number of pages (default 1)")

        self.filename_label = Label(frame, text="Name of the file (without extension)")
        self.filename_entry = Entry(frame, text="Name of the file (without extension)")

        self.search_button = Button(frame, text="Search", width = 20, command=self.runProgram)

        self.status_bar_content = StringVar()
        self.status_bar = Label(frame, text="", anchor=W, relief=SUNKEN, textvariable=self.status_bar_content)

        # Organizing layout

        self.search_label.grid(row=1, column=1, sticky=W, pady = self.separate_y, padx=self.separate_x)
        self.search_entry.grid(row=1, column=2, pady = self.separate_y, padx=self.separate_x)

        self.location_label.grid(row=1, column=3, sticky=W, pady = self.separate_y, padx=self.separate_x)
        self.location_entry.grid(row=1, column=4, pady = self.separate_y, padx=self.separate_x)

        self.num_pages_label.grid(row=2, column=1, sticky=W, pady = self.separate_y, padx=self.separate_x)
        self.num_pages_entry.grid(row=2, column=2, pady = self.separate_y, padx=self.separate_x)

        self.filename_label.grid(row=2, column=3, sticky=W, pady = self.separate_y, padx=self.separate_x)
        self.filename_entry.grid(row=2, column=4, pady = self.separate_y, padx=self.separate_x)

        self.search_button.grid(row=3, column=2, columnspan=2, pady=10)

        self.status_bar.grid(sticky=NSEW, column=1, columnspan=4)

        frame.pack()

    def validateEntries(self):

        items_entry = {self.location_entry:True, self.num_pages_entry:True, self.filename_entry: False,
                       self.search_entry: False}
        true_count = 0
        for item, optional in items_entry.items():
            if self.is_empty(item, optional):
                true_count += 1

        if self.check_number_entry(self.num_pages_entry):
            true_count += 1

        if self.num_pages_entry.get() == '':
            self.num_pages_entry.insert(0, '1')

        # True count must be 5 to have all of them correct
        return true_count

    def is_empty(self, item, optional):

        try:
            if bool(item.get()) is False and optional is True:
                return True
            elif bool(item.get()) is True and optional is True:
                return True
            elif bool(item.get()) is False and optional is False:
                raise ValueError
            elif bool(item.get()) is True and optional is False:
                return True
        except ValueError:
            box.showerror("Incorrect Information", "Please make sure that you have entered the correct information and"
                                                   " in the correct format in this field:\n{}".format(item.cget('text')))
            return False

    def check_number_entry(self, item):
        try:
            if item.get().isdigit():
                return True
            else:
                raise ValueError

        except ValueError:
            box.showerror("Incorrect Information", "Please make sure that you have entered the correct information and"
                                                   " in the correct format in this field:\n{}".format(item.cget('text')))
            return False

    def runProgram(self):

        mainProgram = GumtreeScraper.main(str(self.search_entry.get()), str(self.location_entry.get()),
                                          int(self.num_pages_entry.get()), str(self.filename_entry.get()))

        if self.validateEntries() >= 5:
            if mainProgram:
                self.status_bar_content.set("Done! check your {} file".format(self.filename_entry.get() +
                                                                              filename_extension))

if __name__ == '__main__':

    filename_extension = ".csv"
    app_version = "V1.7"

    root = Tk()
    root.title("Gumtree Scraper {}".format(app_version))

    app = App(root)

    root.mainloop()

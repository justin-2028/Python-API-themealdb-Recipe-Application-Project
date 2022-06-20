from tkinter import *
from tkinter import ttk

import requests


class Recipes(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack(fill=BOTH, expand=True)

        # Create the screen widgets
        self.meal_list_listbox = Listbox(self, width=25, height=10, selectmode=SINGLE)
        self.directions_text = Text(self, borderwidth=1)

        # setup the screen
        self.setup_ui()

    def setup_ui(self):
        """
            This method will setup the UI:
                Add the widgets to the screen
                Configuring each widget as necessary
        """

        # Create and add the label widgets to the screen
        recipe_lbl = Label(self, text="Recipes:")
        recipe_lbl.grid(sticky=W, pady=10, padx=(10, 0))

        categories_lbl = Label(self, text="Categories:")
        categories_lbl.grid(row=2, sticky=W, pady=(10, 0), padx=(10, 0))

        directions_lbl = Label(self, text="Directions:")
        directions_lbl.grid(row=0, column=2, sticky=W, padx=10, pady=10)

        # Get the categories from the site
        category_list = requests.get_categories()

        # Create the display category list
        display_category_list = ["Select:"]
        for item in category_list:
            display_category_list.append(item.get_category())

        # Create the default value to be displayed for the category list
        default_category = StringVar(self)
        default_category.set(display_category_list[0])

        # Create style to update the OptionMenu's look
        self.set_style()

        # Create the Options Menu widget for displaying the categories
        categories_dropdown = ttk.OptionMenu(self, default_category,
                                             *display_category_list,
                                             command=self.load_meals,
                                             style='raised.TMenubutton')
        categories_dropdown.grid(row=3, pady=5, padx=(10, 0))
        categories_dropdown.config(width=20)

        # Configure and add the listbox widget to display the recipe names
        self.meal_list_listbox.configure(exportselection=False)
        self.meal_list_listbox.grid(row=1, padx=(10, 0), sticky='nw')
        self.meal_list_listbox.bind("<<ListboxSelect>>", self.load_meal)

        # Create and attach a vertical scrollbar to the recipe listbox widget
        recipe_list_scrollbar = Scrollbar(self, command=self.meal_list_listbox.yview)
        recipe_list_scrollbar.grid(row=1, column=1, sticky='nsew')
        self.meal_list_listbox['yscrollcommand'] = recipe_list_scrollbar.set

        # Add and configure the textbox to display the recipe directions
        self.directions_text.grid(row=1, column=2, columnspan=2, rowspan=4, 
                                  padx=(10, 0), pady=(0, 10), sticky=(N, S, E, W))

        # Create and attach a vertical scrollbar to the recipe directions widget
        directions_scrollbar = Scrollbar(self, command=self.directions_text.yview)
        directions_scrollbar.grid(row=1, column=4, sticky='nsew', rowspan=4,
                                  padx=(0, 10), pady=(0, 10))
        self.directions_text['yscrollcommand'] = directions_scrollbar.set

        # Create and add an exit button
        exit_button = Button(self, text="Exit", command=self.parent.destroy)
        exit_button.grid(row=5, column=3, pady=(0, 10), padx=10, columnspan=2)

        # Set the row and column to expand when user adjusts the screen size
        self.columnconfigure(2, weight=1)
        self.rowconfigure(4, weight=1)

    def clear_meal(self):
        self.directions_text.config(state="normal")
        self.directions_text.delete(1.0, END)
        self.directions_text.config(state="disabled")

    def load_meal(self, evt):
        """
            This method will populate the recipes names into a listbox.
            The recipe list filtered by category
        """

        try:  # Get the selected recipe from the recipe listbox
            index = int(self.meal_list_listbox.curselection()[0])

            # Get the recipe details
            name = self.meal_list_listbox.get(index)
            meal = requests.search_meals_by_name(name)

            # Clear existing meal directions before new is added
            self.clear_meal()

            # Add the directions for the meal
            self.directions_text.config(state="normal")
            self.directions_text.insert(END, meal.get_meal_instructions())
            self.directions_text.config(state="disabled")
        except IndexError:
            pass

    def load_meals(self, selected_category):
        """
            This method will populate the recipes names into a listbox.
            The recipe list filtered by category
        """

        # Clear all information from the listbox
        self.meal_list_listbox.selection_clear(0, END)
        self.meal_list_listbox.delete(0, END)

        # Get the list of meals from the site
        meals_list = requests.get_meals_by_category(selected_category)

        # Add the meals to the listbox
        for item in meals_list:
            self.meal_list_listbox.insert(END, item.get_meal_name())

        # Clear the meal description when a new category is selected
        self.clear_meal()

    def set_style(self):
        """
            This method creates a style to be used by the ttk widgets
        """

        style = ttk.Style(self.parent)
        style.theme_use('clam')
        style.configure('raised.TMenubutton', borderwidth=1, background="WHITE")


def main():
    """
        This method controls the main flow of the program
    """
    root = Tk()
    app = Recipes(root)
    app.parent.geometry("500x350")
    app.parent.title("My Recipe Program")
    root.mainloop()


if __name__ == '__main__':
    main()

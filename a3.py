from __future__ import annotations
import tkinter as tk
from tkinter import filedialog  # For masters task
from typing import Callable, Union, Optional
from a3_support import *
from model import *
from constants import *


class InfoBar(AbstractGrid):
    """
    The info bar at the last frame at the bottom of the main window which provides information.
    """

    def __init__(self, master: Union[tk.Tk, tk.Frame]) -> None:
        """
        Initializes the InfoBar.

        Parameters:
            master: The master frame for this InfoBar.
        """
        self.day = 1
        self.money = 0
        self.energy = 100

        # Initialize the AbstractGrid superclass
        super().__init__(master, (2, 3), (FARM_WIDTH + INVENTORY_WIDTH, INFO_BAR_HEIGHT))

        # Annotate the cell positions with their respective labels
        self.annotate_position(self.pixel_to_cell(0, 0), text=f'Day:', font=HEADING_FONT)
        self.annotate_position(self.pixel_to_cell(233, 0), text=f'Money:', font=HEADING_FONT)
        self.annotate_position(self.pixel_to_cell(466, 0), text=f'Energy:', font=HEADING_FONT)
        self.annotate_position(self.pixel_to_cell(0, 45), text=f'{self.day}', font=HEADING_FONT)
        self.annotate_position(self.pixel_to_cell(233, 45), text=f'${self.money}', font=HEADING_FONT)
        self.annotate_position(self.pixel_to_cell(466, 45), text=f'{self.energy}', font=HEADING_FONT)

    def redraw(self, day: int, money: int, energy: int) -> None:
        """
        Clears the InfoBar and redraws it to display the provided day, money, and energy.

        Parameters:
            day: The number of days elapsed in the game.
            money: The player's money.
            energy: The player's energy.
        """
        self.clear()
        self.day = day
        self.money = money
        self.energy = energy

        # Annotate the cell positions with updated values
        self.annotate_position(self.pixel_to_cell(0, 0), text=f'Day:', font=HEADING_FONT)
        self.annotate_position(self.pixel_to_cell(233, 0), text=f'Money:', font=HEADING_FONT)
        self.annotate_position(self.pixel_to_cell(466, 0), text=f'Energy:', font=HEADING_FONT)
        self.annotate_position(self.pixel_to_cell(0, 45), text=f'{self.day}', font=HEADING_FONT)
        self.annotate_position(self.pixel_to_cell(233, 45), text=f'${self.money}', font=HEADING_FONT)
        self.annotate_position(self.pixel_to_cell(466, 45), text=f'{self.energy}', font=HEADING_FONT)


class FarmView(AbstractGrid):
    """
    FarmView is a grid displaying the farm map, player, and plants.
    """
    map_file = []

    def __init__(
            self,
            master: tk.Tk | tk.Frame,
            dimensions: tuple[int, int],
            size: tuple[int, int],
            **kwargs
    ) -> None:
        """
        Sets up the FarmView to be an AbstractGrid with the appropriate dimensions and size,
        and creates an instance attribute of an empty dictionary to be used as an image cache.

        Parameters:
            master: The master frame for this FarmView.
            dimensions: The dimensions of the FarmView grid as (#rows, #columns).
            size: The size of the FarmView grid in pixels as (width, height).
        """
        super().__init__(master, dimensions, size, **kwargs)
        self.image_cache = {}

        # Creating initial state of Farm
        tile_list = FarmView.map_file
        for row in range(len(tile_list)):
            for col in range(len(tile_list[row])):
                tile = tile_list[row][col]
                image_name = f'Z:/Prateek/assign3/a3/images/{IMAGES[tile]}'
                image = get_image(image_name, self.get_cell_size(), self.image_cache)
                self.create_image(
                    self.get_midpoint((row, col)),
                    image=image,
                    anchor=tk.CENTER
                )
        # Creating the initial state of player image
        player_image_name = f'Z:/Prateek/assign3/a3/images/{IMAGES[DOWN]}'
        player_image = get_image(player_image_name, self.get_cell_size(), self.image_cache)
        self.create_image(
            self.get_midpoint((0, 0)),
            image=player_image,
            anchor=tk.CENTER
        )

    def redraw(
            self,
            ground: list[str],
            plants: dict[tuple[int, int], Plant],
            player_position: tuple[int, int],
            player_direction: str
    ) -> None:
        """
        Clears the farm view and then creates the images for the ground, plants, and player.
        The player and plants should render in front of the ground, and the player should render
        in front of the plants.

        Parameters:
            ground: The list of strings representing the tiles in the farm.
            plants: The dictionary of plant positions and their corresponding Plant objects.
            player_position: The position of the player on the farm.
            player_direction: The direction the player is facing.
        """

        self.clear()
        # Draw the ground tiles
        for row in range(len(ground)):
            for col in range(len(ground[row])):
                tile = ground[row][col]
                image_name = f'Z:/Prateek/assign3/a3/images/{IMAGES[tile]}'
                ground_image = get_image(image_name, self.get_cell_size(), self.image_cache)
                self.create_image(
                    self.get_midpoint((row, col)),
                    image=ground_image,
                    anchor=tk.CENTER
                )

        # Draw the plant images
        for position, plant in plants.items():
            image_name = get_plant_image_name(plant)
            plant_image = get_image(image_name, self.get_cell_size(), self.image_cache)
            self.create_image(
                self.get_midpoint(position),
                image=plant_image,
                anchor=tk.CENTER
            )

        # Draw the player image
        player_image_name = f'Z:/Prateek/assign3/a3/images/{IMAGES[player_direction]}'
        player_image = get_image(player_image_name, self.get_cell_size(), self.image_cache)
        self.create_image(
            self.get_midpoint(player_position),
            image=player_image,
            anchor=tk.CENTER
        )


class ItemView(tk.Frame):
    """
    A view for displaying information about an item.
    """

    def __init__(self, master: tk.Frame, item_name: str, amount: int,
                 select_command: Optional[Callable[[str], None]] = None,
                 sell_command: Optional[Callable[[str], None]] = None,
                 buy_command: Optional[Callable[[str], None]] = None) -> None:
        """
        Initialize the view with the given item name and amount, and optionally
        with select, sell, and buy commands.

        Parameter:
            master: The master frame for the item view.
            item_name: The name of the item.
            amount: The amount of the item.
            select_command: An optional command to run when the item is selected.
            sell_command: An optional command to run when the item is sold.
            buy_command: An optional command to run when the item is bought.
        """
        self.amount = amount

        background_color = INVENTORY_EMPTY_COLOUR if not amount else INVENTORY_COLOUR

        super().__init__(
            master,
            width=INVENTORY_WIDTH,
            background=background_color,
            highlightbackground=INVENTORY_OUTLINE_COLOUR,
            highlightthickness=1
        )
        self.item_name = item_name
        self.select_command = select_command
        self.sell_command = sell_command
        self.buy_command = buy_command
        # print(select_command)
        # Create a can
        # self.canvas = tk.Canvas(self.master)
        # Create a label to display the item name and amount.
        label_text = f'{self.item_name}: {self.amount}\nSell price: ${SELL_PRICES.get(item_name, "N/A")}\nBuy price: ${BUY_PRICES.get(item_name, "N/A")}'
        if not amount:
            self.label = tk.Label(self, text=label_text, background=INVENTORY_EMPTY_COLOUR)
            self.label.pack(side=tk.LEFT, fill="both")
        else:
            self.label = tk.Label(self, text=label_text, background=INVENTORY_COLOUR)
            self.label.pack(side=tk.LEFT, fill="both")

        # Create buttons for selecting, selling, and buying the item, if commands have been provided.
        self.label.bind("<Button-1>", lambda event: select_command(item_name))
        self.bind("<Button-1>", lambda event: select_command(item_name))

        # Creating the buttons
        if BUY_PRICES.get(item_name, 0):
            self.buy_button = tk.Button(self, text="Buy", command=self.buy_command)
            self.buy_button.pack(side=tk.LEFT, anchor=tk.E, padx=8, ipadx=4)
        self.sell_button = tk.Button(self, text="Sell", command=self.sell_command)
        self.sell_button.pack(side=tk.LEFT, anchor=tk.E, padx=8, ipadx=4)

    def update(self, amount: int, selected: bool = False) -> None:
        """
        Update the amount of the item displayed in the view.

        Parameters:
            amount: The new amount of the item.
            selected: Whether the item is currently selected.
        """
        self.amount = amount
        label_text = f'{self.item_name}: {self.amount}\nSell price: ${SELL_PRICES.get(self.item_name, "N/A")}\nBuy price: ${BUY_PRICES.get(self.item_name, "N/A")}'

        # Update the background color based on the amount and selected status.
        background_color = INVENTORY_EMPTY_COLOUR if not self.amount else INVENTORY_COLOUR

        # Update the label text.
        self.label.config(text=label_text, background=background_color)

        if selected and self.amount > 0:
            background_color = INVENTORY_SELECTED_COLOUR
            self.label.config(text=label_text, background=background_color)
        self.config(background=background_color)


class FarmGame:
    """
    FarmGame is the controller class for the overall game. The controller is responsible for creating and
    maintaining instances of the model and view classes, event handling, and facilitating communication between
    the model and view classes.
    """

    # initialize the game
    def __init__(self, master: tk.Tk, map_file: str) -> None:
        """
        Initialize the game with the given master widget and map file.

        Parameters:
            master: The master widget for the game.
            map_file: The file containing the farm map.
        """
        self.master = master
        self.map_file = map_file

        # Creating the cache instance for the image.
        self.cache = {}

        # Setting the title for the window.
        self.master.title("Farm Game")

        # Inserting the Image into the banner frame

        image_label = tk.Label(self.master, image=get_image('Z:/Prateek/assign3/a3/images/header.png',
                                                            (FARM_WIDTH + INVENTORY_WIDTH, BANNER_HEIGHT), self.cache))
        image_label.pack(side=tk.TOP)

        # Create the FarmModel instance.
        self.farm_model = FarmModel(self.map_file)

        # Create the instances of other view classes.
        # Creating the middle frame for farm view and inventory.
        middle_frame = tk.Frame(self.master, width=INVENTORY_WIDTH + FARM_WIDTH, height=FARM_WIDTH)
        middle_frame.pack(side=tk.TOP, fill=tk.BOTH)

        # Farm View instances
        FarmView.map_file = self.farm_model.get_map()
        self.farm_view = FarmView(middle_frame, self.farm_model.get_dimensions(), (FARM_WIDTH, FARM_WIDTH))
        self.farm_view.pack(side=tk.LEFT, anchor=tk.W)

        # Item View Class
        self.items_list = []
        for items in ITEMS:
            self.item_view = ItemView(middle_frame,
                                      items,
                                      self.farm_model.get_player().get_inventory().get(items, 0),
                                      select_command = lambda item_name=items: self.select_item(item_name) , 
                                      buy_command = lambda item_name=items: self.buy_item(item_name),
                                      sell_command = lambda item_name=items: self.sell_item(item_name))
            # print(items)
            self.item_view.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
            self.items_list.append(self.item_view)

        # Info Bar View Class
        self.info_bar = InfoBar(self.master)
        self.info_bar.pack(side=tk.TOP)

        # Command for next day button to increment days
        def next_day_command():
            self.farm_model.new_day()
            return self.redraw()

        # Create a button to enable users to increment the day.
        next_day_button = tk.Button(self.master, text="Next day", command=next_day_command)
        next_day_button.pack(side=tk.TOP)

        # Bind the handle keypress method to the '<Key>' event.
        self.master.bind("<KeyPress>", self.handle_keypress)

        # Command for loading the map from file menu
        def load_map_file():
            new_map_file = filedialog.askopenfilename(initialdir="maps",
                                                      title="Select map file",
                                                      filetypes=[("text file", "*.txt")])
            if new_map_file:
                self.master.destroy()  # Destroy the current window
                root = tk.Tk()  # Create root window
                farm_game = FarmGame(root, new_map_file)  # Start new game with new map
                root.mainloop()  # Run the new game loop

        #  Create the file menu
        menu_bar = tk.Menu(self.master)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Quit", command=self.master.quit)
        file_menu.add_command(label="Map Selection", command=load_map_file)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.master.config(menu=menu_bar)

        # Call the redraw method to ensure the view draws according to the current model state.
        self.redraw()

    def redraw(self) -> None:
        """
        Redraws the entire game based on the current model state.
        """
        self.farm_view.redraw(self.farm_model.get_map(),
                              self.farm_model.get_plants(),
                              self.farm_model.get_player().get_position(),
                              self.farm_model.get_player().get_direction())

        # selected_item = self.farm_model.get_player().get_selected_item()
        # if selected_item is not None:
        #     for index, item in enumerate(ITEMS):
        #         self.items_list[index].update(self.farm_model.get_player().get_inventory().get(item, 0),
        #                                       selected=True)
        for index, item in enumerate(ITEMS):
            self.items_list[index].update(self.farm_model.get_player().get_inventory().get(item, 0))

        self.info_bar.redraw(day=self.farm_model.get_days_elapsed(),
                             money=self.farm_model.get_player().get_money(),
                             energy=self.farm_model.get_player().get_energy())

    def handle_keypress(self, event: tk.Event) -> None:
        """
        An event handler to be called when a keypress event occurs.

        Parameters:
            event: The event object.
        """
        key = event.keysym.lower()
        # Movement key events are handled
        if key == "w":
            self.farm_model.move_player(UP)
            self.redraw()
        elif key == "a":
            self.farm_model.move_player(LEFT)
            self.redraw()
        elif key == "s":
            self.farm_model.move_player(DOWN)
            self.redraw()
        elif key == "d":
            self.farm_model.move_player(RIGHT)
            self.redraw()

        # Plant the selected item
        elif key == "p":
            player = self.farm_model.get_player()
            inventory = player.get_inventory()
            position = player.get_position()
            row, col = position
            map_file = self.farm_model.get_map()
            selected_item = player.get_selected_item()
            # selected_item = "Potato Seed"

            # index = 0
            # for indx, item in enumerate(ITEMS):
            #     if item == selected_item:
            #         index = indx

            if selected_item is not None and len(selected_item.split()) == 2 and map_file[row][col] == SOIL and inventory.get(selected_item, 0):
                self.farm_model.add_plant(self.farm_model.get_player_position(),
                                          globals()[selected_item.split()[0] + 'Plant']())
                player.remove_item((selected_item, 1))
                # selected_item = None
                # self.items_list[index].update(inventory.get(selected_item, 0), selected=True)
            self.redraw()

        # Harvest the plant
        elif key == "h":
            player = self.farm_model.get_player()
            position = player.get_position()
            harvest_result = self.farm_model.harvest_plant(position)
            # If harvest is successful
            if harvest_result:
                player.add_item(harvest_result)
            self.redraw()

        # Remove the plant
        elif key == "r":
            player = self.farm_model.get_player()
            position = player.get_position()
            self.farm_model.remove_plant(position)
            self.redraw()

        # Till the Soil
        elif key == "t":
            self.farm_model.till_soil(self.farm_model.get_player_position())
            self.redraw()

        # Untill the Soil
        elif key == "u":
            self.farm_model.untill_soil(self.farm_model.get_player_position())
            self.redraw()

    def select_item(self, item_name: str) -> None:
        """
        The callback to be given to each ItemView for item selection.

        Parameters:
            item_name: The name of the item that was selected.
        """
        # print(item_name)

        # temp = self.farm_model.get_player()._selected_item

        self.farm_model.get_player().select_item(item_name)

        # NAME = self.farm_model.get_player()._selected_item
        #  print(NAME)
        index = 0
        for indx, item in enumerate(ITEMS):
            if item == item_name:
                index = indx
                self.items_list[index].update(self.farm_model.get_player().get_inventory().get(item_name, 0), selected=True)
        # self.redraw()

    def buy_item(self, item_name: str) -> None:
        """
        Attempt to buy the item with the given item name, at the price specified in BUY_PRICES, and then
        redraw the view.

        Parameters:
            item_name: The name of the item to buy.
        """
        price = BUY_PRICES.get(item_name, 0)
        if price != 0:
            self.farm_model.get_player().buy(item_name, price)
        self.redraw()

    def sell_item(self, item_name: str) -> None:
        """
        Attempt to sell the given item, and then redraw the view.

        Parameters:
            item_name: The name of the item to sell.
        """
        price = SELL_PRICES[item_name]
        self.farm_model.get_player().sell(item_name, price)
        self.redraw()


def play_game(root: tk.Tk, map_file: str) -> None:
    """

    Parameters:
        root:
        map_file:
    """
    farm_game = FarmGame(root, map_file)
    farm_game.item_view
    root.mainloop()


def main() -> None:
    root = tk.Tk()
    map_file = 'Z:/Prateek/assign3/a3/maps/map1.txt'
    return play_game(root, map_file)


if __name__ == '__main__':
    main()

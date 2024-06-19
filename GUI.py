import tkinter as tk
from tkinter import ttk
import json
from BBS_Helper import by_character as get_character_guide
from BBS_Helper import get_unique_ingredients,CRYSTALS,by_command_ingredient,get_other_ingredient,get_meld,get_type,get_ability
import logging

logging.basicConfig(level=logging.INFO)


class BBS_Guide:
    def __init__(self) -> None:
        self.setup()
        self.root.mainloop()

    def setup_data(self) -> None:
        self.guide_data = json.load(open("BBS_MELDING_GUIDE.json"))
        self.temp_data = [] #took out this
        self.temp_data2 = [] #took out this

    def setup_window(self) -> None:
        self.root = tk.Tk()
        self.root.title("KHBBS Utility")
        self.root.geometry("800x600")
        
    def setup_frames(self) -> None:
        self.character_frame = tk.Frame(self.root)
        self.command_frame = tk.Frame(self.root)
        self.command_selection_frame = tk.Frame(self.command_frame)
        self.command_options_frame = tk.Frame(self.command_frame)
        self.results_frame = tk.Frame(self.root)
        self.frame4 = tk.Frame(self.root) #took this out

    def setup_widges(self) -> None:
            #Frame 1: Character Selection
        self.character_label = tk.Label(self.character_frame, text="Character: ") 
        self.character_selection = ttk.Combobox(self.character_frame, values=["Any","Terra","Ventus","Aqua"])
        self.character_selection.bind("<<ComboboxSelected>>", self.on_character_selection)
            #Frame 2
        self.command1_label = tk.Label(self.command_selection_frame, text="Command 1: ",width=20)
        self.command2_label = tk.Label(self.command_selection_frame, text="Command 2: ",width=20)
        self.crystal_type_label = tk.Label(self.command_selection_frame, text="Crystal Type: ",width=20)

        self.command1_dropdown = ttk.Combobox(self.command_options_frame,width=20,values=get_unique_ingredients(self.guide_data))
        self.command1_dropdown.bind("<<ComboboxSelected>>", self.on_command_selection)
        self.command2_dropdown = ttk.Combobox(self.command_options_frame,width=20,values=get_unique_ingredients(self.guide_data))
        self.command2_dropdown.bind("<<ComboboxSelected>>", self.on_command_selection)
        self.crystal_type_dropdown = ttk.Combobox(self.command_options_frame,width=20,values=CRYSTALS)
        self.crystal_type_dropdown.bind("<<ComboboxSelected>>", self.on_crystal_selection)
            #Frame 3
        self.meld_result_label = tk.Label(self.results_frame, text="Meld Result: ")
        self.result_var = tk.StringVar()
        self.meld_result = tk.Label(self.results_frame,width=12,height=1,textvariable=self.result_var,background="lightgrey")
        self.meld_type_label = tk.Label(self.results_frame, text="Meld Type: ")
        self.result_type_var = tk.StringVar()
        self.meld_type = tk.Label(self.results_frame,width=5,height=1,textvariable=self.result_type_var,background="lightgrey")
        self.ability_label = tk.Label(self.results_frame, text="Ability: ")
        self.result_ability_var = tk.StringVar()
        self.ability = tk.Label(self.results_frame,width=20,height=1,textvariable=self.result_ability_var,background="lightgrey")

    def on_character_selection(self, event) -> None:
        character = event.widget.get()
        print(f"selected {character}")
        self.guide_data = get_character_guide(character)
        self.clear_dropdowns()
        self.update_dropdowns()

    def on_command_selection(self, event) -> None:
        command = event.widget.get()
        print(f"selected {command}")
        if command:
            print("I'm a command")
                # if it's a command restrict the other dropdown to the ingredients that can be used with the selected command 
            self.update_other_dropdown(event.widget,command)
        else:
            print("I'm not a command")
            self.update_self_dropdown(event.widget)

    def on_crystal_selection(self, event) -> None:
        crystal = event.widget.get()
        print(f"selected {crystal}")     
        self.result_ability_var.set(get_ability(crystal,self.result_type_var.get()))

    def update_self_dropdown(self, dropdown):
        print(f"update_self_dropdown: starting with dropdown={dropdown}")

        if dropdown == self.command1_dropdown:
            other_dropdown = self.command2_dropdown
            other_command = self.command2_dropdown.get()
            print(f"update_self_dropdown: other_dropdown={other_dropdown}, other_command={other_command}")
        elif dropdown == self.command2_dropdown:
            other_dropdown = self.command1_dropdown
            other_command = self.command1_dropdown.get()
            print(f"update_self_dropdown: other_dropdown={other_dropdown}, other_command={other_command}")

        if other_command:
            self.guide_data = get_character_guide(self.character_selection.get())
            dropdown['values'] = self.get_other_ingredients(other_command, self.guide_data)
            print(f"update_self_dropdown: dropdown['values']={dropdown['values']}")

            other_dropdown['values'] = get_unique_ingredients(get_character_guide(self.character_selection.get()))
            print(f"update_self_dropdown: other_dropdown['values']={other_dropdown['values']}")



    def update_other_dropdown(self, dropdown, command):
        print(f"update_other_dropdown: dropdown={dropdown}, command={command}")

        if dropdown == self.command1_dropdown:
            print("update_other_dropdown: updating command2_dropdown")
            #I want to update the other dropdown according to the selected command
            self.update_command_dropdown(self.command2_dropdown,command)
        elif dropdown == self.command2_dropdown:
            print("update_other_dropdown: updating command1_dropdown")
            self.update_command_dropdown(self.command1_dropdown,command)



    def update_command_dropdown(self, dropdown, command):
        other_command = self.get_other_command(dropdown)
        if not command and not other_command:
            dropdown['values'] = self.get_other_ingredients(other_command, self.guide_data)
        elif other_command:
            result = get_meld(command, other_command)
            self.result_var.set(result)
            result = get_type(command, other_command)
            self.result_type_var.set(result)
            self.result_ability_var.set(get_ability(self.crystal_type_dropdown.get(),self.result_type_var.get()))
            dropdown['values'] = ['']
        else:
            dropdown['values'] = self.get_other_ingredients(command, self.guide_data)
    
    def get_other_command(self,dropdown):
        if dropdown.get():
            return dropdown.get()
        else:
            return None
        
    def get_other_ingredients(self,command, guide_data):
        return sorted(get_other_ingredient(command, by_command_ingredient(command, guide_data)))

    def clear_dropdowns(self) -> None:
        self.command1_dropdown.set(value="")
        self.command2_dropdown.set(value="")
        self.crystal_type_dropdown.set(value="")
        self.result_var.set(value="")
        self.result_type_var.set(value="")
        self.result_ability_var.set(value="")
        

    def update_dropdowns(self) -> None:
        self.command1_dropdown['values'] = get_unique_ingredients(self.guide_data)
        self.command2_dropdown['values'] = get_unique_ingredients(self.guide_data)

    def reset_dropdowns(self) -> None:
        self.command1_dropdown['values'] = get_unique_ingredients(get_character_guide(self.character_selection.get()))
        self.command2_dropdown['values'] = get_unique_ingredients(get_character_guide(self.character_selection.get()))

    def layout(self) -> None:
        self.character_frame.pack()
        self.command_frame.pack()
        self.command_selection_frame.pack(side=tk.TOP)
        self.command_options_frame.pack(side=tk.TOP)
        self.results_frame.pack()
        self.frame4.pack()

        self.character_label.pack(side=tk.LEFT)
        self.character_selection.pack(side=tk.LEFT)
        self.command1_label.pack(side=tk.LEFT)
        self.command2_label.pack(side=tk.LEFT)
        self.crystal_type_label.pack(side=tk.LEFT)

        self.command1_dropdown.pack(side=tk.LEFT,padx=10)
        self.command2_dropdown.pack(side=tk.LEFT,padx=10)
        self.crystal_type_dropdown.pack(side=tk.LEFT,padx=10)

        self.meld_result_label.pack(side=tk.LEFT)
        self.meld_result.pack(side=tk.LEFT,padx=10)
        self.meld_type_label.pack(side=tk.LEFT)
        self.meld_type.pack(side=tk.LEFT,padx=10)
        self.ability_label.pack(side=tk.LEFT)
        self.ability.pack(side=tk.LEFT,padx=10)


    def setup(self) -> None:
        self.setup_data()
        self.setup_window()
        self.setup_frames()
        self.setup_widges()
        self.layout()


BBS_Guide()
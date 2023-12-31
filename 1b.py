import tkinter as tk
import random
from PIL import Image, ImageTk
from tkinter import OptionMenu,messagebox

# offensive skills
def pierce_shot(target): 
    return [20 + target.dp,"Evasion"]
def fireball(target): 
    return [30,"Fireball"]
def shield_bash(target):  
    return [23,"Shield Bash"]
def claw_swipe(target):  
    return [23,"Claw Swipe"]
# defensive skills 
def evasion(user): 
    user.temp_dp += 5
def ice_barrier(user):
    user.temp_dp += 5
def shield_of_valor(user):  
    user.temp_dp += 10
def regen(user):
    user.hp += 15

CHARACTERS = ["archer", "wizard", "knight", "werewolf"]
CHAR_ATTR = {
    "archer": [10, 1, 3, 10, [pierce_shot, evasion, "pierce_shot", "evasion"], "./images/archer.jpg"],
    "wizard": [15, 2, 2, 20, [fireball, ice_barrier, "fireball", "ice_barrier"], "./images/wizard.jpg"],
    "knight": [12, 3, 1, 25, [shield_bash, shield_of_valor, "shield_bash", "shield_of_valor"], "./images/knight.jpg"],
    "werewolf": [13, 2, 2, 30, [claw_swipe, regen, "claw_swipe", "regen"], "./images/werewolf.jpg"]
}
player_team = []
enemy_team = []
round = 0
one_downed = False

class Character:
    def __init__(self,jobClass):
        self.hp = 150 # +50 hp handicap for the enemy for not being able to defend or use skill
        if jobClass in CHAR_ATTR:
            self.ap, self.dp, self.sp, self.crital_chance, self.skill, self.image = CHAR_ATTR[jobClass]
        self.jobClass = jobClass
        
    def attack(self, target):
        chance = random.randint(1, 100)
        critical_damage = 0
        if chance <= self.crital_chance:
            critical_damage += random.randint(2,5)
        # When dp is higher than ap, there would be no damage
        damage = self.ap + critical_damage
        armour = target.dp
        if isinstance(target, PlayerCharacter): # only if the target is player
            armour = target.temp_dp
        effective_damage = max(damage - armour, 0)
        target.receive_damage(effective_damage)

    def receive_damage(self, damage):   
        self.hp -= damage
    
    def reset_enemy(self):
        self.hp = 150

class PlayerCharacter(Character):
    def __init__(self,jobClass):
        super().__init__(jobClass)
        self.hp = 100
        self.mp = 4
        self.temp_dp = self.dp
        self.got_attacked = False

    def defend(self):
        self.temp_dp += 8
    
    def reset_temp_dp(self):
        if self.got_attacked:  # reset temp_dp only if the player got attacked
            self.temp_dp = self.dp
        self.got_attacked = False

    def use_skill(self,skill_type,target):
        if skill_type == 0: # offensive
            self.mp -= 1
            damage,skill_name = self.skill[0](target)
            target.receive_damage(damage)
            print(f"{self.jobClass.capitalize()} used {skill_name} and dealt {damage} damage")
        else: # defensive
            self.mp -= 2 # will only have 2 chance to use to make the game more balenced
            self.skill[1](self)

    def reset_player(self):
        self.hp = 100
        self.mp = 4

def switch_frame(show_frame, forget_frame):
    show_frame.grid(row=0,column=0)
    forget_frame.grid_forget()

def select_heroes():
    selected_heroes = []
    if archer_var.get():
        selected_heroes.append("archer")
    if wizard_var.get():
        selected_heroes.append("wizard")
    if knight_var.get():
        selected_heroes.append("knight")
    if werewolf_var.get():
        selected_heroes.append("werewolf")
    
    if len(selected_heroes) == 2:
        for player in selected_heroes:
            player_team.append(PlayerCharacter(player))
        remaining_options = list(set(CHARACTERS)-set(selected_heroes))
        enemy1 = Character(remaining_options[0])
        enemy2 = Character(remaining_options[1])
        global enemy_team
        enemy_team = [enemy1,enemy2]
        combat_screen = create_combat_screen(player_team, enemy_team)
        switch_frame(combat_screen, main_screen)
    elif len(selected_heroes) != 2:
        messagebox.showerror("Error","Please select two characters")

def limit_checkbox_selection():
    selected_count = sum([archer_var.get(), wizard_var.get(), knight_var.get(), werewolf_var.get()])
    if selected_count > 2:
        if archer_var.get():
            archer_var.set(False)
        elif wizard_var.get():
            wizard_var.set(False)
        elif knight_var.get():
            knight_var.set(False)
        elif werewolf_var.get():
            werewolf_var.set(False)

root = tk.Tk()
root.title("Turn-Based RPG")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

main_screen = tk.Frame(root)
main_screen.grid(row=0, column=0)

settings_button = tk.Button(main_screen, text="Settings", command=lambda: switch_frame(setting_screen, main_screen))
settings_button.grid(row=8, column=0, sticky="nsew", columnspan=3, padx=2)

quit_button = tk.Button(main_screen, text="Quit", command=root.destroy)
quit_button.grid(row=9, column=0, sticky="nsew", columnspan=3, padx=2)

title = tk.Label(main_screen, text="A Hero Adventure", font=("time new roman", 20))
title.grid(row=1, column=0, sticky="nsew", columnspan=3)

select_label = tk.Label(main_screen, text="Select 2 heroes to start:")
select_label.grid(row=2, column=0, sticky="nsew", columnspan=3)

archer_var = tk.BooleanVar()
wizard_var = tk.BooleanVar()
knight_var = tk.BooleanVar()
werewolf_var = tk.BooleanVar()

archer_image = Image.open("./images/archer.jpg").resize((150,150))
archer_image = ImageTk.PhotoImage(archer_image)
wizard_image = Image.open("./images/wizard.jpg").resize((150,150))
wizard_image = ImageTk.PhotoImage(wizard_image)
knight_image = Image.open("./images/knight.jpg").resize((150,150))
knight_image = ImageTk.PhotoImage(knight_image)
werewolf_image = Image.open("./images/werewolf.jpg").resize((150,150))
werewolf_image = ImageTk.PhotoImage(werewolf_image)

archer_label = tk.Label(main_screen, image=archer_image)
archer_label.grid(row=3, column=0, padx=10)
archer_checkbox = tk.Checkbutton(main_screen, text="Archer", variable=archer_var, command=limit_checkbox_selection)
archer_checkbox.grid(row=4, column=0, padx=10)

wizard_label = tk.Label(main_screen, image=wizard_image)
wizard_label.grid(row=3, column=1, padx=10)
wizard_checkbox = tk.Checkbutton(main_screen, text="Wizard", variable=wizard_var, command=limit_checkbox_selection)
wizard_checkbox.grid(row=4, column=1, padx=10)

knight_label = tk.Label(main_screen, image=knight_image)
knight_label.grid(row=5, column=0, padx=10)
knight_checkbox = tk.Checkbutton(main_screen, text="Knight", variable=knight_var, command=limit_checkbox_selection)
knight_checkbox.grid(row=6, column=0, padx=10)

werewolf_label = tk.Label(main_screen, image=werewolf_image)
werewolf_label.grid(row=5, column=1, padx=10)
werewolf_checkbox = tk.Checkbutton(main_screen, text="Werewolf", variable=werewolf_var, command=limit_checkbox_selection)
werewolf_checkbox.grid(row=6, column=1, padx=10)

submit_button = tk.Button(main_screen, text="Select Heroes", command=select_heroes)
submit_button.grid(row=7, column=0, sticky="nsew", columnspan=3)

main_screen.grid_rowconfigure(0, weight=1)
main_screen.grid_rowconfigure(1, weight=1)
main_screen.grid_rowconfigure(2, weight=1)

main_screen.grid_columnconfigure(0, weight=1)
main_screen.grid_columnconfigure(1, weight=1)
main_screen.grid_columnconfigure(2, weight=1)

# Setting
setting_screen = tk.Frame(root)

setting_label = tk.Label(setting_screen, text = "Settings")
setting_label.grid(row = 0, column = 4)

audio_label = tk.Label(setting_screen, text = "Audio")
audio_label.grid(row = 1, column = 1)

v = tk.IntVar()
tk.Radiobutton(setting_screen, text="On", variable=v, value=1).grid(row = 1, column = 4,sticky="nsew")
tk.Radiobutton(setting_screen, text="Off", variable=v, pady = 10, value=2).grid(row = 1, column = 5)

language_label = tk.Label(setting_screen, text = "Language")
language_label.grid(row = 2, column = 1)        

options = ["English", "Chinese", "Malay"]

variable = tk.StringVar()
variable.set(options[0])

drop = OptionMenu( setting_screen ,variable, *options )
drop.grid(row = 2, column = 4)

scale_label = tk.Label(setting_screen, text = "Difficulties")
scale_label.grid(row = 3, column = 1)  
difficult_scale = tk.Scale(setting_screen, from_=1, to=3,tickinterval=10, orient=tk.HORIZONTAL)
difficult_scale.grid(row = 3, column = 4)

back_button = tk.Button(setting_screen, text="Back", command=lambda: switch_frame(main_screen, setting_screen))
back_button.grid(row = 5, column = 4)

# Combat Screen
def create_combat_screen(pteam, eteam):
    global player, enemy  # Declare player and enemy as global

    player = pteam[0]
    enemy = eteam[0]
    global one_downed

    def attack():
        global round
        round += 1
        if player.sp >= enemy.sp:
            player.attack(enemy)
            if enemy.hp > 0:
                enemy.attack(player)
        else:
            enemy.attack(player)
            if player.hp > 0:
                player.attack(enemy)
        check_hp(player, enemy)

    def defend():
        global round
        round += 1
        player.defend()
        enemy.attack(player)
        check_hp(player, enemy)

    def use_skill1():
        global round
        round += 1
        if player.sp >= enemy.sp:
            if player.mp <= 0:
                round -= 1
                messagebox.showwarning("Skill Usage", "Not enought MP")
            else:
                player.use_skill(0,enemy)
                if player.hp > 0:
                    enemy.attack(player)
        else:
            enemy.attack(player)
            if player.hp > 0:
                if player.mp <= 0:
                    round -= 1
                    messagebox.showwarning("Skill Usage", "Not enought MP")
                else:
                    player.use_skill(0,enemy)
        check_hp(player, enemy)
    
    def use_skill2():
        global round
        round += 1
        if player.sp >= enemy.sp:
            if player.mp <= 1:
                round -= 1
                messagebox.showwarning("Skill Usage", "Not enought MP")
            else:
                player.use_skill(1,enemy)
                if enemy.hp > 0:
                    enemy.attack(player)
        else:
            enemy.attack(player)
            if player.hp > 0:
                if player.mp <= 1:
                    round -= 1
                    messagebox.showwarning("Skill Usage", "Not enought MP")
                else:
                    player.use_skill(1,enemy)
        check_hp(player, enemy)

    def check_hp(p,e):
        global one_downed, player, enemy, player_team, enemy_team
        update_stats(p,e)
        if p.hp <= 0 and p in player_team:
            one_downed = True
            player_team.remove(p)
            if len(player_team) == 1:
                new_hero = player_team[0]
                player = new_hero
                update_stats(new_hero,e)
                print(f"Your second fighter {new_hero.jobClass} came in")
            if len(player_team) == 0:
                messagebox.showinfo("Info","You Lost!!!")
                root.quit()
        if e.hp <= 0 and e in enemy_team:
            one_downed = True
            enemy_team.remove(e)
            if len(enemy_team) == 1:
                new_enemy = enemy_team[0]
                enemy = new_enemy
                update_stats(p,new_enemy)
                print(f"Second fighter {new_enemy.jobClass} came in")
            if len(enemy_team) == 0:
                messagebox.showinfo("Info","Congrats, You Won!")
                root.quit()

    def restart():
        global player, enemy
        player.reset_player()
        enemy.reset_enemy()
        switch_frame(main_screen,combat_screen)

    combat_screen = tk.Frame(root)

    label = tk.Label(combat_screen, text="Combat")
    label.grid(row=0, column=6, sticky="nsew")

    round_label = tk.Label(combat_screen, text="")
    round_label.grid(row=1, column=6,sticky="nsew")

    restart_button = tk.Button(combat_screen, text="Restart", command=lambda: restart())
    restart_button.grid(row=18, column=6, sticky="nsew", pady=5)
    
    player_image = Image.open(player.image).resize((150, 150))
    player_image = ImageTk.PhotoImage(player_image)
    player_image_label = tk.Label(combat_screen, image=player_image)
    player_image_label.image = player_image  # Store a reference to the PhotoImage
    player_image_label.grid(row=3, column=2, sticky="nsew")

    enemy_image = Image.open(enemy.image).resize((150, 150))
    enemy_image = ImageTk.PhotoImage(enemy_image)
    enemy_image_label = tk.Label(combat_screen, image=enemy_image)
    enemy_image_label.image = enemy_image  # Store a reference to the PhotoImage
    enemy_image_label.grid(row=3, column=12, sticky="nsew")

    result_label = tk.Label(combat_screen, text="Game Started")
    result_label.grid(row=6, column=6, sticky="nsew")

    # Player stats
    player_hp_label = tk.Label(combat_screen, text=f"HP: {player.hp}/100")
    player_hp_label.grid(row=7, column=2, sticky="nsew")

    player_ap_label = tk.Label(combat_screen, text=f"AP: {player.ap}")
    player_ap_label.grid(row=8, column=2, sticky="nsew")

    player_dp_label = tk.Label(combat_screen, text=f"DP: {player.dp}")
    player_dp_label.grid(row=9, column=2, sticky="nsew")

    player_sp_label = tk.Label(combat_screen, text=f"SP: {player.sp}")
    player_sp_label.grid(row=10, column=2, sticky="nsew")

    player_mp_label = tk.Label(combat_screen, text=f"MP: {player.mp}/4")
    player_mp_label.grid(row=11, column=2, sticky="nsew")

    # Enemy stats
    enemy_hp_label = tk.Label(combat_screen, text=f"HP: {enemy.hp}/150")
    enemy_hp_label.grid(row=7, column=12, sticky="nsew")

    enemy_ap_label = tk.Label(combat_screen, text=f"AP: {enemy.ap}")
    enemy_ap_label.grid(row=8, column=12, sticky="nsew")

    enemy_dp_label = tk.Label(combat_screen, text=f"DP: {enemy.dp}")
    enemy_dp_label.grid(row=9, column=12, sticky="nsew")

    enemy_sp_label = tk.Label(combat_screen, text=f"SP: {enemy.sp}")
    enemy_sp_label.grid(row=10, column=12, sticky="nsew")

    def update_stats(p,e):
        player_hp_label.config(text=f"HP: {p.hp}/100")
        player_mp_label.config(text=f"MP: {p.mp}/4")
        # result_label.config(text=f""+e.name+" Appeared!")

        round_label.config(text=f"Round: {round}")

        enemy_hp_label.config(text=f"HP: {e.hp}/150")
        global one_downed 
        if one_downed:
            player_image = Image.open(p.image).resize((150, 150))
            player_image = ImageTk.PhotoImage(player_image)
            player_image_label = tk.Label(combat_screen, image=player_image)
            player_image_label.image = player_image  # Store a reference to the PhotoImage
            player_image_label.grid(row=3, column=2, sticky="nsew")

            enemy_image = Image.open(e.image).resize((150, 150))
            enemy_image = ImageTk.PhotoImage(enemy_image)
            enemy_image_label = tk.Label(combat_screen, image=enemy_image)
            enemy_image_label.image = enemy_image  # Store a reference to the PhotoImage
            enemy_image_label.grid(row=3, column=12, sticky="nsew")

            player_ap_label.config(text=f"AP: {p.ap}")
            player_dp_label.config(text=f"DP: {p.dp}")
            player_sp_label.config(text=f"SP: {p.sp}")

            enemy_ap_label.config(text=f"AP: {e.ap}")
            enemy_dp_label.config(text=f"DP: {e.dp}")
            enemy_sp_label.config(text=f"SP: {e.sp}")

            skill_button = tk.Button(combat_screen, text=f"{p.skill[2]} 1 MP", command=use_skill1)
            skill_button.grid(row=15, column=2, sticky="nsew")

            skill_2_button = tk.Button(combat_screen, text=f"{p.skill[3]} 2 MP", command=use_skill2)
            skill_2_button.grid(row=16, column=2, sticky="nsew")

        one_downed = False

    # Actions
    attack_button = tk.Button(combat_screen, text="Attack", command=attack)
    attack_button.grid(row=13, column=2, sticky="nsew")

    defend_button = tk.Button(combat_screen, text="Defend", command=defend)
    defend_button.grid(row=14, column=2, sticky="nsew")

    skill_button = tk.Button(combat_screen, text=f"{player.skill[2]} 1 MP", command=use_skill1)
    skill_button.grid(row=15, column=2, sticky="nsew")

    skill_2_button = tk.Button(combat_screen, text=f"{player.skill[3]} 2 MP", command=use_skill2)
    skill_2_button.grid(row=16, column=2, sticky="nsew")

    return combat_screen

root.mainloop()
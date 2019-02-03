from classes.game import Person, bcolors
from classes.inventory import Item
from classes.magic import Spell
import random


# Create Black Magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 10, 100, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")


# Create some items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 50)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 99999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 99999)

firestone = Item("Firestone", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, cure]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": firestone, "quantity": 5}]

# Instantiate people
player1 = Person("Saro:",3460, 99, 360, 34, player_spells, player_items)
player2 = Person("Sato:", 3460, 95, 260, 34, player_spells, player_items)
player3 = Person("Sabo:",4620, 95, 300, 34, player_spells, player_items)


enemy2 = Person("Imp  ", 1250, 130, 560, 325, enemy_spells, [])
enemy1 = Person("Magus", 31200, 65, 527, 25, enemy_spells, [])
enemy3 = Person("Imp  ", 1250, 130, 560, 325, enemy_spells, [])



players = [player1, player2, player3]
enemies = [enemy2, enemy1, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("===================================")

    print("NAME                            HP                          MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    print("\n")

    for player in players:

        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "")  + " for", dmg, "point of damage.")

            if enemies[enemy].get_hp() == 0:
                print((enemies[enemy].name.replace(" ", "") + " has died."))
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("\n    Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
                print(bcolors.OKBLUE + "----------------------------" + bcolors.ENDC)
            elif spell.type == "black":

                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print((enemies[enemy].name.replace(" ", "")  + " has died."))
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("\n    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC + "\n")

            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp

                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " full restores HP/MP" + bcolors.ENDC)

            elif item.type == "attack":

                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to " + enemies[enemy].name.replace(" ", "")  + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print((enemies[enemy].name.replace(" ", "")  + " has died."))
                    del enemies[enemy]

        else:
            print("That isn't an option...")
            continue
    #check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    #check if player won
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if defeated_enemies == 3:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False


    #check if enemy won
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_players == 3:
        print(bcolors.FAIL + "IN THE END, THE FUTURE REFUSED TO CHANGE..." + bcolors.ENDC)
        running = False

    print("\n")
    #enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0,2)

        #chose attack
        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)

            print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + "for", enemy_dmg)


        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals " + enemy.name + " for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":

                target = random.randrange(0, 3)

                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + enemy.name.replace(" ", "") + "'s " + spell.name + " deals " + str(magic_dmg), "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print((players[target].name.replace(" ", "") + " has died."))
                    del players[player]

            #print("Enemy chose", spell, "damage is: ", magic_dmg)

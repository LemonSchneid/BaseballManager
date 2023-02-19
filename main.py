
import player
import team
import names
import random
import ball_diamond


FIELDER_RANGE = 3
OUTFIELD_SPEED_PENALTY = 1


def reset_count():
    global strikes, balls
    strikes = 0
    balls = 0


def player_range(player1):
    if player1.speed == 1:
        player1.speed = 2
        player1_range = (player1.speed - OUTFIELD_SPEED_PENALTY) * 10
        return player1_range
    else:
        player1_range = (player.speed - OUTFIELD_SPEED_PENALTY) * 10
        return player1_range


def is_inning_over():
    global batter, starting_pitcher, outs, runs, top_of_inning, inning, playing_offense, playing_defense, game_over
    if outs == 3:
        playing_offense.score += runs
        if top_of_inning and inning == 9 and playing_defense.score > playing_offense.score:
            print(f'Game Over. {playing_defense.team_name} wins. Final Score:\n'
                  f'{playing_defense.team_name}: {playing_defense.score}\n'
                  f'{playing_offense.team_name}: {playing_offense.score}')
            game_over = True
        if not top_of_inning and inning == 9:
            if playing_defense.score == playing_offense.score:
                winner = "Tie Game!"
                game_over = True
            elif playing_offense.score > playing_defense.score:
                winner = f'{playing_offense} wins'
            else:
                winner = f'{playing_defense} wins'

            print(f'Game Over. {winner}. Final Score: \n{playing_offense.team_name}: {playing_offense.score},\n'
                  f'{playing_defense.team_name}: {playing_defense.score}')
            game_over = True
        else:

            # switches which team is playing offense and which team is playing defense.
            print("\nInning over!\n")
            print(f"team {playing_offense.team_name} scored {runs} this inning. \n"
                  f"Total score:\n "
                  f"{playing_offense.team_name}: {playing_offense.score},\n"
                  f"{playing_defense.team_name}: {playing_defense.score}\n")
            inning_switch_storage = playing_offense
            playing_offense = playing_defense
            playing_defense = inning_switch_storage
            batter = playing_offense.roster[playing_offense.batting_index]
            starting_pitcher = pitcher(playing_defense.roster)
            outs = 0
            runs = 0

            print(f"Team {playing_defense.team_name} takes the field. "
                  f"Team {playing_offense.team_name} is at the sticks.\n")

            if top_of_inning:
                top_of_inning = False
                start_inning()

            elif not top_of_inning:
                # print(f"Top of inning {inning}\n")
                top_of_inning = True
                inning += 1
                start_inning()

        return True

    return False


def start_inning():
    if top_of_inning:
        top_or_bottom = "Top"

    else:
        top_or_bottom = "Bottom"

    print(f"{top_or_bottom} of inning {inning}\n")
    print(f"Starting pitcher for The {playing_defense.team_name} is {starting_pitcher.name}")
    print(f"throw power: {starting_pitcher.throwing_power} "
          f"throw accuracy: {starting_pitcher.throwing_accuracy}\n")

    print(f"First up for Team {playing_offense.team_name} is {batter.name}")
    print(f"Speed: {batter.speed}, hand eye: {batter.hand_eye}\n")
    print(input("ready for first batter?: "))


def pitcher(team_roster):
    for player1 in team_roster:
        if player1.position_name == 'pitcher':
            team1_pitcher = player1
            return team1_pitcher


def ball_contact():
    in_field = [15, 15]
    home_run = [32, 36]
    y = random.randint(0, 34)
    x = random.randint(0, 38)
    ball_location = [y, x]
    print(f'ball location: {ball_location}')
    # is it a home run?
    if y >= home_run[0] or x >= home_run[1]:
        print('Home Run!')
        contact = ['home run', ball_location]
        return contact

    elif y <= in_field[0] and x <= in_field[1]:
        # base_safe_chance = .25
        # safe_chance = self.speed
        print('infield hit!')
        return 'infield hit', ball_location

    else:
        print('outfield hit!')
        return 'outfield hit', ball_location


def next_batter():
    global batter
    if playing_offense.batting_index == 8:
        playing_offense.batting_index = 0
    else:
        playing_offense.batting_index += 1
    batter = playing_offense.roster[playing_offense.batting_index]
    print(f"\nnext at bat for Team {playing_offense.team_name} is {batter.name}")
    print(f"Speed: {batter.speed}, hand eye: {batter.hand_eye}\n")
    input("ready for next at bat?: ")


def walked(player_at_bat):
    global runs
    # if bases are loaded
    if len(third_base) > 0 and len(second_base) > 0 and len(first_base) > 0:
        print('A run is scored and all runners advance')
        third_base.pop()
        runs += 1
        third_base.append(second_base.pop())
        second_base.append(first_base.pop())
        first_base.append(player_at_bat)
    # if runners on second and first
    elif len(third_base) == 0 and len(second_base) > 0 and len(first_base) > 0:
        print('Runner on second advances to third base, runner on first advances to second base.')
        third_base.append(second_base.pop())
        second_base.append(first_base.pop())
        first_base.append(player_at_bat)
    # if runners on first and third
    elif len(third_base) > 0 and len(first_base) > 0:
        print('batter advances to first base')
        second_base.append(first_base.pop())
        first_base.append(player_at_bat)
    # if runners on first base only
    elif len(third_base) == 0 and len(second_base) == 0 and len(first_base) > 0:
        print('Runner on first advances to second base')
        second_base.append(first_base.pop())
        first_base.append(player_at_bat)

    print('batter advances to first.')
    first_base.append(player_at_bat)


def check_if_double_play(fielder, player_at_bat):
    global outs
    player_position_dictionary = {}
    for player1 in playing_defense.roster:
        player_position_dictionary[player1.position_name] = player1

    # ----------------do we have loaded bases? start working on a triple play --------------
    if len(third_base) > 0 and len(second_base) > 0 and len(first_base) > 0:
        if third_base[0].speed <= 7 and second_base[0].speed <= 7 and first_base[0].speed <= 7:
            print(f'{fielder.position_name} {fielder.name} made a play to home getting {third_base[0].name} out!')
            outs += 1
            third_base.pop()
            if outs <= 2:
                print(f'Catcher {player_position_dictionary["catcher"].name} threw ball to third baseman\n'
                      f'{player_position_dictionary["third baseman"].name} for out number 2! DOUBLE PLAY!')
                outs += 1
                second_base.pop()
            if outs == 2:
                print(f'{player_position_dictionary["third baseman"].name} threw ball to second baseman\n'
                      f'{player_position_dictionary["second baseman"].name} for out number 3! TRIPLE PLAY!!!\n')
                outs += 1
                first_base.pop()

    # --------------runners on second and first. try to get a triple play ----------
    if len(second_base) > 0 and len(first_base) > 0:
        if second_base[0].speed <= 7 and first_base[0].speed <= 7:
            print(f'{fielder.position_name} {fielder.name} made a play to third base getting {second_base[0].name}'
                  f' out!')
            outs += 1
            if outs <= 2:
                print(f'{player_position_dictionary["third baseman"].name} threw ball to second base for the second '
                      f'out\n DOUBLE PLAY!!')
                outs += 1
                second_base.pop()
            if outs == 2:
                print(f'{player_position_dictionary["second baseman"].name} threw ball to first base for\n'
                      f'out number 3! TRIPLE PLAY!!!\n')
                outs += 1
                first_base.pop()

    # ------------- try to get a double play --------------

    if len(first_base) > 0:
        if first_base[0].speed >= 9:
            print(f'{first_base[0].name} is too fast! Safe on second!')
            second_base.append(first_base.pop())
            print(f'out on first!')
            outs += 1
        else:
            print(f'{fielder.name} playing {fielder.position_name} threw ball to second baseman\n'
                  f'{player_position_dictionary["second baseman"].name} for an out!')
            outs += 1
            if outs <= 2:
                print(f'{player_position_dictionary["second baseman"].name} threw ball to first baseman\n'
                      f'{player_position_dictionary["first baseman"].name} for a second out. DOUBLE PLAY!')
                outs += 1

    else:
        print(f'{player_at_bat} was thrown out at first by {fielder.position_name}: {fielder.name}')
        outs += 1


def wild_pitch():
    global runs, balls

    if len(third_base) > 0:
        runs += 1
        third_base.pop()
    if len(second_base) > 0:
        third_base.append(second_base.pop())
    if len(first_base) > 0:
        second_base.append(first_base.pop())
    print('All runners advance!')


def hit_a_single(player_at_bat):
    global runs
    if len(third_base) > 0:
        print(f'{third_base[0].name} scores from third base!')
        third_base.pop()
        runs += 1
    if len(second_base) > 0:
        print(f'{second_base[0].name} advances to third')
        third_base.append(second_base.pop())
    if len(first_base) > 0:
        print(f'{first_base[0].name} advances to second')
        second_base.append(first_base.pop())

    print(f'{player_at_bat.name} is safe at first!')
    first_base.append(player_at_bat)


def hit_a_double(player_at_bat):
    global runs
    if len(third_base) > 0:
        print(f'runner scores from third')
        third_base.pop()
        runs += 1
    if len(second_base) > 0:
        print(f'Runner scores from second')
        second_base.pop()
        runs += 1
    if len(first_base) > 0:

        if first_base[0].speed >= 7:
            print(f'{first_base[0].name} scores from FIRST BASE with their blistering speed!!!')
            first_base.pop()
            runs += 1
        else:
            print('runner advances from first base to third base.')
            third_base.append(first_base.pop())
    print(f'{player_at_bat.name} hit a double!')
    second_base.append(player_at_bat)


def hit_a_triple(player_at_bat):
    global runs
    if len(third_base) > 0:
        print(f'Runner scores from third')
        third_base.pop()
        runs += 1
    if len(second_base) > 0:
        print('Runner scores from second')
        second_base.pop()
        runs += 1
    if len(first_base) > 0:
        print('runner scores from first base')
        first_base.pop()
        runs += 1
    scored = False
    if not scored:
        if player_at_bat.speed == 10:
            print(f'{player_at_bat.name} scored an inside the ball park home run because of their ridiculous speed!!!')
            runs += 1
            scored = True
    if not scored:
        third_base.append(player_at_bat)
        print(f'{player_at_bat.name} hit a triple!')


def reset_bases():
    if len(third_base) > 0:
        third_base.pop()
    if len(second_base) > 0:
        second_base.pop()
    if len(first_base) > 0:
        first_base.pop()


def hit_home_run(player_at_bat):
    global runs, home_run_runs
    if len(third_base) > 0:
        runs += 1
        home_run_runs += 1
        third_base.pop()
    if len(second_base) > 0:
        runs += 1
        home_run_runs += 1
        second_base.pop()
    if len(first_base) > 0:
        runs += 1
        home_run_runs += 1
    runs += 1
    home_run_runs += 1
    print(f'{player_at_bat.name} hit a {home_run_runs} run home run!!!')
    home_run_runs = 0
    reset_bases()


def select_positions(team1):
    position_index_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    position_list = {'pitcher': [5, 4], 'catcher': [0, 0], 'shortstop': [6, 12], 'first baseman': [11, 2],
                     'second baseman': [11, 7], 'third baseman': [2, 12], 'left fielder': [8, 26],
                     'center fielder': [20, 23], 'right fielder': [23, 8]}

    print(f"\n{team1.team_name} select player positions\n")

    for key, position in position_list.items():
        while True:
            try:
                i = int(input(f"\nWho is the {key}? \n"))
                team1.roster[i].position = position
                team1.roster[i].position_name = key
                position_index_list.remove(i)
                for i in range(9):
                    if i not in position_index_list:
                        continue
                    else:
                        print(f"{i}. {team1.roster[i].name} - Speed: {team1.roster[i].speed},"
                              f" Throwing Power: {team1.roster[i].throwing_power}, "
                              f"Throwing Accuracy: {team1.roster[i].throwing_accuracy}, "
                              f"Hand Eye: {team1.roster[i].hand_eye}")
                break
            except ValueError:
                print("ValueError: Input was not a valid response. Please try again.\n")


def show_roster(team1):
    for i in range(9):
        print(f"{i}. {team1.roster[i].name} - Speed: {team1.roster[i].speed},"
              f" Throwing Power: {team1.roster[i].throwing_power}, "
              f"Throwing Accuracy: {team1.roster[i].throwing_accuracy}, "
              f"Hand Eye: {team1.roster[i].hand_eye}")


# ----------- create 2 teams and assign each team a name -----------

team_a = team.Team()
team_b = team.Team()


# team_a.team_name = "Turkeys"
# team_b.team_name = "Hawks"

# ----------- give each team a roster of 9 players, each with names and random stats -----------

team_a.roster = []
team_b.roster = []

teams_playing = [team_a.roster, team_b.roster]

for team in teams_playing:
    for index in range(9):
        name = random.choice(names.names)
        new_player = player.Player()
        new_player.name = name
        new_player.randomize_stats()
        team.append(new_player)

show_roster(team_a)
team_a.team_name = input("\nWhat is the name of team A: \n")
show_roster(team_b)
team_b.team_name = input("\nWhat is the name of team B: \n")


# ----------- Heads or tails to see who is playing defence first -----------

heads = 1
tails = 0

playing_defense = None
playing_offense = None


print(f"\nHeads - {team_a.team_name} play defence first. Tails - {team_b.team_name} play defence first. \n")
# ready = input("ready? (yes/no): ")

heads_or_tails = random.randint(0, 1)

if heads_or_tails == heads:
    print("Heads\n")
    print(f"{team_a.team_name} play defence first.\n")
    playing_defense = team_a
    playing_offense = team_b
else:
    print("Tails\n")
    print(f"{team_b.team_name} play defence first.\n")
    playing_defense = team_b
    playing_offense = team_a

# ----------- show both rosters and select player positions -----------
print(f"\nTaking the field: {playing_defense.team_name}\n")
show_roster(playing_defense)

select_positions(playing_defense)

print(f"Batting first: {playing_offense.team_name}\n")
show_roster(playing_offense)

select_positions(playing_offense)


# ----------- randomly select player positions----------

# ball_diamond.randomize_position(playing_defense)
# ball_diamond.randomize_position(playing_offense)


# ----------- dealing with batter and starting pitcher -----------

starting_pitcher = pitcher(playing_defense.roster)

batter = playing_offense.roster[playing_offense.batting_index]

# ----------- Game Loop -----------

strikes = 0
balls = 0
outs = 0
inning = 1
top_of_inning = True
runs = 0
home_run_runs = 0

at_bat = []
first_base = []
second_base = []
third_base = []
home = []


start_inning()

game_over = False

while not game_over:

    pitch = starting_pitcher.throws_pitch(batter)

    if pitch == "wild pitch":
        wild_pitch()
        pitch = 'ball'

    if pitch == "ball" and balls <= 3:
        balls += 1

    if pitch == 'ball' and balls == 4:
        print(f"Ball 4. {batter.name} was walked. Take your bases.")
        walked(batter)
        reset_count()
        next_batter()

    if pitch == "strike" and strikes <= 1:
        strikes += 1

    elif pitch == "strike" and strikes == 2:
        outs += 1
        print(f"{batter.name} struck out. there are {outs} out")
        reset_count()
        inning_over = is_inning_over()
        if inning_over:
            reset_bases()
        if not inning_over:
            next_batter()

    if pitch == "hit":
        print(f"{batter.name} swung and hit the ball!")
        hit = ball_contact()

        if hit[0] == 'infield hit':

            for player in playing_defense.roster:
                difference_in_position_y = abs(hit[1][0] - player.position[0])
                difference_in_position_x = abs(hit[1][1] - player.position[1])
                # difference_in_position = [difference_in_position_y, difference_in_position_x]
                if FIELDER_RANGE >= difference_in_position_y and FIELDER_RANGE >= difference_in_position_x:
                    print(difference_in_position_y)
                    print(difference_in_position_x)
                    base_safe = .40
                    # defence_attribute = player.speed
                    # offence_attribute = batter.speed
                    safe_chance = base_safe - ((player.speed - batter.speed) / 10)
                    print(f'fielder position: {player.position_name}\n')
                    print(f"fielder speed: {player.speed},\n"
                          f"batter speed: {batter.speed}\n"
                          f"ROLL THE DICEEEEE!!\n"                           
                          f"safe chance {safe_chance}")
                    safe_or_out = random.randint(0, 100) / 100
                    print(f'safe or out: {safe_or_out}\n')
                    if safe_or_out >= safe_chance:
                        check_if_double_play(player, batter)
                        # outs += 1
                        # print(f'{player.position_name}: {player.name} threw the ball to first! oouttt!!! '
                        #       f'{outs} outs')

                        inning_over = is_inning_over()
                        if inning_over:
                            reset_bases()
                        if not inning_over:
                            next_batter()
                        reset_count()

                        break
                    else:
                        hit_a_single(batter)
                        print(f'{batter.name} out ran the throw to first.')
                        next_batter()
                        break

            else:
                hit_a_single(batter)
                reset_count()
                next_batter()

        if hit[0] == 'outfield hit':

            # ----------------- did the speed of the fielder allow him to catch the ball? -----------
            was_caught = False
            if not was_caught:
                for player in playing_defense.roster:
                    difference_in_position_y = abs(hit[1][0] - player.position[0])
                    difference_in_position_x = abs(hit[1][1] - player.position[1])
                    speed_adjusted_catch_range = player.speed - OUTFIELD_SPEED_PENALTY

                    if speed_adjusted_catch_range >= difference_in_position_y \
                            and speed_adjusted_catch_range >= difference_in_position_x:
                        print(difference_in_position_y)
                        print(difference_in_position_x)
                        outs += 1
                        print(f'\n{player.position_name}, speed: {player.speed} '
                              f'{player.name} caught the ball after running \n'
                              f'{(difference_in_position_y + difference_in_position_x) / 2 * 10}'
                              f' feet to make a catch!'
                              f' Oouttt!!! {outs} out')

                        inning_over = is_inning_over()
                        if inning_over:
                            reset_bases()
                        if not inning_over:
                            next_batter()
                        reset_count()
                        was_caught = True
                        break

            if not was_caught:
                time_to_ball = 100.0
                fastest_player_to_ball = None
                for player in playing_defense.roster:
                    difference_in_position_y = abs(hit[1][0] - player.position[0])
                    difference_in_position_x = abs(hit[1][1] - player.position[1])
                    distance_to_ball = (difference_in_position_y + difference_in_position_x) / 2 * 10

                    players_range = player_range(player)
                    # print(f'distance to ball: {distance_to_ball}')
                    speed_adjusted_distance = distance_to_ball / players_range
                    # print(f'speed adjusted range: {speed_adjusted_distance}\n'
                    #       f'position: {player.position_name} player speed: {player.speed}\n')
                    if time_to_ball > speed_adjusted_distance:
                        time_to_ball = speed_adjusted_distance
                        fastest_player_to_ball = player

                print(f'time to ball: {time_to_ball}\nfastest player to ball: '
                      f'{fastest_player_to_ball.position_name} \n speed: {fastest_player_to_ball.speed}')

                if time_to_ball <= 1.5:
                    hit_a_single(batter)
                elif 1.5 < time_to_ball < 2:
                    hit_a_double(batter)
                elif time_to_ball >= 2:
                    hit_a_triple(batter)

                inning_over = is_inning_over()
                if inning_over:
                    reset_bases()
                if not inning_over:
                    next_batter()
                reset_count()

            it_was_caught = False

        elif hit[0] == 'home run':
            hit_home_run(batter)
            reset_count()
            next_batter()

    if pitch == "hit by pitch":
        walked(batter)
        reset_count()
        next_batter()

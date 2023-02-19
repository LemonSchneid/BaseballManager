
import random


class Player:

    def __init__(self):
        self.name = ""
        self.speed = 0
        self.throwing_accuracy = 0
        self.throwing_power = 0
        self.hand_eye = 0
        self.position = []
        self.position_name = ''

    def randomize_stats(self):
        self.speed = random.randint(1, 10)
        self.throwing_power = random.randint(1, 10)
        self.throwing_accuracy = random.randint(1, 10)
        self.hand_eye = random.randint(1, 10)

    def throws_pitch(self, batter):
        # determines weather pitch is a ball or a strike
        ball_odds = .4
        pitch = random.randint(0, 100) / 100
        print(f"pitch roll was {pitch}")

        # pitch is a ball
        if pitch <= ball_odds:
            ball_accuracy = random.randint(0, 100) / 100
            critical_miss = .1
            base_ball_chance = .9
            crit_attribute_odds = (batter.hand_eye - self.throwing_accuracy) / 10
            ball_chance = base_ball_chance - crit_attribute_odds
            print(f"ball_accuracy: {ball_accuracy}")
            print(f"ball_chance: {ball_chance}")

            if ball_accuracy <= critical_miss:
                hit_or_wild = random.randint(0, 100) / 100
                if hit_or_wild < .50:
                    print("Player hit by pitch. Take your base")
                    return 'hit by pitch'
                else:
                    print("Wild Pitch! (If there are runners on base, runners advance a base.). Ball!")

                    return "wild pitch"
            elif ball_accuracy >= ball_chance:
                # could make a function for making contact with ball ------------------------------------------ !!
                print(f"{self.name} threw a ball but...")
                return "hit"
            else:
                print(f"{self.name} threw a ball!")
                return "ball"

        else:    # pitch is a strike
            strike_odds = .60
            strike_or_hit = random.randint(0, 100) / 100
            attribute_odds = (batter.hand_eye - self.throwing_power) / 10
            strike_chance = strike_odds - attribute_odds

            if strike_chance >= 1:
                strike_chance = .95
                print(f"Strike Chance: {strike_chance}")
                print(f"strike or hit {strike_or_hit}")
                if strike_or_hit <= strike_chance:
                    print('strike!')
                    return "strike"
                else:
                    # print('hit!')
                    return 'hit'

            elif strike_chance <= 0:
                strike_chance = .05
                print(f"Strike Chance: {strike_chance}")
                print(f"strike or hit {strike_or_hit}")
                if strike_or_hit <= strike_chance:
                    print('strike!')
                    return "strike"
                else:
                    # print('hit!')
                    return 'hit'
            else:
                print(f"Strike Chance: {strike_chance}")
                print(f"strike or hit {strike_or_hit}")
                if strike_or_hit <= strike_chance:
                    print('strike!')
                    return "strike"
                else:
                    # print('hit!')
                    return 'hit'

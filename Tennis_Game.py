
import csv
import os
import sys
import time


import time


#Name: Monika Pusz
#Student ID: 16024757
#Date: 10/11/2017
#Course: Comupter Science


#########################
# Display intro to user #
#########################

def displayIntro():
    time.sleep(1)
    print("Welcome to Tennis Game! ")
    time.sleep(2)
    print()
    print("What would you like to do? Type following number to: ")
    time.sleep(1)
    print()

###################
# main() function #
###################

def main():

    print("LIST OF FILES: \n\n")
    print("Please enter the following number in order to start the game: \n\n")
    # Create object to access class
    tennis_game = Tennis_Game_Info()
    # Lets user to load files required to play game
    tennis_game.user_file_input()

    while True:
        select_score()  #user select score option

        #########################################
        # Store information from selected files #
        #########################################

        tennis_game.store_ranking_points()
        tennis_game.store_prize_points()

        #user selects files, program calculates only best 16 players
        count = 1
        if user_selection == "1":
            while male_ranking_place > 1 and female_ranking_place > 1:  #  Check if there are any players left
                count += 1
                tennis_game.get_user_files(count)
                with open(maleScoresFile) as csvFile: #open as .csv file
                    readCsv = csv.reader(csvFile, delimiter=',')
                    if len(list(readCsv)) <= 9:  # keep only best 16 players
                        tennis_game.calculate_file_scores()

        # User inputs score manually, program calculates only best 16 players
        elif user_selection == "2":
            while male_ranking_place > 1 and female_ranking_place > 1:  # Check if there are any players left
                count += 1
                tennis_game.reset_player_names()
                tennis_game.user_score_input(count)
                if len(list(male_player_points)) <= 9:  # keep only best 16 players
                    tennis_game.calculate_user_score()

        # Calculate players winnings and display results
        tennis_game.winner_prize()
        if len(previous_rank_male) > 0 or len(previous_rank_female) > 0:  # Adds previous tournament results (if they exist)
            tennis_game.calculate_previous_results()
        tennis_game.print_results()

        #Save results in a file if user decides to do it
        while True:
            userInput = input("Would you like to save your results in a file? Yes/No: \n")
            if userInput == "Yes" or userInput == "y" or userInput == "yes":
                tennis_game.save_result_in_file()
                break
            elif userInput == "No" or userInput == "n" or userInput == "no":
                print("Your results will not be saved \n")
                break
            else:
                print("Invalid Input. Try again \n")

        # Option for user to add scores for extra tournament
        while True:
            userInput = input("Would you like add scores for another tournament? Yes/No: \n ")
            if userInput == "Yes" or userInput == "y" or userInput == "yes":
                tennis_game.store_previous_results()

                #Create arrays
                global female_player_rank
                female_player_rank = []
                global male_player_rank
                male_player_rank = []
                global prize_money
                prize_money = []
                another_tournament = True
                break
            elif userInput == "No" or userInput == "n" or userInput == "no":
                print("No additional tournament scores will be loaded ")
                another_tournament = False
                break
            else:
                print("Invalid Input. Try again. \n")

        if not another_tournament:
            break


########################################################################
# Score Selection - User read the score from file or enter it manually #
########################################################################

def select_score():

    print("Please select one of the following options: \n\n 1 - Read players score from file \n 2 - Enter players score manually \n ")

    global user_selection
    user_selection = input()

    tennis_info = Tennis_Game_Info()

    while True:
        if user_selection == "1":
            tennis_info.get_user_files(1)

            with open(maleScoresFile) as csvFile:
                readCsv = csv.reader(csvFile, delimiter=',')
                if len(list(readCsv)) <= 9:
                    tennis_info.calculate_file_scores()
            tennis_info.set_Game_Difficulty(maleScoresFile)  #set difficulty
            break
        elif user_selection == "2":
            tennis_info.save_player_name()  # Stores player name
            tennis_info.user_score_input(1)
            if len(list(male_player_points)) <= 9:  #process best 16 players only
                tennis_info.calculate_user_score()
            tennis_info.set_Game_Difficulty("")  # User inputs difficulty level
            break
        else:
            print("Invalid Input! Try again\n\n")


########################
# Clear Console/Window #
########################
def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

#######################################################################
# Tennis_Game_Info class, stores all information and functions needed #
#######################################################################

class Tennis_Game_Info:


    #####################################################
    # Access root directory and remove irrelevant files #
    #####################################################

    global tennis_directory
    tennis_directory = os.listdir()
    if '.idea' in tennis_directory:
        tennis_directory.remove('.idea')
    if 'main.py' in tennis_directory:
        tennis_directory.remove('main.py')
    if '.git' in tennis_directory:
        tennis_directory.remove('.git')

    ####################
    # Difficulty level #
    ####################

    global TAC1_DIFFICULTY
    TAC1_DIFFICULTY = 2.7

    global TBS2_DIFFICULTY
    TBS2_DIFFICULTY = 3.25

    global TAE21_DIFFICULTY
    TAE21_DIFFICULTY = 2.3

    global TAW11_DIFFICULTY
    TAW11_DIFFICULTY = 3.1

    def set_Game_Difficulty(self, tournament):

        global tournament_name
        global difficulty_level

        if 'TAC1' in tournament:
            tournament_name = 'TAC1'
            difficulty_level = TAC1_DIFFICULTY

        elif 'TBS2' in tournament:
            tournament_name = 'TBS2'
            difficulty_level = TBS2_DIFFICULTY

        elif 'TAE21' in tournament:
            tournament_name = 'TAE21'
            difficulty_level = TAE21_DIFFICULTY

        elif 'TAW11' in tournament:
            tournament_name = 'TAW11'
            difficulty_level = TAW11_DIFFICULTY

        else:
            userInput = input("Please enter Tournament Name from the list below \n\n TAC1\n TAE21\n TAW11\n TBS2\n\n :")
            Tennis_Game_Info.set_Game_Difficulty(self, userInput)



    ####################################
    # Arrays used to store information #
    ####################################

    global male_player_score
    male_player_score = []
    global male_player_name
    male_player_name = []
    global male_player_rank
    male_player_rank = []
    global male_player_winners
    male_player_winners = []
    global male_player_points
    male_player_points = []
    global previous_rank_male
    previous_rank_male = []


    global female_player_score
    female_player_score = []
    global female_player_name
    female_player_name = []
    global female_player_rank
    female_player_rank = []
    global female_player_winners
    female_player_winners = []
    global female_player_points
    female_player_points = []
    global previous_rank_female
    previous_rank_female = []


    global ranking_points_info
    ranking_points_info = []
    global prize_money
    prize_money = []


    #################################
    # Read Player Scores from File #
    #################################

    def get_user_files(self, round_number):

        clear_console()

        ######################################################
        # Read Female Players scores from file input by user #
        ######################################################

        clear_console()
        while True:
            for list_position, file_name in enumerate(tennis_directory):
                print(list_position, "-", file_name)
            userInput = input("\n\n\nSelect the file with FEMALE PLAYERS scores for round %d: " % round_number)
            if (int(userInput) < 0) or (int(userInput) > len(tennis_directory)):
                print("Invalid Input. Try again. \n")
            else:
                break
        global femaleScoresFile
        femaleScoresFile = tennis_directory[int(userInput)]  # Stores female file name globally
        tennis_directory.remove(femaleScoresFile)  # Removes file from list so it cannot be selecte

        ######################################################
        # Read Male Players scores from file input by user   #
        ######################################################
        clear_console()
        while True:
            for list_position, file_name in enumerate(tennis_directory):
                print(list_position, "-", file_name)
            userInput = input("\n\n\nSelect the file with MALE PLAYERS scores for round %d: " % round_number)
            if (int(userInput) < 0) or (int(userInput) > len(tennis_directory)):
                print("Invalid Input. Try again. \n")
            else:
                break
        global maleScoresFile
        maleScoresFile = tennis_directory[int(userInput)]  # Stores male file name globally
        tennis_directory.remove(maleScoresFile)  # Removes file from list so it cannot be selected again


        #############################################
        # User selects and inputs file into console #
        #############################################

    def user_file_input(self):

        #####################################
        # Female Players List File Selection#
        #####################################
        clear_console()

        while True:
            for list_position, file_name in enumerate(tennis_directory):
                print(list_position, "-", file_name)
            userInput = input("\n Please type number with file containing FEMALE_PLAYERS information: ")
            if (int(userInput) < 0) or (int(userInput) > len(tennis_directory)):
                print("Invalid Input!!!\n")
            else:
                break
        global femalePlayersFile
        femalePlayersFile = tennis_directory[int(userInput)]  # Stores female players file loaded by user (globally)
        tennis_directory.remove(femalePlayersFile)  # Removes file from our list

        ####################################
        # Male Players List File Selection #
        ####################################
        clear_console()
        while True:
            for list_position, file_name in enumerate(tennis_directory):
                print(list_position, "-", file_name)
            userInput = input("\n Please type number with file containing MALE_PLAYERS information: ")
            if (int(userInput) < 0) or (int(userInput) > len(tennis_directory)):
                print("Invalid Input! Try again. \n")
            else:
                break
        global malePlayersFile
        malePlayersFile = tennis_directory[int(userInput)]  # Stores male players file loaded by user (globally)
        tennis_directory.remove(malePlayersFile)  # Removes file from our list

        #################################
        # Ranking Points File Selection #
        #################################
        clear_console()
        while True:
            for list_position, file_name in enumerate(tennis_directory):
                print(list_position, " - ", file_name)
            userInput = input("\n Please type number with file containing RANKING POINTS information: ")
            if (int(userInput) < 0) or (int(userInput) > len(tennis_directory)):
                print("Invalid Input! Try again. \n")
            else:
                break
        global rankingPointsFile
        rankingPointsFile = tennis_directory[int(userInput)]  # Stores ranking points file loaded by user (globally)
        tennis_directory.remove(rankingPointsFile)  # Removes file from our list

        ##############################
        # Prize Money File Selection #
        ##############################
        clear_console()
        while True:
            for list_position, file_name in enumerate(tennis_directory):
                print(list_position, "-", file_name)
            userInput = input("\n Please type number with file containing PRIZE MONEY information: ")
            if (int(userInput) < 0) or (int(userInput) > len(tennis_directory)):
                print("Invalid Input! Try again. \n")
            else:
                break
        global prize_money_file
        prize_money_file = tennis_directory[int(userInput)]  # Stores prize money file loaded by user (globally)
        tennis_directory.remove(prize_money_file)  # Removes file from our list

    ###############################################
    # User inputs scores manually for each player #
    ###############################################

    def user_score_input(self, round_number):

        ######################
        # Female score input #
        ######################

        global female_player_points
        female_player_points = []

        clear_console()

        print("Please enter FEMALE PLAYER scores for round %d: \n" % round_number)
        while len(female_player_name) > 1:  # While there are still female players left without a score
            row = []

            #################################
            # First female player selection #
            #################################

            for list_position, player_name in enumerate(female_player_name):  # List all available players
                print(list_position + 1, " - ", player_name)
            while True:
                userInput = input("\n Please select first FEMALE PLAYER by typing its position on the list: ")
                if int(userInput) < 1 or int(userInput) > len(female_player_name):
                    print("Invalid Input!. Try again. \n")
                else:
                    break
            row.append(female_player_name[int(userInput) - 1])
            female_player_name.remove(female_player_name[int(userInput) - 1])

            #######################################
            # First female player score selection #
            #######################################

            while True:
                first_score = input("\n Please enter the first FEMLAE PLAYER score (0-2):  ")
                if int(first_score) < 0 or int(first_score) > 2:
                    print("Invalid Input! Try again.\n")
                else:
                    break
            row.append(first_score)

            ########################################
            # Second female player score selection #
            ########################################

            for list_position, player_name in enumerate(female_player_name):  # List all available players
                print(list_position + 1, "-", player_name)
            while True:
                userInput = input("\n Please select second female player by typing its position on the list:  ")
                if int(userInput) < 1 or int(userInput) > len(female_player_name):
                    print("Invalid Input! Try again. \n")
                else:
                    break
            row.append(female_player_name[int(userInput) - 1])
            female_player_name.remove(female_player_name[int(userInput) - 1])

            ########################################
            # Second female player score selection #
            ########################################

            while True:
                second_score = input("\n Please enter second female player score (0-2): ")
                if int(second_score) < 0 or int(second_score) > 2:
                    print("Invalid Input! Try again. \n")
                elif (int(first_score) + int(second_score)) > 3:
                    print("Invalid Input! There can only be a total of 3 games per pair.\n")
                elif int(first_score) != 2 and int(second_score) != 2:
                    print("Invalid Input! One of the players needs to score 2 points to win game. \n\n")
                else:
                    break
            row.append(second_score)
            female_player_points.append(row)  # Save data in array[]


        ######################
        # Male score input  #
        ######################

        global male_player_points
        male_player_points = []


        while len(male_player_name) > 1:  # While there are still male players left without a score
            clear_console()
            print("Please enter MALE PLAYER scores for round %d: \n" % round_number)
            row = []

            ###############################
            # First male player selection #
            ###############################

            for list_position, player_name in enumerate(male_player_name):  # List all available players
                print(list_position + 1, " - ", player_name)
            while True:
                userInput = input("\n Please select first MALE PLAYER by typing its position on the list: ")
                if int(userInput) < 1 or int(userInput) > len(male_player_name):
                    print("Invalid Input! Try again. \n")
                else:
                    break
            row.append(male_player_name[int(userInput) - 1])
            male_player_name.remove(male_player_name[int(userInput) - 1])

            #####################################
            # First male player score selection #
            #####################################

            while True:
                first_score = input("\n Please enter the first MALE PLAYER players score (0-3): ")
                if int(first_score) < 0 or int(first_score) > 3:
                    print("Invalid Input!\n")
                else:
                    break
            row.append(first_score)

            ################################
            # Second male player selection #
            ################################

            for list_position, player_name in enumerate(male_player_name):  # List all available players
                print(list_position + 1, "-", player_name)
            while True:
                userInput = input("\n Please select first MALE PLAYER by typing its position on the list: ")
                if int(userInput) < 1 or int(userInput) > len(male_player_name):
                    print("Invalid Input! Try again.\n")
                else:
                    break
            row.append(male_player_name[int(userInput) - 1])
            male_player_name.remove(male_player_name[int(userInput) - 1])

            ######################################
            # Second male player score selection #
            ######################################

            while True:
                second_score = input("\n Please enter the second male players score (0-3): ")
                if int(second_score) < 0 or int(second_score) > 3:
                    print("Invalid Input!\n")
                elif (int(first_score) + int(second_score)) > 5:
                    print("Invalid Input! There can only be a total of 5 games per pair.\n")
                elif int(first_score) != 3 and int(second_score) != 3:
                    print("Invalid Input! One of the players needs to score 3 points to win game.\n")
                else:
                    break
            row.append(second_score)
            male_player_points.append(row)  #save data in array []




        ######################################
        # Store player names taken from file #
        ######################################

    def save_player_name(self):

        with open(malePlayersFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            for i, row in enumerate(readCsv):
                male_player_name.append(row[0]) #Save male players information in array[]


        with open(femalePlayersFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            for i, row in enumerate(readCsv):
                female_player_name.append(row[0]) #Save female player information in array


    ######################################################################################
    # Stores winnings in the player name array - helps to maintain processing of winners #
    ######################################################################################

    def reset_player_names(self):

        for row in female_player_points:
            if row[1] > row[3]:
                female_player_name.append(row[0])  # Adds female winner back to array
            elif row[1] < row[3]:
                female_player_name.append(row[2])


        for row in male_player_points:
            if row[1] > row[3]:
                male_player_name.append(row[0])  # Adds male winner back to array
            elif row[1] < row[3]:
                male_player_name.append(row[2])


    ##############################################################
    # Stores Ranking Points using Array loaded by user from file #
    ##############################################################

    def store_ranking_points(self):

        with open(rankingPointsFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')

            for i, row in enumerate(readCsv):
                ranking_points_info.append(row[0])


            global male_ranking_place
            male_ranking_place = i #Sets male ranking position counter
            global female_ranking_place
            female_ranking_place = i # Sets female ranking position counter


     ###########################################################
     # Stores Prize Money using Array loaded by user from file #
     ###########################################################

    def store_prize_points(self):

        with open(prize_money_file) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            found = False
            previous = 0
            for row in readCsv:
                if tournament_name in row[0]:
                    found = True

                if found is True:
                    if int(row[1]) < int(previous):  # Prevents storing other tournament values
                        break
                    else:
                        prize_money.append(row[2])
                        previous = row[1]



    #####################################################################################################
    # Calculates scores from file loaded by the user and assign them ranking point based on their score #
    #####################################################################################################
    def calculate_file_scores(self):

        global male_ranking_place
        global female_ranking_place

        ##################################################
        # Open the Female Scores file loaded by the user #
        ##################################################

        with open(femaleScoresFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            next(readCsv)   # Read next row (skip headers)

            #############################################################
            # Calculate female ranking points based on the Player Score #
            #############################################################

            ranking_points = int(ranking_points_info[female_ranking_place]) * difficulty_level #Calculates Ranking Points and multiplying by difficulty level
            for row in readCsv:
                if row[1] > row[3]:
                    female_player_rank.append(row[2] + '-' + str(ranking_points))
                elif row[1] < row[3]:
                    female_player_rank.append(row[0] + '-' + str(ranking_points))
                else:
                    print("\n Invalid! The game will exit now. \n\n") #Exit game if there is no winner
                    sys.exit()
                female_ranking_place += -1

                ######################################################################################################
                # If there is only one last player left, make him a winner and assign him the highest ranking points #
                ######################################################################################################
                if female_ranking_place == 1:
                    ranking_points = int(ranking_points_info[female_ranking_place]) * difficulty_level
                    if row[1] > row[3]:
                        female_player_rank.append(row[0] + '-' + str(ranking_points))
                    elif row[1] < row[3]:
                        female_player_rank.append(row[2] + '-' + str(ranking_points))



         ################################################
         # Open the Male Scores file loaded by the user #
         ################################################

        with open(maleScoresFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            next(readCsv)  # Read next row (skip headers)

            ######################################################
            # Calculate ranking points based on the Player Score #
            ######################################################

            ranking_points = int(ranking_points_info[male_ranking_place]) * difficulty_level #Calculates Ranking Points and multiplying by difficulty level
            for row in readCsv:
                if row[1] > row[3]:
                    male_player_rank.append(row[2] + '-' + str(ranking_points))
                elif row[1] < row[3]:
                    male_player_rank.append(row[0] + '-' + str(ranking_points))
                else:
                    print("\n\n Invalid! The game will exit now. \n\n") #Exit game if there is no winner
                    sys.exit()
                male_ranking_place += -1

                ######################################################################################################
                # If there is only one last player left, make him a winner and assign him the highest ranking points #
                ######################################################################################################
                if male_ranking_place == 1:
                    ranking_points = int(ranking_points_info[male_ranking_place]) * difficulty_level #Calculates Ranking Points depending on difficulty level
                    if row[1] > row[3]:
                        male_player_rank.append(row[0] + '-' + str(ranking_points))
                    elif row[1] < row[3]:
                        male_player_rank.append(row[2] + '-' + str(ranking_points))



    #######################################################################################
    # Calculate players scores that has been manually entered by the user into the console#
    #######################################################################################

    def calculate_user_score(self):
        global male_ranking_place
        global female_ranking_place

        ###########################################################################################################################################
        # Calculate Female Players Scores, Assign Ranking Points to losing players and continue until there is only one player left - winner #
        ###########################################################################################################################################

        ranking_points = int(ranking_points_info[female_ranking_place]) * difficulty_level
        for row in female_player_points:
            if row[1] > row[3]:
                female_player_rank.append(row[2] + '-' + str(ranking_points))
            elif row[1] < row[3]:
                female_player_rank.append(row[0] + '-' + str(ranking_points))
            else:  # If no winner is found, display error and exit
                print("\n Invalid! The game will exit now. \n\n")
                sys.exit()
            female_ranking_place += -1
            # If this is the last player, assign them the highest ranking points
            if female_ranking_place == 1:
                ranking_points = int(ranking_points_info[female_ranking_place]) * difficulty_level
                if row[1] > row[3]:
                    female_player_rank.append(row[0] + '-' + str(ranking_points))
                elif row[1] < row[3]:
                    female_player_rank.append(row[2] + '-' + str(ranking_points))

        ####################################################################################################################################
        # Calculate Male Players Scores, Assign Ranking Points to losing players and continue until there is only one player left - winner #
        ####################################################################################################################################

        ranking_points = int(ranking_points_info[male_ranking_place]) * difficulty_level
        for row in male_player_points:
            if row[1] > row[3]:
                male_player_rank.append(row[2] + '-' + str(ranking_points))
            elif row[1] < row[3]:
                male_player_rank.append(row[0] + '-' + str(ranking_points))
            else:  # If no winner is found, display error and exit
                print("\n Invalid! The game will exit now. \n\n")
                sys.exit()
            male_ranking_place += -1
            # If this is the last player, assign them the highest ranking points
            if male_ranking_place == 1:
                ranking_points = int(ranking_points_info[male_ranking_place]) * difficulty_level
                if row[1] > row[3]:
                    male_player_rank.append(row[0] + '-' + str(ranking_points))
                elif row[1] < row[3]:
                    male_player_rank.append(row[2] + '-' + str(ranking_points))


    ##########################################
    # Calculate Prize Money for best players #
    ##########################################

    def winner_prize(selfs):

        count = len(female_player_rank) - 1  # Calculate best Female Player, based on the score assign prize
        for prize in prize_money:
            female_player_rank[count] += ("-" + prize)
            count += -1

        count = len(male_player_rank) - 1 #Calculate best Male Player, based on the score assign prize
        for prize in prize_money:
            male_player_rank[count] += ("-" + prize)
            count += -1



    #############################################################################
    # Stores previous players results in array so they may be accessed any time #
    #############################################################################

    def store_previous_results(self):

        global previous_rank_male
        global previous_rank_female


        for prevPlayer in previous_rank_female:  #Access previous female scores
            if prevPlayer[0] in female_player_rank:
                previous_rank_female.remove(prevPlayer) # Avoids double entry of players
        previous_rank_female.extend(female_player_rank)



        for prevPlayer in previous_rank_male:  # Access previous male scores
            if prevPlayer[0] in male_player_rank:
                previous_rank_male.remove(prevPlayer) # Avoids double entry of players
        previous_rank_male.extend(male_player_rank)


        ###########################################################################################
        # Calculates player previous results (Ranking Points and Prize Money) - if there are any  #
        ###########################################################################################

    def calculate_previous_results(self):

        ############################################################
        # Calculates Male Players Score from previous tournaments  #
        ############################################################

        for i, x in enumerate(male_player_rank):
            player = x.split(" - ")
            for y in previous_rank_male:
                prevPlayer = y.split(" - ")

                if player[0] in prevPlayer[0]: # Checks if there are previous tournaments and if it matches name

                    if len(prevPlayer) > 1 and len(player) > 1:  # Adds previous points to current amount
                        player[1] = (float(player[1]) + float(prevPlayer[1]))
                    elif len(prevPlayer) > 1 >= len(player):  # Adds previous points to empty amount
                        male_player_rank[i] += ("-" + str(prevPlayer[1]))
                    # Adds previous PRIZE MONEY


                    if len(prevPlayer) > 3 and len(player) > 2:  # Adds previous money to current amount
                        playerMoney = player[2].replace(',', '') #Removes commas to calculate money

                        prevPlayerMoney = prevPlayer[2].replace(',', '')

                        total = (int(playerMoney) + int(prevPlayerMoney))
                        total = format(total, ",d")  # Adds commas back

                        male_player_rank[i] = (player[0] + '-' + str(player[1]) + '-' + total)
                    elif len(prevPlayer) > 3 >= len(player):  # Adds previous money to empty amount
                        male_player_rank[i] += ("-" + str(prevPlayer[2]))
                    break  # When player is found, stops the loop

         #############################################################
         # Calculate Female Players Score from previous tournaments  #
         #############################################################

        for i, x in enumerate(female_player_rank):

            player = x.split(" - ")

            for y in previous_rank_female:
                prevPlayer = y.split(" - ")

                ####################################################################
                #  Checks if there are previous tournaments and if it matches name #
                ####################################################################

                if player[0] in prevPlayer[0]:

                    if len(prevPlayer) > 1 and len(player) > 1:
                        player[1] = (float(player[1]) + float(prevPlayer[1]))
                    elif len(prevPlayer) > 1 >= len(player):
                        female_player_rank[i] += ("-" + str(prevPlayer[1]))

                    #################################################
                    # Adds Prize Money from the previous tournament #
                    #################################################

                    if len(prevPlayer) > 3 and len(player) > 2:  #adds Prize Money won in previous tournaments and adds them together

                        playerMoney = player[2].replace(',', '') #Removes commas to calculate money
                        prevPlayerMoney = prevPlayer[2].replace(',', '')

                        total = (int(playerMoney) + int(prevPlayerMoney))
                        total = format(total, ",d")  # Adds commas back

                        female_player_rank[i] = (player[0] + '-' + str(player[1]) + '-' + total)

                    elif len(prevPlayer) > 3 >= len(player):  # Adds money from current tournament (if Player hasn't won anything in the previous tournament)
                        female_player_rank[i] += ("-" + str(prevPlayer[2]))


    ###############################
    # Print results to the user #
    ###############################

    def print_results(self):

        print("Results for Tournament " + tournament_name + " have been calculated: \n")
        print("There are displayed in descending order, showing best player first.\n\n")

        ##############################################################################################
        # Displays female players result in descending order based on Ranking Points they have earned #
        ##############################################################################################

        print("\n\n List of Female Players showed in order of Ranking Points: \n")
        ranking_points_array = []

        for place, players in enumerate(female_player_rank[::-1]):  # loops in descending order
            player = players.split('-')
            female_player_rank[(len(female_player_rank) - (place + 1))] += ('-' + str(place + 1))

            ranking_points_array.append(float(player[1]))

        ranking_points_array.sort()
        ranking_points_array.reverse()
        while len(ranking_points_array) > 1:
            for rankings in female_player_rank[::-1]:
                result = rankings.split('-')
                maximum_points = ranking_points_array[0]
                if float(result[1]) == maximum_points:
                    ranking_points_array.remove(maximum_points)
                    print("Player Name - " + result[0] + ", Ranking Points - " + result[1], end="")
                    if len(result) > 3:  # display prize money if awarded
                        print(", Prize Money - " + result[2] + ", Place - " + result[3])

                    else:
                        print(", Place - " + result[2])


        #############################################################################################
        # Displays male players result in descending order based on Ranking Points they have earned #
        #############################################################################################


        print("\n\nList of Male Players showed in order of Ranking Points:\n ")
        ranking_points_array = []

        for place, players in enumerate(male_player_rank[::-1]): #loops in descending order
            player = players.split('-')
            male_player_rank[(len(male_player_rank) - (place + 1))] += ('-' + str(place + 1))

            ranking_points_array.append(float(player[1]))

        ranking_points_array.sort()
        ranking_points_array.reverse()
        while len(ranking_points_array) > 1:
            for rankings in male_player_rank[::-1]:
                result = rankings.split('-')
                maximum_points = ranking_points_array[0]
                if float(result[1]) == maximum_points:
                    ranking_points_array.remove(maximum_points)
                    print("Player Name - " + result[0] + ", Ranking Points - " + result[1], end = "")
                    if len(result) > 3: #display prize money if awarded
                        print(", Prize Money - " + result[2] + ", Place - " + result[3])

                    else:
                        print(", Place - " + result[2])


    ###############################
    # Save results in a .csv file #
    ###############################

    def save_result_in_file(self):
        directory = str(os.path.dirname(os.path.realpath(__file__)))  # Retrieves directory path

        #############################################
        # Saves Female Player scores in a .csv file #
        #############################################

        fileName = input("\n Please enter name of a file you would like to save Female Player results in: ")

        with open((directory + "\\" + fileName + ".csv"), 'w', newline="\n", encoding="utf-8") as csvFile:
            writer = csv.writer(csvFile, dialect='excel')
            first_row = ['Place', 'Player Name', 'Ranking Points', 'Prize Money']  # Creates headers within first row
            writer.writerow(first_row)

            ##############################################################################
            # Saves Female Player information in descending order to file chosen by user #
            ##############################################################################

            for row in female_player_rank[::-1]:
                data = row.split('-')
                if len(data) == 4:
                    line = [str(data[3]), str(data[0]), str(data[1]), str(data[2])]
                    writer.writerow(line)
                else:
                    line = [str(data[2]), str(data[0]), str(data[1]), 'NO MONEY WON'] #option for Female Players without Prize Money
                    writer.writerow(line)


         #############################################
         # Saves Female Player scores in a .csv file #
         #############################################

        fileName = input("\n Please enter name of a file you would like to save Male Player results in: ")

        with open((directory + "\\" + fileName + ".csv"), 'w', newline="\n", encoding="utf-8") as csvFile:
            writer = csv.writer(csvFile, dialect='excel')
            first_row = ['Place', 'Player Name', 'Ranking Points', 'Prize Money']  # Creates headers within first row
            writer.writerow(first_row)

            ############################################################################
            # Saves Male Player information in descending order to file chosen by user #
            ############################################################################

            for row in male_player_rank[::-1]:
                data = row.split('-')
                if len(data) == 4:
                    line = [str(data[3]), str(data[0]), str(data[1]), str(data[2])]
                    writer.writerow(line)
                else:
                    line = [str(data[2]), str(data[0]), str(data[1]), 'NO MONEY WON'] #option for Female Players without Prize Money
                    writer.writerow(line)



##########################################
# chooseOption() - displays user options #
##########################################

def chooseOption():
    option = ""
    while option != "1" and option != "2" and option != "3":  # input validation
        option = input(" 1. Start \n 2. Credits \n 3. Exit \n \n ")
        if option == "1":
            main()
        elif option == "2":
            print(
                " Created by Monika Pusz \n UWE Bristol \n Student Number: 16024757 \n Date: 10/11/2017 \n \n")  # Game Credits
            displayIntro()
            chooseOption()
        else:
            import sys
            sys.exit(0) #exit program


displayIntro()
chooseOption()

if __name__ == "__main__": main()

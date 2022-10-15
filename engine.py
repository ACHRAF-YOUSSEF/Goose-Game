class GameState:
    def __init__(self):
        self.board = [
            [["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"]],
            [["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"]],
            [["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"]],
            [["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"]],
            [["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"]],
            [["red", "green"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"], ["-", "-"]]
        ]
        self.boardTxt = [
            ["19", "18", "17", "16", "15", "14", "13", "12"],
            ["20", "37", "36", "35", "34", "33", "32", "11"],
            ["21", "38", "exit", "46", "45", "44", "31", "10"],
            ["22", "39", "40", "41", "42", "43", "30", "9"],
            ["23", "24", "25", "26", "27", "28", "29", "8"],
            ["start", "1", "2", "3", "4", "5", "6", "7"]
        ]
        self.boardDescription = [
            ["rewind same moves", "", "", "", "", "move forward by 1", "", "move back by 1"],
            ["", "", "", "", "", "", "", ""],
            ["move back by 6", "", "", "start over!", "move forward by 1", "", "", ""],
            ["move forward by 4", "", "", "", "", "", "", ""],
            ["", "start over!", "replay same moves", "", "", "", "", ""],
            ["", "move back by 1", "move forward by 1", "start over!", "", "", "jail", ""]
        ]
        self.coords = {"start":(5, 0), "1":(5, 1), "2":(5, 2), "3":(5, 3), "4":(5, 4), "5":(5, 5), "6":(5, 6), "7":(5, 7), 
                       "8":(4, 7), "9":(3, 7), "10":(2, 7), "11":(1, 7), "12":(0, 7), "13":(0, 6), "14":(0, 5), "15":(0, 4),
                       "16":(0, 3), "17":(0, 2), "18":(0, 1), "19":(0, 0), "20":(1, 0), "21":(2, 0), "22":(3, 0), "23":(4, 0),
                        "24":(4, 1), "25":(4, 2), "26":(4, 3), "27":(4, 4), "28":(4, 5), "29":(4, 6), "30":(3, 6), "31":(2, 6),
                        "32":(1, 6), "33":(1, 5), "34":(1, 4), "35":(1, 3), "36":(1, 2), "37":(1, 1), "38":(2, 1), "39":(3, 1),
                        "40":(3, 2), "41":(3, 3), "42":(3, 4), "43":(3, 5), "44":(2, 5), "45":(2, 4), "46":(2, 3), "exit":(2, 2),      
                       }
        self.boardColors = [
            ["1", "black", "black", "black", "black", "2", "black", "1"],
            ["black", "black", "black", "black", "black", "black", "black", "black"],
            ["1", "black", "black", "3", "2", "black", "black", "black"],
            ["2", "black", "black", "black", "black", "black", "black", "black"],
            ["black", "3", "2", "black", "black", "black", "black", "black"],
            ["black", "1", "2", "3", "black", "black", "4", "black"]
        ]
        
        self.player_1 = True
        
        self.inJail = False
        self.inJail_1 = False
        self.inJail_2 = False
        
        self.wasInJail = False
        self.wasInJail_1 = False
        self.wasInJail_2 = False
        
        self.hasWaited = 0
        self.hasWaited_1 = 0
        self.hasWaited_2 = 0
        
        self.l_1 = []
        self.l_2 = []
        
        for i, k in self.coords.items():
            self.l_1.append(i)
            self.l_2.append(k)
            
        self.startIndex = 0
        self.startIndex_1 = 0
        self.startIndex_2 = 0
        
        self.index = 0
        self.index_1 = 0
        self.index_2 = 0
        
        self.count = 0
        
        self.moveLog = []
        self.moveLog_1 = []
        self.moveLog_2 = []
        
        self.throwLog = []
        
    def makeMove(self, move):
        self.board[move.endrow][move.endcol][move.i] = move.color
        self.board[move.startrow][move.startcol][move.i] = "-"
        
    def end_game(self):
        return True if ("red" == self.board[2][2][0] or "green" == self.board[2][2][1]) else False
        
        
class Move:
    def __init__(self, startrow, startcol, endrow, endcol, i, color):
        self.i = i
        
        self.startrow = startrow
        self.startcol = startcol
        
        self.endrow = endrow
        self.endcol = endcol
        
        self.color = color

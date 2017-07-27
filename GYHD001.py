#!/usr/bin/env python
import wx
import PBN
## Author : Nick Thompson
## Date : 2017.05.28
## Base : BridgeBoss039
## To remove DataBase Menu
ModuleName = "GYHD001"

import pickle
import cPickle
import time
import string
import random
import os
import XHeader as X1
import XPlayer as P1
import Practice as P2
import PlayTheCards as PTC
import SessionDeals
import Neanderthal, SAYC, Precision, ACOL
import wx.grid as GridLib
import AutoPlayDeal as APD
import sqlite3

OrigPosSmallX = [
    (X1.MiniTableTopX + 20),
    (X1.MiniTableTopX + X1.MiniTableWidth + 20),
    (X1.MiniTableTopX + 20),
    (X1.MiniTableTopX - 130)]

OrigPosSmallY = [
    (X1.MiniTableTopY - 130),
    (X1.MiniTableTopY),
    (X1.MiniTableTopY + X1.MiniTableHeight + 20),
    (X1.MiniTableTopY)]


DebugTime = 4567
SizeBigX = 1920
SizeBigY = 1920
SizeDefaultX = 1920
SizeDefaultY = 1050
MyDialogYes = 91
MenuNumber001 = 16021
MenuNumber002 = 16022
MenuNumber003 = 16023
MenuNumber004 = 16024
MenuNumber012 = 16033
MenuNumber013 = 16034
MenuNumber038 = 16097
MenuNumber039 = 16098
MenuNumber040 = 16099
MenuNumber041 = 16100
MenuNumber042 = 16101
MenuNumber046 = 16102
MenuNumber047 = 16103
MenuNumber401 = 16201
MenuNumber407 = 16207
##MenuNumber402 = 16202
MenuNumber140 = 15099
MenuNumber141 = 15100
##MenuNumber142 = 15101
MenuNumber240 = 12100
MenuNumber241 = 12101
MenuNumber242 = 12102
MenuNumber243 = 12103
MenuNumber202 = 12104

DebugResolved = 0

## Start of DataBase Initialisation
DataBase = sqlite3.connect('Data/GYHD.db')
Cursor = DataBase.cursor()


Cursor.execute("CREATE TABLE IF NOT EXISTS pbn\
(Uniquer TEXT PRIMARY KEY NOT NULL, Dealer TEXT, Declarer TEXT, Contract TEXT, Result TEXT, Event TEXT, Site TEXT, EventDate TEXT, Board TEXT, North TEXT, \
South TEXT, East TEXT, West TEXT, Vulnerable TEXT, Deal TEXT,  \
HomeTeam TEXT, Room TEXT, Round TEXT, Score TEXT, Section TEXT, EventTable TEXT, \
VisitTeam TEXT, Auction TEXT, Play TEXT, FileName TEXT, DealNum INT)")
DataBase.commit()

Cursor.execute("CREATE TABLE IF NOT EXISTS practice\
(Uniquer TEXT PRIMARY KEY NOT NULL, BidNum TEXT, Declarer INT, Dealer INT, Type INT,\
Level INT, Suit INT, BidType INT, Contract INT, Result TEXT, Success INT, Tricks INT, Variance INT,\
Pack TEXT NOT NULL, PackBlob BLOB, System INT, UserName TEXT NOT NULL, Player INT, FromUniquer TEXT)")
DataBase.commit()

Cursor.execute("CREATE TABLE IF NOT EXISTS score\
(Uniquer TEXT PRIMARY KEY NOT NULL, UserName TEXT NOT NULL, NS_Rubbers INT, EW_Rubbers INT, NS_Games INT, EW_Games INT,\
NS_AboveLine INT, EW_AboveLine INT, NS_BelowLine INT, EW_BelowLine INT)")
DataBase.commit()

Cursor.execute("CREATE TABLE IF NOT EXISTS user\
(Uniquer TEXT PRIMARY KEY NOT NULL, UserName TEXT NOT NULL, Seat INT, System INT, Active INT, \
ScoreStyle INT, HandsDealt INT, HandsPlayed INT, HandsWon INT, \
ReviewPosX INT, ReviewPosY INT, ScorePosX INT, ScorePosY INT, \
DataBasePosX INT, DataBasePosY INT, PBNPosX INT, PBNPosY INT)")
DataBase.commit()

Cursor.execute("CREATE TABLE IF NOT EXISTS userfeature\
(Uniquer TEXT PRIMARY KEY NOT NULL, UserName TEXT NOT NULL, System INT, \
Feature0 Bool,Feature1 Bool, Feature2 Bool, Feature3 Bool, Feature4 Bool, Feature5 Bool, Feature6 Bool, \
Feature7 Bool, Feature8 Bool, Feature9 Bool)")
DataBase.commit()


Cursor.execute("SELECT * FROM user WHERE UserName=?;", ("DefaultUser",))
Rows = Cursor.fetchall()
FoundOne = False
for Row in Rows:
    FoundOne = True
if FoundOne == False:
    MyUniquer = time.time()
    MySeat = 2
    MyActive = 1
    MyStyle = 0
    Cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                    (MyUniquer, str("DefaultUser"), MySeat, 0, MyActive, MyStyle, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    DataBase.commit()
    Cursor.execute("INSERT INTO score VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                    (MyUniquer, str("DefaultUser"), 0, 0, 0, 0, 0, 0, 0, 0))
    DataBase.commit()


## End of DataBase Initialisation

def GetPBNTagPos(MyPlayer):
    MyTags = []
    for x in range(4):
        MyTags.append(-1)
    if MyPlayer == 0:
        MyTags[0] = 0
        MyTags[1] = 1
        MyTags[2] = 2
        MyTags[3] = 3
        return MyTags

    if MyPlayer == 1:
        MyTags[0] = 3
        MyTags[1] = 0
        MyTags[2] = 1
        MyTags[3] = 2
        return MyTags

    if MyPlayer == 2:
        MyTags[0] = 2
        MyTags[1] = 3
        MyTags[2] = 0
        MyTags[3] = 1
        return MyTags

    if MyPlayer == 3:
        MyTags[0] = 1
        MyTags[1] = 2
        MyTags[2] = 3
        MyTags[3] = 0
        return MyTags
    return NyTags

def ResolvePBNPlay(MyContext):
    ReturnCardNum = -100
    ReturnMsg = "MyMsg"
    if MyContext.PBNMode == False:
        return False, ReturnCardNum, ReturnMsg
    if MyContext.PBNContinue == False:
        return False, ReturnCardNum, ReturnMsg
    try:
        MyTags = GetPBNTagPos(MyContext.PBNOrigLeader)
##        print "MyTags " + str(MyTags)
##        print "Orig " + str(MyContext.PBNOrigLeader)
##        print "Current " + str(MyContext.CurrentPlayer)
        MyTag = MyTags[MyContext.CurrentPlayer]
        PBNCardCount = (MyContext.CurrentTrick * 4) + MyTag
##        print "ResolvePBNPlay MyTag " + str(MyTag)
##        print "ResolvePBNPlay Card " + X1.CardStr(PBNCardCount)
        ReturnCardNum = MyContext.PBNPlay[PBNCardCount]
        ReturnMsg = "PBN"
        return True, ReturnCardNum, ReturnMsg
    except:
##        print "End of story, Morning Glory"
        return False, ReturnCardNum, ReturnMsg


class SimplePBNGrid(GridLib.Grid):
    def __init__(self, parent):
        Cursor.execute("SELECT * FROM pbn")
        col_name_list = [tuple[0] for tuple in Cursor.description]
##
##        print str(col_name_list)
##        R1 = []
        MyCount = 0
        for Things in col_name_list:
##            R1.append(Things)
            MyCount = MyCount + 1
##        print str(R1)
##        print str(MyCount)
        self.GridColumns = MyCount
        self.PrevRowSelected = -1
        GridLib.Grid.__init__(self, parent, -1, size=(700,300))
        self.parent = parent
        self.CreateGrid(10000, self.GridColumns)
        self.RowNum = 0
        for x in range(MyCount):
            self.SetColSize(x, 100)
            self.SetColLabelValue(x, col_name_list[x])
        self.SetColSize(0, 0)
        self.Bind(GridLib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(GridLib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)        
        return

    def OnLeftClick(self, evt):
        if self.PrevRowSelected != -1:
            for MyCol in range(self.GridColumns):
                MyCol = MyCol + 1
                self.SetCellBackgroundColour(self.PrevRowSelected, MyCol, wx.WHITE)
        for MyCol in range(self.GridColumns):
            MyCol = MyCol + 1
            self.SetCellBackgroundColour(evt.GetRow(), MyCol, wx.RED)
        self.PrevRowSelected = evt.GetRow()
        self.Refresh()
        return

    def OnLabelLeftClick(self, evt):
        MyUniquer = self.GetCellValue(evt.GetRow(), 0)
        self.OnLeftClick(evt)
        self.parent.OnPBNHand(MyUniquer)
        return

    def OnCellLeftClick(self, evt):
        MyUniquer = self.GetCellValue(evt.GetRow(), 0)
        self.OnLeftClick(evt)
        self.parent.OnPBNHand(MyUniquer)
        return
    
    def UpdateColumns(self, MyRow):
        try:
            for MyCol in range(self.GridColumns):
                self.SetCellValue(self.RowNum, MyCol, str(MyRow[MyCol]))
            self.RowNum = self.RowNum + 1
            return
        except:
            MyDebug(DebugResolved, "More hands than rows")
        return
       
class MyPBNDialog(wx.Dialog):
    def __init__(self, parent, id, title, MyContext):
        wx.Dialog.__init__(self, parent, id, title, size=(700,300))
        VertBox = wx.BoxSizer(wx.VERTICAL)
        self.InformationButton = wx.BitmapButton(self, -1, wx.Bitmap('Buttons/Information.png'))
        self.InformationButton.Bind(wx.EVT_ENTER_WINDOW, self.InformationButtonMouseOver)
        self.InformationButton.Bind(wx.EVT_LEAVE_WINDOW, self.InformationButtonMouseLeave)        
        self.InformationStr = "The idea is you are replaying hands from different Events.\n"
        self.InformationStr = self.InformationStr + "These were originally played in competitions.\n"
        self.InformationStr = self.InformationStr + "If you select a hand, you'll then play that hand exactly as the experts did.\n"
        self.InformationStr = self.InformationStr + "However, should you vary the bidding or play of the cards, from that point, you're on your own.\n"
        self.InformationStr = self.InformationStr + "Regardless, the hand will then be saved to your data base, to then play using your chosen system."
        InformationSizer = wx.BoxSizer(wx.HORIZONTAL)
        InformationSizer.Add(self.InformationButton, 0, wx.ALL, 5)
        self.parent = parent
        self.MyGrid = SimplePBNGrid(self)
        self.Context = MyContext
        TableName = "pbn"
        Cursor.execute("SELECT * from " + TableName)        
        Rows = Cursor.fetchall()
        for Row in Rows:
            self.MyGrid.UpdateColumns(Row)
        VertBox.Add(InformationSizer, 0, wx.ALIGN_CENTER, 5)
        VertBox.Add(self.MyGrid, 0, wx.ALIGN_CENTER, 5)
        self.SetSizer(VertBox)
        self.SetPosition((MyContext.User.PBNPosX, MyContext.User.PBNPosY))
        self.SetBackgroundColour(wx.Colour(250,128,114))
        self.Bind(wx.EVT_CLOSE, self.Handler)
        return


    def InformationButtonMouseOver(self, event):
        self.OldBitmap = self.InformationButton.GetBitmap()
        self.InformationButton.SetToolTipString(self.InformationStr)
        event.Skip()
        
    def InformationButtonMouseLeave(self, event):
        self.InformationButton.SetToolTipString("Information")
        event.Skip()

    def Handler(self, event):
        self.parent.OnPBNDialogClose()
        event.Skip()
        return

    def OnPBNHand(self, MyUniquer):
        self.parent.OnPBNHand(MyUniquer)
        return
    
def DoSessionUniquer(MyUniquer, MyTableName):
    MyContext = X1.Context(False)
    MyContext.Reset()
    Cursor.execute("SELECT * FROM " + MyTableName + " WHERE Uniquer=?;", (MyUniquer,))
    Rows = Cursor.fetchall()
    FoundOne = False 
    for Row in Rows:
        FoundOne = True
        CurrentSession = X1.PracticeSession()
        CurrentSession.Num = 0
        CurrentSession.Declarer = Row[2]
        CurrentSession.Dealer = Row[3]
        CurrentSession.Contract = Row[8]
        CurrentSession.Result = Row[9]
        CurrentSession.Tricks = Row[11]
        CurrentSession.Variance = Row[12]
        CurrentSession.Success = Row[10]
        CurrentSession.System = Row[15]
        CurrentSession.Player = Row[17]        
        MyPack = Row[24]
        TempPack = string.splitfields(string.strip(string.strip(MyPack, "["), "]"), ",")
        MyNewPack = []
        for Things in TempPack:
            MyNewPack.append(int(Things))
        CurrentSession.Pack = MyNewPack
        MyContext.SetDealer(CurrentSession.Dealer)
        MySession = X1.PracticeSession()
        MyContext, MyNewMsg = BidPracticeHand(CurrentSession.Pack, MyContext)
        if MyContext.TossIn:
            return MyContext, MySession, CurrentSession
        MySuccess, MyContext = APD.PlayDeal(MyContext)
        MyTeam = X1.GetTeam(MyContext.Declarer)
        MySession.Tricks = MyContext.Teams[MyTeam].TricksWon
        MyTricksReqd = MyContext.Teams[MyTeam].TricksReqd
        MySession.Variance = MyContext.Teams[MyTeam].TricksWon - MyContext.Teams[MyTeam].TricksReqd       
        MySession.Success = MySuccess
        MySession.Contract = MyContext.Contract
        MySession.Result = APD.GetResult(MyContext)
        MySession.Pack = CurrentSession.Pack
        MySession.Declarer = MyContext.Declarer
        if MyContext.Trumps == X1.SuitSpades:
            MySession.Suit = X1.PracticeSuitMajors
        if MyContext.Trumps == X1.SuitHearts:
            MySession.Suit = X1.PracticeSuitMajors
        if MyContext.Trumps == X1.SuitDiamonds:
            MySession.Suit = X1.PracticeSuitMinors
        if MyContext.Trumps == X1.SuitClubs:
            MySession.Suit = X1.PracticeSuitMinors
        if MyContext.Trumps == X1.SuitNoTrumps:
            MySession.Suit = X1.PracticeSuitNoTrumps
        MySession.Level = X1.PracticeLevelSuitBid(MySession.Suit, MyContext.Contract)
        MySession.BidType = X1.GetPracticeBidType(MyContext, X1.GetTeam(MyContext.Declarer))
        return MyContext, MySession, CurrentSession
    ## MyDebug(DebugResolved, "Should never get here")
    return MyContext, MySession, CurrentSession

def ResetScoreForUser(MyUserName):
    Cursor.execute("SELECT * from score where UserName = ?", (MyUserName, ))
    MyUserNames = []
    Rows = Cursor.fetchall()
    RowCount = 0
    for Row in Rows:
        FoundOne = True
        MyUserNames.append(Row[0])
        RowCount = RowCount + 1
    for Things in range(RowCount):
        MyNS_Rubbers = 0
        MyEW_Rubbers = 0
        MyNS_Games = 0
        MyEW_Games = 0
        MyNS_AboveLine = 0
        MyEW_AboveLine = 0
        MyNS_BelowLine = 0
        MyEW_BelowLine = 0
        Cursor.execute("UPDATE score SET NS_Rubbers = ?, EW_Rubbers = ?, NS_Games = ?, EW_Games = ?, \
                        NS_AboveLine = ?, EW_AboveLine = ?, NS_BelowLine = ?, EW_BelowLine = ? where Uniquer = ?;",
                (MyNS_Rubbers, MyEW_Rubbers, MyNS_Games, MyEW_Games, MyNS_AboveLine, MyEW_AboveLine,
                 MyNS_BelowLine, MyEW_BelowLine, MyUserNames[Things]))
        DataBase.commit()
    return
    
def UpdateUserHandsDealt(MyUniquer):
    Cursor.execute("SELECT * FROM user WHERE Uniquer=?;", (MyUniquer, ))
    Rows = Cursor.fetchall()
    MyUserName = "UserName"
    MyHandsDealt = 0
    for Row in Rows:
        MyUniquer = Row[0]
        MyUserName = Row[1]
        MyHandsDealt = Row[6]
    MyHandsDealt = MyHandsDealt + 1
    Cursor.execute("UPDATE user SET HandsDealt = ? where Uniquer = ?;", (MyHandsDealt, MyUniquer))
    DataBase.commit()
    return

def UpdateUserHandsPlayed(MyUniquer):
    Cursor.execute("SELECT * FROM user WHERE Uniquer=?;", (MyUniquer, ))
    Rows = Cursor.fetchall()
    MyUserName = "UserName"
    MyHandsPlayed = 0
    for Row in Rows:
        MyUniquer = Row[0]
        MyUserName = Row[1]
        MyHandsPlayed = Row[7]
    MyHandsPlayed = MyHandsPlayed + 1
    Cursor.execute("UPDATE user SET HandsPlayed = ? where Uniquer = ?;", (MyHandsPlayed, MyUniquer))
    DataBase.commit()
    return

def UpdateUserHandsWon(MyUniquer):
    Cursor.execute("SELECT * FROM user WHERE Uniquer=?;", (MyUniquer, ))
    Rows = Cursor.fetchall()
    MyUserName = "UserName"
    MyHandsWon = 0
    for Row in Rows:
        MyUniquer = Row[0]
        MyUserName = Row[1]
        MyHandsWon = Row[8]
    MyHandsWon = MyHandsWon + 1
    Cursor.execute("UPDATE user SET HandsWon = ? where Uniquer = ?;", (MyHandsWon, MyUniquer))
    ## MyDebug(DebugResolved, "Update User " + str(MyUserName) + " Won " + str(MyHandsWon))
    DataBase.commit()
    return

def GetScoreForUser(MyUserName):
    MyScoreInfo = X1.ScoreInfo()
    Cursor.execute("SELECT * from score where UserName = ?", (MyUserName, ))
    Rows = Cursor.fetchall()
    for Row in Rows:
        FoundOne = True
        MyScoreInfo.Rubber[0] = Row[2]
        MyScoreInfo.Rubber[1] = Row[3]
        MyScoreInfo.Game[0] = Row[4]
        MyScoreInfo.Game[1] = Row[5]
        MyScoreInfo.AboveLine[0] = Row[6]
        MyScoreInfo.AboveLine[1] = Row[7]
        MyScoreInfo.BelowLine[0] = Row[8]
        MyScoreInfo.BelowLine[1] = Row[9]
    return MyScoreInfo
    
def GetUserByUniquer(MyUniquer):
    Cursor.execute("SELECT * FROM user WHERE Uniquer=?;", (MyUniquer, ))
    Rows = Cursor.fetchall()
    MyUserName = "UserName"
    MyHandsPlayed = 0
    MyUserName = "HelloTest"
    MySeat = 0
    MyUniquer = "NotSet"
    MySystem = 0
    MyActive = 0
    MyScoreStyle = 0
    MyHandsDealt = 0
    MyHandsPlayed = 0
    MyHandsWon = 0
    MyReviewPosX = 0
    MyReviewPosY = 0
    MyScorePosX = 0
    MyScorePosY = 0
    MyDataBasePosX = 0
    MyDataBasePosY = 0
    MyPBNPosX = 0
    MyPBNPosY = 0

    for Row in Rows:
        MyUniquer = Row[0]
        MyUserName = Row[1]
        MySeat = Row[2]
        MySystem = Row[3]
        MyActive = Row[4]
        MyScoreStyle = Row[5]
        MyHandsDealt = Row[6]
        MyHandsPlayed = Row[7]
        MyHandsWon = Row[8]
        MyReviewPosX = Row[9]
        MyReviewPosY = Row[10]        
        MyScorePosX = Row[11]
        MyScorePosY = Row[12]        
        MyDataBasePosX = Row[13]
        MyDataBasePosY = Row[14]        
        MyPBNPosX = Row[15]
        MyPBNPosY = Row[16]        

    MyUser = X1.User(MyUserName)
    MyUser.Uniquer = MyUniquer
    MyUser.Seat = MySeat
    MyUser.System = MySystem
    MyUser.Active = MyActive
    MyUser.ScoreStyle = MyScoreStyle
    MyUser.HandsDealt = MyHandsDealt
    MyUser.HandsPlayed = MyHandsPlayed
    MyUser.HandsWon = MyHandsWon
    MyUser.ReviewPosX = MyReviewPosX
    MyUser.ReviewPosY = MyReviewPosY
    MyUser.ScorePosX = MyScorePosX
    MyUser.ScorePosY = MyScorePosY
    MyUser.DataBasePosX = MyDataBasePosX
    MyUser.DataBasePosY = MyDataBasePosY
    MyUser.PBNPosX = MyPBNPosX
    MyUser.PBNPosY = MyPBNPosY
    return MyUser

def SetDefaultUser():
    Cursor.execute("SELECT * FROM user WHERE Active=?;", (1,))
    Rows = Cursor.fetchall()
    FoundOne = False
    MyUserName = "HelloTest"
    MySeat = 0
    MyUniquer = "NotSet"
    MySystem = 0
    MyActive = 0
    MyScoreStyle = 0
    MyHandsDealt = 0
    MyHandsPlayed = 0
    MyHandsWon = 0
    MyReviewPosX = 0
    MyReviewPosY = 0
    MyScorePosX = 0
    MyScorePosY = 0
    MyDataBasePosX = 0
    MyDataBasePosY = 0
    MyPBNPosX = 0
    MyPBNPosY = 0

    for Row in Rows:
        FoundOne = True
        MyUniquer = Row[0]
        MyUserName = Row[1]
        MySeat = Row[2]
        MySystem = Row[3]
        MyActive = Row[4]
        MyScoreStyle = Row[5]
        MyHandsDealt = Row[6]
        MyHandsPlayed = Row[7]
        MyHandsWon = Row[8]
        MyReviewPosX = Row[9]
        MyReviewPosY = Row[10]        
        MyScorePosX = Row[11]
        MyScorePosY = Row[12]        
        MyDataBasePosX = Row[13]
        MyDataBasePosY = Row[14]        
        MyPBNPosX = Row[15]
        MyPBNPosY = Row[16]        

    MyUser = X1.User(MyUserName)
    MyUser.Uniquer = MyUniquer
    MyUser.Seat = MySeat
    MyUser.System = MySystem
    MyUser.Active = MyActive
    MyUser.ScoreStyle = MyScoreStyle
    MyUser.HandsDealt = MyHandsDealt
    MyUser.HandsPlayed = MyHandsPlayed
    MyUser.HandsWon = MyHandsWon
    MyUser.ReviewPosX = MyReviewPosX
    MyUser.ReviewPosY = MyReviewPosY
    MyUser.ScorePosX = MyScorePosX
    MyUser.ScorePosY = MyScorePosY
    MyUser.DataBasePosX = MyDataBasePosX
    MyUser.DataBasePosY = MyDataBasePosY
    MyUser.PBNPosX = MyPBNPosX
    MyUser.PBNPosY = MyPBNPosY
    return MyUser


class MyResultPanel(wx.Panel):
    def __init__(self, parent, id, TheContext, MyMsg):
##        wx.Panel.__init__(self, parent, id, pos=(X1.TableTopX, X1.TableTopY), style=wx.RAISED_BORDER)
        wx.Panel.__init__(self, parent, id, style=wx.RAISED_BORDER)
        self.SetBackgroundColour("green")
        self.Msg = MyMsg
        self.Context = TheContext
        self.parent = parent
        UserNameLabel = wx.StaticText(self, wx.ID_ANY, 'User Name', size=(80,-1))
        UserNameInput = wx.TextCtrl(self, wx.ID_ANY, TheContext.User.UserName, size=(200,-1))
        UserNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        UserNameInput.Enable(False)
        UserNameSizer.Add(UserNameLabel, 0, wx.ALL, 5)
        UserNameSizer.Add(UserNameInput, 0, wx.ALL, 5)
        VertBox = wx.BoxSizer(wx.VERTICAL)
        VertBox.Add(UserNameSizer, 0, wx.ALIGN_CENTER, 5)

        SeatLabel = wx.StaticText(self, wx.ID_ANY, 'Seat', size=(80,-1))
        SeatInput = wx.TextCtrl(self, wx.ID_ANY, X1.PlayerStr(TheContext.User.Seat), size=(200,-1))
        SeatSizer = wx.BoxSizer(wx.HORIZONTAL)
        SeatInput.Enable(False)
        SeatSizer.Add(SeatLabel, 0, wx.ALL, 5)
        SeatSizer.Add(SeatInput, 0, wx.ALL, 5)
        VertBox.Add(SeatSizer, 0, wx.ALIGN_CENTER, 5)
        
        DealerLabel = wx.StaticText(self, wx.ID_ANY, 'Dealer', size=(80,-1))
        self.Dealer = wx.TextCtrl(self, wx.ID_ANY, X1.PlayerStr(TheContext.Dealer), size=(200,-1))
        DealerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Dealer.Enable(False)
        DealerSizer.Add(DealerLabel, 0, wx.ALL, 5)
        DealerSizer.Add(self.Dealer, 0, wx.ALL, 5)
        VertBox.Add(DealerSizer, 0, wx.ALIGN_CENTER, 5)

        ContractLabel = wx.StaticText(self, wx.ID_ANY, 'Contract', size=(80,-1))
        self.Contract = wx.TextCtrl(self, wx.ID_ANY, str(TheContext.FullContract), size=(200,-1))
        ContractSizer   = wx.BoxSizer(wx.HORIZONTAL)
        self.Contract.Enable(False)
        ContractSizer.Add(ContractLabel, 0, wx.ALL, 5)
        ContractSizer.Add(self.Contract, 0, wx.ALL, 5)
        VertBox.Add(ContractSizer, 0, wx.ALIGN_CENTER, 5)

        ResultLabel = wx.StaticText(self, wx.ID_ANY, 'Result', size=(80,-1))
        self.Result = wx.TextCtrl(self, wx.ID_ANY, MyMsg, size=(200,-1))
        ResultSizer   = wx.BoxSizer(wx.HORIZONTAL)
        self.Result.Enable(False)
        ResultSizer.Add(ResultLabel, 0, wx.ALL, 5)
        ResultSizer.Add(self.Result, 0, wx.ALL, 5)
        VertBox.Add(ResultSizer, 0, wx.ALIGN_CENTER, 5)      
##        self.OkayButton = wx.BitmapButton(self, -1, wx.Bitmap('Buttons/StartCardPlay.png'))
        self.OkayButton = wx.Button(self, -1, "Okay")
        self.OkayButton.SetToolTipString(MyMsg)
        ButtonSizer   = wx.BoxSizer(wx.HORIZONTAL)
        ButtonSizer.Add(self.OkayButton, 0, wx.ALL, 5)
        VertBox.Add(ButtonSizer, 0, wx.ALIGN_CENTER, 5)
        self.SetSizerAndFit(VertBox)
        self.OkayButton.Bind(wx.EVT_BUTTON, self.OnOkayButton)
        MySize = self.GetSize()        
        MyPos = (X1.TableTopX + (X1.TableWidth / 2) - (MySize[0] / 2), X1.TableTopY + (X1.TableHeight / 2) - (MySize[1] / 2))
        self.SetPosition(MyPos)
        self.Show()        
        return

    def OnOkayButton(self, Event):
        MyDebug(DebugResolved, "OnOkayButton")
        self.parent.OnResultPanelOkay()
        return

class MyContinuePanel(wx.Panel):
    def __init__(self, parent, id, TheContext, MyMsg):
##        wx.Panel.__init__(self, parent, id, pos=(X1.TableTopX, X1.TableTopY), style=wx.RAISED_BORDER)
        wx.Panel.__init__(self, parent, id, style=wx.RAISED_BORDER)
        self.SetBackgroundColour("green")
        self.Msg = MyMsg
        self.Context = TheContext
        self.parent = parent
        UserNameLabel = wx.StaticText(self, wx.ID_ANY, 'User Name', size=(80,-1))
        UserNameInput = wx.TextCtrl(self, wx.ID_ANY, TheContext.User.UserName, size=(200,-1))
        UserNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        UserNameInput.Enable(False)
        UserNameSizer.Add(UserNameLabel, 0, wx.ALL, 5)
        UserNameSizer.Add(UserNameInput, 0, wx.ALL, 5)
        VertBox = wx.BoxSizer(wx.VERTICAL)
        VertBox.Add(UserNameSizer, 0, wx.ALIGN_CENTER, 5)

        SeatLabel = wx.StaticText(self, wx.ID_ANY, 'Seat', size=(80,-1))
        SeatInput = wx.TextCtrl(self, wx.ID_ANY, X1.PlayerStr(TheContext.User.Seat), size=(200,-1))
        SeatSizer = wx.BoxSizer(wx.HORIZONTAL)
        SeatInput.Enable(False)
        SeatSizer.Add(SeatLabel, 0, wx.ALL, 5)
        SeatSizer.Add(SeatInput, 0, wx.ALL, 5)
        VertBox.Add(SeatSizer, 0, wx.ALIGN_CENTER, 5)
        
        DealerLabel = wx.StaticText(self, wx.ID_ANY, 'Dealer', size=(80,-1))
        self.Dealer = wx.TextCtrl(self, wx.ID_ANY, X1.PlayerStr(TheContext.Dealer), size=(200,-1))
        DealerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Dealer.Enable(False)
        DealerSizer.Add(DealerLabel, 0, wx.ALL, 5)
        DealerSizer.Add(self.Dealer, 0, wx.ALL, 5)
        VertBox.Add(DealerSizer, 0, wx.ALIGN_CENTER, 5)

        ContractLabel = wx.StaticText(self, wx.ID_ANY, 'Contract', size=(80,-1))
        self.Contract = wx.TextCtrl(self, wx.ID_ANY, str(TheContext.FullContract), size=(200,-1))
        ContractSizer   = wx.BoxSizer(wx.HORIZONTAL)
        self.Contract.Enable(False)
        ContractSizer.Add(ContractLabel, 0, wx.ALL, 5)
        ContractSizer.Add(self.Contract, 0, wx.ALL, 5)
        VertBox.Add(ContractSizer, 0, wx.ALIGN_CENTER, 5)

        LeaderLabel = wx.StaticText(self, wx.ID_ANY, 'Leader', size=(80,-1))
        self.Leader = wx.TextCtrl(self, wx.ID_ANY, X1.PlayerStr(TheContext.CurrentPlayer), size=(200,-1))
        LeaderSizer   = wx.BoxSizer(wx.HORIZONTAL)
        self.Leader.Enable(False)
        LeaderSizer.Add(LeaderLabel, 0, wx.ALL, 5)
        LeaderSizer.Add(self.Leader, 0, wx.ALL, 5)
        VertBox.Add(LeaderSizer, 0, wx.ALIGN_CENTER, 5)      
        self.ContinueButton = wx.BitmapButton(self, -1, wx.Bitmap('Buttons/StartCardPlay.png'))
        self.ContinueButton.SetToolTipString(MyMsg)
        ButtonSizer   = wx.BoxSizer(wx.HORIZONTAL)
        ButtonSizer.Add(self.ContinueButton, 0, wx.ALL, 5)
        VertBox.Add(ButtonSizer, 0, wx.ALIGN_CENTER, 5)

        self.SetSizerAndFit(VertBox)
        self.ContinueButton.Bind(wx.EVT_BUTTON, self.OnContinueButton)
        MySize = self.GetSize()        
        MyPos = (X1.TableTopX + (X1.TableWidth / 2) - (MySize[0] / 2), X1.TableTopY + (X1.TableHeight / 2) - (MySize[1] / 2))
        self.SetPosition(MyPos)
        self.Show()        
        return

    def OnContinueButton(self, Event):
        MyDebug(DebugResolved, "OnContinueButton")
        self.parent.OnContinuePanel(self.Msg)
        return
    
class MyProgressPanel(wx.Panel):
    def __init__(self, parent, id, TheContext, TheSession):
        self.MaxIter = 200
        wx.Panel.__init__(self, parent, id, pos=(100,100), style=wx.RAISED_BORDER)
        self.SetBackgroundColour("cyan")
        AnyLevelVal = TheSession.Level
        AnySuitVal = TheSession.Suit        
##        if TheSession.BidType != X1.PracticeBidTypeNone:
##            AnyLevelVal = X1.PracticeLevelAny
##            AnySuitVal = X1.PracticeSuitAny
        self.Context = TheContext
        self.Session = TheSession
        UserNameLabel = wx.StaticText(self, wx.ID_ANY, 'User Name', size=(100,-1))
        UserNameInput = wx.TextCtrl(self, wx.ID_ANY, TheContext.User.UserName, size=(100,-1))
        UserNameSizer   = wx.BoxSizer(wx.HORIZONTAL)
        UserNameInput.Enable(False)
        UserNameSizer.Add(UserNameLabel, 0, wx.ALL, 5)
        UserNameSizer.Add(UserNameInput, 0, wx.ALL, 5)
        VertBox = wx.BoxSizer(wx.VERTICAL)
        VertBox.Add(UserNameSizer, 0, wx.ALIGN_CENTER, 5)
        DealerLabel = wx.StaticText(self, wx.ID_ANY, 'Dealer', size=(100,-1))
        self.Dealer = wx.TextCtrl(self, wx.ID_ANY, X1.PlayerStr(TheSession.Dealer), size=(100,-1))
        DealerSizer   = wx.BoxSizer(wx.HORIZONTAL)
        self.Dealer.Enable(False)
        DealerSizer.Add(DealerLabel, 0, wx.ALL, 5)
        DealerSizer.Add(self.Dealer, 0, wx.ALL, 5)
        VertBox.Add(DealerSizer, 0, wx.ALIGN_CENTER, 5)
        TypeLabel = wx.StaticText(self, wx.ID_ANY, 'Type', size=(100,-1))
        self.Type = wx.TextCtrl(self, wx.ID_ANY, X1.PracticeTypeStr(TheSession.Type), size=(100,-1))
        TypeSizer   = wx.BoxSizer(wx.HORIZONTAL)
        self.Type.Enable(False)
        TypeSizer.Add(TypeLabel, 0, wx.ALL, 5)
        TypeSizer.Add(self.Type, 0, wx.ALL, 5)
        VertBox.Add(TypeSizer, 0, wx.ALIGN_CENTER, 5)
        LevelLabel = wx.StaticText(self, wx.ID_ANY, 'Level', size=(100,-1))
        self.Level = wx.TextCtrl(self, wx.ID_ANY, X1.PracticeLevelStr(AnyLevelVal), size=(100,-1))
        LevelSizer   = wx.BoxSizer(wx.HORIZONTAL)
        self.Level.Enable(False)
        LevelSizer.Add(LevelLabel, 0, wx.ALL, 5)
        LevelSizer.Add(self.Level, 0, wx.ALL, 5)
        VertBox.Add(LevelSizer, 0, wx.ALIGN_CENTER, 5)
        SuitLabel = wx.StaticText(self, wx.ID_ANY, 'Suit', size=(100,-1))
        self.Suit = wx.TextCtrl(self, wx.ID_ANY, X1.PracticeSuitStr(AnySuitVal), size=(100,-1))
        SuitSizer   = wx.BoxSizer(wx.HORIZONTAL)
        self.Suit.Enable(False)
        SuitSizer.Add(SuitLabel, 0, wx.ALL, 5)
        SuitSizer.Add(self.Suit, 0, wx.ALL, 5)
        VertBox.Add(SuitSizer, 0, wx.ALIGN_CENTER, 5)
        BidTypeLabel = wx.StaticText(self, wx.ID_ANY, 'Bid Type', size=(100,-1))
        self.BidType = wx.TextCtrl(self, wx.ID_ANY, X1.PracticeBidTypeStr(TheSession.BidType), size=(100,-1))
        BidTypeSizer   = wx.BoxSizer(wx.HORIZONTAL)
        self.BidType.Enable(False)
        BidTypeSizer.Add(BidTypeLabel, 0, wx.ALL, 5)
        BidTypeSizer.Add(self.BidType, 0, wx.ALL, 5)
        VertBox.Add(BidTypeSizer, 0, wx.ALIGN_CENTER, 5)
        DealsLabel = wx.StaticText(self, wx.ID_ANY, 'Hands Dealt', size=(100,-1))
        self.HandsDealt = wx.TextCtrl(self, wx.ID_ANY, "0", size=(100,-1))
        DealsSizer   = wx.BoxSizer(wx.HORIZONTAL)
        self.HandsDealt.Enable(False)
        DealsSizer.Add(DealsLabel, 0, wx.ALL, 5)
        DealsSizer.Add(self.HandsDealt, 0, wx.ALL, 5)
        VertBox.Add(DealsSizer, 0, wx.ALIGN_CENTER, 5)
        GeneratedLabel = wx.StaticText(self, wx.ID_ANY, 'Deals Needed', size=(100,-1))
        self.HandsGenerated = wx.TextCtrl(self, wx.ID_ANY, "0", size=(100,-1))
        GeneratedSizer   = wx.BoxSizer(wx.HORIZONTAL)
        self.HandsGenerated.Enable(False)
        GeneratedSizer.Add(GeneratedLabel, 0, wx.ALL, 5)
        GeneratedSizer.Add(self.HandsGenerated, 0, wx.ALL, 5)
        VertBox.Add(GeneratedSizer, 0, wx.ALIGN_CENTER, 5)
        self.CancelButton = wx.Button(self, wx.ID_ANY, 'Cancel')        
        self.ContinueButton = wx.Button(self, wx.ID_ANY, 'Continue')
        ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        ButtonSizer.Add(self.CancelButton, 0, wx.ALL, 5)
        ButtonSizer.Add(self.ContinueButton, 0, wx.ALL, 5)
        VertBox.Add(ButtonSizer, 0, wx.ALIGN_CENTER, 5)
        self.ProgressGauge = wx.Gauge(self, -1, self.MaxIter, size=(250, 25))
        ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        ButtonSizer.Add(self.ProgressGauge, 0, wx.ALL, 5)
        VertBox.Add(ButtonSizer, 0, wx.ALIGN_CENTER, 5)
        ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.MyProgressButton = []
        for x in range(20):
            MyTitle = str(x + 1)
            Button1 = wx.Button(self, -1, str(MyTitle), size=(30, 30))
            ButtonSizer.Add(Button1, 0, wx.ALL, 5)
            self.MyProgressButton.append(Button1)
        VertBox.Add(ButtonSizer, 0, wx.ALIGN_CENTER, 5)        
        self.SetSizerAndFit(VertBox)
        self.SetBackgroundColour("white")
        self.CancelButton.Bind(wx.EVT_BUTTON, self.OnCancelButton)
        self.ContinueButton.Bind(wx.EVT_BUTTON, self.OnContinueButton)
        self.Show()        
        return

    def OnContinueButton(self, Event):
        StartTime = time.time()
        MyDebug(DebugTime, "Start Time : " + str(StartTime))
        TotalDeals = 0
        ScoreCount = 0
        ScoreSuccess = 0
        ScoreSuccessPercent = 0
        MySession = self.Session
        if self.Suit == X1.PracticeSuitAny:
            MySession.Suit = X1.PracticeSuitAny
        if self.Level == X1.PracticeLevelAny:
            MySession.Level = X1.PracticeLevelAny
##        print "Suit " + X1.PracticeSuitStr(MySession.Suit)
##        print "Level " + X1.PracticeLevelStr(MySession.Level)
        
        MaxIter = self.MaxIter
        MyContext = self.Context       
        for Test1 in range(MaxIter):
            MyLoad, MyPack, MyDeclarer, MyContract, MyGetDealNum = LoadPracticeDealRandom(MyContext, MySession)
            TotalDeals = TotalDeals + (MyGetDealNum + 1)
##            self.MyProgressButton[Test1].SetForegroundColour("blue")
            self.Refresh(True)
            MySession.UpdateNum(Test1)
            MySession.UpdatePack(MyPack)
            MySession.UpdateContract(MyContract)
            MySession.Declarer = MyDeclarer
            MySession.Player = MyContext.User.Seat
            MySession.Uniquer = time.time()
            PickleData = cPickle.dumps(MyPack, cPickle.HIGHEST_PROTOCOL)
            Cursor.execute("INSERT INTO " + MyContext.TableName + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                            (MySession.Uniquer, str(Test1), MySession.Declarer, MySession.Dealer, MySession.Type,
                             MySession.Level, MySession.Suit, MySession.BidType, MySession.Contract, str(MySession.Result),
                             MySession.Success, MySession.Tricks, MySession.Variance, str(MySession.Pack), sqlite3.Binary(PickleData),
                             str(MySession.System), MyContext.User.UserName, MyContext.User.Seat, MySession.Uniquer))
            DataBase.commit()
            MyDebug(DebugTime, "Example : " + str(Test1))
            ScoreCount = ScoreCount + 1
            MySuccess, MyContext = APD.PlayDeal(MyContext)
            if MySuccess:
                ScoreSuccess = ScoreSuccess + 1
            MyTeam = X1.GetTeam(MyDeclarer)
            MySession.Tricks = MyContext.Teams[MyTeam].TricksWon
            MyTricksReqd = MyContext.Teams[MyTeam].TricksReqd
            MySession.Variance = abs(MyContext.Teams[MyTeam].TricksWon - MyContext.Teams[MyTeam].TricksReqd)
            MySession.Success = MySuccess
            MySession.Result = APD.GetResult(MyContext)
            Cursor.execute("UPDATE " + MyContext.TableName + " SET Result = ?, Success = ?, Tricks = ?, Variance = ? where Uniquer = ?;",
                        (str(MySession.Result), MySession.Success, MySession.Tricks, MySession.Variance, MySession.Uniquer))
            DataBase.commit()
            MyLine = P2.PrintDealtCards(self.Session.Num, self.Context)
            self.Session.WriteFile(MyLine)
            MyLine = P2.PrintBids(self.Context)
            self.Session.WriteFile(MyLine)            
            MyLine = P2.PrintPlayedCards(self.Context)
            self.Session.WriteFile(MyLine)               
        self.UpdateValues((Test1 + 1), TotalDeals)
        MyDebug(DebugTime, "Total Deals  " + str(TotalDeals))
        ScorePercent =  float(float(ScoreSuccess) / float(ScoreCount))
        MyDebug(DebugTime, "Total Played " + str(ScoreCount) + " Won " + str(ScoreSuccess) + " Percent " + str(ScorePercent))
        EndTime = time.time()
        MyDebug(DebugTime, "End Time : " + str(EndTime))
        Duration = EndTime - StartTime
        MyDebug(DebugTime, "Duration : " + str(Duration))
        return

    def OnCancelButton(self, Event):
        self.Hide()
        Event.Skip()
        return
    
    def UpdateValues(self, MyHandsDealt, MyHandsGenerated):
        self.HandsDealt.SetValue(str(MyHandsDealt))
        self.HandsGenerated.SetValue(str(MyHandsGenerated))
        self.Refresh(True, self.GetClientRect())
        return
    
class MyScoreDialog(wx.Dialog):
    def __init__(self, parent, id, title, MyContext):
        wx.Dialog.__init__(self, parent, id, title)
        self.SetBackgroundColour("cyan")
        UserNameLabel = wx.StaticText(self, wx.ID_ANY, 'User Name')
        UserNameInput = wx.TextCtrl(self, wx.ID_ANY, MyContext.User.UserName, size=(100,-1))
        UserNameSizer   = wx.BoxSizer(wx.HORIZONTAL)
        UserNameInput.Enable(False)
        UserNameSizer.Add(UserNameLabel, 0, wx.ALL, 5)
        UserNameSizer.Add(UserNameInput, 0, wx.ALL, 5)
        VertBox = wx.BoxSizer(wx.VERTICAL)
        VertBox.Add(UserNameSizer, 0, wx.ALIGN_CENTER, 5)
        self.parent = parent
        self.Score0 = []
        self.Score1 = []        
        if MyContext.User.ScoreStyle == X1.ScoreStyleRubber:
            VertBox1 = self.StyleRubber(MyContext.ScoreInfo)
        if MyContext.User.ScoreStyle == X1.ScoreStyleDuplicate:
            VertBox1 = self.StyleDuplicate(MyContext.ScoreInfo)
        VertBox.Add(VertBox1, 0, wx.ALIGN_CENTER, 5)
        self.SetSizer(VertBox)
        self.SetPosition((MyContext.User.ScorePosX, MyContext.User.ScorePosY))
        self.SetBackgroundColour(wx.Colour(250,128,114))
        self.Bind(wx.EVT_CLOSE, self.Handler)
        return

    def ResetScoreDialog(self, MyContext):
        if MyContext.User.ScoreStyle == X1.ScoreStyleRubber:
            self.Score0[1].SetLabelText(str(MyContext.ScoreInfo.Rubber[0]))
            self.Score1[1].SetLabelText(str(MyContext.ScoreInfo.Rubber[1]))
            self.Score0[2].SetLabelText(str(MyContext.ScoreInfo.Game[0]))
            self.Score1[2].SetLabelText(str(MyContext.ScoreInfo.Game[1]))
            self.Score0[3].SetLabelText(str(MyContext.ScoreInfo.AboveLine[0]))
            self.Score1[3].SetLabelText(str(MyContext.ScoreInfo.AboveLine[1]))
            self.Score0[4].SetLabelText(str(MyContext.ScoreInfo.BelowLine[0]))
            self.Score1[4].SetLabelText(str(MyContext.ScoreInfo.BelowLine[1]))
        if MyContext.User.ScoreStyle == X1.ScoreStyleDuplicate:
            self.Score0[1].SetLabelText(str(MyContext.ScoreInfo.AboveLine[0]))
            self.Score1[1].SetLabelText(str(MyContext.ScoreInfo.AboveLine[1]))
            self.Score0[2].SetLabelText(str(MyContext.ScoreInfo.BelowLine[0]))
            self.Score1[2].SetLabelText(str(MyContext.ScoreInfo.BelowLine[1]))
        return
    
    def Handler(self, event):
        self.parent.OnScoreDialogClose()
        event.Skip()
        return

    def ScoreLine(self, MyTitle, MyVal0, MyVal1):
        HorizBox = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD )
        TheTitle = wx.Button(self, -1, str(MyTitle), size=(114,30))
        TheTitle.SetFont(font)
        HorizBox.Add(TheTitle, 0)
        Score0 = wx.Button(self, -1, str(MyVal0), size=(114,30))
        Score0.SetFont(font)
        HorizBox.Add(Score0, 0)
        Score1 = wx.Button(self, -1, str(MyVal1), size=(114,30))
        Score1.SetFont(font)
        self.Score0.append(Score0)
        self.Score1.append(Score1)
        HorizBox.Add(Score1, 0)
        return HorizBox

    def DrawScoreBoard(self, MyContext):
        if MyContext.User.ScoreStyle == X1.ScoreStyleRubber:
            self.StyleRubber(MyContext.ScoreInfo)
        if MyContext.User.ScoreStyle == X1.ScoreStyleDuplicate:
            self.StyleDuplicate(MyContext.ScoreInfo)
        return
            
    def StyleDuplicate(self, MyScoreInfo):
        VertBox = wx.BoxSizer(wx.VERTICAL)
        HorizBox = self.ScoreLine("Teams", "North/South", "East/West")
        HorizBox3 = self.ScoreLine("Bonus Score", MyScoreInfo.AboveLine[0], MyScoreInfo.AboveLine[1])
        HorizBox4 = self.ScoreLine("Part Score", MyScoreInfo.BelowLine[0], MyScoreInfo.BelowLine[1])
        HorizBox2B = wx.BoxSizer(wx.HORIZONTAL)
        ScoreLine2B = wx.StaticLine(self, -1, wx.DefaultPosition, (300, 6), wx.LI_HORIZONTAL)       
        HorizBox2B.Add(ScoreLine2B, 0)
        VertBox.Add(HorizBox, 0)
        VertBox.Add(HorizBox3, 0)
        VertBox.Add(HorizBox2B, 0)
        VertBox.Add(HorizBox4, 0)
        return VertBox

    def StyleRubber(self, MyScoreInfo):
        VertBox = wx.BoxSizer(wx.VERTICAL)
        HorizBox = self.ScoreLine("Teams", "North/South", "East/West")
        HorizBox1 = self.ScoreLine("Rubbers", MyScoreInfo.Rubber[0], MyScoreInfo.Rubber[1])
        HorizBox2 = self.ScoreLine("Games", MyScoreInfo.Game[0], MyScoreInfo.Game[1])
        HorizBox3 = self.ScoreLine("Bonus Score", MyScoreInfo.AboveLine[0], MyScoreInfo.AboveLine[1])
        HorizBox4 = self.ScoreLine("Part Score", MyScoreInfo.BelowLine[0], MyScoreInfo.BelowLine[1])
        HorizBox2B = wx.BoxSizer(wx.HORIZONTAL)
        ScoreLine2B = wx.StaticLine(self, -1, wx.DefaultPosition, (300, 6), wx.LI_HORIZONTAL)       
        HorizBox2B.Add(ScoreLine2B, 0)
        VertBox.Add(HorizBox, 0)
        VertBox.Add(HorizBox1, 0)
        VertBox.Add(HorizBox2, 0)
        VertBox.Add(HorizBox2B, 0)
        VertBox.Add(HorizBox3, 0)
        VertBox.Add(HorizBox2B, 0)
        VertBox.Add(HorizBox4, 0)
        return VertBox

class MyUserListDialog(wx.Dialog):
    def __init__(self, parent, id, title, MyContext):
        wx.Dialog.__init__(self, parent, id, title, size=(530, 400))
        self.Context = MyContext
        VertBox = wx.BoxSizer(wx.VERTICAL)
        self.parent = parent
        self.PrevSel = []
        self.SelectedUserUniquer = []
        Cursor.execute("SELECT * from user")
        Rows = Cursor.fetchall()
        self.RowCount = 0
        for Row in Rows:
            if self.RowCount == 0:
                self.PrevSel.append(True)
                self.SelectedUserUniquer.append(str(Row[0]))
            if self.RowCount > 0:  
                self.PrevSel.append(False)
                self.SelectedUserUniquer.append("Sailor")
            self.RowCount = self.RowCount + 1
        self.MyGrid = SimpleUserGrid(self, self.RowCount)
        for Row in Rows:        
            self.MyGrid.UpdateColumns(Row[0], Row[1], Row[2], Row[3], Row[7], Row[8])
        VertBox.Add(self.MyGrid, 0, wx.ALIGN_CENTER, 5)
        self.CancelButton = wx.Button(self, wx.ID_ANY, 'Cancel')        
        self.ContinueButton = wx.Button(self, wx.ID_ANY, 'Continue')
        ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        ButtonSizer.Add(self.CancelButton, 0, wx.ALL, 5)
        ButtonSizer.Add(self.ContinueButton, 0, wx.ALL, 5)
        VertBox.Add(ButtonSizer, 0, wx.ALIGN_CENTER, 5)
        self.SetSizer(VertBox)
        self.SetPosition((MyContext.User.ReviewPosX, MyContext.User.ReviewPosY))
        self.SetBackgroundColour(wx.Colour(250,128,114))
        self.Bind(wx.EVT_CLOSE, self.Handler)
        self.ContinueButton.Bind(wx.EVT_BUTTON, self.SystemComparisonTest)
        return

    def UpdateSelectedUserUniquer(self, MyRow, MyTrueFalse, MyUniquer):
##        print "UpdateSelectedUserUniquer Row " + str(MyRow) + " TF " + str(MyTrueFalse) + " Uniquer " + str(MyUniquer)
        self.PrevSel[MyRow] = MyTrueFalse
        self.SelectedUserUniquer[MyRow] = MyUniquer
        return
        
    def SystemComparisonTest(self, Event):
## System Comparison Test       
        StartTime = time.time()
        MyDebug(DebugTime, "Start Time : " + str(StartTime))
##        print "System Comparison Test Start Time : " + str(StartTime)
##        MyContext = self.Context
        MyContext = X1.Context(False)
        MyContext.Reset()

        for x in range(self.RowCount):
            MyContext.User = GetUserByUniquer(self.SelectedUserUniquer[x])
            print "Name " + str(MyContext.User.UserName)
        return

    def Handler(self, event):
        self.parent.OnUserListDialogClose()
        event.Skip()
        return
        
    def OnUserHand(self, MyUniquer):
##        self.parent.OnUserHand(MyUniquer)
        return

class MyUserDialog(wx.Dialog):
    def __init__(self, parent, id, title, MyContext, UserSet):
        wx.Dialog.__init__(self, parent, id, title, size=(576,300))
        UserNameLabel = wx.StaticText(self, wx.ID_ANY, 'User Name')
        UserNameSizer   = wx.BoxSizer(wx.HORIZONTAL)
        if UserSet:
            UserNameInput = wx.TextCtrl(self, wx.ID_ANY, MyContext.User.UserName, size=(100,-1))            
        if UserSet == False:
            UserNameInput = wx.TextCtrl(self, wx.ID_ANY, "All Users", size=(100,-1))
        UserNameInput.Enable(False)
        self.Context = MyContext
        UserNameSizer.Add(UserNameLabel, 0, wx.ALL, 5)
        UserNameSizer.Add(UserNameInput, 0, wx.ALL, 5)
        VertBox = wx.BoxSizer(wx.VERTICAL)
        self.parent = parent
        self.MyGrid = SimpleHandGrid(self)
        if UserSet:
            Cursor.execute("SELECT * from " + MyContext.TableName + " where UserName = ?", (MyContext.User.UserName, ))
        if UserSet == False:
            Cursor.execute("SELECT * from " + MyContext.TableName)
        Rows = Cursor.fetchall()
        for Row in Rows:
            self.MyGrid.UpdateColumns(Row[0], Row[8], Row[3], Row[2], Row[9], Row[7])
        VertBox.Add(UserNameSizer, 0, wx.ALIGN_CENTER, 5)
        VertBox.Add(self.MyGrid, 0, wx.ALIGN_CENTER, 5)
        self.SetSizer(VertBox)
        self.SetPosition((MyContext.User.ReviewPosX, MyContext.User.ReviewPosY))
        self.SetBackgroundColour(wx.Colour(250,128,114))
        self.Bind(wx.EVT_CLOSE, self.Handler)
        return

    def Handler(self, event):
        self.parent.OnUserReviewDialogClose()
        event.Skip()
        return

    def OnPuddleHand(self, MyUniquer):
        print "OnPuddleHand"
        Cursor.execute("SELECT * FROM " + self.Context.TableName + " WHERE Uniquer=?;", (MyUniquer,))
        Rows = Cursor.fetchall()
        FoundOne = False
        for Row in Rows:
            FoundOne = True
            MyPack = Row[13]
        if FoundOne == False:
            return     
        TempPack = string.splitfields(string.strip(string.strip(MyPack, "["), "]"), ",")
        MyNewPack = []
        for Things in TempPack:
            MyNewPack.append(int(Things))
        MyPuddleFrame = PuddleFrame(self, -1, X1.XXBridgeThing, self.Context, MyNewPack)
        MyPuddleFrame.Show(True)
        return
        
    def OnUserHand(self, MyUniquer):
        self.parent.OnUserHand(MyUniquer)
        return

class MyDataBaseDialog(wx.Dialog):
    def __init__(self, parent, id, title, MyContext, MySession):
        wx.Dialog.__init__(self, parent, id, title, size=(576,300))
        UserNameLabel = wx.StaticText(self, wx.ID_ANY, 'DBUser Name')
        UserNameInput = wx.TextCtrl(self, wx.ID_ANY, MyContext.User.UserName, size=(100,-1))
        UserNameSizer   = wx.BoxSizer(wx.HORIZONTAL)
        UserNameInput.Enable(False)
        UserNameSizer.Add(UserNameLabel, 0, wx.ALL, 5)
        UserNameSizer.Add(UserNameInput, 0, wx.ALL, 5)
        VertBox = wx.BoxSizer(wx.VERTICAL)
        self.parent = parent
        self.MyGrid = SimpleHandGrid(self)
        self.Context = MyContext
        FieldName = []
        FieldVal = []

        FieldName.append("Level")
        FieldVal.append(-1)
        FieldName.append("Suit")
        FieldVal.append(-1)
        FieldName.append("BidType")
        FieldVal.append(-1)


        
        MyFieldCount = 0
##        print "Level " + X1.PracticeLevelStr(MySession.DBLevel)
##        print "Suit " + X1.PracticeSuitStr(MySession.DBSuit)
##        print "Type " + X1.PracticeBidTypeStr(MySession.DBBidType)
        if MySession.DBLevel != X1.PracticeLevelAny:
            FieldVal[0] = MySession.DBLevel
            MyFieldCount = MyFieldCount + 1
        if MySession.DBSuit != X1.PracticeSuitAny:
            FieldVal[1] = MySession.DBSuit
            MyFieldCount = MyFieldCount + 1
        if MySession.DBBidType != X1.PracticeBidTypeNone:
            FieldVal[2] = MySession.DBBidType
            MyFieldCount = MyFieldCount + 1
        
        if MySession.DBLevel != X1.PracticeLevelAny:
            if MySession.DBSuit != X1.PracticeSuitAny:
                if MySession.DBBidType != X1.PracticeBidTypeNone:
##                    print "test1 Level Suit BidType"
                    Cursor.execute("SELECT * FROM " + MyContext.TableName + " WHERE Level=? AND Suit=? AND BidType=?;", (FieldVal[0], FieldVal[1],FieldVal[2],))

        if MySession.DBLevel == X1.PracticeLevelAny:
            if MySession.DBSuit != X1.PracticeSuitAny:
                if MySession.DBBidType != X1.PracticeBidTypeNone:
##                    print "test2 Suit and BidType"
                    Cursor.execute("SELECT * FROM " + MyContext.TableName + " WHERE Suit=? AND BidType=?;", (FieldVal[1], FieldVal[2],))

        if MySession.DBLevel == X1.PracticeLevelAny:
            if MySession.DBSuit == X1.PracticeSuitAny:
                if MySession.DBBidType != X1.PracticeBidTypeNone:
##                    print "test3 BidType only"
                    Cursor.execute("SELECT * FROM " + MyContext.TableName + " WHERE BidType=?;", (FieldVal[2],))

        if MySession.DBLevel != X1.PracticeLevelAny:
            if MySession.DBSuit != X1.PracticeSuitAny:
                if MySession.DBBidType == X1.PracticeBidTypeNone:
##                    print "test4 Level and Suit"
                    Cursor.execute("SELECT * FROM " + MyContext.TableName + " WHERE Level=? AND Suit=?;", (FieldVal[0], FieldVal[1],))


        if MySession.DBLevel != X1.PracticeLevelAny:
            if MySession.DBSuit != X1.PracticeSuitAny:
                if MySession.DBBidType != X1.PracticeBidTypeNone:
##                    print "test5 Level and BidType"
                    Cursor.execute("SELECT * FROM " + MyContext.TableName + " WHERE Level=? AND BidType=?;", (FieldVal[0], FieldVal[2],))

        if MySession.DBLevel != X1.PracticeLevelAny:
            if MySession.DBSuit == X1.PracticeSuitAny:
                if MySession.DBBidType == X1.PracticeBidTypeNone:
##                    print "test6 Level only"
                    Cursor.execute("SELECT * FROM " + MyContext.TableName + " WHERE Level=?;", (FieldVal[0],))

            
        if MyFieldCount == 0:
##            MySQL = '"SELECT * from " + MyContext.TableName'
##            print str(MySQL)
##            Cursor.execute(eval(MySQL))
            Cursor.execute("SELECT * from " + MyContext.TableName)        
        Rows = Cursor.fetchall()


        for Row in Rows:
            self.MyGrid.UpdateColumns(Row[0], Row[8], Row[3], Row[2], Row[9], Row[7])
        VertBox.Add(UserNameSizer, 0, wx.ALIGN_CENTER, 5)
        VertBox.Add(self.MyGrid, 0, wx.ALIGN_CENTER, 5)
        self.SetSizer(VertBox)
        self.SetPosition((MyContext.User.DataBasePosX, MyContext.User.DataBasePosY))
        self.SetBackgroundColour(wx.Colour(250,128,114))
        self.Bind(wx.EVT_CLOSE, self.Handler)
        return

    def Handler(self, event):
        self.parent.OnDataBaseDialogClose()
        event.Skip()
        return

    def OnPuddleHand(self, MyUniquer):
##        print "OnPuddleHand"
        Cursor.execute("SELECT * FROM " + self.Context.TableName + " WHERE Uniquer=?;", (MyUniquer,))
        Rows = Cursor.fetchall()
        FoundOne = False
        for Row in Rows:
            FoundOne = True
            MyPack = Row[13]
        if FoundOne == False:
            return     
        TempPack = string.splitfields(string.strip(string.strip(MyPack, "["), "]"), ",")
        MyNewPack = []
        for Things in TempPack:
            MyNewPack.append(int(Things))
##        print str(MyNewPack)
        MyPuddleFrame = PuddleFrame(self, -1, X1.XXBridgeThing, self.Context, MyNewPack)
        MyPuddleFrame.Show(True)
        return
      
    def OnUserHand(self, MyUniquer):
        self.parent.OnDataBaseHand(MyUniquer)
        return

class MyDialog(wx.Dialog):
    def __init__(self, parent, id, title, MyPlayer):
        wx.Dialog.__init__(self, parent, id, title, size=(155,74))
        vbox = wx.BoxSizer(wx.VERTICAL)
        sizer =  self.CreateButtonSizer(wx.OK)
        vbox.Add(sizer, 0, wx.ALIGN_CENTER)
        self.SetSizer(vbox)
        self.SetPosition((435,508))
        self.SetBackgroundColour(wx.Colour(250,128,114))
        return

def X1FormatStr(Num):
    if Num >= 0:
        if Num < 2:
            MyStr = ["Big", "Small"]
            return MyStr[Num]
    return "Not Set"

def X1ExampleName(Num):
    if Num >= 0:
        if Num < 4:
            MyStr = ["example", "example1", "example2", "Jacoby NT"]
            return MyStr[Num]
    return "NotSet"

def X1ExampleStr(Num):
    if Num >= 0:
        if Num < 4:
            MyStr = ["Limit Ask", "Control Ask", "Sustainable", "Jacoby NT"]
            return MyStr[Num]
    return "Not Set"

def ExpLenStr(MyExpLen):
    ## MyDebug(0, "ExpLenStr " + str(MyExpLen))
    MyStr = ""
    ExpLenBool = False
    for MyCount in range(4):
        MySuit = 3 - MyCount
        if MyExpLen[MySuit] != 0:
            ExpLenBool = True
            MyStr = MyStr + X1.TrumpStr(MySuit) + ":" + str(MyExpLen[MySuit]) + " "
    if ExpLenBool == False:
        MyStr = "No info"
    return MyStr

def DoSessionNumber(MyNum):
    MyContext = X1.Context(False)
    MyContext.Reset()
    MyContext.SetDealer(0)
    MySession = X1.PracticeSession()
    MySession.Num = MyNum
    MyNewMsg = "Nothing"
    KosherDeal, CurrentSession = SessionDeals.GetSessionDeal(MyNum)
    if KosherDeal == False:
        return MyContext, MySession, CurrentSession
    if KosherDeal:
        MyContext, MyNewMsg = BidPracticeHand(CurrentSession.Pack, MyContext)
        if MyContext.TossIn:
            return MyContext, MySession, CurrentSession
        MySuccess, MyContext = APD.PlayDeal(MyContext)
        MyTeam = X1.GetTeam(MyContext.Declarer)
        MySession.Tricks = MyContext.Teams[MyTeam].TricksWon
        MyTricksReqd = MyContext.Teams[MyTeam].TricksReqd
        MySession.Variance = MyContext.Teams[MyTeam].TricksWon - MyContext.Teams[MyTeam].TricksReqd       
        MySession.Success = MySuccess
        MySession.Contract = MyContext.Contract
        MySession.Result = APD.GetResult(MyContext)
        MySession.Pack = CurrentSession.Pack
        MySession.Declarer = MyContext.Declarer
        if MyContext.Trumps == X1.SuitSpades:
            MySession.Suit = X1.PracticeSuitMajors
        if MyContext.Trumps == X1.SuitHearts:
            MySession.Suit = X1.PracticeSuitMajors
        if MyContext.Trumps == X1.SuitDiamonds:
            MySession.Suit = X1.PracticeSuitMinors
        if MyContext.Trumps == X1.SuitClubs:
            MySession.Suit = X1.PracticeSuitMinors
        if MyContext.Trumps == X1.SuitNoTrumps:
            MySession.Suit = X1.PracticeSuitNoTrumps
        MySession.Level = X1.PracticeLevelSuitBid(MySession.Suit, MyContext.Contract)
        MySession.BidType = X1.GetPracticeBidType(MyContext, X1.GetTeam(MyContext.Declarer))
        return MyContext, MySession, CurrentSession
    ## MyDebug(DebugResolved, "Should never get here")
    return MyContext, MySession, CurrentSession

def LoadRandomSession13():
    MyContext = X1.Context(False)
    MyContext.Reset()
    MyContext.SetDealer(0)
    MySession = X1.PracticeSession()
    MyNewMsg = "Nothing"
    KosherDeal, NewPack, TestString = X1.ShufflePack()
    MyContext, MyNewMsg = BidPracticeHand(NewPack, MyContext)
    if MyContext.TossIn:
        return False, MyContext, MySession, MyNewMsg
    MyTeam = X1.GetTeam(MyContext.Declarer)
    MySession.Contract = MyContext.Contract
    MySession.Pack = NewPack
    MySession.Declarer = MyContext.Declarer
    if MyContext.Trumps == X1.SuitSpades:
        MySession.Suit = X1.PracticeSuitMajors
    if MyContext.Trumps == X1.SuitHearts:
        MySession.Suit = X1.PracticeSuitMajors
    if MyContext.Trumps == X1.SuitDiamonds:
        MySession.Suit = X1.PracticeSuitMinors
    if MyContext.Trumps == X1.SuitClubs:
        MySession.Suit = X1.PracticeSuitMinors
    if MyContext.Trumps == X1.SuitNoTrumps:
        MySession.Suit = X1.PracticeSuitNoTrumps
    MySession.Level = X1.PracticeLevelSuitBid(MySession.Suit, MyContext.Contract)
    MySession.BidType = X1.GetPracticeBidType(MyContext, X1.GetTeam(MyContext.Declarer))
    return True, MyContext, MySession, MyNewMsg      


def LoadRandomSession():
    MyContext = X1.Context(False)
    MyContext.Reset()
    MyContext.SetDealer(0)
    MySession = X1.PracticeSession()
    MyNewMsg = "Nothing"
    KosherDeal, NewPack, TestString = X1.ShufflePack()
    if KosherDeal == False:
        return MyContext, MySession, MyNewMsg
    if KosherDeal:
        MyContext, MyNewMsg = BidPracticeHand(NewPack, MyContext)
        if MyContext.TossIn:
            return MyContext, MySession, MyNewMsg
        MySuccess, MyContext = APD.PlayDeal(MyContext)
        MyTeam = X1.GetTeam(MyContext.Declarer)
        MySession.Tricks = MyContext.Teams[MyTeam].TricksWon
        MyTricksReqd = MyContext.Teams[MyTeam].TricksReqd
        MySession.Variance = MyContext.Teams[MyTeam].TricksWon - MyContext.Teams[MyTeam].TricksReqd
        MySession.Success = MySuccess
        MySession.Contract = MyContext.Contract
        MySession.Result = APD.GetResult(MyContext)
        MySession.Pack = NewPack
        MySession.Declarer = MyContext.Declarer
        if MyContext.Trumps == X1.SuitSpades:
            MySession.Suit = X1.PracticeSuitMajors
        if MyContext.Trumps == X1.SuitHearts:
            MySession.Suit = X1.PracticeSuitMajors
        if MyContext.Trumps == X1.SuitDiamonds:
            MySession.Suit = X1.PracticeSuitMinors
        if MyContext.Trumps == X1.SuitClubs:
            MySession.Suit = X1.PracticeSuitMinors
        if MyContext.Trumps == X1.SuitNoTrumps:
            MySession.Suit = X1.PracticeSuitNoTrumps
        MySession.Level = X1.PracticeLevelSuitBid(MySession.Suit, MyContext.Contract)
        MySession.BidType = X1.GetPracticeBidType(MyContext, X1.GetTeam(MyContext.Declarer))
        return MyContext, MySession, MyNewMsg
    ## MyDebug(DebugResolved, "Should never get here")
    return MyContext, MySession, MyNewMsg

def GetDealByBidType(MyContext, MyTeam, MyBidType):
    for Things in MyContext.Bids:
        if Things.SubType == MyBidType:
            ThingTeam = X1.GetTeam(Things.Owner)
            if ThingTeam == MyTeam:
                return True
    return False

def BidPracticeHand(NewPack, MyContext):
    MyContext.User = SetDefaultUser()
    MyContext.ScoreInfo = GetScoreForUser(MyContext.User.UserName)
    ReturnMsg = "Sailor"
    for PlayerCount in range(4):
        MyPlayer = P1.Player(PlayerCount)
        MyContext.AddPlayer(MyPlayer)
    for PlayerCount in range(4):        
        MyContext.Players[PlayerCount].Name = X1.PlayerStr(PlayerCount)
        MyContext.Players[PlayerCount].InitHands()
        MyContext.Players[PlayerCount].UpdateHand(NewPack)
        MyContext.Players[PlayerCount].SortHands()
    for PlayerCount in range(4):
        for MyCard in range(13):
            MyCount = MyContext.Players[PlayerCount].SortHand[MyCard]
            WK = X1.WorkCard(MyCount, (MyCount % 13))
            WK.Owner = PlayerCount
            WK.HandLoc = MyCard
            MyContext.DealtPack.append(WK)
            MyContext.Players[PlayerCount].InitPoints(WK)
            MyContext.WorkPack.append(WK)            
    for PlayerCount in range(4):        
        MyContext.Players[PlayerCount].UpdateDPs()
        MyContext.Players[PlayerCount].UpdateLPs()
        MyContext.Players[PlayerCount].UpdateLTC()
    while MyContext.KeepBidding:               
        MyBidType = X1.GetBidType(MyContext.Bids, MyContext.BidCounter)
        MyTeam = X1.GetTeam(MyContext.CurrentPlayer)
        FnStr = X1.BidTypeStr(MyBidType)
        MyBid = eval(X1.SystemStr(MyContext.Teams[MyTeam].System) + "." + FnStr + "(" + str(MyContext.CurrentPlayer) + ", MyContext)")
        Msg = X1.PlayerStr(MyContext.CurrentPlayer) + " Bid : " + X1.BidStr(MyBid) + " ... Hint " + str(MyContext.HintMsg)
        Mine = X1.Bid(MyBid)    
        Mine.Owner = MyContext.CurrentPlayer
        Mine.Type = MyBidType
        MyFn = X1.SystemStr(MyContext.Teams[MyTeam].System) + ".GetBidSubType(Mine, MyContext)"
        MyBidSubType = eval(MyFn)
        Mine.SubType = MyBidSubType
        MyStrFn = X1.SystemStr(MyContext.Teams[MyTeam].System) + ".BidSubTypeStr(Mine.SubType)"
        MyBidSubTypeStr = eval(MyStrFn) 
        Mine.HintMsg = MyContext.HintMsg     
        if Mine.Num != -1:
            MyLine = "Bid " + X1.BidStr(Mine.Num)
            MyLine = MyLine  + " Type " + X1.BidTypeStr(Mine.Type)
            MyLine = MyLine  + " Suit " + X1.TrumpStr(Mine.Suit)
            MyLine = MyLine  + " SubType " + MyBidSubTypeStr
            MyLine = MyLine  + " Hint " + str(Mine.HintMsg) 
            ## MyDebug(DebugResolved, MyLine)
        ReturnMsg = MyContext.AddBid(Mine)
        MyFn = X1.SystemStr(MyContext.Teams[MyTeam].System) + ".GetBidExpPts(Mine, MyContext)"
        MyMinExpPts, MyMaxExpPts = eval(MyFn)
        MyFn = X1.SystemStr(MyContext.Teams[MyTeam].System) + ".GetBidExpLen(Mine, MyContext)"
        Thing = eval(MyFn)
        MyContext.Players[MyContext.CurrentPlayer].UpdateExpLen(Thing)
        MyContext.Players[MyContext.CurrentPlayer].MinExpPts = MyContext.Players[MyContext.CurrentPlayer].MinExpPts + MyMinExpPts
        MyContext.Players[MyContext.CurrentPlayer].MaxExpPts = MyContext.Players[MyContext.CurrentPlayer].MaxExpPts + MyMaxExpPts
        if MyContext.KeepBidding == False:
            if MyContext.TossIn:
                return MyContext, ReturnMsg
            DefendTeam = X1.GetTeam(MyContext.Leader)
            MyContext.Teams[DefendTeam].UpdatePlayMode(X1.PlayModeDefend)
            MyContext.Teams[DefendTeam].UpdateTricksReqd(14 - MyContext.TricksReqd)
            AttackTeam = (DefendTeam + 1) % 2
            MyContext.Teams[AttackTeam].UpdatePlayMode(X1.PlayModeAttack)
            MyContext.Teams[AttackTeam].UpdateTricksReqd(MyContext.TricksReqd)
            return MyContext, ReturnMsg
        MyContext.BidCounter = MyContext.BidCounter + 1
        MyContext.CurrentPlayer = (MyContext.CurrentPlayer + 1) % 4
        MyContext.CurrentBidder = MyContext.CurrentPlayer
    return MyContext, ReturnMsg


def LoadPracticeDealRandomBidType(TheContext, TheSession):
##    print "LoadPracticeDealRandomBidType"
    TestCounter = 0
    for MyNum in range(10000):
        TheContext.Reset()
        KosherDeal, NewPack, TestString = X1.ShufflePack()
        if KosherDeal:
            TheContext.SetDealer(TheSession.Dealer)
            TheContext, MyNewMsg = BidPracticeHand(NewPack, TheContext)
            if TheContext.TossIn == False:
                SeatContinue = False
                if TheSession.Type == X1.PracticeTypeDeclarer:                
                    if TheContext.Declarer == TheContext.User.Seat:
                        SeatContinue = True
                if TheSession.Type == X1.PracticeTypeDefender:                
                    if ((TheContext.Declarer + 3) % 4) == TheContext.User.Seat:
                        SeatContinue = True
                if SeatContinue:
                    TheSession.Declarer = TheContext.Declarer
                    TheSession.Player = TheContext.User.Seat
                    ContinueLevel = True                
                    ContinueSuit = True
                    MyTeam = X1.GetTeam(TheContext.Declarer)
                    if TheSession.BidType == X1.PracticeBidTypeControl:
                        MyVal = GetDealByBidType(TheContext, MyTeam, X1.BidTypeRespControlQuery)
                    if TheSession.BidType == X1.PracticeBidTypeBlackwood:
                        MyVal = GetDealByBidType(TheContext, MyTeam, X1.BidTypeReplyBlackwoodAceAsk)
                    if TheSession.BidType == X1.PracticeBidTypeGerber:
                        MyVal = GetDealByBidType(TheContext, MyTeam, X1.BidTypeReplyGerberAceAsk)
                    if TheSession.BidType == X1.PracticeBidTypeLimit:
                        MyVal = GetDealByBidType(TheContext, MyTeam, X1.BidTypeReplyLimitHonourAsk)
                    if TheSession.BidType == X1.PracticeBidTypeSustain:
                        MyVal = GetDealByBidType(TheContext, MyTeam, X1.BidTypeCallSustain)
                    if MyVal:
                        return True, NewPack, TheContext.Declarer, TheContext.Contract, MyNum  
    return False, NewPack, -1, -1, -1



def LoadPracticeDealRandom(TheContext, TheSession):
    if TheSession.BidType != X1.PracticeBidTypeNone:
        MyLoad, MyPack, MyDeclarer, MyContract, MyGetDealNum = LoadPracticeDealRandomBidType(TheContext, TheSession)
        return MyLoad, MyPack, MyDeclarer, MyContract, MyGetDealNum

    TestCounter = 0
    for MyNum in range(10000):
        TheContext.Reset()
        KosherDeal, NewPack, TestString = X1.ShufflePack()
        if KosherDeal:
            TheContext.SetDealer(TheSession.Dealer)
            TheContext, MyNewMsg = BidPracticeHand(NewPack, TheContext)
            if TheContext.TossIn == False:
                SeatContinue = False
                if TheSession.Type == X1.PracticeTypeDeclarer:                
                    if TheContext.Declarer == TheContext.User.Seat:
                        SeatContinue = True
                if TheSession.Type == X1.PracticeTypeDefender:                
                    if ((TheContext.Declarer + 3) % 4) == TheContext.User.Seat:
                        SeatContinue = True
                if SeatContinue:
                    TheSession.Declarer = TheContext.Declarer
                    TheSession.Player = TheContext.User.Seat
                    ContinueLevel = False
                    if TheSession.LevelInterest == False:
                        ContinueLevel = True                
                    ContinueSuit = False
                    if TheSession.SuitInterest == False:
                        ContinueSuit = True                            
                    if TheContext.Contract >= TheSession.MinBidNum:
                        if TheContext.Contract <= TheSession.MaxBidNum:
                            if TheSession.LevelInterest == True:
                                ContinueLevel = True
                    if ContinueLevel:
                        MySuit = False
                        MyVal = True    
                        if TheSession.Suit == X1.PracticeSuitMajors:
                            if TheContext.Trumps == X1.SuitSpades:
                                MySuit = True
                            if TheContext.Trumps == X1.SuitHearts:
                                MySuit = True
                        if TheSession.Suit == X1.PracticeSuitMinors:
                            if TheContext.Trumps == X1.SuitDiamonds:
                                MySuit = True
                            if TheContext.Trumps == X1.SuitClubs:
                                MySuit = True
                        if TheSession.Suit == X1.PracticeSuitNoTrumps:
                            if TheContext.NoTrumps == True:
                                MySuit = True
                        if MySuit == False:
                            if ContinueSuit == True:
                                MySuit = True                        
                        if MySuit:
                            return True, NewPack, TheContext.Declarer, TheContext.Contract, MyNum  
    return False, NewPack, -1, -1, -1

def PrintPlayedCards(MyContext):
    GeneralPad = "    "
    MyLines = ""
    MyLine = GeneralPad
    for MyPlayer in range(7):
        MyLine = MyLine + string.center(X1.PlayerStr(MyPlayer % 4), 7)
    MyLines = MyLines + MyLine + "\n"
    for MyTrick in range(MyContext.CurrentTrick):
        for MyCount in range(4):
            MyLine = GeneralPad
            for Things in range(MyContext.PlayedTricks[MyTrick].PlayedCard[0].Owner):
                MyLine = MyLine + string.ljust("", 7)                
            MyLine = MyLine + string.center(X1.CardStr(MyContext.PlayedTricks[MyTrick].PlayedCard[0].Num), 7)
            MyLine = MyLine + string.center(X1.CardStr(MyContext.PlayedTricks[MyTrick].PlayedCard[1].Num), 7)
            MyLine = MyLine + string.center(X1.CardStr(MyContext.PlayedTricks[MyTrick].PlayedCard[2].Num), 7)
            MyLine = MyLine + string.center(X1.CardStr(MyContext.PlayedTricks[MyTrick].PlayedCard[3].Num), 7)
        MyLines = MyLines + MyLine + "\n"
        for MyCount in range(4):
            MyLine1 = GeneralPad
            for Things in range(MyContext.PlayedTricks[MyTrick].PlayedCard[0].Owner):
                MyLine1 = MyLine1 + string.ljust("", 7)
            for SecondTest in range(MyCount):
                MyLine1 = MyLine1 + string.ljust("", 7)   
            MyLine = MyLine1 + MyContext.PlayedTricks[MyTrick].PlayedCard[MyCount].HintMsg
            MyLines = MyLines + MyLine + "\n"            
    return MyLines

def PrintBids(MyContext):
    GeneralPad = "    "
    MyLine = GeneralPad
    for x in range(4):
        MyLine = MyLine + string.center(X1.PlayerStr(x), 7)
    MyLine = MyLine + "\n"
    InitLine = GeneralPad
    B1 = string.ljust("", 7)
    for Things in range(MyContext.Dealer):
        InitLine = InitLine + B1
    MyCounter = MyContext.Dealer
    for Things in MyContext.Bids:
        InitLine = InitLine + string.center(X1.BidStr(Things.Num), 7)
        MyCounter = MyCounter + 1
        if (MyCounter % 4) == 0:
            MyLine = MyLine + InitLine + "\n"
            InitLine = GeneralPad
    for Things in MyContext.Bids:
        InitLine = str(Things.SubType) +  " ... " + Things.HintMsg
        MyLine = MyLine + InitLine + "\n"
    return MyLine
            
def PrintShortSuit(MyPlayer, MySuit, MyContext):
    ReturnHand = X1.SuitLtr(MySuit) + ":"
    for MyCards in MyContext.DealtPack:
        if MyCards.Owner == MyPlayer:
            if MyCards.Suit == MySuit:
                ReturnHand = ReturnHand + X1.PipStr((MyCards.Num % 13))
    return ReturnHand

def PrintHand(MyHand):
    ReturnHand = ""
    for MySuit in range(4):
        BackSuit = 3 - MySuit
        MyStr = X1.SuitStr(BackSuit) + ":"
        for MyCards in MyHand:
            TheSuit = int(MyCards / 13)
            if TheSuit == BackSuit:
                MyStr = MyStr + X1.PipStr((MyCards / 13))
            ReturnHand = ReturnHand + MyStr + "\n"
    return ReturnHand

def ConvertPartnerExpLen(PartnerExpLen):
    SuitInit = ["S:", "H:", "D:", "C:"]
    ReturnStr = "["
    for x in range(4):
        MyCounter = X1.ReserveCounter[x]
        ReturnStr = ReturnStr + SuitInit[x]
        ReturnStr = ReturnStr + str(PartnerExpLen[MyCounter])
        if x < 3:
            ReturnStr = ReturnStr + ", "
    ReturnStr = ReturnStr + "]"
    return ReturnStr

class NotSimpleGridHeading(GridLib.Grid):
    def __init__(self, parent, MyContext):
        GridLib.Grid.__init__(self, parent, -1)
        self.MyFont = self.GetFont()
        if MyContext.Format == X1.FormatBig:
            self.MyFont.SetPointSize(11)
        if MyContext.Format == X1.FormatSmall:
            self.MyFont.SetPointSize(8)
        self.CreateGrid(0, 4)
        self.SetColSize(0, 22)
        self.SetColSize(1, 22)
        self.SetColSize(2, 22)
        self.SetColSize(3, 22)
        self.SetColLabelValue(0, "N")
        self.SetColLabelValue(1, "E")
        self.SetColLabelValue(2, "S")
        self.SetColLabelValue(3, "W")
        self.HideRowLabels()
        return

class SimpleGrid(GridLib.Grid):
    def __init__(self, parent, MyContext):
        GridLib.Grid.__init__(self, parent, -1)
        self.MyFont = self.GetFont()
        if MyContext.Format == X1.FormatBig:
            self.MyFont.SetPointSize(11)
        if MyContext.Format == X1.FormatSmall:
            self.MyFont.SetPointSize(8)
        self.CreateGrid(13, 2)
        if MyContext.ShowPlayed == False:
            self.SetColSize(0, 105)
            self.SetColSize(1, 235)
        if MyContext.ShowPlayed == True:
            self.SetColSize(0, 70)
            self.SetColSize(1, 185)
        for x in range(13):
            self.SetRowSize(x, 35)
            self.SetReadOnly(x, 0, True)
            self.SetReadOnly(x, 1, True)
        self.RowNum = 0
        self.SetColLabelValue(0, "Won by")
        self.SetColLabelValue(1, "--- Comments ---")
        self.HideRowLabels()
        return

    def Reset(self):
        self.ClearGrid()
        self.RowNum = 0
        self.SetColLabelValue(0, "Won by")
        self.SetColLabelValue(1, "--- Comments ---")
        return
    
    def UpdateColumns(self, WonBy, WonByColour, Comments, CommentsColour):
        self.SetCellTextColour(self.RowNum, 0, WonByColour)
        self.SetCellValue(self.RowNum, 0, WonBy)
        self.SetCellFont(self.RowNum, 0, self.MyFont)

        self.SetCellTextColour(self.RowNum, 1, CommentsColour)
        self.SetCellValue(self.RowNum, 1, Comments)
        self.SetCellFont(self.RowNum, 1, self.MyFont)
        self.RowNum = self.RowNum + 1
        return

def MyDebug(MyLevel, MyMsg):
    if MyLevel != DebugTime:
        return
    TotalStr = ModuleName + str(MyLevel) + " " + str(MyMsg)
    print TotalStr
    return

## Another thing to draw the Table
class XThing:
    def __init__(self, Num, bmp):
        self.Num = Num
        self.bmp = bmp
        self.Position = (0,0)
        self.Altbmp = bmp
        self.Shown = True
        return

    def Draw(self, dc, op = wx.COPY):
        if self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)
            dc.Blit(self.Position[0], self.Position[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)
            return True
        else:
            return False

    def UpdateAltbmp(self, bmp):
        self.Altbmp = bmp
        return
    
    def AltDraw(self, dc, op = wx.COPY):
        if self.Altbmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.Altbmp)
            dc.Blit(self.Position[0], self.Position[1],
                    self.Altbmp.GetWidth(), self.Altbmp.GetHeight(),
                    memDC, 0, 0, op, True)
            return True
        else:
            return False

class ShowBid(wx.Panel):
    def __init__(self, parent, id, MyContext):
        wx.Panel.__init__(self, parent, id, style=wx.RAISED_BORDER)
        MyFont = self.GetFont()
        MyButtonHeight = 25
        if MyContext.Format == X1.FormatBig:
            self.SetPosition((970, 50))
            MyFont.SetPointSize(11)
        if MyContext.Format == X1.FormatSmall:
            MyButtonHeight = 20
            self.SetPosition((470, 50))
            MyFont.SetPointSize(8)
        self.MyContext = MyContext
        self.parent = parent
        self.PlayerLabels = []
        self.BidButtons = []
        MyFont3 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD)        
        self.MyContract = wx.StaticText(self, -1, MyContext.FullContract)
        self.MyContract.SetFont(MyFont3)
        for i in range(4):
            self.PlayerLabels.append(wx.Button(self, -1, X1.PlayerStr(i), size=(81, MyButtonHeight)))
            self.PlayerLabels[i].SetBackgroundColour(wx.Colour(250,128,114))
        i = 0
        for Things in MyContext.Bids:
            self.BidButtons.append(wx.Button(self, -1, X1.BidStr(Things.Num), size=(81, MyButtonHeight)))
            self.BidButtons[i].SetBackgroundColour("cyan")
            self.BidButtons[i].Enable(True)
            self.BidButtons[i].SetFont(MyFont)
            i = i + 1
        MyRows = 2 + int(i / 4)
        self.MySizer = wx.GridBagSizer(MyRows, 4)
        self.MySizer.SetHGap(5)
        self.MySizer.SetVGap(5)
        for x in range(4):
            self.MySizer.Add(self.PlayerLabels[x], (0, x), wx.DefaultSpan,  wx.ALIGN_LEFT|wx.ALIGN_RIGHT|wx.ALIGN_TOP, border=15)
        x = 0
        for Things in MyContext.Bids:
            MyRow = 1 + int((MyContext.Dealer + x) / 4)
            MyCol = Things.Owner
            self.MySizer.Add(self.BidButtons[x], (MyRow, MyCol), wx.DefaultSpan,  wx.ALIGN_LEFT|wx.ALIGN_RIGHT, border=15)
            x = x + 1
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox0 = wx.BoxSizer(wx.VERTICAL)
        self.vbox1 = wx.BoxSizer(wx.VERTICAL)
        self.vbox2 = wx.BoxSizer(wx.VERTICAL)
        self.vbox3 = wx.BoxSizer(wx.VERTICAL)
        self.vbox1.Add(self.MySizer, 0, wx.ALIGN_CENTER)
        self.vbox0.Add(self.MyContract, 0, wx.ALIGN_CENTER)
        self.MyGrid = SimpleGrid(self, MyContext)
        if MyContext.ShowPlayed == False:
            self.vbox2.Add(self.MyGrid, 0, wx.ALIGN_CENTER)

        if MyContext.ShowPlayed == True:
            self.hbox23 = wx.BoxSizer(wx.HORIZONTAL)
            self.hbox23.Add(self.MyGrid, 0, wx.ALIGN_LEFT)
            vbox10 = wx.BoxSizer(wx.VERTICAL)
            Mine = NotSimpleGridHeading(self, MyContext)
            self.LoopArray = []
            self.MyGrid1 = wx.GridSizer(13, 4, 0, 0)
            for MyCard in range(52): 
                LoopButton = wx.BitmapButton(self, -1, wx.Bitmap('Cards/M99.png'), size=(-1, 35), style=wx.NO_BORDER)
                LoopButton.Show(True)
                self.LoopArray.append(LoopButton)
                self.MyGrid1.Add(LoopButton,0,wx.EXPAND)
            vbox10.Add(Mine, 0, wx.ALIGN_CENTER)
            vbox10.Add(self.MyGrid1, 0, wx.ALIGN_CENTER)
            self.hbox23.Add(vbox10, 0, wx.ALIGN_LEFT)
            self.vbox2.Add(self.hbox23, 0, wx.ALIGN_CENTER)
        self.Slider1 = wx.Slider(self, -1, 0, 0, 13, size=(330,50), style=wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.Slider1.SetTickFreq(1)
        self.Slider1.Disable()
        self.Slider2 = wx.Slider(self, -1, 0, 0, 13, size=(330,50), style=wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.Slider2.SetTickFreq(1)
        self.Slider2.Disable()
        self.vbox3.Add(self.Slider1, 0, wx.ALIGN_CENTER)
        self.vbox3.Add(self.Slider2, 0, wx.ALIGN_CENTER)
        self.vbox.Add(self.vbox1, 0, wx.ALIGN_CENTER)
        self.vbox.Add(self.vbox0, 0, wx.ALIGN_CENTER)
        self.vbox.Add(self.vbox2, 0, wx.ALIGN_CENTER)
        self.vbox.Add(self.vbox3, 0, wx.ALIGN_CENTER)
        self.SetSizerAndFit(self.vbox)
        self.SetBackgroundColour("white")
        self.Show()        
        return

    def NotSimpleGrid(self, MyContext):
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        Mine = NotSimpleGridHeading(self, MyContext)
        self.LoopArray = []
        gs = wx.GridSizer(13, 4, 0, 0)	
        for MyCard in range(52): 
            LoopButton = wx.BitmapButton(self, -1, wx.Bitmap('Cards/M' + str(MyCard) + '.png'))
            LoopButton.Show(True)
            self.LoopArray.append(LoopButton)
            gs.Add(LoopButton,0,wx.EXPAND)
            
        vbox1.Add(Mine, 0, wx.ALIGN_CENTER)
        vbox1.Add(gs, 0, wx.ALIGN_CENTER)
        return vbox1

    def UpdatePlayedCards(self, MyContext):
        for x in range(52):
            self.LoopArray[x].Show(False)
        MyCounter = 0
        for MyTrick in range(MyContext.CurrentTrick):
            MyNorth = -1
            MyEast = -1
            MySouth = -1
            MyWest = -1         
            for MyCount in range(4):
                MyCard = MyContext.PlayedTricks[MyTrick].PlayedCard[MyCount].Num           
                MyOwner = MyContext.PlayedTricks[MyTrick].PlayedCard[MyCount].Owner
                if MyOwner == 0:
                    MyNorth = MyCard
                if MyOwner == 1:
                    MyEast = MyCard
                if MyOwner == 2:
                    MySouth = MyCard
                if MyOwner == 3:
                    MyWest = MyCard
            self.LoopArray[MyCounter].SetBitmap(wx.Bitmap('Cards/M' + str(MyNorth) + '.png'))
            self.LoopArray[MyCounter].Show(True)
            MyCounter = MyCounter + 1
            self.LoopArray[MyCounter].SetBitmap(wx.Bitmap('Cards/M' + str(MyEast) + '.png'))
            self.LoopArray[MyCounter].Show(True)
            MyCounter = MyCounter + 1
            self.LoopArray[MyCounter].SetBitmap(wx.Bitmap('Cards/M' + str(MySouth) + '.png'))
            self.LoopArray[MyCounter].Show(True)
            MyCounter = MyCounter + 1
            self.LoopArray[MyCounter].SetBitmap(wx.Bitmap('Cards/M' + str(MyWest) + '.png'))
            self.LoopArray[MyCounter].Show(True)
            MyCounter = MyCounter + 1
        return
    
    def UpdateGrid(self, WonBy, WonByColour, Comments, CommentsColour):
        self.MyGrid.UpdateColumns(WonBy, WonByColour, Comments, CommentsColour)
        return

    def Reset(self):
        self.MyGrid.Reset()
        self.Slider1.SetValue(0)
        self.Slider2.SetValue(0)
        return

    def UpdateToTrickNumber(self, TrickNumber, MyContext):
        for Count in range(TrickNumber):
            WonBy = MyContext.PlayedTricks[Count].Winner
            WonByColour = MyContext.PlayedTricks[Count].WonByColour
            Comments = MyContext.PlayedTricks[Count].CommentStr
            CommentsColour = MyContext.PlayedTricks[Count].CommentColour
            self.MyGrid.UpdateColumns(X1.PlayerStr(WonBy), WonByColour, Comments, CommentsColour)
            self.UpdateSliders(WonBy)
        return

    def UpdateSliders(self, MyPlayer):
        MyTeam = X1.GetTeam(MyPlayer)
        if X1.GetTeam(self.MyContext.Declarer) == MyTeam:
            MyVal = self.Slider1.GetValue() + 1
            self.Slider1.SetValue(MyVal)
            return
        MyVal = self.Slider2.GetValue() + 1
        self.Slider2.SetValue(MyVal)
        return

class ShowHand(wx.Panel):
    def __init__(self, parent, id, MyContext, MyPracticeSession):
##        print "Mode " + str(MyContext.PBNMode)
##        if MyContext.PBNMode:
##            print "Play " + str(MyContext.PBNPlay)
        
        self.StartMsg = "Hello"
        self.Width = SizeDefaultX
        self.Height = SizeDefaultY - 50
        PanelPosX = 0
        PanelPosY = 0
        self.OldBitmap = None
        self.ClaimHand = False
        self.StepByStep = True
        self.Session = MyPracticeSession
        MessagePosX = 30
        MessagePosY = 60
        self.MyMessagePos = (MessagePosX, MessagePosY)
        wx.Panel.__init__(self, parent, id, pos=((PanelPosX, PanelPosY)), size=(self.Width, self.Height))
        self.parent = parent
        self.parent.ShowHandOpen = True
        self.SPC = MyContext
##        print "ShowHumans " + str(self.SPC.Human)
        self.SetBackgroundColour("green")
        self.OtherThingy = None
        self.ShowBidThingy = None
        self.FlipNames = []
        self.TestPack = []
        self.Printed = False
        if MyContext.Format == X1.FormatBig:
            self.CardHint = wx.BitmapButton(self, -1, wx.Bitmap('Buttons/CardHint.png'), style=wx.NO_BORDER)
        if MyContext.Format == X1.FormatSmall:
            self.CardHint = wx.BitmapButton(self, -1, wx.Bitmap('Buttons/MiniCardHint.bmp'), style=wx.NO_BORDER)
            self.CardHint.SetToolTipString("Hello Sailor info")
        self.CardHint.Bind(wx.EVT_BUTTON, self.OnCardHint)
        self.CardHint.Bind(wx.EVT_ENTER_WINDOW, self.CardHintMouseOver)
        self.CardHint.Bind(wx.EVT_LEAVE_WINDOW, self.CardHintMouseLeave)        
        self.CardHint.Enable(False)
        self.CardHint.Show(False)
        self.CardHintFn = ""
        self.CardHintBool = False
##        self.SaveDeal = wx.BitmapButton(self, -1, wx.Bitmap('Buttons/StartButton.bmp'), pos=(1350,50))
##        self.SaveDeal.Bind(wx.EVT_BUTTON, self.OnStartTest)
        self.DealtPack = []
        self.Players = []
        self.PlayedTricks = []
        self.LedSuit = -1                   
        self.DragPlayingCardImage = None
        self.DragPlayingCard = None
        if MyContext.Format == X1.FormatBig:
            bmp = wx.Bitmap('Things/Table.png')
        if MyContext.Format == X1.FormatSmall:
            bmp = wx.Bitmap('Things/NewTable.png')
        TheThing = XThing(4, bmp)
        if MyContext.Format == X1.FormatBig:
            TheThing.Position = (X1.TableTopX, X1.TableTopY)
        if MyContext.Format == X1.FormatSmall:
            TheThing.Position = (X1.MiniTableTopX, X1.MiniTableTopY)
        self.TheTable = TheThing
        self.ResumePlaySlider = wx.Slider(self, -1, 0, 0, 13, size=(340,50), style=wx.SL_AUTOTICKS | wx.SL_LABELS)
        if MyContext.Format == X1.FormatBig:
            self.ResumePlaySlider.SetPosition((40, 860))          
        if MyContext.Format == X1.FormatSmall:
            self.ResumePlaySlider.SetPosition((40, 860))
        self.ResumePlaySlider.SetTickFreq(1)
        self.ResumePlaySlider.Bind(wx.EVT_SLIDER, self.OnResumePlaySlider)
        self.ResumePlaySlider.Show(False)
        font = wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD )
        self.ResumePlay = wx.Button(self, -1, "Resume Play at Trick Number", size=(340,35))
        if MyContext.Format == X1.FormatBig:
            self.ResumePlay.SetPosition((40, 920))          
        if MyContext.Format == X1.FormatSmall:
            self.ResumePlay.SetPosition((40, 920))
        self.ResumePlay.SetFont(font)
        self.ResumePlay.Show(False)
        self.ResumePlay.Enable(False)
        self.ResumePlay.Bind(wx.EVT_BUTTON, self.OnResumePlay)
        bmp = wx.Bitmap('Things/Claim.png')
        self.ClaimButton = wx.BitmapButton(self, -1, bmp, pos=(400, 920))
        self.ClaimButton.Show(False)
        self.ClaimButton.Enable(False)
        self.ClaimButton.Bind(wx.EVT_BUTTON, self.OnClaimButton)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDoubleClick)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        return

    def OnResultPanelOkay(self):
##        print "OnResultPanelOkay"
        self.ResultPanel.Hide()
        self.parent.ResetScore(self.SPC.User.UserName)
        self.parent.ShowHandOpen = False
        self.ClaimButton.Show(False)
        self.ClaimButton.Enable(False)
        self.ResumePlay.Enable(True)
        self.ClaimHand = False
        self.StepByStep = True
        return

    def CardHintMouseOver(self, event):
        self.OldBitmap = self.CardHint.GetBitmap()
##        self.OldSize = self.CardHint.GetSize()
        
        self.CardHintBool = True
        X = eval(self.CardHintFn)
        self.CardHintBool = False
        if X != -1:            
            bmp = wx.Bitmap('Cards/M' + str(X) + '.png')
            self.CardHint.SetBitmap(bmp)
##            self.CardHint.SetSize(self.OldSize)
        self.CardHint.SetToolTipString(self.SPC.HintMsg)
        event.Skip()
        
    def CardHintMouseLeave(self, event):
        self.CardHint.SetBitmap(self.OldBitmap)
        self.CardHint.SetToolTipString("Information")
        event.Skip()

    
    def OnClaimButton(self, evt):
        self.StepByStep = False
        self.ClaimHand = True
        self.PTCStep1(0)
        self.ClaimButton.Enable(False)
        return

    def OnResumePlay(self, evt):
        self.ShowBidsThingy.Reset()
        MyTrickNumber = self.ResumePlaySlider.GetValue()
        self.ShowBidsThingy.UpdateToTrickNumber(MyTrickNumber, self.SPC)
        MyFileName = "Pickle/" + self.SPC.PickleName + "_" + str(MyTrickNumber) + ".p"
        self.SPC = pickle.load(open(MyFileName, "rb" ))
        if self.SPC.ShowPlayed == True:
            self.ShowBidsThingy.UpdatePlayedCards(self.SPC)
        for Things in self.DealtPack:
            Things.ResumeValues(self.SPC.DealtPack, self.SPC)
        self.LedSuit = -1
        self.ClaimButton.Enable(True)
        self.parent.ResumeContext(self.SPC)
        self.Refresh()
        self.PTCStep1(0)
        return

    def OnResumePlaySlider(self, evt):
        MaxVal = self.SPC.CurrentTrick
        MyVal = self.ResumePlaySlider.GetValue()
        if MyVal >= MaxVal:
            self.ResumePlaySlider.SetValue(MaxVal)
            return
        return

    def ShowHandInit(self, MyPack):
        self.DealtPack = []
        self.Players = []
        self.PlayedTricks = []
        self.LedSuit = -1
        self.ResumePlaySlider.SetValue(0)
        self.ResumePlaySlider.Enable(False)
        if self.SPC.Practice:
##            print "PracticeMode"
            self.TestPack = MyPack
            self.parent.TestPack = self.TestPack
            self.SPC.SetFlatPack(self.TestPack)
            self.SPC.SetPracticeSystem(self.SPC.User.System)
            ## MyDebug(DebugResolved, "SSS " + str(self.SPC.User.System))
            self.Session.PrintPracticeSession()
            ## MyDebug(DebugResolved, "Practice makes perfect")
        if self.SPC.Review:
            self.TestPack = MyPack
            self.parent.TestPack = self.TestPack
            self.SPC.SetPracticeSystem(self.SPC.User.System)

        if self.SPC.PBNMode:
            self.TestPack = MyPack
            self.parent.TestPack = self.TestPack

        if self.SPC.PBNMode == False:            
            if self.SPC.Practice == False:
                if self.SPC.Review == False:
                    KosherDeal = False
                    ## MyDebug(DebugResolved, "LoopTest  " + str(self.SPC.LoopTest))
    ##                print "Shuffling"
                    KosherDeal, self.TestPack, TestString = X1.ShufflePack()
    ##                KosherDeal = True
    ##                TestString = "GG"
    ####
    ##                self.TestPack = [11, 46, 41, 25, 12, 22, 4, 50, 23, 51, 24, 33, 39, 6, 8, 36, 15, 48, 21, 13, 20, 49, 34, 27, 30, 18, 44, 3, 42, 5, 7, 38, 35, 19, 2, 0, 28, 45, 10, 14, 17, 37, 16, 40, 32, 31, 43, 47, 1, 26, 9, 29]

    ##
    ## Alt Technology                
    ##              KosherDeal, NewSession = SessionDeals.GetSessionDeal(21)
    ##              self.TestPack = NewSession.Pack
    ##              self.SPC.Dealer = NewSession.Dealer                
                    self.parent.TestPack = self.TestPack
                    if KosherDeal == False:
                        Msg = "Something wrong with the deal. No touching!"
                        Hello = X1.MyMessage(self, Msg, X1.XXBridgeThing, self.MyMessagePos, wx.OK, wx.ICON_ERROR)
                        return -1
        PickleData = cPickle.dumps(self.TestPack, cPickle.HIGHEST_PROTOCOL)
        Cursor.execute("INSERT INTO " + self.SPC.TableName + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                        (self.SPC.Uniquer, str(-1), -1, -1, -1, -1, -1, -1,
                        -1, str(-1), -1, 0, 0, str(self.TestPack), sqlite3.Binary(PickleData),
                         str(-1), self.SPC.User.UserName, self.SPC.User.Seat, self.SPC.Uniquer))
        DataBase.commit()    
        UpdateUserHandsDealt(self.SPC.User.Uniquer)
        for x in range(4):
            MyPlayer = P1.Player(x)
            self.Players.append(MyPlayer)
        for x in range(4):        
            self.Players[x].Name = X1.PlayerStr(x)
            self.Players[x].InitHands()
            self.Players[x].UpdateHand(self.TestPack)
            self.Players[x].SortHands()
        if self.SPC.Format == X1.FormatBig:
            for x in range(4):
                StartPosX, StartPosY = X1.GetCheatStartPos(x, self.SPC)
                PosX = StartPosX[x]
                PosY = StartPosY[x]
                for MyCard in range(13):
                    MyCount = self.Players[x].SortHand[MyCard]
                    bmp = wx.Bitmap('Cards/' + str(MyCount) + '.png')
                    TheCard = X1.PlayingCard(bmp, MyCount, self.SPC.Format)
                    TheCardXX = X1.MiniPlayingCard(MyCount)
                    WK = X1.WorkCard(MyCount, (MyCount % 13))
                    WK.Owner = x
                    WK.HandLoc = MyCard
                    TheCard.Owner = x
                    TheCard.HandLoc = MyCard
                    TheCardXX.Owner = x
                    TheCardXX.HandLoc = MyCard
                    if self.SPC.Human[x] == False:
                        if self.SPC.Cheat[x] == False:
                            TheCard.SetXXBitmap(False, False)
                    if MyCard == 12:
                        TheCard.Exposed = True
                        TheCardXX.Exposed = True
                    MineX, MineY = X1.GetCheatSep(x, self.SPC)
                    PosX = PosX + MineX[x]
                    PosY = PosY + MineY[x]
                    TheCard.Position = (PosX, PosY)
                    TheCardXX.Position = (PosX, PosY)
                    WK.Position = (PosX, PosY)
                    self.DealtPack.append(TheCard)
                    self.SPC.DealtPack.append(TheCardXX)
                    self.Players[x].InitPoints(TheCard)
                    self.SPC.WorkPack.append(WK)
            for x in range(4):
                self.SPC.AddPlayer(self.Players[x])
                self.SPC.Players[x].UpdateDPs()
                self.SPC.Players[x].UpdateLPs()
                self.SPC.Players[x].UpdateLTC()
                self.SPC.Players[x].PrintPlayer()
            for x in range(4):
                AltCount = (x + 2) % 4
                Val = "V"
                if x == 0 or x == 2:
                    Val = "H"
                MyFile = 'Things/' + X1.PlayerStr(x) + str(Val) + '.png'
                bmp = wx.Bitmap(MyFile)
                TheThing = XThing(10 + x, bmp)
                TheThing.Position = (X1.FlipNamePosX[x], X1.FlipNamePosY[x])
                MyAltFile = 'Things/' + X1.PlayerStr(AltCount) + str(Val) + '.png'
                Altbmp = wx.Bitmap(MyAltFile)
                TheThing.UpdateAltbmp(Altbmp)
                self.FlipNames.append(TheThing)
            return

        if self.SPC.Format == X1.FormatSmall:
            for x in range(4):
                MySuit = -1
                SuitCount = 0
                MyMiniRow = 0
                MyMiniCol = 0
                for MyCard in range(13):
                    MyCount = self.Players[x].SortHand[MyCard]
                    bmp = wx.Bitmap('Cards/M' + str(MyCount) + '.png')
                    TheCard = X1.PlayingCard(bmp, MyCount, self.SPC.Format)
                    TheCardXX = X1.MiniPlayingCard(MyCount)
                    WK = X1.WorkCard(MyCount, (MyCount % 13))
                    if MySuit != TheCard.Suit:
                        MySuit = TheCard.Suit
                        SuitCount = 0
                    MyMiniRow = X1.SuitOrder[TheCard.Suit]
                    MyMiniCol = SuitCount
                    WK.Owner = x
                    WK.HandLoc = MyCard
                    TheCard.Owner = x
                    TheCard.HandLoc = MyCard
                    TheCardXX.Owner = x
                    TheCardXX.HandLoc = MyCard
                    if self.SPC.Human[x] == False:
                        if self.SPC.Cheat[x] == False:
                            TheCard.SetXXBitmap(False, False)
                            MyMiniRow = int(MyCard / 5)
                            MyMiniCol = MyCard % 5
                    PosX = OrigPosSmallX[x] + (MyMiniCol * 15)
                    PosY = OrigPosSmallY[x] + (MyMiniRow * 32)
                    TheCard.Position = (PosX, PosY)
                    TheCardXX.Position = (PosX, PosY)
                    WK.Position = (PosX, PosY)
                    self.DealtPack.append(TheCard)
                    self.SPC.DealtPack.append(TheCardXX)
                    self.Players[x].InitPoints(TheCard)
                    self.SPC.WorkPack.append(WK)
                    SuitCount = SuitCount + 1
            for x in range(4):
                self.SPC.AddPlayer(self.Players[x])
                self.SPC.Players[x].UpdateDPs()
                self.SPC.Players[x].UpdateLPs()
                self.SPC.Players[x].UpdateLTC()
                self.SPC.Players[x].PrintPlayer()
            return
        return

    def UpdateUserPositions(self):
        MyUniquer = self.SPC.User.Uniquer
        MyReviewPosX = 0
        MyReviewPosY = 0
        MyScorePosX = 0
        MyScorePosY = 0
        MyDataBasePosX = 0
        MyDataBasePosY = 0
        MyPBNPosX = 0
        MyPBNPosY = 0

        if self.SPC.PBNMode == True:
            MyPBNPosX, MyPBNPosY = self.parent.PBNDialog.GetPosition()

        if self.SPC.DataBase == True:
            MyDataBasePosX, MyDataBasePosY = self.parent.DataBaseDialog.GetPosition()
        if self.SPC.Review == True:
            if self.SPC.DataBase == False:            
                MyReviewPosX, MyReviewPosY = self.parent.UserReviewDialog.GetPosition()
        if self.SPC.Score == True:
            MyScorePosX, MyScorePosY = self.parent.UserScoreDialog.GetPosition()
        Cursor.execute("UPDATE user SET ReviewPosX = ?, ReviewPosY = ?, ScorePosX = ?, \
                        ScorePosY = ?, DataBasePosX = ?, DataBasePosY = ?, PBNPosX = ?, PBNPosY = ? where Uniquer = ?;",
                       (MyReviewPosX, MyReviewPosY, MyScorePosX, MyScorePosY, MyDataBasePosX, MyDataBasePosY, MyPBNPosX, MyPBNPosY, MyUniquer))
        DataBase.commit()
        return
        
    def UpdateResumePlaySlider(self):
        MyVal = self.ResumePlaySlider.GetValue() + 1
        self.ResumePlaySlider.SetValue(MyVal)
        return
           
    def PTCInit(self, Msg, PlayCounter, DummyVisible):
        ## MyDebug(DebugResolved, Msg)
        ## MyDebug(DebugResolved, "PTCInit PlayCounter " + str(PlayCounter))        
        if DummyVisible == False:
            self.ShowBidsThingy = ShowBid(self, -1, self.SPC)
        self.PTCStep1(PlayCounter)
        return
    
    def ShowDummy(self):
        ## MyDebug(DebugResolved, "ShowDummy " + X1.PlayerStr(self.SPC.Dummy))
        if self.SPC.Format == X1.FormatBig:
            for MyPlayingCard in self.DealtPack:
                if MyPlayingCard.Owner == self.SPC.Dummy:
                    MyPlayingCard.SetXXBitmap(True, False)
                    MyPlayingCard.UpdateFaceUp(True)
                    MyPlayingCard.UpdateShown(True)
            self.UpdateEntireHand(self.SPC.Dummy, True)
            return

        if self.SPC.Format == X1.FormatSmall:
            for MyPlayingCard in self.DealtPack:
                if MyPlayingCard.Owner == self.SPC.Dummy:
                    MyPlayingCard.SetXXNewBitmap(True, False)
                    MyPlayingCard.UpdateFaceUp(True)
                    MyPlayingCard.UpdateShown(True)
            self.UpdateEntireHand(self.SPC.Dummy, True)
            self.OnPaint(-1)
            return
        
    def PTCStep1(self, PlayerPos):
        if self.SPC.Format == X1.FormatBig:
            MyX = X1.CardHintPosX[self.SPC.CurrentPlayer]
            MyY = X1.CardHintPosY[self.SPC.CurrentPlayer]
        if self.SPC.Format == X1.FormatSmall:
            MyX = X1.MiniCardHintPosX[self.SPC.CurrentPlayer]
            MyY = X1.MiniCardHintPosY[self.SPC.CurrentPlayer]
        if self.SPC.ShowPlayHint:
            self.CardHint.SetPosition((MyX, MyY))
            self.CardHint.Enable(True)
            self.CardHint.Show(True)
        UseSlider = False
        for x in range(4):
            if self.SPC.Human[x] == True:
                UseSlider = True
        if UseSlider:
            self.ResumePlaySlider.Show(True)
            self.ResumePlay.Show(True)
        if PlayerPos == 0:
            if self.SPC.CurrentTrick == 13:
                self.CardHint.Enable(False)
                self.ResumePlay.Enable(False)
                self.CardHint.Show(False)
                self.ClaimButton.Enable(False)
                MyVal = X1.GetBidGamePts(self.SPC.CurrentBid, self.SPC.DoubleStatus)
                MyTricksWon = self.SPC.Teams[X1.GetTeam(self.SPC.Declarer)].TricksWon
                MyTricksReqd = self.SPC.Teams[X1.GetTeam(self.SPC.Declarer)].TricksReqd
                MyVariance = MyTricksWon - MyTricksReqd
                MyDeclarerSystem = self.SPC.Teams[X1.GetTeam(self.SPC.Declarer)].System
                MyNonDeclarerSystem = self.SPC.Teams[X1.GetTeam(self.SPC.LHO)].System
                MyBaseGameLevel = X1.BaseGameLevel(self.SPC.CurrentBid.Suit)
                self.SPC.ScoreInfo.UpdateScore(MyTricksWon, MyTricksReqd, self.SPC)
                MySuccess = False
                ## MyDebug(DebugResolved, "Team " + X1.TeamStr(self.SPC.ScoreInfo.WinningTeam) + " Above " + str(self.SPC.ScoreInfo.ContractAboveLine) + " Below " + str(self.SPC.ScoreInfo.ContractBelowLine))
                Msg = self.SPC.FullContract + " won by " + X1.TeamStr(self.SPC.ScoreInfo.WinningTeam)
                if self.SPC.ScoreInfo.WinningTeam == X1.GetTeam(self.SPC.Declarer):
                    MySuccess = True
                    Msg = Msg + " Points Below Line " + str(self.SPC.ScoreInfo.ContractBelowLine)
                    if self.SPC.ScoreInfo.ContractAboveLine != 0:
                        Msg = Msg + " Points Above Line " + str(self.SPC.ScoreInfo.ContractAboveLine)
                if self.SPC.ScoreInfo.WinningTeam != X1.GetTeam(self.SPC.Declarer):
                    Msg = Msg + " Points Above Line " + str(self.SPC.ScoreInfo.ContractAboveLine)             
                ## MyDebug(DebugResolved, Msg)
                MyResult = self.SPC.FullContract + " won by " + X1.TeamStr(self.SPC.ScoreInfo.WinningTeam)
##                print "Update " + str(self.SPC.TableName)
                Cursor.execute("UPDATE " + self.SPC.TableName + " SET Dealer = ?, Declarer = ?, Contract = ?, \
                                Result = ?, Success = ?, Tricks = ?, Variance = ?, System = ? where Uniquer = ?;",
                            (self.SPC.Dealer, self.SPC.Declarer, self.SPC.Contract, str(MyResult), MySuccess, MyTricksWon,
                             MyVariance, MyDeclarerSystem, self.SPC.Uniquer))
                DataBase.commit()
                UpdateUserHandsPlayed(self.SPC.User.Uniquer)
                self.UpdateUserPositions()
                if MySuccess:
                    UpdateUserHandsWon(self.SPC.User.Uniquer)
                Cursor.execute("SELECT * from score where UserName = ?", (self.SPC.User.UserName, ))
                MyUserNames = []
                Rows = Cursor.fetchall()
                RowCount = 0
                for Row in Rows:
                    FoundOne = True
                    MyUserNames.append(Row[0])
                    RowCount = RowCount + 1
                for Things in range(RowCount):
                    MyNS_Rubbers = self.SPC.ScoreInfo.Rubber[0]
                    MyEW_Rubbers = self.SPC.ScoreInfo.Rubber[1]
                    MyNS_Games = self.SPC.ScoreInfo.Game[0]
                    MyEW_Games = self.SPC.ScoreInfo.Game[1]
                    MyNS_AboveLine = self.SPC.ScoreInfo.AboveLine[0]
                    MyEW_AboveLine = self.SPC.ScoreInfo.AboveLine[1]
                    MyNS_BelowLine = self.SPC.ScoreInfo.BelowLine[0]
                    MyEW_BelowLine = self.SPC.ScoreInfo.BelowLine[1]
                    Cursor.execute("UPDATE score SET NS_Rubbers = ?, EW_Rubbers = ?, NS_Games = ?, EW_Games = ?, \
                                    NS_AboveLine = ?, EW_AboveLine = ?, NS_BelowLine = ?, EW_BelowLine = ? where Uniquer = ?;",
                            (MyNS_Rubbers, MyEW_Rubbers, MyNS_Games, MyEW_Games, MyNS_AboveLine, MyEW_AboveLine,
                             MyNS_BelowLine, MyEW_BelowLine, MyUserNames[Things]))
                    DataBase.commit()                
                if self.SPC.Practice:
                    MySuccess = False
                    if MyTricksWon >= MyTricksReqd:
                        MySuccess = True
                    MyLine = P2.PrintPlayedCards(self.SPC)
                    self.Session.WriteFile(MyLine)               
                    MyTeam = X1.GetTeam(self.SPC.Declarer)
                    MyResult = self.SPC.FullContract + " won by " + X1.TeamStr(self.SPC.ScoreInfo.WinningTeam)
##                    print "Update " + str(self.SPC.TableName)
                    Cursor.execute("UPDATE " + self.SPC.TableName + " SET Result = ?, Success = ?, Tricks = ?, Variance=? where Uniquer = ?;",
                                (str(MyResult), MySuccess, MyTricksWon, MyVariance, self.Session.Uniquer))
                    DataBase.commit()
                    MySuit = X1.PracticeSuitNoTrumps
                    MyLevel = X1.PracticeLevelPartScore
                    if self.SPC.Trumps == X1.SuitClubs:
                        MySuit = X1.PracticeSuitMinors
                    if self.SPC.Trumps == X1.SuitDiamonds:
                        MySuit = X1.PracticeSuitMinors
                    if self.SPC.Trumps == X1.SuitHearts:
                        MySuit = X1.PracticeSuitMajors
                    if self.SPC.Trumps == X1.SuitSpades:
                        MySuit = X1.PracticeSuitMajors
                    if self.SPC.Contract > X1.Bid5N:
                        MyLevel = X1.PracticeLevelSlam
                    if MySuit == X1.PracticeSuitMinors:
                        if self.SPC.Contract >= X1.Bid5C:
                            if self.SPC.Contract <= X1.Bid5D:
                                MyLevel = X1.PracticeLevelGame
                    if MySuit == X1.PracticeSuitMajors:
                        if self.SPC.Contract >= X1.Bid4H:
                            if self.SPC.Contract <= X1.Bid5S:
                                MyLevel = X1.PracticeLevelGame
                    if MySuit == X1.PracticeSuitNoTrumps:
                        if self.SPC.Contract >= X1.Bid3N:
                            if self.SPC.Contract <= X1.Bid5N:
                                MyLevel = X1.PracticeLevelGame
                    MyBidType = X1.GetPracticeBidType(self.SPC, X1.GetTeam(self.SPC.Declarer))
                    Cursor.execute("UPDATE " + self.SPC.TableName + " SET Level = ?, Suit = ?, BidType = ? where Uniquer = ?;",
                                (str(MyLevel), MySuit, MyBidType, self.Session.Uniquer))
                    DataBase.commit()
                self.ResultPanel = MyResultPanel(self, -1, self.SPC, MyResult)
                return
            if self.SPC.CurrentTrick == 0:
                Cursor.execute("UPDATE " + self.SPC.TableName + " SET Dealer = ?, Declarer = ?, Contract = ? where Uniquer = ?;",
                            (self.SPC.Dealer, self.SPC.Declarer, self.SPC.Contract, self.SPC.Uniquer))
                DataBase.commit()                
                if self.SPC.Human[self.SPC.Dummy] == True:
                    self.FlipPack()                    
                self.LedSuit = -1            
                self.CardHintFn = "self.PTCLead()"
                self.PTCLead()
                return
            self.CardHintFn = "self.PTCSubsequentLead()"
            self.PTCSubsequentLead()
            return
            
        if PlayerPos == 1:
            if self.SPC.CurrentTrick == 0:
                self.ShowDummy()                
            self.CardHintFn = "self.PTCSecondPlayer()"
            self.ResumePlaySlider.Enable(False)
            self.ResumePlay.Enable(False)
            self.PTCSecondPlayer()
            return
        if PlayerPos == 2:
            self.CardHintFn = "self.PTCThirdPlayer()"
            self.PTCThirdPlayer()
            return
        self.CardHintFn = "self.PTCLastPlayer()"
        self.PTCLastPlayer()
        return

    def PTCLead(self):
        self.SPC.PBNOrigLeader = self.SPC.CurrentPlayer        
        MyBool, PBNCardNum, PBNMsg = ResolvePBNPlay(self.SPC)
##        print "PTCLead MyBool " + str(MyBool) + " Play " + X1.CardStr(PBNCardNum) + " Msg " + str(PBNMsg)
        ## MyDebug(DebugResolved, "PTCLead Trick " + str(self.SPC.CurrentTrick))
        MyPlayerStr = X1.PlayerStr(self.SPC.CurrentPlayer)
        MyTeam = X1.GetTeam(self.SPC.CurrentPlayer)
        MyPartner = X1.GetPartner(self.SPC.CurrentPlayer)
        OppTeam = X1.GetTeam(X1.GetLHO(self.SPC.CurrentPlayer))
        AttackTeam = X1.GetTeam(self.SPC.Declarer)
        for Things in self.SPC.DealtPack:
            Things.UpdateResumePosition(self.DealtPack)
            Things.UpdateResumeExposed(self.DealtPack)
        MyFileName = "Pickle/" + self.SPC.PickleName + "_" + str(self.SPC.CurrentTrick) + ".p"
        ## MyDebug(132, "MyFileName " + MyFileName)
        pickle.dump(self.SPC, open(MyFileName, "wb"))
        X = PTC.Lead(self.SPC.CurrentPlayer, self.SPC)
        if MyBool:
            X = PBNCardNum
            self.SPC.HintMsg = PBNMsg            
        if self.CardHintBool:
            return X
        if self.SPC.CurrentPlayer == self.SPC.Dummy:
            if self.SPC.Human[MyPartner] == True:
                ## MyDebug(DebugResolved, "PTCLead Dummy with Human Partner [" + MyPlayerStr + "] ignored")
                return X
        if self.SPC.Human[self.SPC.CurrentPlayer] == True:
            ## MyDebug(DebugResolved, "PTCLead Human Player [" + MyPlayerStr + "] ignored")
            return X      
        self.PTCAuto(X)
        return

    def PTCSubsequentLead(self):
        ## MyDebug(DebugResolved, "PTCSubsequentLead Trick " + str(self.SPC.CurrentTrick))
        MyBool, PBNCardNum, PBNMsg = ResolvePBNPlay(self.SPC)
##        print "PTCSubsequentLead MyBool " + str(MyBool) + " Play " + X1.CardStr(PBNCardNum) + " Msg " + str(PBNMsg)

        MyPlayerStr = X1.PlayerStr(self.SPC.CurrentPlayer)
##        MyTeam = X1.GetTeam(self.SPC.CurrentPlayer)
        MyPartner = X1.GetPartner(self.SPC.CurrentPlayer)
##        OppTeam = X1.GetTeam(X1.GetLHO(self.SPC.CurrentPlayer))
##        AttackTeam = X1.GetTeam(self.SPC.Declarer)
        for Things in self.SPC.DealtPack:
            Things.UpdateResumePosition(self.DealtPack)
            Things.UpdateResumeExposed(self.DealtPack)
        MyFileName = "Pickle/" + self.SPC.PickleName + "_" + str(self.SPC.CurrentTrick) + ".p"
        ## MyDebug(132, "MyFileName " + MyFileName)
        pickle.dump(self.SPC, open(MyFileName, "wb"))
##        if self.SPC.CurrentTrick == 0:
##            X = PTC.Lead(self.SPC.CurrentPlayer, self.SPC)
##        if self.SPC.CurrentTrick > 0:
        X = PTC.SubsequentLead(self.SPC.CurrentPlayer, self.SPC)
        if MyBool:
            X = PBNCardNum
            self.SPC.HintMsg = PBNMsg

        if self.ClaimHand:
            self.PTCAuto(X)
            return
        if self.CardHintBool:
            return X
        if self.SPC.CurrentPlayer == self.SPC.Dummy:
            if self.SPC.Human[MyPartner] == True:
                ## MyDebug(DebugResolved, "PTCSubsequentLead Dummy with Human Partner [" + MyPlayerStr + "] ignored")
                return X
        if self.SPC.Human[self.SPC.CurrentPlayer] == True:
            ## MyDebug(DebugResolved, "PTCSubsequentLead Human Player [" + MyPlayerStr + "] ignored")
            return X      
        self.PTCAuto(X)
        return

    def PTCSecondPlayer(self):

        MyBool, PBNCardNum, PBNMsg = ResolvePBNPlay(self.SPC)
##        print "PTCSecondPlayer MyBool " + str(MyBool) + " Play " + X1.CardStr(PBNCardNum) + " Msg " + str(PBNMsg)
        ## MyDebug(DebugResolved, "PTCSecondPlayer")
        MyPlayerStr = X1.PlayerStr(self.SPC.CurrentPlayer)
        MyTeam = X1.GetTeam(self.SPC.CurrentPlayer)
        MyPartner = X1.GetPartner(self.SPC.CurrentPlayer)
        X = PTC.SecondPlayer(self.SPC.CurrentPlayer, self.SPC)
        ## MyDebug(DebugResolved, "PTCSecondPlayer " + X1.CardStr(X))
        if MyBool:
            X = PBNCardNum
            self.SPC.HintMsg = PBNMsg
        if self.ClaimHand:
            self.PTCAuto(X)
            return
        if self.CardHintBool:
            ## MyDebug(DebugResolved, "PTCSecondPlayer Hint Player  " + MyPlayerStr)
            return X
        if self.SPC.CurrentPlayer == self.SPC.Dummy:
            if self.SPC.Human[MyPartner] == True:
                ## MyDebug(DebugResolved, "PTCSecondPlayer Dummy with Human Partner [" + MyPlayerStr + "] ignored")
                return X
        if self.SPC.Human[self.SPC.CurrentPlayer] == True:
            ## MyDebug(DebugResolved, "PTCSecondPlayer Human Player [" + MyPlayerStr + "] ignored")
            return X
        self.PTCAuto(X)
        return

    def PTCThirdPlayer(self):
        MyBool, PBNCardNum, PBNMsg = ResolvePBNPlay(self.SPC)
##        print "PTCThirdPlayer MyBool " + str(MyBool) + " Play " + X1.CardStr(PBNCardNum) + " Msg " + str(PBNMsg)

        ## MyDebug(DebugResolved, "PTCThirdPlayer")
        MyPlayerStr = X1.PlayerStr(self.SPC.CurrentPlayer)
        MyTeam = X1.GetTeam(self.SPC.CurrentPlayer)
        MyPartner = X1.GetPartner(self.SPC.CurrentPlayer)
        X = PTC.ThirdPlayer(self.SPC.CurrentPlayer, self.SPC)
        ## MyDebug(DebugResolved, "PTCThirdPlayer " + X1.CardStr(X))
        if MyBool:
            X = PBNCardNum
            self.SPC.HintMsg = PBNMsg
        if self.ClaimHand:
            self.PTCAuto(X)
            return
        if self.CardHintBool:
            ## MyDebug(DebugResolved, "PTCThirdPlayer Hint Player  " + MyPlayerStr)
            return X
        if self.SPC.CurrentPlayer == self.SPC.Dummy:
            if self.SPC.Human[MyPartner] == True:
                ## MyDebug(DebugResolved, "PTCThirdPlayer Dummy with Human Partner [" + MyPlayerStr + "] ignored")
                return X
        if self.SPC.Human[self.SPC.CurrentPlayer] == True:
            ## MyDebug(DebugResolved, "PTCThirdPlayer Human Player [" + MyPlayerStr + "] ignored")
            return X
        self.PTCAuto(X)
        return

    def PTCLastPlayer(self):
        MyBool, PBNCardNum, PBNMsg = ResolvePBNPlay(self.SPC)
##        print "PTCLastPlayer MyBool " + str(MyBool) + " Play " + X1.CardStr(PBNCardNum) + " Msg " + str(PBNMsg)
        ## MyDebug(DebugResolved, "PTCLastPlayer")
        MyPlayerStr = X1.PlayerStr(self.SPC.CurrentPlayer)
        MyTeam = X1.GetTeam(self.SPC.CurrentPlayer)
        MyPartner = X1.GetPartner(self.SPC.CurrentPlayer)
        X = PTC.LastPlayer(self.SPC.CurrentPlayer, self.SPC)
        ## MyDebug(DebugResolved, "PTCLastPlayer " + X1.CardStr(X))
        if MyBool:
            X = PBNCardNum
            self.SPC.HintMsg = PBNMsg
        if self.ClaimHand:
            self.PTCAuto(X)
            return
        if self.CardHintBool:
            ## MyDebug(DebugResolved, "PTCLastPlayer Hint Player  " + MyPlayerStr)
            return X
        if self.SPC.CurrentPlayer == self.SPC.Dummy:
            if self.SPC.Human[MyPartner] == True:
                ## MyDebug(DebugResolved, "PTCLastPlayer Dummy with Human Partner [" + MyPlayerStr + "] ignored")
                return X
        if self.SPC.Human[self.SPC.CurrentPlayer] == True:
            ## MyDebug(DebugResolved, "PTCLastPlayer Human Player [" + MyPlayerStr + "] ignored")
            return X
        self.PTCAuto(X)
        return

    def FlipPack(self):
        ## MyDebug(DebugResolved, "FlipPack")
        if self.SPC.Flip == False:
            return
        for MyPlayingCard in self.DealtPack:
            CurrentOwner = MyPlayingCard.Owner
            FlipOwner = (CurrentOwner + 2) % 4
            MyPlayingCard.UpdateOwner(FlipOwner)
            if CurrentOwner == self.SPC.Declarer:
                MyPlayingCard.UpdateFlipCard()
        for MyPlayingCard in self.SPC.DealtPack:
            CurrentOwner = MyPlayingCard.Owner
            FlipOwner = (CurrentOwner + 2) % 4
            MyPlayingCard.UpdateOwner(FlipOwner)
            if CurrentOwner == self.SPC.Declarer:
                MyPlayingCard.UpdateFlipCard()
        self.SPC.UpdateFlip()
        for MyPlayer in range(4):
            self.UpdateEntireHand(MyPlayer, False)
        self.OnPaint(-1)
        return

    def UpdateEntireHand(self, Owner, Exposed):
        ## MyDebug(DebugResolved, "UpdateEntireHand " + X1.PlayerStr(Owner))
        if self.SPC.Format == X1.FormatBig:
            LastCard = -1
            for MyPlayingCard in self.DealtPack:
                if MyPlayingCard.Owner == Owner:
                    if MyPlayingCard.Played == False:
                        if MyPlayingCard.Tabled == False:
                            LastCard = MyPlayingCard.Num
            ## MyDebug(DebugResolved, "LastCard " + X1.CardStr(LastCard))    
            StartPosX, StartPosY = X1.GetCheatStartPos(Owner, self.SPC)
            PlayerWidth = X1.PlayerCoverWidth[Owner]
            PlayerHeight = X1.PlayerCoverHeight[Owner]
            if Exposed:
                PlayerWidth = PlayerWidth + 50
                PlayerHeight = PlayerHeight + 50
            ## MyDebug(DebugResolved, "PlayerWidth " + str(PlayerWidth))
            ## MyDebug(DebugResolved, "PlayerHeight " + str(PlayerHeight))
            MyX, MyY = X1.MultiCheatSep(Owner, self.SPC.CurrentTrick, self.SPC)
            PosX = StartPosX[Owner] + int(MyX[Owner] / 2)
            PosY = StartPosY[Owner] + int(MyY[Owner] / 2)
            ## MyDebug(DebugResolved, "Owner " + X1.PlayerStr(Owner) + " PH " + str(PlayerHeight) + " PW " + str(PlayerWidth))
            Test1 = wx.Rect(StartPosX[Owner], StartPosY[Owner], PlayerWidth, PlayerHeight)
            MineX, MineY = X1.GetCheatSep(Owner, self.SPC)
            for MyPlayingCard in self.DealtPack:
                if MyPlayingCard.Played == False:
                    if MyPlayingCard.Owner == Owner:
                        self.RefreshRect(MyPlayingCard.GetRect())
            for MyPlayingCard in self.DealtPack:
                if MyPlayingCard.Played == False:
                    if MyPlayingCard.Tabled == False:
                        if MyPlayingCard.Owner == Owner:
                            PosX = PosX + MineX[Owner]
                            PosY = PosY + MineY[Owner]
                            MyPlayingCard.UpdatePosition((PosX, PosY))
                            if MyPlayingCard.Num == LastCard:
                                ## MyDebug(DebugResolved, "LastCard Exposure Updated" + X1.CardStr(LastCard))
                                MyPlayingCard.UpdateExposed(True)
            self.RefreshRect(Test1)
            return
        if self.SPC.Format == X1.FormatSmall:
            CurrentSuit = -1
            MyCounter = 0
            Test1 = wx.Rect(OrigPosSmallX[Owner], OrigPosSmallY[Owner], 130, 130)
            for MyPlayingCard in self.DealtPack:
                if MyPlayingCard.Played == False:
                    if MyPlayingCard.Tabled == False:
                        if MyPlayingCard.Owner == Owner:
                            if MyPlayingCard.Suit != CurrentSuit:
                                MyCounter = 0
                                CurrentSuit = MyPlayingCard.Suit
                            MyMiniRow = X1.SuitOrder[MyPlayingCard.Suit]
                            MyMiniCol = MyCounter
                            if self.SPC.Human[MyPlayingCard.Owner] == False:
                                if self.SPC.Cheat[MyPlayingCard.Owner] == False:
                                    if MyPlayingCard.Owner != self.SPC.Dummy:
                                        MyMiniRow = int(MyCounter / 5)
                                        MyMiniCol = MyCounter % 5
                            PosX = OrigPosSmallX[Owner] + (MyMiniCol * 15)
                            PosY = OrigPosSmallY[Owner] + (MyMiniRow * 32)
                            MyPlayingCard.UpdatePosition((PosX, PosY))
                            MyCounter = MyCounter + 1
            self.RefreshRect(Test1)
            return
        return

    def FindPlayingCard(self, pt):
        for MyPlayingCard in self.DealtPack:
            if MyPlayingCard.HitTest(pt):
                return MyPlayingCard
        return None

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        return

    def VoidInSuit(self, ThePlayer, TheSuit):
        for MyPlayingCard in self.DealtPack:
            if MyPlayingCard.Owner == ThePlayer:
                if MyPlayingCard.Suit == TheSuit:
                    if MyPlayingCard.Played == False:
                        return False
        return True

    def OnRightDown(self, evt):
        pt = evt.GetPosition()
        print pt

    def OnLeftDoubleClick(self, evt):
        ## MyDebug(DebugTime, "OnLeftDoubleClick")
        MyPlayingCard = self.FindPlayingCard(evt.GetPosition())
        if MyPlayingCard:
            if MyPlayingCard.Played == True:
                return
            if self.SPC.TossIn:
                Msg = "A Toss In ... may as well Redeal"
                X1.MyMessage(self, Msg, X1.XXBridgeThing, self.MyMessagePos, wx.OK, wx.ICON_ERROR)
                return
            if self.SPC.Play == False:
                Msg = "The bidding has not finished yet. No touching!"
                X1.MyMessage(self, Msg, X1.XXBridgeThing, self.MyMessagePos, wx.OK, wx.ICON_ERROR)
                return
            ## MyDebug(DebugResolved, "OnLeftDown " + str(MyPlayingCard.HintMsg))
            if MyPlayingCard.Owner != self.SPC.CurrentPlayer:
                MsgVar = X1.PlayerStr(MyPlayingCard.Owner)
                Msg = "This card is owned by " + MsgVar + ". No touching!"
                X1.MyMessage(self, Msg, X1.XXBridgeThing, self.MyMessagePos, wx.OK, wx.ICON_ERROR)
                return
            if self.SPC.PlayCounter != 0:
                if MyPlayingCard.Suit != self.LedSuit:
                    if self.VoidInSuit(MyPlayingCard.Owner, self.LedSuit) == False:
                        return
            self.DragPlayingCard = MyPlayingCard
            self.dragStartPos = evt.GetPosition()
            self.PTCAutoCard(self.DragPlayingCard, True)
            MyMsg = X1.PlayerStr(self.SPC.CurrentPlayer) + " to play"
            self.parent.SetStatusText(MyMsg)
            ## MyDebug(DebugResolved, MyMsg)
            self.DragPlayingCard = None
            self.PTCInit(MyMsg, self.SPC.PlayCounter, True)
        return

    def OnLeftDown(self, evt):
        MyPlayingCard = self.FindPlayingCard(evt.GetPosition())
        if MyPlayingCard:
            if MyPlayingCard.Played == True:
                return
            if self.SPC.TossIn:
                Msg = "A Toss In ... may as well Redeal"
                X1.MyMessage(self, Msg, X1.XXBridgeThing, self.MyMessagePos, wx.OK, wx.ICON_ERROR)
                return
            if self.SPC.Play == False:
                Msg = "The bidding has not finished yet. No touching!"
                X1.MyMessage(self, Msg, X1.XXBridgeThing, self.MyMessagePos, wx.OK, wx.ICON_ERROR)
                return
            ## MyDebug(DebugResolved, "OnLeftDown " + str(MyPlayingCard.HintMsg))
            if MyPlayingCard.Owner != self.SPC.CurrentPlayer:
                MsgVar = X1.PlayerStr(MyPlayingCard.Owner)
                Msg = "This card is owned by " + MsgVar + ". No touching!"
                X1.MyMessage(self, Msg, X1.XXBridgeThing, self.MyMessagePos, wx.OK, wx.ICON_ERROR)
                return
            if self.SPC.PlayCounter != 0:
                if MyPlayingCard.Suit != self.LedSuit:
                    if self.VoidInSuit(MyPlayingCard.Owner, self.LedSuit) == False:
                        return
            self.DragPlayingCard = MyPlayingCard
            self.dragStartPos = evt.GetPosition()
        return

    def OnLeftUp(self, evt):
        if not self.DragPlayingCardImage or not self.DragPlayingCard:
            self.DragPlayingCardImage = None
            self.DragPlayingCard = None
            return
        self.DragPlayingCardImage.Hide()
        self.DragPlayingCardImage.EndDrag()
        self.DragPlayingCardImage = None            
        if self.DragPlayingCard.DumpTest(evt.GetPosition(), self.SPC.Format):
            self.DragPlayingCard.Position = (
                self.DragPlayingCard.Position[0] + evt.GetPosition()[0] - self.dragStartPos[0],
                self.DragPlayingCard.Position[1] + evt.GetPosition()[1] - self.dragStartPos[1]
                )
            self.PTCAutoCard(self.DragPlayingCard, True)
            MyMsg = X1.PlayerStr(self.SPC.CurrentPlayer) + " to play"
            self.parent.SetStatusText(MyMsg)
            ## MyDebug(DebugResolved, MyMsg)
            self.DragPlayingCard = None
            self.PTCInit(MyMsg, self.SPC.PlayCounter, True)
            return
        self.DragPlayingCard.Shown = True
        self.RefreshRect(self.DragPlayingCard.GetRect())
        self.DragPlayingCard = None
    
    def PTCAutoCard(self, MyPlayingCard, MyHumanIntervene):
        ## MyDebug(DebugResolved, "PTCAutoCard " + X1.CardStr(MyPlayingCard.Num))
        ## MyDebug(DebugResolved, "HumanIntervention " + str(MyHumanIntervene))
        MyTeam = X1.GetTeam(MyPlayingCard.Owner)
        MyOppTeam = X1.GetTeam(self.SPC.Declarer)
        if MyTeam == MyOppTeam:
            ## MyDebug(DebugResolved, "Matching Teams ... i.e. attacking team")
            if self.SPC.PlayCounter == 2:
                ## MyDebug(DebugResolved, "Matching attacking Teams and ThirdPlayer")
                self.SPC.Teams[MyOppTeam].ResetFinesseCards()
                self.SPC.Teams[MyOppTeam].ResetReturnLeadInfo()               
        if MyHumanIntervene:
##            print "Here with Human Intervene"
            self.CardHintBool = True
            X = eval(self.CardHintFn)
            self.CardHintBool = False
##            print "Hint " + self.SPC.HintMsg
            if X != MyPlayingCard:
                self.SPC.Teams[MyTeam].SetFinesseCards(-1, -1, -1)
        MyPlayingCard.FaceUp = True
        MyPlayingCard.Shown = True
        MyPlayingCard.Tabled = True
        MyPlayingCard.UpdateThrowPos(self.SPC.Format)
        self.SPC.UpdateWorkPack(MyPlayingCard.Num)
        self.SPC.UpdateDealtPack(MyPlayingCard.Num)
        MyPlayingCard.Trick = self.SPC.CurrentTrick
        self.RefreshRect(MyPlayingCard.GetRect())
        CC1 = X1.WorkPlayedTrick()
        CC1.Owner = MyPlayingCard.Owner
        CC1.Num = MyPlayingCard.Num
        CC1.Val = MyPlayingCard.Num
        CC1.Suit = MyPlayingCard.Suit
        CC1.Trick = self.SPC.CurrentTrick
        if MyPlayingCard.Suit == self.SPC.Trumps:
            CC1.Val = CC1.Val + 100
        if self.SPC.PlayCounter == 0:
            self.LedSuit = MyPlayingCard.Suit
            self.SPC.UpdateLedCard(self.SPC.CurrentTrick, MyPlayingCard.Owner, MyPlayingCard.Num, MyPlayingCard.Pip, CC1.Val)
        if self.SPC.PlayCounter != 0:
            if MyPlayingCard.Suit != self.LedSuit:
                ## MyDebug(DebugResolved, "immediate updatepip for throw-off " + str(MyPlayingCard.Num))
                for DC in range(52):
                    if self.SPC.DealtPack[DC].Suit == MyPlayingCard.Suit:
                        if self.SPC.DealtPack[DC].Num < MyPlayingCard.Num:
                            ## MyDebug(DebugResolved, "for real throw-off Update Cards below " + X1.CardStr(MyPlayingCard.Num))
                            self.SPC.DealtPack[DC].UpdatePip()
##  immediate updatepip for throw-off 
            if MyPlayingCard.Suit != self.SPC.Trumps:
                if MyPlayingCard.Suit != self.LedSuit:                  
                    CC1.Val = -88
            self.SPC.UpdatePlayedCard(self.SPC.CurrentTrick, MyPlayingCard.Owner, MyPlayingCard.Num, MyPlayingCard.Pip, CC1.Val)
        self.PlayedTricks.append(CC1)
        MyPlayingCard.SetXXBitmap(True, False)
        ## MyDebug(DebugResolved, "Exposed " + str(MyPlayingCard.Exposed))
        self.UpdateEntireHand(MyPlayingCard.Owner, MyPlayingCard.Exposed)
        self.UpdateCurrentWinner(MyPlayingCard.Suit, CC1.Num, CC1.Val)

        MyBool, PBNCardNum, PBNMsg = ResolvePBNPlay(self.SPC)
        if MyBool:
            if MyPlayingCard.Num != PBNCardNum:
##                print "Bets are off!"
                self.SPC.PBNContinue = False            
##        if self.SPC.PBNMode == True:
##            MyTag = (4 - (self.SPC.PBNOrigLeader - self.SPC.CurrentPlayer)) % 4
##            PBNCardCount = (self.SPC.CurrentTrick * 4) + MyTag
##            print "re Bet " + str(PBNCardCount)
##            if self.SPC.PBNValidPlay[PBNCardCount]:
##                print "re Bet1 " + str(PBNCardCount)
##                print "Frm DB " + str(self.SPC.PBNPlay[PBNCardCount])
##                print "MyCard " + str(MyPlayingCard.Num)
##                if MyPlayingCard.Num != self.SPC.PBNPlay[PBNCardCount]:
##                    print "Bets are off!"
##                    self.SPC.PBNContinue = False            
        self.IncrementCounters()      
        return
  
    def PTCAuto(self, MyCardNum):
        for Things in self.DealtPack:
            if Things.Num == MyCardNum:
                self.PTCAutoCard(Things, False)
                MyMsg = X1.PlayerStr(self.SPC.CurrentPlayer) + " to play"
                self.parent.SetStatusText(MyMsg)
                ## MyDebug(DebugResolved, MyMsg)
                self.DragPlayingCard = None
                self.PTCInit(MyMsg, self.SPC.PlayCounter, True)
                return
        
    def OnMotion(self, evt):
        if not self.DragPlayingCard or not evt.Dragging() or not evt.LeftIsDown():
            return
        if self.DragPlayingCard and not self.DragPlayingCardImage:
            MyTolerance = 2
            pt = evt.GetPosition()
            dx = abs(pt.x - self.dragStartPos.x)
            dy = abs(pt.y - self.dragStartPos.y)
            if dx <= MyTolerance and dy <= MyTolerance:
                return
            self.DragPlayingCard.Shown = False
            self.RefreshRect(self.DragPlayingCard.GetRect(), True)
            self.Update()
            if self.DragPlayingCard.FaceUp == True:
                self.DragPlayingCardImage = wx.DragImage(self.DragPlayingCard.bmp,
                                             wx.StockCursor(wx.CURSOR_HAND))
            if self.DragPlayingCard.FaceUp == False:
                self.DragPlayingCardImage = wx.DragImage(self.DragPlayingCard.AltBitmap,
                                             wx.StockCursor(wx.CURSOR_HAND))
            hotspot = self.dragStartPos - self.DragPlayingCard.Position
            self.DragPlayingCardImage.BeginDrag(hotspot, self, self.DragPlayingCard.fullscreen)
            self.DragPlayingCardImage.Move(pt)
            self.DragPlayingCardImage.Show()
        elif self.DragPlayingCard and self.DragPlayingCardImage:
            self.FindPlayingCard(evt.GetPosition())
            self.DragPlayingCardImage.Move(evt.GetPosition())
        return
            
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.TheTable.Draw(dc)
        if self.SPC.DoFlip:
            self.DrawAltFlipNames(dc)
        if self.SPC.DoFlip == False:
            self.DrawFlipNames(dc)
        self.DrawDealtCards(dc)
        return

    def DrawFlipNames(self, dc):
        ## MyDebug(DebugResolved, "DrawFlipNames")
        for Things in self.FlipNames:
            Things.Draw(dc)
        return

    def DrawAltFlipNames(self, dc):
        ## MyDebug(DebugResolved, "DrawAltFlipNames")
        for Things in self.FlipNames:
            Things.AltDraw(dc)
        return
               
    def DrawDealtCards(self, dc):
        for DealtCard in self.DealtPack:
            if DealtCard.Shown:
                DealtCard.Draw(dc)
        return

    def UpdateMessageGrid(self):
        TR = self.SPC.Teams[X1.GetTeam(self.SPC.CurrentPlayer)].TricksReqd
        TW = self.SPC.Teams[X1.GetTeam(self.SPC.CurrentPlayer)].TricksWon
        CommentStr = "HelloSailor"
        CommentColour = wx.BLACK
        WonByColour = wx.RED
        DeclarerTeam = False
        WinningTeam = -1
        if X1.GetTeam(self.SPC.CurrentPlayer) == X1.GetTeam(self.SPC.Declarer):
            WonByColour = wx.BLACK
            DeclarerTeam = True
        AltTeam = 0
        if X1.GetTeam(self.SPC.CurrentPlayer) == AltTeam:
            AltTeam = 1
        AltTR = self.SPC.Teams[AltTeam].TricksReqd
        AltTW = self.SPC.Teams[AltTeam].TricksWon
        AltTN = AltTR - AltTW
        ## MyDebug(DebugResolved, "Alt Tricks Required " + str(AltTR))
        ## MyDebug(DebugResolved, "Alt Tricks Won " + str(AltTW))
        SomeWinner = False
        if AltTN <= 0:
            ## MyDebug(DebugResolved, "Alt Tricks has already won")
            SomeWinner = True
            WinningTeam = AltTeam
        ## MyDebug(DebugResolved, "Tricks Required " + str(TR))
        ## MyDebug(DebugResolved, "Tricks Won " + str(TW))
        MyTeamStr = X1.TeamStr(X1.GetTeam(self.SPC.CurrentPlayer))
        DeclarerTeamStr = X1.TeamStr(X1.GetTeam(self.SPC.Declarer))
        TN = TR - TW
        if TN == 0:
            CommentStr = DeclarerTeamStr + " down 1 !!!"
            CommentColour = wx.RED
            if DeclarerTeam:
                CommentStr = DeclarerTeamStr + " have won"
                CommentColour = wx.GREEN
            SomeWinner = True
            WinningTeam = X1.GetTeam(self.SPC.CurrentPlayer)
        if TN < 0:
            SomeWinner = True
            WinningTeam = X1.GetTeam(self.SPC.CurrentPlayer)
            MyExtraStr = " have " + str(abs(TN)) + " overtricks"
            if TN == -1:
                MyExtraStr = " have an overtrick"
            CommentStr = MyTeamStr + MyExtraStr
            CommentColour = wx.RED
            if DeclarerTeam:
                CommentColour = wx.GREEN

            if WinningTeam != X1.GetTeam(self.SPC.Declarer):
                MyExtraStr = " have " + str(abs(TN) + 1) + " penalty tricks"
                if TN == -1:
                    MyExtraStr = " have 2 penalty tricks"
                CommentStr = MyTeamStr + MyExtraStr
                CommentColour = wx.RED
                if DeclarerTeam:
                    CommentColour = wx.GREEN                
        if TN > 0:
            if SomeWinner == False:
                CommentStr = MyTeamStr + " now require " + str(TN)
            if SomeWinner == True:
                CommentStr = MyTeamStr + " to limit overtricks"                
        self.ShowBidsThingy.UpdateGrid(X1.PlayerStr(self.SPC.CurrentPlayer), WonByColour, CommentStr, CommentColour)        
        self.SPC.PlayedTricks[self.SPC.CurrentTrick].UpdatePlayedTrickResult(self.SPC.CurrentPlayer, WonByColour, CommentStr, CommentColour)
        return

    def IncrementCounters(self):
        ## MyDebug(DebugResolved, "IncrementCounters")
        ## MyDebug(DebugResolved, "Led Suit " + X1.TrumpStr(self.LedSuit))
        DefendTeam = 1
        AttackTeam = X1.GetTeam(self.SPC.Declarer)
        if AttackTeam == 1:
            DefendTeam = 0
        if self.SPC.PlayCounter != 3:
            self.SPC.CurrentPlayer = (self.SPC.CurrentPlayer + 1) % 4
            self.SPC.PlayCounter = self.SPC.PlayCounter + 1
            return
        MyBig = -100
        MyOwner = -1
        for x in self.PlayedTricks:
            if x.Val > MyBig:
                MyBig = x.Val
                MyOwner = x.Owner                
        self.SPC.CurrentPlayer = MyOwner
        Msg = "Trick won by " + X1.PlayerStr(self.SPC.CurrentPlayer)
        self.ShowBidsThingy.UpdateSliders(self.SPC.CurrentPlayer)
        self.ResumePlaySlider.Enable(True)
        self.ResumePlay.Enable(True)
        self.CardHint.Enable(False)
        self.CardHint.Show(False)
        if X1.GetTeam(self.SPC.CurrentPlayer) == X1.GetTeam(self.SPC.Declarer):
            self.ClaimButton.Show(True)
            self.ClaimButton.Enable(True)
        Msg = "Won by " + X1.PlayerStr(self.SPC.CurrentPlayer)
        self.SPC.Teams[X1.GetTeam(self.SPC.CurrentPlayer)].UpdateTricksWon(self.SPC.CurrentTrick)
        self.UpdateMessageGrid()
        self.UpdateResumePlaySlider()
        if self.StepByStep:
            dia = MyDialog(None, -1, Msg, self.SPC.CurrentPlayer)
            dia.ShowModal()
            dia.Destroy()
        for x in self.PlayedTricks:
            for DealtCard in self.DealtPack:
                if DealtCard.Num == x.Num:
                    DealtCard.UpdatePosition((10,10))
                    DealtCard.UpdatePlayed(True)
                    DealtCard.UpdateShown(False)
        for x in self.PlayedTricks:
            for DealtCard in self.SPC.DealtPack:
                if DealtCard.Num == x.Num:
                    DealtCard.UpdatePosition((10,10))
                    DealtCard.UpdatePlayed(True)
                    DealtCard.UpdateShown(False)
                    self.Refresh()
## PTC needs this to keep suits in synch for calculating LikelyWinners etc.                   
                    self.SPC.Players[DealtCard.Owner].UpdateSuitLen(DealtCard.Suit)
        for x in self.PlayedTricks:
            for DC in range(52):
                if self.SPC.DealtPack[DC].Suit == self.LedSuit:
                    if self.SPC.DealtPack[DC].Suit == x.Suit:
                        if self.SPC.DealtPack[DC].Num < x.Num:
                            ## MyDebug(DebugResolved, "for real non-throw-off Update Cards below " + X1.CardStr(x.Num))
                            self.SPC.DealtPack[DC].UpdatePip()
        for x in self.PlayedTricks:
            self.SPC.UpdatePipArray(x.Num)                
        self.LedSuit = -1
        self.SPC.PlayCounter = 0
        self.PlayedTricks = []
        self.SPC.UpdateCurrentTrick(self.SPC.CurrentTrick + 1)
        if self.SPC.ShowPlayed == True:
            self.ShowBidsThingy.UpdatePlayedCards(self.SPC)
        return


    def UpdateCurrentWinner(self, MySuit, MyCardNum, MyPipVal):
        ## MyDebug(DebugResolved, "UpdateCurrentWinner Suit " + str(MySuit) + " Pip " + str(MyPipVal))
        if self.SPC.PlayCounter == 0:
            self.SPC.CurrentWinner = self.SPC.CurrentPlayer
            self.SPC.HasBeenTrumped = False
            self.SPC.CurrentSuit = MySuit
            self.SPC.CurrentPipVal = MyPipVal
            self.SPC.CurrentWinningCardNum = MyCardNum
            ## MyDebug(DebugResolved, "Leader " + X1.PlayerStr(self.SPC.CurrentPlayer) + " set as winner")
            return
        if MyPipVal > self.SPC.CurrentPipVal:
            self.SPC.CurrentWinner = self.SPC.CurrentPlayer
            self.SPC.CurrentPipVal = MyPipVal
            self.SPC.CurrentWinningCardNum = MyCardNum
            ## MyDebug(DebugResolved, "New Winner " + X1.PlayerStr(self.SPC.CurrentPlayer))
            if MySuit != self.SPC.CurrentSuit:
                if MySuit == self.SPC.Trumps:
                    self.SPC.HasBeenTrumped = True
        return
    
    def OnStartTest(self, evt):
        ## MyDebug(DebugResolved, "OnStartTest")
        if self.Printed == False:
            Text = X1.PrintedPack(self.TestPack)
            FileTime = time.time()
            MyFileName = "Results/Deal" + str(FileTime) + ".br"
            file = open(MyFileName, 'w')
            file.write(Text + "\n")
            file.close()
        return

    def OnCardHint(self, evt):
        ## MyDebug(DebugResolved, "OnCardHint")
        X = eval(self.CardHintFn)
        self.CardHint.SetBitmap(self.OldBitmap)
        self.CardHint.SetToolTipString("Information")
        self.PTCAuto(X)
        return
    
class MyBiddingBox(wx.Panel):
    def __init__(self, parent, id, MyContext, MyPracticeSession):
        wx.Panel.__init__(self, parent, id)
##        print "Mode " + str(MyContext.PBNMode)
##        if MyContext.PBNMode:
##            print "Auction " + str(MyContext.PBNAuction)

        
        self.MyMessagePos = (0, 0)
        self.BidRows = 1
        MyFont = self.GetFont()
        MyButtonHeight = 30
        MyButtonWidth = 65
        self.Context = MyContext
        self.Session = MyPracticeSession
        self.SetBackgroundColour("green")
        self.ButtonForegroundColour = "green"
        if MyContext.Format == X1.FormatBig:
            MyFont.SetPointSize(11)
            self.SetPosition((970, 50))
        if MyContext.Format == X1.FormatSmall:
            MyButtonHeight = 20
            MyButtonWidth = 35
            MyFont.SetPointSize(8)
            self.SetPosition((470, 50))            
        self.parent = parent
        ## MyDebug(DebugResolved, "Do Bidding " + str(self.Context.PracticeBidding))
        self.BidButtons = []
        for i in range(38):
            self.BidButtons.append(wx.Button(self, -1, X1.BidName[i], size=(MyButtonWidth, MyButtonHeight)))
            self.BidButtons[i].SetBackgroundColour("cyan")
            self.BidButtons[i].Enable(False)
            self.BidButtons[i].SetFont(MyFont)
            self.Bind(wx.EVT_BUTTON, lambda evt, index = i: self.HumanBid(evt, index), self.BidButtons[i])
        MyRow = 0
        MyCol = 0
        MyButton = 0
        MySizer = wx.GridBagSizer(16, 5)
        MySizer.SetHGap(5)
        MySizer.SetVGap(5)
        for x in range(7):
            MyCol = 0
            for y in range(5):
                MySizer.Add(self.BidButtons[MyButton], (MyRow, MyCol), wx.DefaultSpan,  wx.ALIGN_LEFT, border=wx.ALL)
                MyButton = MyButton + 1
                MyCol = MyCol + 1
            MyRow = MyRow + 1
        MySizer.Add(self.BidButtons[36], (7, 0), wx.DefaultSpan,  wx.ALIGN_LEFT)
        MySizer.Add(self.BidButtons[35], (7, 1), (1, 3),  wx.EXPAND)
        MySizer.Add(self.BidButtons[37], (7, 4), wx.DefaultSpan,  wx.ALIGN_LEFT)
        Players = ["North", "East", "South", "West" ]
        self.DealerSelect = wx.ComboBox(self, 899, choices=Players, style=wx.CB_READONLY, size=(100,50))
        if self.Context.Practice:
            self.Context.Dealer = MyPracticeSession.Dealer            
        ## MyDebug(DebugResolved, "Dealer " + str(self.Context.Dealer))
        self.DealerSelect.SetValue(Players[self.Context.Dealer])
        if self.Context.DealerSelect == False:
            self.DealerSelect.Enable(False)
            
        self.Bind(wx.EVT_COMBOBOX, self.OnSetDealer)
        MySizer.Add(self.DealerSelect, (8, 0), (1, 2),  wx.EXPAND)
        self.StartBidButton = wx.BitmapButton(self, -1, wx.Bitmap("Buttons/StartButton.bmp"))
        self.StartBidButton.Bind(wx.EVT_BUTTON, self.OnStartBid)
        self.StartBidButton.Bind(wx.EVT_ENTER_WINDOW, self.StartBidButtonMouseOver)
        self.StartBidButton.Bind(wx.EVT_LEAVE_WINDOW, self.StartBidButtonMouseLeave)
        self.DealerSelect.Bind(wx.EVT_ENTER_WINDOW, self.DealerSelectMouseOver)
        self.DealerSelect.Bind(wx.EVT_LEAVE_WINDOW, self.DealerSelectMouseLeave)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        MySizer.Add(self.StartBidButton, (8, 2), (1, 1),  wx.EXPAND)
##        self.HintButton = wx.BitmapButton(self, -1, wx.Bitmap("Buttons/Hint.bmp"))
##        self.HintButton = wx.BitmapButton(self, -1, wx.Bitmap("Buttons/Help.png"))
##        self.HintButton.Bind(wx.EVT_BUTTON, self.OnHintBid)
        MyBitmap = wx.Bitmap("Buttons/BidHint.png")
        if self.Context.PBNMode:
            if self.Context.PBNContinue:
                MyBitmap = wx.Bitmap("Buttons/PBNBidHint.png")
                
        self.HintButton = wx.BitmapButton(self, -1, MyBitmap)
        self.HintButton.Bind(wx.EVT_ENTER_WINDOW, self.HintBidMouseOver)

        self.HintButton.Enable(False)
        MySizer.Add(self.HintButton, (8, 3), (1, 2),  wx.EXPAND)
        self.MyBidGrid = X1.BidGrid(self, self.Context)
        self.MyBidGrid.GridClearBids()
        MySizer.Add(self.MyBidGrid, (9, 0), (4, 5),  wx.EXPAND)
        self.SetSizerAndFit(MySizer)
        MyX, MyY = self.GetSizeTuple()
        self.MyMessagePos = (1070 + (MyX / 2), 200 + (MyY / 2))
        self.parent.StatusBar.SetStatusText("Start the Bidding. Click on the green Button in the Bidding Box")
        self.Show(True)
        return

    def OnQuit(self, event):
        ## MyDebug(DebugResolved, "OnQuit")
        event.Skip()
        return

    def HintBidMouseOver(self, event):
##        print "HintBidMouseOver"
        if self.Context.PBNMode == True:
            MyBid = self.Context.PBNAuction[self.Context.BidCounter]
##            print "PBN MachineBid My Bid " + str(MyBid)
            Msg = X1.PlayerStr(self.Context.CurrentPlayer) + " PBN No Hint"
            NewToolStr = "Hint : " + str(Msg)
        if self.Context.PBNMode == False:        
            MyTeam = X1.GetTeam(self.Context.CurrentPlayer)
            MyPartner = X1.GetPartner(self.Context.CurrentPlayer)
            MyPartnerExpPts = self.Context.Players[MyPartner].MinExpPts
            MyPartnerExpLen = self.Context.Players[MyPartner].ExpLen
            Msg = ""
            PartnerBid = False
            if self.Context.BidCounter > 1:
                PartnerBid = True
            Mine = X1.Bid(-1)    
            Mine.Owner = self.Context.CurrentPlayer
            MyBidType = X1.GetBidType(self.Context.Bids, self.Context.BidCounter)
            Mine.Type = MyBidType    
            MyFn = X1.SystemStr(self.Context.Teams[MyTeam].System) + ".GetBidSubType(Mine, self.Context)"
            MyBidSubType = eval(MyFn)
            FnStr = X1.BidTypeStr(MyBidType)
            MyBid = eval(X1.SystemStr(self.Context.Teams[MyTeam].System) + "." + FnStr + "(" + str(self.Context.CurrentPlayer) + ", self.Context)")
            NewToolStr = "Partner Points : " + str(MyPartnerExpPts) + " Length : " + ExpLenStr(MyPartnerExpLen) + "\nHint : " + str(self.Context.HintMsg)
##            MyDebug(DebugResolved, "Hint MachineBid My Bid " + X1.BidStr(MyBid))
        ButtonNum = X1.BidStrToButtonNum(X1.BidStr(MyBid))
        self.BidButtons[ButtonNum].SetToolTipString(NewToolStr)
        self.BidButtons[ButtonNum].SetForegroundColour("magenta")
        if self.Context.PBNMode:
            if self.Context.PBNContinue:
                self.BidButtons[ButtonNum].SetForegroundColour("red")
        return

    

    def OnStartBid(self, event):
        ## MyDebug(DebugResolved, "OnStartBid " + self.DealerSelect.GetValue() + " selected")
        Dealer = X1.GetPlayerNumByName(self.DealerSelect.GetValue())
        ## MyDebug(DebugResolved, "OnStartBid - Player Number " + str(Dealer))
        self.DealerSelect.Enable(False)
        self.Context.SetDealer(Dealer)
##        print "FP " + str(self.Context.FlatPack)
##        PickleData = cPickle.dumps(self.Context.FlatPack, cPickle.HIGHEST_PROTOCOL)
##        Cursor.execute("INSERT INTO " + self.Context.TableName + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
##                        (self.Context.Uniquer, str(-1), -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,-1, -1, -1, -1, -1, -1,
##                        -1, str(-1), -1, 0, 0, str(self.Context.FlatPack), sqlite3.Binary(PickleData),
##                         str(-1), self.Context.User.UserName, self.Context.User.Seat))
##        DataBase.commit()    



        
        for i in range(38):
            self.BidButtons[i].Enable(True)
        self.StartBidButton.Enable(False)
        Msg = X1.PlayerStr(Dealer) + " to bid"
        self.parent.StatusBar.SetStatusText(Msg)
        HP = False
        if self.Context.PracticeBidding == True:
            HP = self.Context.Human[self.Context.CurrentPlayer]
            ## MyDebug(DebugResolved, "Human " + str(HP))
##        print "HP " + str(HP)
        if HP == True:
##            print "Show Hint " + str(self.Context.ShowBidHint)
            if self.Context.ShowBidHint:
                self.HintButton.Enable(True)
                ## MyDebug(DebugResolved, "Human continue")
            return
        self.HintButton.Enable(False)
        MyBidType = X1.GetBidType(self.Context.Bids, self.Context.BidCounter)
        ## MyDebug(DebugResolved, "OnStartBid BidType " + X1.BidTypeStr(MyBidType))
        self.MachineBid(MyBidType)
        return
       
    def HumanBid(self, event, index):
        ## MyDebug(DebugResolved, "HumanBid " + str(index))
        if index == X1.BidButtonDouble:
            ## MyDebug(DebugResolved, "Double Check")
            if X1.ValidDouble(self.Context) == False:
                ReturnMsg = "Invalid Double"
                X1.MyMessage(self, ReturnMsg, X1.XXBridgeThing, self.MyMessagePos, wx.OK, wx.ICON_ERROR)
                ## MyDebug(DebugResolved, ReturnMsg)
                return
        if index == X1.BidButtonRedouble:
            ## MyDebug(DebugResolved, "Redouble Check")
            if X1.ValidRedouble(self.Context) == False:
                ReturnMsg = "Invalid Redouble"
                X1.MyMessage(self, ReturnMsg, X1.XXBridgeThing, self.MyMessagePos, wx.OK, wx.ICON_ERROR)
                ## MyDebug(DebugResolved, ReturnMsg)
                return            
        MyBid = X1.ConvertBid(index)
        MyType = X1.GetBidType(self.Context.Bids, self.Context.BidCounter)
        self.MakeBid(MyBid, MyType)
        return
    
    def MakeBid(self, MyBid, MyBidType):
        MyTeam = X1.GetTeam(self.Context.CurrentPlayer)
        ## MyDebug(DebugResolved, "MakeBid " + str(MyBid) + " Type " + X1.BidTypeStr(MyBidType))
        Mine = X1.Bid(MyBid)
        if self.Context.PBNMode:
            DBBid = self.Context.PBNAuction[self.Context.BidCounter]
##            print "DB BID " + str(DBBid)
            if MyBid != DBBid:
                self.Context.PBNContinue = False
                MyBitmap = wx.Bitmap("Buttons/BidHint.png")
                self.HintButton.SetBitmap(MyBitmap)
                self.HintButton.Update()

##                self.HintButton = wx.BitmapButton(self, -1, MyBitmap)

                
##            print "PBN Continue " + str(self.Context.PBNContinue)
        Mine.Owner = self.Context.CurrentPlayer
        ## MyDebug(DebugResolved, "MakeBid " + X1.BidStr(Mine.Num) + " Player " + X1.PlayerStr(self.Context.CurrentPlayer))
        Mine.Type = MyBidType
        ## MyDebug(DebugResolved, "MakeBid Bid Num   " + str(Mine.Num))
        ## MyDebug(DebugResolved, "MakeBid Bid Str   " + X1.BidStr(Mine.Num))
        ## MyDebug(DebugResolved, "MakeBid Bid Type  " + X1.BidTypeStr(Mine.Type))
        ## MyDebug(DebugResolved, "MakeBid Bid Suit  " + X1.TrumpStr(Mine.Suit))
        ## MyDebug(DebugResolved, "MakeBid Bid Level " + str(Mine.Level))
        MyFn = X1.SystemStr(self.Context.Teams[MyTeam].System) + ".GetBidSubType(Mine, self.Context)"
        MyBidSubType = eval(MyFn)
        Mine.SubType = MyBidSubType
        MyStrFn = X1.SystemStr(self.Context.Teams[MyTeam].System) + ".BidSubTypeStr(Mine.SubType)"
        MyBidSubTypeStr = eval(MyStrFn) 
        Mine.HintMsg = self.Context.HintMsg
        ## MyDebug(DebugResolved, "Player " + X1.PlayerStr(self.Context.CurrentPlayer) +" Bid " + X1.BidStr(Mine.Num) + " SubType  " + str(MyBidSubTypeStr) + " Hint  " + str(Mine.HintMsg))
        if Mine.Num != -1:
            MyLine = "Bid " + X1.BidStr(Mine.Num)
            MyLine = MyLine  + " Type " + X1.BidTypeStr(Mine.Type)
            MyLine = MyLine  + " Suit " + X1.TrumpStr(Mine.Suit)
            MyLine = MyLine  + " SubType " + MyBidSubTypeStr
##            MyLine = MyLine  + " Hint " + str(Mine.HintMsg)
            ## MyDebug(DebugResolved, MyLine)
        ReturnMsg = self.Context.AddBid(Mine)
##        Nuke the TooTip here
        for i in range(38):
            self.BidButtons[i].SetToolTipString("")
            self.BidButtons[i].SetForegroundColour(self.ButtonForegroundColour)  
        ## MyDebug(DebugResolved, "Contract " + X1.BidStr(self.Context.Contract))
        ## MyDebug(DebugResolved, "Prior Contract " + X1.BidStr(self.Context.PriorContract))
        ## MyDebug(DebugResolved, "Prior Contract " + X1.BidStr(self.Context.PriorBid.Num))
        MyFn = X1.SystemStr(self.Context.Teams[MyTeam].System) + ".GetBidExpPts(Mine, self.Context)"
        MyMinExpPts, MyMaxExpPts = eval(MyFn)
        MyFn = X1.SystemStr(self.Context.Teams[MyTeam].System) + ".GetBidExpLen(Mine, self.Context)"
        Thing = eval(MyFn)
##        if Mine.Num != -1:
            ## MyDebug(DebugResolved, "Player " + X1.PlayerStr(self.Context.CurrentPlayer) + " MyMinExpPts " + str(MyMinExpPts) + " MyMaxExpPts " + str(MyMaxExpPts))
            ## MyDebug(DebugResolved, "ExpLen " + str(Thing))
##        if self.Context.Human[self.Context.CurrentPlayer]:
            ## MyDebug(DebugResolved, "Clubs Length  " + str(Thing[0]))
            ## MyDebug(DebugResolved, "Diamonds Len  " + str(Thing[1]))
            ## MyDebug(DebugResolved, "Hearts Length " + str(Thing[2]))
            ## MyDebug(DebugResolved, "Spades Length " + str(Thing[3]))
        self.Context.Players[self.Context.CurrentPlayer].UpdateExpLen(Thing)
##        if Mine.Num != -1:
            ## MyDebug(DebugResolved, "ExpLen Updated Player " + X1.PlayerStr(self.Context.CurrentPlayer))
            ## MyDebug(DebugResolved, self.Context.Players[self.Context.CurrentPlayer].ExpLen)
        self.Context.Players[self.Context.CurrentPlayer].MinExpPts = self.Context.Players[self.Context.CurrentPlayer].MinExpPts + MyMinExpPts
        self.Context.Players[self.Context.CurrentPlayer].MaxExpPts = self.Context.Players[self.Context.CurrentPlayer].MaxExpPts + MyMaxExpPts
        ## MyDebug(DebugResolved, "Player : " + X1.PlayerStr(self.Context.CurrentPlayer))
##        if Mine.Num != -1:
            ## MyDebug(DebugResolved, "MakeBid MinExpPts " + str(MyMinExpPts))
            ## MyDebug(DebugResolved, "Player Accum MinExpPts " + str(self.Context.Players[self.Context.CurrentPlayer].MinExpPts))
        ## MyDebug(DebugResolved, "Current Bid Player : " + X1.PlayerStr(self.Context.CurrentBid.Owner))
        ## MyDebug(DebugResolved, "Current Bid Suit : " + X1.TrumpStr(self.Context.CurrentBid.Suit))
        Row = int((self.Context.BidCounter + self.Context.Dealer) / 4)
        Col = self.Context.CurrentBidder
        ## MyDebug(DebugResolved, "MakeBid " + str(Col) + " Player " + X1.PlayerStr(self.Context.CurrentBidder))
        Val = X1.BidStr(MyBid)
        self.MyBidGrid.GridMakeBid(Row, Col, Val)
        if self.Context.KeepBidding == False:
            DefendTeam = X1.GetTeam(self.Context.Leader)
            self.Context.Teams[DefendTeam].UpdatePlayMode(X1.PlayModeDefend)
            self.Context.Teams[DefendTeam].UpdateTricksReqd(14 - self.Context.TricksReqd)
            AttackTeam = (DefendTeam + 1) % 2
            self.Context.Teams[AttackTeam].UpdatePlayMode(X1.PlayModeAttack)
            self.Context.Teams[AttackTeam].UpdateTricksReqd(self.Context.TricksReqd)
            if self.Context.Practice:
                MyLine = P2.PrintDealtCards(self.Session.Num, self.Context)
                self.Session.WriteFile(MyLine)
                MyLine = P2.PrintBids(self.Context)
                self.Session.WriteFile(MyLine)            
            self.parent.StatusBar.SetStatusText(ReturnMsg)
            self.HintButton.Enable(False)
            self.parent.Destroyed = True
            self.BidRows = int(self.Context.BidCounter / 4)
            if self.BidRows > 0:
                OldXPos, OldYPos = self.MyMessagePos
                OldYPos = OldYPos + (self.BidRows * 25)
                self.MyMessagePos = (OldXPos, OldYPos)
            if self.Context.TossIn:
                Msg = "A Toss In ... may as well Redeal!!"
                MyVal = X1.MyMessage(self, Msg, X1.XXBridgeThing, self.MyMessagePos, wx.OK, wx.ICON_ERROR)
                print "Why does this not work"
                self.Close()
                return
            self.Close()
            self.parent.PTCInit(ReturnMsg)
            return
        self.Context.BidCounter = self.Context.BidCounter + 1
        self.Context.CurrentPlayer = (self.Context.CurrentPlayer + 1) % 4
        self.Context.CurrentBidder = self.Context.CurrentPlayer
        ## MyDebug(DebugResolved, "Increment Current Player to Player " + str(self.Context.CurrentPlayer))
        self.parent.StatusBar.SetStatusText(X1.PlayerStr(self.Context.CurrentPlayer) + " to bid")
        if MyBid < 35:
            for x in range(MyBid + 1):
                ## MyDebug(DebugResolved, "HumanBid " + X1.BidName[x] + " button disabled")
                self.BidButtons[x].Enable(False)
                self.BidButtons[x].SetBackgroundColour("white")
        HP = False
        if self.Context.PracticeBidding == True:
            HP = self.Context.Human[self.Context.CurrentPlayer]
        ## MyDebug(DebugResolved, "Human " + str(HP))
        if HP == True:
            if self.Context.ShowBidHint:
                self.HintButton.Enable(True)
                ## MyDebug(DebugResolved, "Human continue")
            return
        MyBidType = X1.GetBidType(self.Context.Bids, self.Context.BidCounter)
        ## MyDebug(DebugResolved, "to Machine BidType " + X1.BidTypeStr(MyBidType))
        self.HintButton.Enable(False)
        self.MachineBid(MyBidType)
        return
    
    def MachineBid(self, MyBidType):
        ## MyDebug(DebugResolved, "MachineBid Player " + X1.PlayerStr(self.Context.CurrentPlayer))
        ## MyDebug(DebugResolved, "MachineBid BidType " + str(MyBidType))
        ## MyDebug(DebugResolved, "Contract " + str(self.Context.Contract))
        MyTeam = X1.GetTeam(self.Context.CurrentPlayer)
        Resolved = False
        if self.Context.PBNMode == True:
            if self.Context.PBNContinue == True:
                Resolved = True
                MyBid = self.Context.PBNAuction[self.Context.BidCounter]
                ## MyDebug(DebugResolved, "MachineBid My Bid " + str(MyBid))
                Msg = X1.PlayerStr(self.Context.CurrentPlayer) + " PBN No Hint"
                ## MyDebug(DebugResolved, str(Msg))

        if Resolved == False:
            FnStr = X1.BidTypeStr(MyBidType)
            MyBid = eval(X1.SystemStr(self.Context.Teams[MyTeam].System) + "." + FnStr + "(" + str(self.Context.CurrentPlayer) + ", self.Context)")
            ## MyDebug(DebugResolved, "MachineBid My Bid " + str(MyBid))
            Msg = X1.PlayerStr(self.Context.CurrentPlayer) + " Hint " + str(self.Context.HintMsg)
            ## MyDebug(DebugResolved, str(Msg))
        
        self.MakeBid(MyBid, MyBidType)
        return
        
    def DealerSelectMouseOver(self, event):
        self.OldMsg = self.parent.StatusBar.GetStatusText()
        self.parent.StatusBar.SetStatusText("This drop box enables you to choose the Dealer")
        event.Skip()
        
    def DealerSelectMouseLeave(self, event):
        self.parent.StatusBar.SetStatusText(self.OldMsg)
        event.Skip()

    def StartBidButtonMouseOver(self, event):
        self.OldMsg = self.parent.StatusBar.GetStatusText()
        self.parent.StatusBar.SetStatusText("This button starts the bidding")
        event.Skip()
        
    def StartBidButtonMouseLeave(self, event):
        self.parent.StatusBar.SetStatusText(self.OldMsg)
        event.Skip()

    def OnSetDealer(self, event):
        MyDealer = self.DealerSelect.GetValue()
        ## MyDebug(DebugResolved, "OnSetDealer " + MyDealer + " selected")
        self.parent.StatusBar.SetStatusText(MyDealer + " to deal")
        return
            
class SimpleUserGrid(GridLib.Grid):
    def __init__(self, parent, MyRows):
        self.PrevRowSelected = -1
        self.PrevSel = []
        self.SelectedUserUniquer = []
        for Row in range(MyRows):
            self.PrevSel.append(False)
            self.SelectedUserUniquer.append("Sailor")
            
        GridLib.Grid.__init__(self, parent, -1, size=(520,-1))
        self.parent = parent
        self.CreateGrid(MyRows, 6)
        self.SetColSize(0, 0)
        self.SetColSize(1, 120)
        self.SetColSize(2, 70)
        self.SetColSize(3, 100)
        self.SetColSize(4, 70)
        self.SetColSize(5, 70)
        self.RowNum = 0
        self.SetColLabelValue(1, "Name")
        self.SetColLabelValue(2, "Seat")
        self.SetColLabelValue(3, "System")
        self.SetColLabelValue(4, "Played")
        self.SetColLabelValue(5, "Won")
        self.Bind(GridLib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(GridLib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)        
        return

    def OnLabelLeftClick(self, evt):
        MyRow = evt.GetRow()
        MyUniquer = self.GetCellValue(MyRow, 0)
        if MyRow == 0:
            return
##        print "OnLabelLeftClick MyRow " + str(MyRow) + " Sel " + str(self.PrevSel[MyRow])
        if self.PrevSel[MyRow] == True:
            for MyCol in range(5):
                MyCol = MyCol + 1
                self.SetCellBackgroundColour(MyRow, MyCol, wx.WHITE)
            self.PrevSel[MyRow] = False
            self.SelectedUserUniquer[MyRow] = "Sailor"
            self.parent.UpdateSelectedUserUniquer(MyRow, False, "Sailor")
            self.Refresh()
            return
        for MyCol in range(5):
            MyCol = MyCol + 1
            self.SetCellBackgroundColour(MyRow, MyCol, wx.RED)
        self.PrevSel[MyRow] = True
        self.SelectedUserUniquer[MyRow] = MyUniquer
        self.parent.UpdateSelectedUserUniquer(MyRow, True, MyUniquer)
        self.Refresh()
        return

    def OnCellLeftClick(self, evt):
        MyRow = evt.GetRow()
        MyUniquer = self.GetCellValue(MyRow, 0)
        if MyRow == 0:
            return
##        print "OnLabelLeftClick MyRow " + str(MyRow) + " Sel " + str(self.PrevSel[MyRow])
        if self.PrevSel[MyRow] == True:
            for MyCol in range(5):
                MyCol = MyCol + 1
                self.SetCellBackgroundColour(MyRow, MyCol, wx.WHITE)
            self.PrevSel[MyRow] = False
            self.SelectedUserUniquer[MyRow] = "Sailor"
            self.parent.UpdateSelectedUserUniquer(MyRow, False, "Sailor")
            self.Refresh()
            return
        for MyCol in range(5):
            MyCol = MyCol + 1
            self.SetCellBackgroundColour(MyRow, MyCol, wx.RED)
        self.PrevSel[MyRow] = True
        self.SelectedUserUniquer[MyRow] = MyUniquer
        self.parent.UpdateSelectedUserUniquer(MyRow, True, MyUniquer)
        self.Refresh()
        return
    
    def Reset(self):
        ## MyDebug(132, "Made it to Reset SimpleGrid")
        self.ClearGrid()
        self.RowNum = 0
        self.PrevSel = []
        self.SelectedUserUniquer = []
        self.SetColLabelValue(1, "Name")
        self.SetColLabelValue(2, "Seat")
        self.SetColLabelValue(3, "System")
        self.SetColLabelValue(4, "Played")
        self.SetColLabelValue(5, "Won")
        return
    
    def UpdateColumns(self, MyUniquer, MyName, MySeat, MySystem, MyPlayed, MyWon):
        try:
            self.SelectedUserUniquer.append("Sailor")
            self.PrevSel.append(False)
            self.SetCellValue(self.RowNum, 0, str(MyUniquer))
            self.SetCellValue(self.RowNum, 1, str(MyName))
            self.SetCellValue(self.RowNum, 2, X1.PlayerStr(MySeat))
            self.SetCellValue(self.RowNum, 3, X1.SystemStr(MySystem))
            self.SetCellValue(self.RowNum, 4, str(MyPlayed))
            self.SetCellValue(self.RowNum, 5, str(MyWon))
            if self.RowNum == 0:
                for MyCol in range(5):
                    MyCol = MyCol + 1
                    self.SetCellBackgroundColour(0, MyCol, wx.RED)
                self.PrevSel[0] = True
                
            self.RowNum = self.RowNum + 1
            return
        except:
##            print "More hands than rows"
            MyDebug(DebugResolved, "More hands than rows")
        return

class SimpleHandGrid(GridLib.Grid):
    def __init__(self, parent):
        self.PrevRowSelected = -1
        GridLib.Grid.__init__(self, parent, -1, size=(576,470))
        self.parent = parent
        self.CreateGrid(10000, 6)
        self.SetColSize(0, 0)
        self.SetColSize(1, 70)
        self.SetColSize(2, 70)
        self.SetColSize(3, 70)
        self.SetColSize(4, 140)
        self.SetColSize(5, 70)
        self.RowNum = 0
        self.SetColLabelValue(1, "Contract")
        self.SetColLabelValue(2, "Dealer")
        self.SetColLabelValue(3, "Declarer")
        self.SetColLabelValue(4, "Result")
        self.SetColLabelValue(5, "BidType")
        self.Bind(GridLib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(GridLib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)        
        self.Bind(GridLib.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick) 
        return

    def OnLabelRightClick(self, evt):
        MyUniquer = self.GetCellValue(evt.GetRow(), 0)
        if self.PrevRowSelected != -1:
            for MyCol in range(5):
                MyCol = MyCol + 1
                self.SetCellBackgroundColour(self.PrevRowSelected, MyCol, wx.WHITE)
        for MyCol in range(5):
            MyCol = MyCol + 1
            self.SetCellBackgroundColour(evt.GetRow(), MyCol, wx.RED)
        self.PrevRowSelected = evt.GetRow()
        self.Refresh()
##        print "Here"
        self.parent.OnPuddleHand(MyUniquer)
        return

    def OnLabelLeftClick(self, evt):
        MyUniquer = self.GetCellValue(evt.GetRow(), 0)
        if self.PrevRowSelected != -1:
            for MyCol in range(5):
                MyCol = MyCol + 1
                self.SetCellBackgroundColour(self.PrevRowSelected, MyCol, wx.WHITE)
        for MyCol in range(5):
            MyCol = MyCol + 1
            self.SetCellBackgroundColour(evt.GetRow(), MyCol, wx.RED)
        self.PrevRowSelected = evt.GetRow()
        self.Refresh()
        self.parent.OnUserHand(MyUniquer)
        return

    def OnCellLeftClick(self, evt):
        MyUniquer = self.GetCellValue(evt.GetRow(), 0)
        if self.PrevRowSelected != -1:
            for MyCol in range(5):
                MyCol = MyCol + 1
                self.SetCellBackgroundColour(self.PrevRowSelected, MyCol, wx.WHITE)
        for MyCol in range(5):
            MyCol = MyCol + 1
            self.SetCellBackgroundColour(evt.GetRow(), MyCol, wx.RED)
        self.PrevRowSelected = evt.GetRow()
        self.Refresh()
        self.parent.OnUserHand(MyUniquer)
        return

    def Reset(self):
        ## MyDebug(132, "Made it to Reset SimpleGrid")
        self.ClearGrid()
        self.RowNum = 0
        self.SetColLabelValue(0, "Uniquer")
        self.SetColLabelValue(1, "Contract")
        self.SetColLabelValue(2, "Dealer")
        self.SetColLabelValue(3, "Declarer")
        self.SetColLabelValue(4, "Result")
        self.SetColLabelValue(5, "Bid Type")
        return
    
    def UpdateColumns(self, MyUniquer, MyContract, MyDealer, MyDeclarer, MyResult, MyType):
        try:
            self.SetCellValue(self.RowNum, 0, str(MyUniquer))
            self.SetCellValue(self.RowNum, 1, X1.BidStr(MyContract))
            self.SetCellValue(self.RowNum, 2, X1.PlayerStr(MyDealer))
            self.SetCellValue(self.RowNum, 3, X1.PlayerStr(MyDeclarer))
            self.SetCellValue(self.RowNum, 4, MyResult)
            self.SetCellValue(self.RowNum, 5, X1.PracticeBidTypeStr(MyType))

##            self.SetCellValue(self.RowNum, 0, str(MyUniquer))
##            self.SetCellValue(self.RowNum, 1, X1.BidStr(MyContract))
##            self.SetCellValue(self.RowNum, 2, str(MyDealer))
##            self.SetCellValue(self.RowNum, 3, str(MyDeclarer))
##            self.SetCellValue(self.RowNum, 4, str(MyResult))
##            self.SetCellValue(self.RowNum, 5, str(MyType))

            self.RowNum = self.RowNum + 1
            return
        except:
##            print "More hands than rows"
            MyDebug(DebugResolved, "More hands than rows")
        return

class PuddleTargetPanel(wx.Panel):
    def __init__(self, parent, id, MyContext, MyPlayer, MyHand):
##        wx.Panel.__init__(self, parent, id, size=(340,140), style=wx.RAISED_BORDER)
        wx.Panel.__init__(self, parent, id, size=(340,140))
        self.SetBackgroundColour("green")
        self.parent = parent
        MyPos = (X1.PuddleTopX[MyPlayer], X1.PuddleTopY[MyPlayer])
        self.SetPosition(MyPos)
        self.SetToolTipString("Click on any card to delete it from " + X1.PlayerStr(MyPlayer) + " and add it to the Puddle")
        self.ChosenCards = []
        self.ChosenPlayer = MyPlayer
        self.x12 = wx.StaticText(self, wx.ID_ANY, X1.PlayerStr(MyPlayer), size=(80,-1), pos=(10,0))
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD )
        self.x12.SetFont(font)

        self.SPC = MyContext
        XSep = 20
        XOffSet = 10
##        print str(MyHand)
        x1 = sorted(MyHand, reverse=True)
##        print str(x1)
        LastCardNum = -1
        for Things in x1:
            LastCardNum = Things
        
        MyCount = 0
        for Things in x1:
            bmp = wx.Bitmap('Cards/' + str(Things) + '.png')
            TheCard = X1.CobbleCard(bmp, Things, self.SPC.Format)
            TheCard.Shown = True
            TheCard.FaceUp = True
            TheCard.Owner = -1
            TheCard.HandLoc = -1
            TheCard.Exposed = False
            if Things == LastCardNum:
                TheCard.Exposed = True
            TheCard.UpdatePosition(((XSep * MyCount) + XOffSet, 25))
            self.ChosenCards.append(TheCard)
            MyCount = MyCount + 1

            
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDoubleClick)
        self.Show()        
        return

    def ResetTarget(self):
        self.ChosenCards = []
        return
        
    def GetHeldCards(self):
        TestArray = []
        for Thing in self.ChosenCards:
            TestArray.append(Thing.Num)
        return TestArray
        
    def GetHoldingCount(self):
        TestCount = 0
        for Thing in self.ChosenCards:
            TestCount = TestCount + 1
        return TestCount
        
    def AddCard(self, MyPlayer, MyCardNum, MyContext):
        XSep = 20
        XOffSet = 10
        CurrVal = []
        NewVal = []
        MyCount = 0
        TestCount = 0
        for Thing in self.ChosenCards:
            TestCount = TestCount + 1
        if TestCount > 12:
            print "No more cards please"
            return
        
        for Thing in self.ChosenCards:
            CurrVal.append(Thing.Num)
            MyCount = MyCount + 1
        if MyCount != 0:
            AddOnce = True
            for Things in range(MyCount):
                if MyCardNum > CurrVal[Things]:
                    if AddOnce:
                        NewVal.append(MyCardNum)
                        AddOnce = False
                        MyCount = MyCount + 1
                NewVal.append(CurrVal[Things])
            if AddOnce == True:
                NewVal.append(MyCardNum)
                MyCount = MyCount + 1                
        if MyCount == 0:
            NewVal.append(MyCardNum)
            MyCount = 1
        LastCardNum = -1
        for Things in NewVal:
            LastCardNum = Things


            
        self.ChosenCards = []
        for x in range(MyCount):
            bmp = wx.Bitmap('Cards/' + str(NewVal[x]) + '.png')
            TheCard = X1.CobbleCard(bmp, NewVal[x], MyContext.Format)
            TheCard.Shown = True
            TheCard.FaceUp = True
            TheCard.Exposed = False
            if NewVal[x] == LastCardNum:
                TheCard.Exposed = True            

            TheCard.Owner = MyPlayer
            TheCard.HandLoc = -1
            TheCard.UpdatePosition(((XSep * x) + XOffSet, 25))
            self.ChosenCards.append(TheCard)
        self.OnPaint(-1)

    def FindPlayingCard(self, pt):
        for MyPlayingCard in self.ChosenCards:
            if MyPlayingCard.HitTest(pt):
                return MyPlayingCard
        return None

    def OnLeftDoubleClick(self, evt):
##        print "OnLeftDoubleClick"
        MyPlayingCard = self.FindPlayingCard(evt.GetPosition())
        if not MyPlayingCard:
##            print "No card"
            return        
##        print "MPC " + str(MyPlayingCard.Num)
        NewVal = []
        MyCount = 0
        XSep = 20
        XOffSet = 10
        for Thing in self.ChosenCards:
            if Thing.Num != MyPlayingCard.Num:
                NewVal.append(Thing.Num)
                MyCount = MyCount + 1
##        print str(NewVal)
        LastCardNum = -1
        for Things in NewVal:
            LastCardNum = Things
        self.ChosenCards = []
        for x in range(MyCount):
            bmp = wx.Bitmap('Cards/' + str(NewVal[x]) + '.png')
            TheCard = X1.CobbleCard(bmp, NewVal[x], self.SPC.Format)
            TheCard.Shown = True
            TheCard.FaceUp = True
            TheCard.Exposed = False
            if NewVal[x] == LastCardNum:
                TheCard.Exposed = True            
            TheCard.Owner = self.ChosenPlayer
            TheCard.HandLoc = -1
            TheCard.UpdatePosition(((XSep * x) + XOffSet, 25))
            self.ChosenCards.append(TheCard)   
        self.RefreshRect(wx.Rect(0, 0, 240, 100))
        self.OnPaint(-1)
        self.parent.ReinstateCard(MyPlayingCard.Num)        
        return
    
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.DrawDealtCards(dc)
        return

    def DrawDealtCards(self, dc):
        for DealtCard in self.ChosenCards:
            if DealtCard.Shown:
                DealtCard.Draw(dc)
        return



class PuddleFrame(wx.Frame):
    def __init__(self, parent, id, title, MyContext, MyPack):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(1200, 900))
        MyMenuBar = wx.MenuBar()
        MyMenu = wx.Menu()
        self.OldMsg = "hello"
        self.KosherPuddle = False


        
        self.SetBackgroundColour("green")
        MyMenuItem = wx.MenuItem(MyMenu, MenuNumber012, '&Save\tCtrl+S', 'Save Hands')
        MyMenuItem.SetBitmap(wx.Image("Buttons/Play.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        MyMenu.AppendItem(MyMenuItem)
        MyMenuItem = wx.MenuItem(MyMenu, MenuNumber013, '&Quit\tCtrl+Q', 'Quit the Application')
        MyMenuItem.SetBitmap(wx.Image("Buttons/Exit.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        MyMenu.AppendItem(MyMenuItem)        
        MyMenuBar.Append(MyMenu, "Actions")
        self.SetMenuBar(MyMenuBar)
        self.StatusBar = self.CreateStatusBar()
        self.StatusBar.SetStatusText("Puddling is fun")

        
        self.MyPack = []        
        self.MyTest = 0
        self.parent = parent
        self.SPC = MyContext
        self.Session = X1.PracticeSession()
        self.DragPlayingCardImage = None
        self.DragPlayingCard = None
        self.CurrentPlayer = self.SPC.User.Seat
        MyX = 400
        self.MyButtons = []
        for x in range(4):
            MyButton = wx.Button(self, -1, X1.PlayerStr(x), size=(80,50), pos=(MyX,10))
            MyButton.SetToolTipString("Select this Player if you wish to ADD Cards")
            if x == self.CurrentPlayer:
                MyButton.SetToolTipString("Cards can only be ADDED to this Player")
                MyButton.SetForegroundColour("magenta")  
            self.MyButtons.append(MyButton)
            self.Bind(wx.EVT_BUTTON, lambda evt, index = x: self.OnOkayButton(evt, index), self.MyButtons[x])            
            MyX = MyX + 85     
        XSep = 20
        XOffSet = 50
        self.DealtPack = []
        self.CobbledHands = []
##        self.PuddleNames = []
        self.CompleteButton = wx.Button(self, wx.ID_ANY, 'Complete Hands', size=(165,50), pos=(485,70))
        self.CompleteButton.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.OnCompleteButton, self.CompleteButton)
##        self.Bind(wx.EVT_ENTER_WINDOW, self.PuddlePanelMouseOver)
##        self.Bind(wx.EVT_LEAVE_WINDOW, self.PuddlePanelMouseLeave)        

        wx.StaticLine(self, -1, (40, 170), size=(1120, -1))       
        wx.StaticLine(self, -1, (38, 171), size=(-1, 121), style=wx.LI_VERTICAL)       

        wx.StaticLine(self, -1, (40, 290), size=(1120, -1))       
        wx.StaticLine(self, -1, (1158, 171), size=(-1, 121), style=wx.LI_VERTICAL)       
##        self.FakeButton = wx.Panel(self, -1, size=(1100,116), pos=(42,174))
##        self.FakeButton.SetBackgroundColour("green")
####        self.FakeButton.Enable(False)
##        self.FakeButton.SetToolTipString("FakeButton")
##        self.FakeButton.Show(False)

        for x in range(52):


            MyCount = 51 - x
            bmp = wx.Bitmap('Cards/' + str(MyCount) + '.png')
            TheCard = X1.CobbleCard(bmp, MyCount, self.SPC.Format)
            TheCard.Shown = False
            TheCard.FaceUp = False
            TheCard.Owner = -1
            TheCard.HandLoc = -1
            self.DealtPack.append(TheCard)

        for x in range(4):
            MyArray = []
            for y in range(13):
                MyVal = (x * 13) + y
                MyArray.append(MyPack[MyVal])             
            TheThing = PuddleTargetPanel(self, x, self.SPC, x, MyArray)
            self.CobbledHands.append(TheThing)

##            for x in range(4):
##                Val = "H"
##                MyFile = 'Things/' + X1.PlayerStr(x) + str(Val) + '.png'
##                bmp = wx.Bitmap(MyFile)
##                TheThing = XThing(10 + x, bmp)
##                TheThing.Position = (X1.FlipNamePosX[x], X1.FlipNamePosY[x])
####                MyAltFile = 'Things/' + X1.PlayerStr(AltCount) + str(Val) + '.png'
####                Altbmp = wx.Bitmap(MyAltFile)
####                TheThing.UpdateAltbmp(Altbmp)
##                self.PuddleNames.append(TheThing)



            
        wx.EVT_MENU(self, MenuNumber012, self.OnSaveCobble)
        wx.EVT_MENU(self, MenuNumber013, self.OnClose)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDoubleClick)
        self.Show(True)
        return

##    def PuddlePanelMouseOver(self, event):
##        self.OldMsg = self.parent.StatusBar.GetStatusText()
##        self.parent.StatusBar.SetStatusText("weeeelllllllll")
##        event.Skip()
##        
##    def PuddlePanelMouseLeave(self, event):
##        self.parent.StatusBar.SetStatusText(self.OldMsg)
##        event.Skip()

    def CompletePack(self):
        KosherDeal, NewPack, TestString = X1.ShufflePack()
        if KosherDeal == False:
            return -1
        MyHeld = []
        for x in range(52):
            MyHeld.append(False)
        for x in range(4):
            for Things in self.CobbledHands[x].GetHeldCards():
                MyHeld[Things] = True
        CardPack = []
        for x in range(52):
            if not MyHeld[NewPack[x]]:
                CardPack.append(NewPack[x])
        DestPack = []
        for x in range(52):
            DestPack.append(-1)
        for x in range(4):
            MultVal = x * 13
            MyElse = 0
            for Things in self.CobbledHands[x].GetHeldCards():
                Val = MultVal + MyElse
                DestPack[Val] = Things
                MyElse = MyElse + 1
        MyCount = 0
        for x in range(52):
            if DestPack[x] == -1:
                DestPack[x] = CardPack[MyCount]
                MyCount = MyCount + 1
        return DestPack

    def OnOkayButton(self, event, MyPlayer):
##        print "MyPlayer " + str(MyPlayer)
        self.CurrentPlayer = MyPlayer
        for x in range(4):
            self.MyButtons[x].SetToolTipString("Select this Player if you wish to ADD Cards")
            self.MyButtons[x].SetForegroundColour("black")
        self.MyButtons[self.CurrentPlayer].SetForegroundColour("magenta")
        self.MyButtons[self.CurrentPlayer].SetToolTipString("Cards can only be ADDED to this Player")
        return

##    def DrawPuddleNames(self, dc):
##        ## MyDebug(DebugResolved, "DrawPuddleNames")
##        for Things in self.PuddleNames:
##            Things.Draw(dc)
##        return

    
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
##        self.DrawPuddleNames(dc)
        self.DrawDealtCards(dc)
        return

    def ReinstateCard(self, MyCardNum):
##        print "PuddleFrame ReinstateCard " + str(MyCardNum)
        self.CompleteButton.Enable(True)
        self.KosherPuddle = False
        LastCardNum = -1
##        LastPos = (0, 0)
        for MyPlayingCard in self.DealtPack:
            MyPlayingCard.UpdatePosition((0, 0))

        for MyPlayingCard in self.DealtPack:
            if MyPlayingCard.Num == MyCardNum:
                MyPlayingCard.Played = False
                MyPlayingCard.Owner = -1
                MyPlayingCard.Shown = True
        XSep = 20
        XOffSet = 50
        x = 0

        for MyPlayingCard in self.DealtPack:
            if MyPlayingCard.Shown == True:
                LastCardNum = MyPlayingCard.Num

        for MyPlayingCard in self.DealtPack:
            if MyPlayingCard.Shown == True:
                MyPlayingCard.Exposed = False
                if MyPlayingCard.Num == LastCardNum:
                    MyPlayingCard.Exposed = True
                MyPlayingCard.UpdatePosition(((XSep * x) + XOffSet, 180))
                x = x + 1
        self.RefreshRect(wx.Rect(50, 180, 700, 100))
        self.OnPaint(-1)
        return

    def UpdateCard(self, MyPlayer, MyCardNum):
##        print "UpdateCard for Player "+ str(MyPlayer) + " Card " + str(MyCardNum)
        XSep = 20
        XOffSet = 50
        x = 0
        for MyPlayingCard in self.DealtPack:
            if MyPlayingCard.Num == MyCardNum:
                MyPlayingCard.Played = True
                MyPlayingCard.Shown = False
        LastCardNum = -1
        x = 0
        for MyPlayingCard in self.DealtPack:
            if MyPlayingCard.Shown == True:
                MyPlayingCard.UpdatePosition(((XSep * x) + XOffSet, 180))
                x = x + 1
                LastCardNum = MyPlayingCard.Num
        for MyPlayingCard in self.DealtPack:
            MyPlayingCard.Exposed = False
            if MyPlayingCard.Num == LastCardNum:
                MyPlayingCard.Exposed = True
        self.RefreshRect(wx.Rect(50, 180, 700, 100))
        self.OnPaint(-1)
        return

    def FindPlayingCard(self, pt):
        for MyPlayingCard in self.DealtPack:
            if MyPlayingCard.HitTest(pt):
                return MyPlayingCard
        return None

    def UpdatePack(self, MyPlayer, MyCardNum, MyContext):
##        print "UpdatePack for Player "+ str(MyPlayer) + " Card " + str(MyCardNum)
        self.CobbledHands[MyPlayer].AddCard(MyPlayer, MyCardNum, MyContext)
        return

    def OnLeftDoubleClick(self, evt):
        MyPlayingCard = self.FindPlayingCard(evt.GetPosition())
        if not MyPlayingCard:
            return
        if self.CobbledHands[self.CurrentPlayer].GetHoldingCount() > 12:
            return
        MyPlayingCard.Position = (0,0)
        MyPlayingCard.Played = True
        MyPlayingCard.Shown = False        
        self.UpdatePack(self.CurrentPlayer, MyPlayingCard.Num, self.SPC)
        self.UpdateCard(self.CurrentPlayer, MyPlayingCard.Num)
        self.RefreshRect(MyPlayingCard.GetRect())
        return

    def DrawTables(self, dc):
        for Things in self.CobbledHands:
            Things.Draw(dc)
        return
             
    def DrawDealtCards(self, dc):
        for DealtCard in self.DealtPack:
            if DealtCard.Shown:
                DealtCard.Draw(dc)
        return

    def OnCompleteButton(self, event):
##        print "OnCompleteButton - CobbleFrame"
        self.MyPack = self.CompletePack()
        for MyPlayingCard in self.DealtPack:
            MyPlayingCard.Played = True
            MyPlayingCard.Shown = False
        self.RefreshRect(wx.Rect(50, 180, 700, 100))
        self.OnPaint(-1)        
        for x in range(4):
            self.CobbledHands[x].ResetTarget()
            MultiVal = x * 13
            for y in range(13):
                MyVal = MultiVal + y
                self.UpdatePack(x, self.MyPack[MyVal], self.SPC)
        self.KosherPuddle = True
        return

    def OnSaveCobble(self, event):
        if self.KosherPuddle == False:
##            print "Not kosher"
            return
        MyUniquer = time.time()
        PickleData = cPickle.dumps(self.MyPack, cPickle.HIGHEST_PROTOCOL)
        Cursor.execute("INSERT INTO " + self.SPC.TableName + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                        (MyUniquer, str("Cobble"), -1, -1, -1, -1, -1, -1, -1, str("Cobble"), -1, -1, -1,
                         str(self.MyPack), sqlite3.Binary(PickleData),
                         str(self.SPC.User.System), self.SPC.User.UserName, self.SPC.User.Seat, MyUniquer))
        DataBase.commit()
        return

    def OnClose(self, event):
        self.Destroy()
        event.Skip()
        return

class UserFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(200, 200))
        self.EditRecord = False
        self.Continue = False
        self.parent = parent
        self.panel = wx.Panel(self, wx.ID_ANY)
        title = wx.StaticText(self.panel, wx.ID_ANY, 'User Maintenance')
        UserNameLabel = wx.StaticText(self.panel, wx.ID_ANY, 'Name')
        UserNameInput = wx.TextCtrl(self.panel, wx.ID_ANY, "")
        UserNameInput.SetToolTipString("Name cannot be blank")
        self.UserNameInput = UserNameInput
        self.Uniquer = "Hello"
        SeatLabel = wx.StaticText(self.panel, wx.ID_ANY, 'Seat')
        self.Seats = ["North", "East", "South", "West" ]
        SeatInput = wx.ComboBox(self.panel, wx.ID_ANY, choices=self.Seats, style=wx.CB_READONLY, size=(50,25))
        self.SeatInput = SeatInput
        SystemLabel = wx.StaticText(self.panel, wx.ID_ANY, 'System')
        self.Systems = ["Neanderthal", "SAYC", "ACOL", "Precision"]
        SystemInput = wx.ComboBox(self.panel, wx.ID_ANY, choices=self.Systems, style=wx.CB_READONLY, size=(50,25))
        self.SystemInput = SystemInput
        ScoreStyleLabel = wx.StaticText(self.panel, wx.ID_ANY, 'Style')
        self.ScoreStyles = ["None", "Rubber", "Duplicate"]
        ScoreStyleInput = wx.ComboBox(self.panel, wx.ID_ANY, choices=self.ScoreStyles, style=wx.CB_READONLY, size=(50,25))
        self.ScoreStyleInput = ScoreStyleInput
        ContinueButton = wx.Button(self.panel, wx.ID_ANY, 'Continue')
        ActivateButton = wx.Button(self.panel, wx.ID_ANY, 'Activate')
        CancelButton = wx.Button(self.panel, wx.ID_ANY, 'Cancel')
        self.ResetButton = wx.Button(self.panel, wx.ID_ANY, 'Reset Score')
        self.ResetButton.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.OnActivateButton, ActivateButton)
        self.Bind(wx.EVT_BUTTON, self.OnCancelButton, CancelButton)
        self.Bind(wx.EVT_BUTTON, self.OnResetButton, self.ResetButton)
        self.Bind(wx.EVT_BUTTON, self.onContinue, ContinueButton)
        topSizer        = wx.BoxSizer(wx.VERTICAL)
        titleSizer      = wx.BoxSizer(wx.HORIZONTAL)
        UserNameSizer   = wx.BoxSizer(wx.HORIZONTAL)
        SeatSizer   = wx.BoxSizer(wx.HORIZONTAL)
        SystemSizer = wx.BoxSizer(wx.HORIZONTAL)
        ScoreStyleSizer  = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer        = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer1        = wx.BoxSizer(wx.HORIZONTAL)
        titleSizer.Add(title, 0, wx.ALL, 5)
        UserNameSizer.Add(UserNameLabel, 0, wx.ALL, 5)
        UserNameSizer.Add(UserNameInput, 1, wx.ALL|wx.EXPAND, 5)
        
        SeatSizer.Add(SeatLabel, 0, wx.ALL, 5)
        SeatSizer.Add(SeatInput, 1, wx.ALL|wx.EXPAND, 5)
        SystemSizer.Add(SystemLabel, 0, wx.ALL, 5)
        SystemSizer.Add(SystemInput, 1, wx.ALL|wx.EXPAND, 5)
        ScoreStyleSizer.Add(ScoreStyleLabel, 0, wx.ALL, 5)
        ScoreStyleSizer.Add(ScoreStyleInput, 1, wx.ALL|wx.EXPAND, 5)
        btnSizer1.Add(ContinueButton, 0, wx.ALL, 5)
        btnSizer.Add(ActivateButton, 0, wx.ALL, 5)
        btnSizer.Add(self.ResetButton, 0, wx.ALL, 5)
        btnSizer.Add(CancelButton, 0, wx.ALL, 5)
        topSizer.Add(titleSizer, 0, wx.CENTER)
        topSizer.Add(wx.StaticLine(self.panel,), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(UserNameSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btnSizer1, 0, wx.ALL|wx.CENTER, 5)
        topSizer.Add(SeatSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(SystemSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(ScoreStyleSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btnSizer, 0, wx.ALL|wx.CENTER, 5)
        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)

    
    def InitUser(self):
        self.Continue = False
        Cursor.execute("SELECT * FROM user WHERE Active=?;", (1,))
        Rows = Cursor.fetchall()
        MyUniquer = "Hello"
        FoundOne = False
        for Row in Rows:
            FoundOne = True
            MyUniquer = Row[0]
        if FoundOne == False:
            return
        return

    def onContinue(self, event):
        self.UserName = self.UserNameInput.GetValue()
        if len(self.UserName) == 0:
            return
        self.Continue = True
        Cursor.execute("SELECT * FROM user WHERE UserName=?;", (self.UserName,))
        Rows = Cursor.fetchall()
        MyUniquer = "Hello"
        MyUserName = self.UserName
        FoundOne = False
        MySeat = 0
        MySystem = 0
        MyActive = 0
        MyScoreStyle = 0
        for Row in Rows:
            FoundOne = True
            MyUniquer = Row[0]
            MyUserName = Row[1]
            MySeat = Row[2]
            MySystem = Row[3]
            MyActive = Row[4]
            MyScoreStyle = Row[5]
        if FoundOne == False:
            MyUniquer = time.time()
            self.Uniquer = MyUniquer
            Cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                            (MyUniquer, str(MyUserName), MySeat, 0, MyActive, MyScoreStyle, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))   
            DataBase.commit()            
            Cursor.execute("INSERT INTO score VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                            (MyUniquer, str(MyUserName), 0, 0, 0, 0, 0, 0, 0, 0))
            DataBase.commit()
            ## MyDebug(DebugResolved, "Adding score for " + str(MyUserName))
            self.SeatInput.SetValue(self.Seats[MySeat])
            self.SystemInput.SetValue(self.Systems[MySystem])
            self.ScoreStyleInput.SetValue(self.ScoreStyles[MyScoreStyle])
            return
        if FoundOne:
            self.Uniquer = MyUniquer
            self.EditRecord = True
            self.SeatInput.SetValue(self.Seats[MySeat])
            self.SystemInput.SetValue(self.Systems[MySystem])
            self.ScoreStyleInput.SetValue(self.ScoreStyles[MyScoreStyle])
            self.ResetButton.Enable(True)
        return

    def OnActivateButton(self, event):     
        if self.Continue == False:
            return
        MyActive = 1
        Cursor.execute("SELECT * from user where Active = ?", (MyActive, ))
        MyUserNames = []
        Rows = Cursor.fetchall()
        RowCount = 0
        for Row in Rows:
            FoundOne = True
            MyUserNames.append(Row[0])
            RowCount = RowCount + 1
        MyActive = 0
        for Things in range(RowCount):
            Cursor.execute("UPDATE user SET Active = ? where Uniquer = ?;",
                    (MyActive, MyUserNames[Things]))
            DataBase.commit()
        MyActive = 1    
        MySeat = X1.CvtSeatToInt(self.SeatInput.GetValue())
        MySystem = X1.CvtSystemToInt(self.SystemInput.GetValue())
        MyScoreStyle = X1.CvtStyleToInt(self.ScoreStyleInput.GetValue())
        Cursor.execute("UPDATE user SET Seat = ?, Active = ?, System = ?, ScoreStyle = ? where Uniquer = ?;",
                    (MySeat, MyActive, MySystem, MyScoreStyle, self.Uniquer))
        DataBase.commit()
        self.parent.UpdateUser(self.UserName)
        self.Close()
        return

    def OnCancelButton(self, event):
        self.Close()
        return

    def OnResetButton(self, event):
        ResetScoreForUser(self.UserName)
        return

class MyMainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(SizeDefaultX, SizeDefaultY))
        self.TestPack = []
        self.Example = -1
        self.FullMenuSelect = False
        self.MyChild = "Hello"
        self.UserReviewDialog = None
        self.DataBaseDialog = None
        self.BiddingBox = "Sailor"
        self.UserScoreDialog = None
        self.UserListDialog = None
        self.UserListDialogShown = False
        self.UserScoreDialogShown = False
        self.UserReviewDialogShown = False
        self.UserReviewDialogAllUsers = False
        self.DataBaseDialogShown = False
        self.PBNDialogShown = False
        self.SetBackgroundColour("yellow")
        self.parent = parent
        self.ShowHandOpen = False
        self.Context = X1.Context(True)
        self.Context.User = SetDefaultUser()
        ## MyDebug(DebugResolved, "MyMainFrame User " + str(self.Context.User.UserName) + " Style " + str(self.Context.User.ScoreStyle))
        self.Context.ScoreInfo = GetScoreForUser(self.Context.User.UserName)        
        self.Context.Flip = True
        self.Session = X1.PracticeSession()
        MyMenuBar = wx.MenuBar()
        MyMenu = wx.Menu()
        MyMenu.Append(1011, "Open", "Open")
        MyMenuItem = wx.MenuItem(MyMenu, 1012, '&Review\tCtrl+R', 'Review Hands')
        MyMenuItem.SetBitmap(wx.Image("Buttons/Review.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        MyMenu.AppendItem(MyMenuItem)



        MyMenuBar.Append(MyMenu, "PBN")
        self.Bind(wx.EVT_MENU, self.OpenPBNFile, id=1011)
        self.Bind(wx.EVT_MENU, self.OnPBNReview, id=1012)

        MyMenu = wx.Menu()        
        MyMenuItem = wx.MenuItem(MyMenu, MenuNumber001, '&Play\tCtrl+P', 'Play a Hand')
        MyMenuItem.SetBitmap(wx.Image("Buttons/Play.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        MyMenu.AppendItem(MyMenuItem)
        MyMenuItem = wx.MenuItem(MyMenu, MenuNumber002, '&User Review\tCtrl+U', 'User Review')
        MyMenuItem.SetBitmap(wx.Image("Buttons/Review.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        MyMenu.AppendItem(MyMenuItem)
        MyMenuItem = wx.MenuItem(MyMenu, MenuNumber202, '&General Review\tCtrl+G', 'General Review')
        MyMenuItem.SetBitmap(wx.Image("Buttons/Review.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        MyMenu.AppendItem(MyMenuItem)

        MyMenuItem = wx.MenuItem(MyMenu, MenuNumber004, '&Cobble\tCtrl+C', 'Cobble Hands')
        MyMenuItem.SetBitmap(wx.Image("Buttons/Boot.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        MyMenu.AppendItem(MyMenuItem)

        MyMenuItem = wx.MenuItem(MyMenu, MenuNumber003, '&Quit\tCtrl+Q', 'Quit the Application')
        MyMenuItem.SetBitmap(wx.Image("Buttons/Exit.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        MyMenu.AppendItem(MyMenuItem)        
        MyMenuBar.Append(MyMenu, "Play Hands")

        MyMenu = wx.Menu()
        MySubMenu = wx.Menu()
        MySubMenu.Append(MenuNumber039, 'No', kind=wx.ITEM_RADIO)
        MySubMenu.Append(MenuNumber038, 'Yes', kind=wx.ITEM_RADIO)
        MyMenu.AppendMenu(-1, 'Practice Session', MySubMenu)

        MySubMenu = wx.Menu()
        MySubMenu.Append(MenuNumber040, 'Yes', kind=wx.ITEM_RADIO)
        MySubMenu.Append(MenuNumber041, 'No', kind=wx.ITEM_RADIO)
        MyMenu.AppendMenu(-1, 'Practice Bidding', MySubMenu)

        MySubMenu = wx.Menu()
        for PlayerCount in range(4):
            StartId = wx.NewId()
            MySubMenu.Append(StartId, X1.PlayerStr(PlayerCount), kind = wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, lambda evt, index = PlayerCount: self.SetPracticeDealer(evt, index), id = StartId)
        MyMenu.AppendMenu(-1, "Practice Dealer", MySubMenu)

        MySubMenu = wx.Menu()
        for PlayerCount in range(2):
            StartId = wx.NewId()
            MySubMenu.Append(StartId, X1.PracticeTypeStr(PlayerCount), kind = wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, lambda evt, index = PlayerCount: self.SetPracticeType(evt, index), id = StartId)
        MyMenu.AppendMenu(-1, "Practice Type", MySubMenu)

        MySubMenu = wx.Menu()
        for PlayerCount in range(3):
            StartId = wx.NewId()
            MySubMenu.Append(StartId, X1.PracticeLevelStr(PlayerCount), kind=wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, lambda evt, index = PlayerCount: self.SetPracticeLevel(evt, index), id = StartId)
        MyMenu.AppendMenu(-1, "Practice Level", MySubMenu)

        MySubMenu = wx.Menu()
        for PlayerCount in range(3):
            StartId = wx.NewId()
            MySubMenu.Append(StartId, X1.PracticeSuitStr(PlayerCount), kind=wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, lambda evt, index = PlayerCount: self.SetPracticeSuit(evt, index), id = StartId)
        MyMenu.AppendMenu(-1, "Practice Suit", MySubMenu)

        MySubMenu = wx.Menu()
        for PlayerCount in range(6):
            StartId = wx.NewId()
            MySubMenu.Append(StartId, X1.PracticeBidTypeStr(PlayerCount), kind=wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, lambda evt, index = PlayerCount: self.SetPracticeBidType(evt, index), id = StartId)
        MyMenu.AppendMenu(-1, "BidType", MySubMenu)
        MyMenu.Append(MenuNumber042, "Generate 20", "20 specific hands to Database")        
        MyMenu.Append(MenuNumber046, "Generate 1000", "1000 to Database")        
        MyMenu.Append(MenuNumber047, "Test 8", "Test 8")        

        MyMenuBar.Append(MyMenu, "Practice")


##
##        MyMenu = wx.Menu()
####        MySubMenu = wx.Menu()
####        for PlayerCount in range(2):
####            StartId = wx.NewId()
####            MySubMenu.Append(StartId, X1.PracticeTypeStr(PlayerCount), kind = wx.ITEM_RADIO)
####            self.Bind(wx.EVT_MENU, lambda evt, index = PlayerCount: self.SetDataBaseType(evt, index), id = StartId)
####        MyMenu.AppendMenu(-1, "Type", MySubMenu)
##
##        MySubMenu = wx.Menu()
##        for PlayerCount in range(4):
##            StartId = wx.NewId()
##            MySubMenu.Append(StartId, X1.PracticeLevelStr(PlayerCount), kind=wx.ITEM_RADIO)
##            self.Bind(wx.EVT_MENU, lambda evt, index = PlayerCount: self.SetDataBaseLevel(evt, index), id = StartId)
##        MyMenu.AppendMenu(-1, "Level", MySubMenu)
##
##        MySubMenu = wx.Menu()
##        for PlayerCount in range(4):
##            StartId = wx.NewId()
##            MySubMenu.Append(StartId, X1.PracticeSuitStr(PlayerCount), kind=wx.ITEM_RADIO)
##            self.Bind(wx.EVT_MENU, lambda evt, index = PlayerCount: self.SetDataBaseSuit(evt, index), id = StartId)
##        MyMenu.AppendMenu(-1, "Suit", MySubMenu)
##
##        MySubMenu = wx.Menu()
##        for PlayerCount in range(6):
##            StartId = wx.NewId()
##            MySubMenu.Append(StartId, X1.PracticeBidTypeStr(PlayerCount), kind=wx.ITEM_RADIO)
##            self.Bind(wx.EVT_MENU, lambda evt, index = PlayerCount: self.SetDataBaseBidType(evt, index), id = StartId)
##        MyMenu.AppendMenu(-1, "BidType", MySubMenu)
##        MyMenu.Append(MenuNumber142, "Review", "Review Database")        
##        MyMenuBar.Append(MyMenu, "DataBase")
##



        MyMenu = wx.Menu()
        MyMenuItem = wx.MenuItem(MyMenu, MenuNumber401, '&Maintain\tCtrl+M', 'Maintain User')
        MyMenuItem.SetBitmap(wx.Image("Buttons/Maintain.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        MyMenu.AppendItem(MyMenuItem)

        MyMenuItem = wx.MenuItem(MyMenu, MenuNumber407, '&List\tCtrl+L', 'List Users')
        MyMenuItem.SetBitmap(wx.Image("Buttons/Maintain.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        MyMenu.AppendItem(MyMenuItem)

        MyMenuBar.Append(MyMenu, "Users")       
        MyMenu = wx.Menu()
        self.NTStr1 = ("No", "Yes")
        MySubMenu = wx.Menu()
        for PlayerCount in range(2):
            StartId = wx.NewId()
            MySubMenu.Append(StartId, self.NTStr1[PlayerCount], kind=wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, lambda evt, index = PlayerCount: self.SetCheatControl(evt, index), id=StartId)
        MyMenu.AppendMenu(-1, "Cheat", MySubMenu)        
        MySubMenu = wx.Menu()
        MySubMenu.Append(MenuNumber141, 'No', kind=wx.ITEM_RADIO)
        MySubMenu.Append(MenuNumber140, 'Yes', kind=wx.ITEM_RADIO)
        MyMenu.AppendMenu(-1, 'Show Played Cards', MySubMenu)

        MySubMenu = wx.Menu()
        MySubMenu.Append(MenuNumber240, 'Yes', kind=wx.ITEM_RADIO)
        MySubMenu.Append(MenuNumber241, 'No', kind=wx.ITEM_RADIO)
        MyMenu.AppendMenu(-1, 'Bidding Hints', MySubMenu)
        MySubMenu = wx.Menu()
        MySubMenu.Append(MenuNumber242, 'Yes', kind=wx.ITEM_RADIO)
        MySubMenu.Append(MenuNumber243, 'No', kind=wx.ITEM_RADIO)
        MyMenu.AppendMenu(-1, 'Card Play Hints', MySubMenu)



        MyMenuBar.Append(MyMenu, "Options")


        MyMenu = wx.Menu()
        self.NTStr1 = ("No", "Yes")
        MySubMenu = wx.Menu()
        for PlayerCount in range(2):
            StartId = wx.NewId()
            MySubMenu.Append(StartId, self.NTStr1[PlayerCount], kind=wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, lambda evt, index = PlayerCount: self.SetHelpControl(evt, index), id=StartId)
        MyMenu.AppendMenu(-1, "Activate", MySubMenu)        
        MyMenuBar.Append(MyMenu, "Help")

        
        self.SetMenuBar(MyMenuBar)        
        wx.EVT_MENU(self, MenuNumber001, self.DealTheCards)
        wx.EVT_MENU(self, MenuNumber002, self.OnReviewUserHands)
        wx.EVT_MENU(self, MenuNumber202, self.OnAllUserHands)

        wx.EVT_MENU(self, MenuNumber038, self.OnPracticeYes)
        wx.EVT_MENU(self, MenuNumber039, self.OnPracticeNo)
        wx.EVT_MENU(self, MenuNumber040, self.OnPracticeBiddingYes)
        wx.EVT_MENU(self, MenuNumber041, self.OnPracticeBiddingNo)
        wx.EVT_MENU(self, MenuNumber140, self.OnShowPlayedCardsYes)
        wx.EVT_MENU(self, MenuNumber141, self.OnShowPlayedCardsNo)
##        wx.EVT_MENU(self, MenuNumber142, self.OnDataBaseHands)
        wx.EVT_MENU(self, MenuNumber240, self.OnShowBidHintYes)
        wx.EVT_MENU(self, MenuNumber241, self.OnShowBidHintNo)
        wx.EVT_MENU(self, MenuNumber242, self.OnShowPlayHintYes)
        wx.EVT_MENU(self, MenuNumber243, self.OnShowPlayHintNo)

        wx.EVT_MENU(self, MenuNumber004, self.OnCobble)        


        wx.EVT_MENU(self, MenuNumber401, self.UserAdd)        
        wx.EVT_MENU(self, MenuNumber407, self.OnUserList)
        wx.EVT_MENU(self, MenuNumber042, self.OnPopulate4)
        wx.EVT_MENU(self, MenuNumber046, self.OnPopulate3)
        wx.EVT_MENU(self, MenuNumber047, self.OnPopulate1)
        
        wx.EVT_MENU(self, MenuNumber003, self.OnClose)
        self.StatusBar = self.CreateStatusBar()
        self.StatusBar.SetStatusText("Use the Menus to start the game or manipulate the set-up")
        return


    def OpenPBNFile(self, event):
        print "OpenPBNFile"
        filename = "Hello"
        MyLines = []
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.pbn", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
##            path = dlg.GetPath()
##            mypath = os.path.basename(path)
##            self.SetStatusText("You selected: %s" % mypath)
##        MyFile = open(path, 'r')
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            f = open(os.path.join(dirname, filename), 'r')
            MyLines = f.readlines()
            f.close()
        MyDealNum = 1
        MyPBN = PBN.PortableBridgeNotation()
        MyPBN.FileName = filename
        MyPBN.DealNum = MyDealNum
        
        DoAuction = False
        MyAuction = []
        DoPlay = False
        MyPlay = []
        for Things in MyLines:
##            TempPack = string.strip(string.strip(MyPack, "["), "]")
            if PBN.IsBlankLine(Things) == True:
##                MyPBN.ParseDeal()
                ValidPack, ThePack = PBN.ParseDeal(MyPBN.Deal)
            
                MyPBN.Auction = str(MyAuction)
                MyPBN.Play = str(MyPlay)
##                MyPBN.ParseAuction()
                
##                MyPBN.PrintPBN()
                MyAuction = []
                MyPlay = []
##                print str(MyAuction)
##                print str(MyPlay)
                if ValidPack == True:
                    MyUniquer = time.time()

                    Cursor.execute("INSERT INTO pbn VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                                    (MyUniquer, MyPBN.Dealer, MyPBN.Declarer, MyPBN.Contract, MyPBN.Result, MyPBN.Event, MyPBN.Site, MyPBN.Date,
                                     MyPBN.Board, MyPBN.North, MyPBN.East, MyPBN.South, MyPBN.West, MyPBN.Vulnerable, MyPBN.Deal,
                                     MyPBN.HomeTeam, MyPBN.Room, MyPBN.Round, MyPBN.Score, MyPBN.Section, MyPBN.Table,
                                     MyPBN.VisitTeam, MyPBN.Auction, MyPBN.Play, MyPBN.FileName, MyPBN.DealNum))
##0  Uniquer
##1 Dealer
##2 Declarer
##3 Contract
##4 Result
##5  Event
##6  Site
##7  EventDate
##8   Board
##9  North
##10  South
##11  East
##12 West
##13 Vulnerable
##14 Deal
##15 HomeTeam
##16 Room
##17 Round
##18 Score
##19 Section
##20 EventTable
##21 VisitTeam
##22 Auction
##23 Play
##24 FileName
##25 DealNum


##
##                    
##                    PickleData = cPickle.dumps(MyPBN.Pack, cPickle.HIGHEST_PROTOCOL)
##                    print str(MyUniquer)
##                    Cursor.execute("INSERT INTO " + self.Context.TableName + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
##                                    (MyUniquer, str(-1), MyPBN.Declarer, MyPBN.Dealer, -1, -1, -1, -1,
##                                    -1, str(-1), -1, 0, 0, str(MyPBN.Pack), sqlite3.Binary(PickleData),
##                                     str(-1), self.Context.User.UserName, self.Context.User.Seat, MyUniquer))
                    DataBase.commit()
                MyPBN.Reset()
                MyDealNum = MyDealNum + 1
                MyPBN.FileName = filename
                MyPBN.DealNum = MyDealNum
            if PBN.IsBlankLine(Things) == False:            
                MyString = string.strip(string.strip(Things, "\n"))                    
##                if PBN.IsKeyWordLineStart(MyString):
##                    if PBN.IsKeyWordLineEnd(MyString):
                KeyBool, KeyName, KeyText = PBN.GetKeyWordLine(MyString)
                if KeyBool == False:
                    if MyString != "*":
                        if DoAuction:
                            Test = string.splitfields(MyString, " ")
                            for Things in Test:
                                MyAuction.append(Things)
                        if DoPlay:
                            Test = string.splitfields(MyString, " ")
                            for Things in Test:
                                MyPlay.append(Things)                        
##                        print "Play " + str(MyString)
                if KeyBool:
                    if KeyText != "#":
                        MyPBN.UpdateKey(KeyName, KeyText)
                    DoAuction = False
                    if KeyName == "Auction":
                        DoAuction = True
                    DoPlay = False
                    if KeyName == "Play":
                        DoPlay = True

        print "finish"                                      
        dlg.Destroy()
        return

    
    
    def ResetScore(self, MyUserName):
        if self.Context.Score == False:
           return
        if self.UserScoreDialogShown == False:
            return            
        self.Context.ScoreInfo = GetScoreForUser(MyUserName)
        self.Context.User = SetDefaultUser()
        self.UserScoreDialog.ResetScoreDialog(self.Context)
        return
        
    def OnScoreDialogClose(self):
        self.Context.Score = False
        self.UserScoreDialogShown = False
        return

    def OnUserListDialogClose(self):
        self.Context.Review = False
        self.UserListDialogShown = False
##        print "UserListDialogShown now False"
        return

    def OnUserReviewDialogClose(self):
        self.Context.Review = False
        self.UserReviewDialogShown = False
        self.UserReviewDialogAllUsers = False
##        print "UserReviewDialogShown now False"
        return

    def OnPBNDialogClose(self):
##        print "OnPBNDialogClose"
        self.Context.Review = False
        self.Context.DataBase = False
        self.PBNDialogShown = False
        return

    def OnDataBaseDialogClose(self):
        self.Context.Review = False
        self.Context.DataBase = False
        self.DataBaseDialogShown = False
        return

    def OnDataBaseHands(self, event):
        if self.DataBaseDialogShown == True:
            return
        self.Context.DataBase = True
        self.DataBaseDialog = MyDataBaseDialog(self, -1, "Review of DataBase", self.Context, self.Session)
        self.DataBaseDialog.Show()
        self.DataBaseDialogShown = True
        return

    def OnPBNReview(self, event):
        if self.PBNDialogShown == True:
            return
##        self.Context.DataBase = True
        self.PBNDialog = MyPBNDialog(self, -1, "Review of PBN DataBase", self.Context)
        self.PBNDialog.Show()
        self.PBNDialogShown = True
        return
        
    def OnReviewUserHands(self, event):
        if self.UserReviewDialogAllUsers == False:
            if self.UserReviewDialogShown == True:
                return
        if self.UserReviewDialogShown == True:
            self.UserReviewDialog.Destroy()
        self.UserReviewDialogAllUsers = False
        self.UserReviewDialog = MyUserDialog(self, -1, "Review of User Hands", self.Context, True)
        self.UserReviewDialog.Show()
        self.UserReviewDialogShown = True
        return

    def OnAllUserHands(self, event):
        if self.UserReviewDialogShown == True:
            if self.UserReviewDialogAllUsers:
                return
            self.UserReviewDialog.Destroy()
####            return
##        if self.UserReviewDialogShown == True:
##            self.UserReviewDialog.Destroy()
##
##                
        self.UserReviewDialog = MyUserDialog(self, -1, "Review of User Hands", self.Context, False)
        self.UserReviewDialogAllUsers = True        
        self.UserReviewDialog.Show()
        self.UserReviewDialogShown = True
        return
    
    def OnUserHand(self, MyUniquer):
        self.Context.Review = True
        for MyCount in range(4):
            self.Context.Human[MyCount] = False        
        self.Context.Human[self.Context.User.Seat] = True
        self.Context.UpdateSystem(X1.GetTeam(self.Context.User.Seat), self.Context.User.System)
        Cursor.execute("SELECT * FROM " + self.Context.TableName + " WHERE Uniquer=?;", (MyUniquer,))
        Rows = Cursor.fetchall()
        FoundOne = False
        for Row in Rows:
            FoundOne = True
            MyPack = Row[13]
        if FoundOne == False:
            return     
        TempPack = string.splitfields(string.strip(string.strip(MyPack, "["), "]"), ",")
        MyNewPack = []
        for Things in TempPack:
            MyNewPack.append(int(Things))
        self.FullMenuSelect = True
        self.Context.MetaDealer = True
        self.Context.Reset()
        self.Context.PBNMode = False
        self.Context.PBNContinue = False
        self.Context.ScoreInfo = GetScoreForUser(self.Context.User.UserName)
        if self.Context.User.ScoreStyle != X1.ScoreStyleNone:
            self.Context.Score = True
            if self.UserScoreDialogShown == False:
                self.UserScoreDialog = MyScoreDialog(self, -1, "User Score", self.Context)
                self.UserScoreDialog.Show()
                self.UserScoreDialogShown = True
        self.Context.MetaDealer = False
        if self.ShowHandOpen:
            self.MyChild.Destroy()
            self.ShowHandOpen = False
        self.MyChild = ShowHand(self, -1, self.Context, self.Session)
        self.MyChild.ShowHandInit(MyNewPack)
        self.BiddingBox = MyBiddingBox(self, -1, self.Context, self.Session)
        return


    def OnPBNHand(self, MyUniquer):
##        print "OnDataBaseHand"
        TableName = "pbn"
        Cursor.execute("SELECT * FROM " + TableName + " WHERE Uniquer=?;", (MyUniquer,))
        Rows = Cursor.fetchall()
        FoundOne = False

##pbn
##0  Uniquer
##1 Dealer
##2 Declarer
##3 Contract
##4 Result
##5  Event
##6  Site
##7  EventDate
##8   Board
##9  North
##10  South
##11  East
##12 West
##13 Vulnerable
##14 Deal
##15 HomeTeam
##16 Room
##17 Round
##18 Score
##19 Section
##20 EventTable
##21 VisitTeam
##22 Auction
##23 Play
##24 FileName
##25 DealNum

        for Row in Rows:
            FoundOne = True
            MyDealer = Row[1]
            MyDeal = Row[14]
            MyAuction = Row[22]
            MyPlay = Row[23]
        if FoundOne == False:
            return
        ValidPack, ThePack = PBN.ParseDeal(MyDeal)
        ValidAuction, TheAuction = PBN.ParseAuction(MyAuction)
        ValidPlay, ThePlay, ValidArray, ValidCount = PBN.ParsePlay(MyPlay)
        MyDealer1 = PBN.GetDealer(MyDealer)
        
##        print "ValidPack " + str(ValidPack)
##        print "The Pack " + str(ThePack)
##        print "Dealer " + str(MyDealer)        
##        print "Dealer1 " + str(MyDealer1)
##        print "Deal " + str(MyDeal)
##        print "Auction " + str(MyAuction)
##        print "Valid Auction " + str(ValidAuction)
##        print "The Auction " + str(TheAuction)
##        print "Play " + str(MyPlay)        
##        print "ValidPlay " + str(ValidPlay)
##        print "MyPlay " + str(ThePlay)
##        print "Valid  " + str(ValidArray)
##        print "Counter " + str(ValidCount)
##        for MyCount in range(4):
##            self.Context.Human[MyCount] = False        
##        self.Context.Human[self.Context.User.Seat] = True
##        self.Context.UpdateSystem(X1.GetTeam(self.Context.User.Seat), self.Context.User.System)
        self.FullMenuSelect = True
        self.Context.Reset()
        self.Context.PBNMode = True
        self.Context.PBNContinue = True
        for MyCount in range(4):
            self.Context.Human[MyCount] = False
        self.Context.Human[self.Context.User.Seat] = True
        self.Context.UpdateSystem(X1.GetTeam(self.Context.User.Seat), self.Context.User.System)
        self.Context.PBNAuction = TheAuction
        self.Context.PBNPlay = ThePlay
        self.Context.Dealer = MyDealer1
##        self.Context.PBNValidPlay = ValidArray
        self.Context.DealerSelect = False
        self.Context.ScoreInfo = GetScoreForUser(self.Context.User.UserName)
        if self.Context.User.ScoreStyle != X1.ScoreStyleNone:
            self.Context.Score = True
            if self.UserScoreDialogShown == False:
                self.UserScoreDialog = MyScoreDialog(self, -1, "User Score", self.Context)
                self.UserScoreDialog.Show()
                self.UserScoreDialogShown = True
        self.Context.MetaDealer = False
        if self.ShowHandOpen:
            self.MyChild.Destroy()
            self.ShowHandOpen = False
        self.MyChild = ShowHand(self, -1, self.Context, self.Session)
        self.MyChild.ShowHandInit(ThePack)
        self.BiddingBox = MyBiddingBox(self, -1, self.Context, self.Session)
        return

    def OnDataBaseHand(self, MyUniquer):
##        print "OnDataBaseHand"
        self.Context.Review = True
        self.Context.DataBase =  True
        self.Context.PBNMode = False
        self.Context.PBNContinue = False

        
        for MyCount in range(4):
            self.Context.Human[MyCount] = False        
        self.Context.Human[self.Context.User.Seat] = True
        self.Context.UpdateSystem(X1.GetTeam(self.Context.User.Seat), self.Context.User.System)
        Cursor.execute("SELECT * FROM " + self.Context.TableName + " WHERE Uniquer=?;", (MyUniquer,))
        Rows = Cursor.fetchall()
        FoundOne = False
        for Row in Rows:
            FoundOne = True
            MyPack = Row[13]
        if FoundOne == False:
            return     
        TempPack = string.splitfields(string.strip(string.strip(MyPack, "["), "]"), ",")
        MyNewPack = []
        for Things in TempPack:
            MyNewPack.append(int(Things))
        self.FullMenuSelect = True
        self.Context.MetaDealer = True
        self.Context.Reset()
        self.Context.ScoreInfo = GetScoreForUser(self.Context.User.UserName)
        if self.Context.User.ScoreStyle != X1.ScoreStyleNone:
            self.Context.Score = True
            if self.UserScoreDialogShown == False:
                self.UserScoreDialog = MyScoreDialog(self, -1, "User Score", self.Context)
                self.UserScoreDialog.Show()
                self.UserScoreDialogShown = True
        self.Context.MetaDealer = False
        if self.ShowHandOpen:
            self.MyChild.Destroy()
            self.ShowHandOpen = False
        self.MyChild = ShowHand(self, -1, self.Context, self.Session)
        self.MyChild.ShowHandInit(MyNewPack)
        self.BiddingBox = MyBiddingBox(self, -1, self.Context, self.Session)
        return

    def OnClose(self, event):
        DataBase.close()
        if self.Context.Practice:
            MyStr = "## that's all folks!"
            self.Session.WriteFile(MyStr)
            self.Session.CloseFile()
        self.Destroy()
        return

    def ResumeContext(self, MyContext):
        self.Context = MyContext
        return
    
    def OnAutomaticDealer(self, event):
        self.Context.DealerSelect = False
        return

    def OnSelectableDealer(self, event):
        self.Context.DealerSelect = True
        return

    def OnFlipOff(self, event):
        self.Context.Flip = False

    def OnFlipOn(self, event):
        self.Context.Flip = True

    def OnShowPlayHintYes(self, event):
        self.Context.ShowPlayHint = True
        return            

    def OnShowPlayHintNo(self, event):
        self.Context.ShowPlayHint = False
        return            

    def OnShowBidHintYes(self, event):
        self.Context.ShowBidHint = True
        return            

    def OnShowBidHintNo(self, event):
        self.Context.ShowBidHint = False
##        print "OnShowBidHintNo"
        return            
        
    def OnShowPlayedCardsYes(self, event):
        self.Context.ShowPlayed = True
        return            

    def OnShowPlayedCardsNo(self, event):
        self.Context.ShowPlayed = False
        return            

    def OnPracticeBiddingYes(self, event):
        self.Context.PracticeBidding = True
        return            

    def OnPracticeBiddingNo(self, event):
        self.Context.PracticeBidding = False
        return

    def OnPracticeYes(self, event):
        self.Context.Practice = True
        self.Session.OpenFile()
        MyStr = "## Hello, Sailor!" + "\n\n"
        self.Session.WriteFile(MyStr)
        return            

    def OnPracticeNo(self, event):
        self.Context.Practice = False
        return


    def SetDataBaseLevel(self, event, MyLevel):
        self.Session.UpdateDBLevel(MyLevel)
        return

    def SetDataBaseType(self, event, MyType):
        self.Session.UpdateDBType(MyType)
        return

    def SetDataBaseSuit(self, event, MySuit):
        self.Session.UpdateDBSuit(MySuit)
        return

    def SetDataBaseBidType(self, event, MyBidType):
        self.Session.UpdateDBBidType(MyBidType)
        return

    def SetHelpControl(self, event, MyVal):
        self.Context.UpdateHelp(MyVal)
        return 

    def SetCheatControl(self, event, index):
        for x in range(4):
            self.Context.UpdateCheat(x, index)
        return 

    def SetFormat(self, event, MyFormat):
        self.Context.UpdateFormat(MyFormat)
        return

    def SetExample(self, event, MyExample):
        self.Example = MyExample
        self.Context.SetTableName(X1ExampleName(MyExample))
        return

    def SetPracticeBidType(self, event, MyBidType):
        self.Session.UpdateBidType(MyBidType)
        return

    def SetPracticeDealer(self, event, MyDealer):
        self.Session.UpdateDealer(MyDealer)
        return
    
    def SetPracticeType(self, event, MyType):
        self.Session.UpdateType(MyType)
        return

    def SetPracticeSuit(self, event, MySuit):
##        print "SetSuit " + str(MySuit)
        if MySuit == 0:
            return
        self.Session.UpdateSuit(MySuit)
        self.Session.UpdateMinMaxBids()
##        print "SetPracticeSuit Min Bid " + X1.BidStr(self.Session.MinBidNum)
##        print "SetPracticeSuit Max Bid " + X1.BidStr(self.Session.MaxBidNum)
        return

    def SetPracticeLevel(self, event, MyLevel):
        self.Session.UpdateLevel(MyLevel)
        self.Session.UpdateMinMaxBids()
##        print "SetPracticeLevel Min Bid " + X1.BidStr(self.Session.MinBidNum)
##        print "SetPracticeLevel Max Bid " + X1.BidStr(self.Session.MaxBidNum)
        return
    
    def SetPlayerControl(self, event, MyPlayer, index):
        IndexStr = "False"
        if index == True:
            IndexStr = "True"
        self.Context.UpdateHuman(MyPlayer, index)
        return

    def SetTeamRule(self, event, team, index):
        self.Context.UpdateRule(team, index)
        return

    def SetTeamSys(self, event, team, index):
        self.Context.UpdateSystem(team, index)
        return

    def UpdateUser(self, MyUserName):
        MyUser = X1.User(MyUserName)
        MyUniquer = "Hello"
        MySeat = 0
        MySystem = 0
        MyActive = 0
        MyScoreStyle = 0
        MyHandsDealt = 0
        MyHandsPlayed = 0
        MyHandsWon = 0
        Cursor.execute("SELECT * FROM user WHERE UserName=?;", (MyUserName,))
        Rows = Cursor.fetchall()
        FoundOne = False
        for Row in Rows:
            FoundOne = True
            MyUniquer = Row[0]
            ## MyDebug(DebugResolved, "MyUserName " + str(MyUserName) + " there")
            MySeat = Row[2]
            MySystem = Row[3]
            MyActive = Row[4]
            MyScoreStyle = Row[5]
            MyHandsDealt = Row[6]
            MyHandsPlayed = Row[7]
            MyHandsWon = Row[8]
        MyUser.Uniquer = MyUniquer
        MyUser.Seat = MySeat
        MyUser.System = MySystem
        MyUser.Active = MyActive
        MyUser.ScoreStyle = MyScoreStyle
        MyUser.HandsDealt = MyHandsDealt
        MyUser.HandsWon = MyHandsWon
        MyUser.HandsPlayed = MyHandsPlayed
        self.Context.User = MyUser
        return


    def OnCobble(self, event):
        ## MyDebug(DebugResolved, "OnCobble")

        KosherDeal, NewPack, TestString = X1.ShufflePack()
        MyPuddleFrame = PuddleFrame(self, -1, X1.XXBridgeThing, self.Context, NewPack)
        MyPuddleFrame.Show(True)
##        
##        MyCobbleFrame = CobbleFrame(self, -1, X1.XXBridgeThing, self.Context)
####        MyUserFrame.InitUser()
##        MyCobbleFrame.Show(True)
        return
    
    def UserAdd(self, event):
        ## MyDebug(DebugResolved, "UserAdd")
        MyUserFrame = UserFrame(self, -1, X1.XXBridgeThing)
        MyUserFrame.InitUser()
        MyUserFrame.Show(True)
        return

    def OnUserList(self, event):
        if self.UserListDialogShown == True:
            return        
        self.UserListDialog = MyUserListDialog(self, -1, "Review of Users", self.Context)
        self.UserListDialog.Show()
        self.UserListDialogShown = True
        return

    def DealTheCards(self, event):
        ## MyDebug(DebugResolved, "DealTheCards")
        self.FullMenuSelect = True
        self.Context.Reset()
        self.Context.ScoreInfo = GetScoreForUser(self.Context.User.UserName)
        self.Context.Review = False
        self.Context.DataBase =  False
        self.Context.PBNMode = False
        self.Context.PBNContinue = False

        for MyCount in range(4):
            self.Context.Human[MyCount] = False
        if self.Context.User.ScoreStyle != X1.ScoreStyleNone:
            self.Context.Score = True
            if self.UserScoreDialogShown == False:
                self.UserScoreDialog = MyScoreDialog(self, -1, "User Score", self.Context)
                self.UserScoreDialog.Show()
                self.UserScoreDialogShown = True
        self.Context.Human[self.Context.User.Seat] = True
        self.Context.UpdateSystem(X1.GetTeam(self.Context.User.Seat), self.Context.User.System)
        if self.Context.Practice:           
            MyLoad, MyPack, MyDeclarer, MyContract, MyGetDealNum = LoadPracticeDealRandom(self.Context, self.Session)
            self.Session.UpdateNum(MyGetDealNum)
            self.Session.UpdatePack(MyPack)
            self.Session.UpdateContract(MyContract)
            self.Context.UpdatePracticeDeals(MyGetDealNum)               
            self.Session.Declarer = MyDeclarer
            self.Session.Player = self.Context.User.Seat
            self.Session.Uniquer = time.time()
            PickleData = cPickle.dumps(MyPack, cPickle.HIGHEST_PROTOCOL)
            Cursor.execute("INSERT INTO " + self.Context.TableName + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                            (self.Session.Uniquer, str(MyGetDealNum), self.Session.Declarer, self.Session.Dealer, self.Session.Type,
                             self.Session.Level, self.Session.Suit, self.Session.BidType,
                             self.Session.Contract, str(self.Session.Result), self.Session.Success,
                             self.Session.Tricks, self.Session.Variance, str(self.Session.Pack),
                             sqlite3.Binary(PickleData), str(self.Session.System), self.Context.User.UserName,
                             self.Context.User.Seat, self.Session.Uniquer))
            DataBase.commit()
            for MyPlayers in range(4):
                self.Context.Human[MyPlayers] = False
                self.Context.Cheat[MyPlayers] = False
            self.Context.Human[self.Session.Player] = True
            if MyLoad:
                self.Context.Reset()
                if self.ShowHandOpen:
                    self.MyChild.Destroy()
                    self.ShowHandOpen = False
                self.MyChild = ShowHand(self, -1, self.Context, self.Session)
                self.MyChild.ShowHandInit(MyPack)
                self.BiddingBox = MyBiddingBox(self, -1, self.Context, self.Session)
                return
        if self.ShowHandOpen:
            self.MyChild.Destroy()
            self.ShowHandOpen = False
        self.MyChild = ShowHand(self, -1, self.Context, self.Session)
        self.MyChild.ShowHandInit("Hello")
        self.BiddingBox = MyBiddingBox(self, -1, self.Context, self.Session)
        return

    def OnPopulate4(self, event):
        StartTime = time.time()
        self.ProgressPanel = MyProgressPanel(self, -1, self.Context, self.Session)
        return

    def OnPopulate14(self, event):
        StartTime = time.time()
        MyDebug(DebugTime, "Start Time : " + str(StartTime))
        TossInCount = 0        
        TestBidCount = 0
        TestBidSuccess = 0
        TotalDeals = 0
        MaxIter = 120000
        MyContext = self.Context
        TotalHandsBid = 0
        for Test1 in range(MaxIter):
            if TotalDeals < 100:
                MyBid, MyContext, MySession, MyMsg = LoadRandomSession13()
                if MyBid == False:
                    TossInCount = TossInCount + 1

                if MyBid == True:
                    MyContext.User = SetDefaultUser()
                    TotalHandsBid = TotalHandsBid + 1
                    if MySession.Contract == X1.Bid3N:
                        TotalDeals = TotalDeals + 1
                        MySuccess, MyContext = APD.PlayDeal(MyContext)
                        MyTeam = X1.GetTeam(MyContext.Declarer)
                        MySession.Tricks = MyContext.Teams[MyTeam].TricksWon
                        MyTricksReqd = MyContext.Teams[MyTeam].TricksReqd
                        MySession.Variance = MyContext.Teams[MyTeam].TricksWon - MyContext.Teams[MyTeam].TricksReqd       
                        MySession.Success = MySuccess
                        MySession.Contract = MyContext.Contract
                        MySession.Result = APD.GetResult(MyContext)
                        MySession.Declarer = MyContext.Declarer                        
                        MySession.Num = TotalDeals
                        MyDebug(DebugTime, "Deal : " + str(TotalDeals))
                        TestBidCount = TestBidCount + 1
                        if MySession.Success:
                            TestBidSuccess = TestBidSuccess + 1                        
                        MySession.Uniquer = time.time()
                        PickleData = cPickle.dumps(MySession.Pack, cPickle.HIGHEST_PROTOCOL)
                        Cursor.execute("INSERT INTO " + MyContext.TableName + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                                        (MySession.Uniquer, str(MySession.Num), MySession.Declarer, MySession.Dealer, MySession.Type,
                                         MySession.Level, MySession.Suit, MySession.BidType, 
                                         MySession.Contract, str(MySession.Result), MySession.Success, MySession.Tricks,
                                         MySession.Variance, str(MySession.Pack), sqlite3.Binary(PickleData),
                                         str(MySession.System), MyContext.User.UserName, MyContext.User.Seat, MySession.Uniquer))
                        DataBase.commit()
                    
        EndTime = time.time()
        MyDebug(DebugTime, "End Time : " + str(EndTime))
        Duration = EndTime - StartTime
        MyDebug(DebugTime, "Duration : " + str(Duration))
        TestBidPercent =  0
        if TestBidCount > 0:
            TestBidPercent =  float(float(TestBidSuccess) / float(TestBidCount))
        MyDebug(DebugTime, "Total Hands        : " + str(TotalHandsBid + TossInCount))
        MyDebug(DebugTime, "Toss-Ins           : " + str(TossInCount))
        MyDebug(DebugTime, "Total Hands Bid    : " + str(TotalHandsBid))
        MyDebug(DebugTime, "Total Deals        : " + str(TotalDeals))
        MyDebug(DebugTime, "3NT Bids           : " + str(TestBidCount) + " Won : " + str(TestBidSuccess) + " % "+ str(TestBidPercent))        
        EndTime = time.time()
        MyDebug(DebugTime, "End Time : " + str(EndTime))
        Duration = EndTime - StartTime
        MyDebug(DebugTime, "Duration : " + str(Duration))
        return


    def OnPopulate15(self, event):
        StartTime = time.time()
        MyDebug(DebugTime, "Start Time : " + str(StartTime))
        TossInCount = 0
        TotalHandsBid = 0
        TestBidCount = 0
        TestBidSuccess = 0
        BidIdCount = []
        BidIdSuccess = []
        for x in range(35):
            BidIdCount.append(0)
            BidIdSuccess.append(0)
            
        MaxIter = 120000
        MyContext = self.Context
        for Test1 in range(MaxIter):
            if TotalHandsBid < 10000:
                MyBid, MyContext, MySession, MyMsg = LoadRandomSession13()
                if MyBid == False:
                    TossInCount = TossInCount + 1
                if MyBid == True:
                    MyContext.User = SetDefaultUser()
                    TotalHandsBid = TotalHandsBid + 1
                    MySuccess, MyContext = APD.PlayDeal(MyContext)
                    MyTeam = X1.GetTeam(MyContext.Declarer)
                    MySession.Tricks = MyContext.Teams[MyTeam].TricksWon
                    MyTricksReqd = MyContext.Teams[MyTeam].TricksReqd
                    MySession.Variance = MyContext.Teams[MyTeam].TricksWon - MyContext.Teams[MyTeam].TricksReqd       
                    MySession.Success = MySuccess
                    MySession.Contract = MyContext.Contract
                    MySession.Result = APD.GetResult(MyContext)
                    MySession.Declarer = MyContext.Declarer                        
                    MySession.Num = TotalHandsBid
                    MyDebug(DebugTime, "Deal : " + str(TotalHandsBid))
                    BidIdCount[MySession.Contract] = BidIdCount[MySession.Contract] + 1                    
                    if MySession.Success:
                        BidIdSuccess[MySession.Contract] = BidIdSuccess[MySession.Contract] + 1                       
                    MySession.Uniquer = time.time()
                    PickleData = cPickle.dumps(MySession.Pack, cPickle.HIGHEST_PROTOCOL)
                    Cursor.execute("INSERT INTO " + MyContext.TableName + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                                    (MySession.Uniquer, str(MySession.Num), MySession.Declarer, MySession.Dealer, MySession.Type,
                                     MySession.Level, MySession.Suit, MySession.BidType, 
                                     MySession.Contract, str(MySession.Result), MySession.Success, MySession.Tricks,
                                     MySession.Variance, str(MySession.Pack), sqlite3.Binary(PickleData),
                                     str(MySession.System), MyContext.User.UserName, MyContext.User.Seat, MySession.Uniquer))
                    DataBase.commit()
                    
        EndTime = time.time()
        MyDebug(DebugTime, "End Time : " + str(EndTime))
        Duration = EndTime - StartTime
        MyDebug(DebugTime, "Duration : " + str(Duration))
        TestBidPercent =  0
        if TestBidCount > 0:
            TestBidPercent =  float(float(TestBidSuccess) / float(TestBidCount))
        MyDebug(DebugTime, "Total Hands        : " + str(TotalHandsBid + TossInCount))
        MyDebug(DebugTime, "Toss-Ins           : " + str(TossInCount))
        MyDebug(DebugTime, "Total Hands Bid    : " + str(TotalHandsBid))
        for x in range(35):
            TestBidPercent =  0
            if BidIdCount[x] > 0:
                TestBidPercent =  float(float(BidIdSuccess[x]) / float(BidIdCount[x]))
            MyDebug(DebugTime, "Bid [" + X1.BidStr(x) + "]   : " + str(BidIdCount[x]) + " Won : " + str(BidIdSuccess[x]) + " % "+ str(TestBidPercent))        
        EndTime = time.time()
        MyDebug(DebugTime, "End Time : " + str(EndTime))
        Duration = EndTime - StartTime
        MyDebug(DebugTime, "Duration : " + str(Duration))
        return




    def OnPopulate13(self, event):
        StartTime = time.time()
        MyDebug(DebugTime, "Start Time : " + str(StartTime))
        TossInCount = 0        
        GerberCount = 0
        GerberSuccess = 0
        BlackwoodCount = 0
        BlackwoodSuccess = 0
        ControlCount = 0
        ControlSuccess = 0
        LimitCount = 0
        LimitSuccess = 0
        SustainCount = 0
        SustainSuccess = 0
        SlamScoreCount = 0
        SlamScoreSuccess = 0
        SlamScoreMajorsCount = 0
        SlamScoreMinorsCount = 0
        SlamScoreNoTrumpsCount = 0
        SlamScoreMajorsSuccess = 0
        SlamScoreMinorsSuccess = 0
        SlamScoreNoTrumpsSuccess = 0
        TotalDeals = 0
        MaxIter = 120000
        MyContext = self.Context
        TotalHandsBid = 0
        for Test1 in range(MaxIter):
            if TotalDeals < 1000:
                MyBid, MyContext, MySession, MyMsg = LoadRandomSession13()
                if MyBid == False:
                    TossInCount = TossInCount + 1

                if MyBid == True:
                    MyContext.User = SetDefaultUser()
                    TotalHandsBid = TotalHandsBid + 1
                    if MySession.Level == X1.PracticeLevelSlam:
                        TotalDeals = TotalDeals + 1
                        MySuccess, MyContext = APD.PlayDeal(MyContext)
                        MyTeam = X1.GetTeam(MyContext.Declarer)
                        MySession.Tricks = MyContext.Teams[MyTeam].TricksWon
                        MyTricksReqd = MyContext.Teams[MyTeam].TricksReqd
                        MySession.Variance = MyContext.Teams[MyTeam].TricksWon - MyContext.Teams[MyTeam].TricksReqd       
                        MySession.Success = MySuccess
                        MySession.Contract = MyContext.Contract
                        MySession.Result = APD.GetResult(MyContext)
                        MySession.Declarer = MyContext.Declarer





                        
                        MySession.Num = TotalDeals
                        MyDebug(DebugTime, "Deal : " + str(TotalDeals))

                        SlamScoreCount = SlamScoreCount + 1
                        if MySession.Suit == X1.PracticeSuitMajors:
                            SlamScoreMajorsCount = SlamScoreMajorsCount + 1
                        if MySession.Suit == X1.PracticeSuitMinors:
                            SlamScoreMinorsCount = SlamScoreMinorsCount + 1
                        if MySession.Suit == X1.PracticeSuitNoTrumps:
                            SlamScoreNoTrumpsCount = SlamScoreNoTrumpsCount + 1
                        if MySession.Success:
                            SlamScoreSuccess = SlamScoreSuccess + 1                        
                            if MySession.Suit == X1.PracticeSuitMajors:
                                SlamScoreMajorsSuccess = SlamScoreMajorsSuccess + 1
                            if MySession.Suit == X1.PracticeSuitMinors:
                                SlamScoreMinorsSuccess = SlamScoreMinorsSuccess + 1
                            if MySession.Suit == X1.PracticeSuitNoTrumps:
                                SlamScoreNoTrumpsSuccess = SlamScoreNoTrumpsSuccess + 1

                        MyTeam = X1.GetTeam(MySession.Declarer)
                        if GetDealByBidType(MyContext, MyTeam, X1.BidTypeRespControlQuery):
                            ControlCount = ControlCount + 1
                            if MySession.Success:
                                ControlSuccess = ControlSuccess + 1   
                        if GetDealByBidType(MyContext, MyTeam, X1.BidTypeReplyBlackwoodAceAsk):
                            BlackwoodCount = BlackwoodCount + 1
                            if MySession.Success:
                                BlackwoodSuccess = BlackwoodSuccess + 1
                        if GetDealByBidType(MyContext, MyTeam, X1.BidTypeReplyGerberAceAsk):
                            GerberCount = GerberCount + 1
                            if MySession.Success:
                                GerberSuccess = GerberSuccess + 1
                        if GetDealByBidType(MyContext, MyTeam, X1.BidTypeReplyLimitHonourAsk):
                            LimitCount = LimitCount + 1
                            if MySession.Success:
                                LimitSuccess = LimitSuccess + 1
                        if GetDealByBidType(MyContext, MyTeam, X1.BidTypeCallSustain):
                            SustainCount = SustainCount + 1
                            if MySession.Success:
                                SustainSuccess = SustainSuccess + 1                        
                        MySession.Uniquer = time.time()
                        PickleData = cPickle.dumps(MySession.Pack, cPickle.HIGHEST_PROTOCOL)
                        Cursor.execute("INSERT INTO " + MyContext.TableName + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                                        (MySession.Uniquer, str(MySession.Num), MySession.Declarer, MySession.Dealer, MySession.Type,
                                         MySession.Level, MySession.Suit, MySession.BidType, 
                                         MySession.Contract, str(MySession.Result), MySession.Success, MySession.Tricks,
                                         MySession.Variance, str(MySession.Pack), sqlite3.Binary(PickleData),
                                         str(MySession.System), MyContext.User.UserName, MyContext.User.Seat, MySession.Uniquer))
                        DataBase.commit()



                    
        EndTime = time.time()
        MyDebug(DebugTime, "End Time : " + str(EndTime))
        Duration = EndTime - StartTime
        MyDebug(DebugTime, "Duration : " + str(Duration))
        SlamScorePercent =  0
        SlamScoreMajorsPercent =  0
        SlamScoreMinorsPercent =  0
        SlamScoreNoTrumpsPercent =  0
        GerberPercent = 0
        LimitPercent = 0
        BlackwoodPercent = 0
        ControlPercent = 0
        SustainPercent = 0
        if GerberCount > 0:
            GerberPercent =  float(float(GerberSuccess) / float(GerberCount))
        if BlackwoodCount > 0:
            BlackwoodPercent =  float(float(BlackwoodSuccess) / float(BlackwoodCount))
        if ControlCount > 0:
            ControlPercent =  float(float(ControlSuccess) / float(ControlCount))
        if LimitCount > 0:
            LimitPercent =  float(float(LimitSuccess) / float(LimitCount))
        if SustainCount > 0:
            SustainPercent =  float(float(SustainSuccess) / float(SustainCount))        
        if SlamScoreCount > 0:
            SlamScorePercent =  float(float(SlamScoreSuccess) / float(SlamScoreCount))
        if SlamScoreMajorsCount > 0:
            SlamScoreMajorsPercent =  float(float(SlamScoreMajorsSuccess) / float(SlamScoreMajorsCount))
        if SlamScoreMinorsCount > 0:
            SlamScoreMinorsPercent =  float(float(SlamScoreMinorsSuccess) / float(SlamScoreMinorsCount))
        if SlamScoreNoTrumpsCount > 0:
            SlamScoreNoTrumpsPercent =  float(float(SlamScoreNoTrumpsSuccess) / float(SlamScoreNoTrumpsCount))
        MyDebug(DebugTime, "Total Hands        : " + str(TotalHandsBid + TossInCount))
        MyDebug(DebugTime, "Toss-Ins           : " + str(TossInCount))
        MyDebug(DebugTime, "Total Hands Bid    : " + str(TotalHandsBid))
        MyDebug(DebugTime, "Slams Bid          : " + str(TotalDeals))
        MyDebug(DebugTime, "SlamScore Majors   : " + str(SlamScoreMajorsCount) + " Won : " + str(SlamScoreMajorsSuccess) + " % "+ str(SlamScoreMajorsPercent))
        MyDebug(DebugTime, "SlamScore Minors   : " + str(SlamScoreMinorsCount) + " Won : " + str(SlamScoreMinorsSuccess) + " % "+ str(SlamScoreMinorsPercent))
        MyDebug(DebugTime, "SlamScore NoTrumps : " + str(SlamScoreNoTrumpsCount) + " Won : " + str(SlamScoreNoTrumpsSuccess) + " % "+ str(SlamScoreNoTrumpsPercent))
        MyDebug(DebugTime, "SlamScore Count    : " + str(SlamScoreCount) + " Won : " + str(SlamScoreSuccess) + " % "+ str(SlamScorePercent))
        MyDebug(DebugTime, "Gerber Count       : " + str(GerberCount) + " Won : " + str(GerberSuccess) + " % "+ str(GerberPercent))
        MyDebug(DebugTime, "Blackwood Count       : " + str(BlackwoodCount) + " Won : " + str(BlackwoodSuccess) + " % "+ str(BlackwoodPercent))
        MyDebug(DebugTime, "Control Count       : " + str(ControlCount) + " Won : " + str(ControlSuccess) + " % "+ str(ControlPercent))
        MyDebug(DebugTime, "Limit Count       : " + str(LimitCount) + " Won : " + str(LimitSuccess) + " % "+ str(LimitPercent))
        MyDebug(DebugTime, "Sustain Count       : " + str(SustainCount) + " Won : " + str(SustainSuccess) + " % "+ str(SustainPercent))
 

##        ## MyDebug(DebugDevel, "Total " + str(TotalDeals))        
        EndTime = time.time()
        MyDebug(DebugTime, "End Time : " + str(EndTime))
        Duration = EndTime - StartTime
        MyDebug(DebugTime, "Duration : " + str(Duration))
        return

















    def OnPopulate8(self, event):

        PartScoreCount = 0
        GameScoreCount = 0
        SlamScoreCount = 0
        PartScoreSuccess = 0
        GameScoreSuccess = 0
        SlamScoreSuccess = 0
        TossInCount = 0
        PartScoreMajorsCount = 0
        GameScoreMajorsCount = 0
        SlamScoreMajorsCount = 0
        PartScoreMinorsCount = 0
        GameScoreMinorsCount = 0
        SlamScoreMinorsCount = 0
        PartScoreNoTrumpsCount = 0
        GameScoreNoTrumpsCount = 0
        SlamScoreNoTrumpsCount = 0
        PartScoreMajorsSuccess = 0
        GameScoreMajorsSuccess = 0
        SlamScoreMajorsSuccess = 0
        PartScoreMinorsSuccess = 0
        GameScoreMinorsSuccess = 0
        SlamScoreMinorsSuccess = 0
        PartScoreNoTrumpsSuccess = 0
        GameScoreNoTrumpsSuccess = 0
        SlamScoreNoTrumpsSuccess = 0
        TotalDeals = 0
        StartTime = time.time()
        MyDebug(DebugTime, "Test8 - Start Time : " + str(StartTime))
        Cursor.execute("SELECT * FROM " + self.Context.TableName + " WHERE System=?;", (X1.SystemNeanderthal,))
        Rows = Cursor.fetchall()
        FoundOne = False
        for Row in Rows:
            TotalDeals = TotalDeals + 1
            TheUniquer = Row[0]
            TheDealNum = Row[1]
            TheDeclarer = Row[2]
            TheDealer = Row[3]
            MyPack = Row[13]
##            print "Num " + str(TheDealNum) + " Uniquer " + str(TheUniquer)
            TempPack = string.splitfields(string.strip(string.strip(MyPack, "["), "]"), ",")
            MyNewPack = []
            for Things in TempPack:
                MyNewPack.append(int(Things))
            ThePack = MyNewPack
            MyContext = X1.Context(False)
            MyContext.Reset()
            MyContext.SetDealer(TheDealer)
            MyContext.UpdateSystem(X1.GetTeam(TheDeclarer), X1.SystemSAYC)
            MySession = X1.PracticeSession()
            MySession.System = X1.SystemSAYC
            MyContext, MyNewMsg = BidPracticeHand(ThePack, MyContext)
            if MyContext.TossIn == False:
                MySuccess, MyContext = APD.PlayDeal(MyContext)
                MyTeam = X1.GetTeam(MyContext.Declarer)
                MySession.Tricks = MyContext.Teams[MyTeam].TricksWon
                MyTricksReqd = MyContext.Teams[MyTeam].TricksReqd
                MySession.Variance = MyContext.Teams[MyTeam].TricksWon - MyContext.Teams[MyTeam].TricksReqd       
                MySession.Success = MySuccess
                MySession.Contract = MyContext.Contract
                MySession.Result = APD.GetResult(MyContext)
                MySession.Pack = ThePack
                MySession.Declarer = MyContext.Declarer
                if MyContext.Trumps == X1.SuitSpades:
                    MySession.Suit = X1.PracticeSuitMajors
                if MyContext.Trumps == X1.SuitHearts:
                    MySession.Suit = X1.PracticeSuitMajors
                if MyContext.Trumps == X1.SuitDiamonds:
                    MySession.Suit = X1.PracticeSuitMinors
                if MyContext.Trumps == X1.SuitClubs:
                    MySession.Suit = X1.PracticeSuitMinors
                if MyContext.Trumps == X1.SuitNoTrumps:
                    MySession.Suit = X1.PracticeSuitNoTrumps
                MySession.Level = X1.PracticeLevelSuitBid(MySession.Suit, MyContext.Contract)
                MySession.BidType = X1.GetPracticeBidType(MyContext, X1.GetTeam(MyContext.Declarer))
                MySession.Player = MyContext.User.Seat
                MySession.Uniquer = time.time()
                PickleData = cPickle.dumps(MyPack, cPickle.HIGHEST_PROTOCOL)
                Cursor.execute("INSERT INTO " + self.Context.TableName + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                                (MySession.Uniquer, str(TheDealNum), MySession.Declarer, MySession.Dealer, MySession.Type,
                                 MySession.Level, MySession.Suit, MySession.BidType,
                                 MySession.Contract, str(MySession.Result), MySession.Success,
                                 MySession.Tricks, MySession.Variance, str(MyPack),
                                 sqlite3.Binary(PickleData), str(MySession.System), MyContext.User.UserName,
                                 MyContext.User.Seat, MySession.Uniquer))
                DataBase.commit()
                if MySession.Level == X1.PracticeLevelPartScore:
                    PartScoreCount = PartScoreCount + 1
                    if MySession.Suit == X1.PracticeSuitMajors:
                        PartScoreMajorsCount = PartScoreMajorsCount + 1
                    if MySession.Suit == X1.PracticeSuitMinors:
                        PartScoreMinorsCount = PartScoreMinorsCount + 1
                    if MySession.Suit == X1.PracticeSuitNoTrumps:
                        PartScoreNoTrumpsCount = PartScoreNoTrumpsCount + 1
                    if MySession.Success:
                        PartScoreSuccess = PartScoreSuccess + 1
                        if MySession.Suit == X1.PracticeSuitMajors:
                            PartScoreMajorsSuccess = PartScoreMajorsSuccess + 1
                        if MySession.Suit == X1.PracticeSuitMinors:
                            PartScoreMinorsSuccess = PartScoreMinorsSuccess + 1
                        if MySession.Suit == X1.PracticeSuitNoTrumps:
                            PartScoreNoTrumpsSuccess = PartScoreNoTrumpsSuccess + 1                            
                if MySession.Level == X1.PracticeLevelGame:
                    GameScoreCount = GameScoreCount + 1
                    if MySession.Suit == X1.PracticeSuitMajors:
                        GameScoreMajorsCount = GameScoreMajorsCount + 1
                    if MySession.Suit == X1.PracticeSuitMinors:
                        GameScoreMinorsCount = GameScoreMinorsCount + 1
                    if MySession.Suit == X1.PracticeSuitNoTrumps:
                        GameScoreNoTrumpsCount = GameScoreNoTrumpsCount + 1
                    if MySession.Success:
                        GameScoreSuccess = GameScoreSuccess + 1
                        if MySession.Suit == X1.PracticeSuitMajors:
                            GameScoreMajorsSuccess = GameScoreMajorsSuccess + 1
                        if MySession.Suit == X1.PracticeSuitMinors:
                            GameScoreMinorsSuccess = GameScoreMinorsSuccess + 1
                        if MySession.Suit == X1.PracticeSuitNoTrumps:
                            GameScoreNoTrumpsSuccess = GameScoreNoTrumpsSuccess + 1
                if MySession.Level == X1.PracticeLevelSlam:
                    SlamScoreCount = SlamScoreCount + 1
                    if MySession.Suit == X1.PracticeSuitMajors:
                        SlamScoreMajorsCount = SlamScoreMajorsCount + 1
                    if MySession.Suit == X1.PracticeSuitMinors:
                        SlamScoreMinorsCount = SlamScoreMinorsCount + 1
                    if MySession.Suit == X1.PracticeSuitNoTrumps:
                        SlamScoreNoTrumpsCount = SlamScoreNoTrumpsCount + 1
                    if MySession.Success:
                        SlamScoreSuccess = SlamScoreSuccess + 1                        
                        if MySession.Suit == X1.PracticeSuitMajors:
                            SlamScoreMajorsSuccess = SlamScoreMajorsSuccess + 1
                        if MySession.Suit == X1.PracticeSuitMinors:
                            SlamScoreMinorsSuccess = SlamScoreMinorsSuccess + 1
                        if MySession.Suit == X1.PracticeSuitNoTrumps:
                            SlamScoreNoTrumpsSuccess = SlamScoreNoTrumpsSuccess + 1

        EndTime = time.time()
        MyDebug(DebugTime, "End Time : " + str(EndTime))
        Duration = EndTime - StartTime
        MyDebug(DebugTime, "Duration : " + str(Duration))
        PartScorePercent =  0
        GameScorePercent =  0
        SlamScorePercent =  0
        PartScoreMajorsPercent =  0
        PartScoreMinorsPercent =  0
        PartScoreNoTrumpsPercent = 0
        GameScoreMajorsPercent = 0
        GameScoreMinorsPercent =  0
        GameScoreNoTrumpsPercent =  0
        SlamScoreMajorsPercent =  0
        SlamScoreMinorsPercent =  0
        SlamScoreNoTrumpsPercent =  0
        if PartScoreCount > 0:
            PartScorePercent =  float(float(PartScoreSuccess) / float(PartScoreCount))
        if GameScoreCount > 0:
            GameScorePercent =  float(float(GameScoreSuccess) / float(GameScoreCount))
        if SlamScoreCount > 0:
            SlamScorePercent =  float(float(SlamScoreSuccess) / float(SlamScoreCount))
        if PartScoreMajorsCount > 0:
            PartScoreMajorsPercent =  float(float(PartScoreMajorsSuccess) / float(PartScoreMajorsCount))
        if PartScoreMinorsCount > 0:
            PartScoreMinorsPercent =  float(float(PartScoreMinorsSuccess) / float(PartScoreMinorsCount))
        if PartScoreNoTrumpsCount > 0:
            PartScoreNoTrumpsPercent =  float(float(PartScoreNoTrumpsSuccess) / float(PartScoreNoTrumpsCount))

        if GameScoreMajorsCount > 0:
            GameScoreMajorsPercent =  float(float(GameScoreMajorsSuccess) / float(GameScoreMajorsCount))
        if GameScoreMinorsCount > 0:
            GameScoreMinorsPercent =  float(float(GameScoreMinorsSuccess) / float(GameScoreMinorsCount))
        if GameScoreNoTrumpsCount > 0:
            GameScoreNoTrumpsPercent =  float(float(GameScoreNoTrumpsSuccess) / float(GameScoreNoTrumpsCount))
        if SlamScoreMajorsCount > 0:
            SlamScoreMajorsPercent =  float(float(SlamScoreMajorsSuccess) / float(SlamScoreMajorsCount))
        if SlamScoreMinorsCount > 0:
            SlamScoreMinorsPercent =  float(float(SlamScoreMinorsSuccess) / float(SlamScoreMinorsCount))
        if SlamScoreNoTrumpsCount > 0:
            SlamScoreNoTrumpsPercent =  float(float(SlamScoreNoTrumpsSuccess) / float(SlamScoreNoTrumpsCount))
        MyDebug(DebugTime, "Hands              : " + str(TotalDeals))
        MyDebug(DebugTime, "Toss-Ins           : " + str(TossInCount))
        MyDebug(DebugTime, "PartScore Majors   : " + str(PartScoreMajorsCount) + " Won : " + str(PartScoreMajorsSuccess) + " % "+ str(PartScoreMajorsPercent))
        MyDebug(DebugTime, "PartScore Minors   : " + str(PartScoreMinorsCount) + " Won : " + str(PartScoreMinorsSuccess) + " % "+ str(PartScoreMinorsPercent))
        MyDebug(DebugTime, "PartScore NoTrumps : " + str(PartScoreNoTrumpsCount) + " Won : " + str(PartScoreNoTrumpsSuccess) + " % "+ str(PartScoreNoTrumpsPercent))
        MyDebug(DebugTime, "PartScore Count   : " + str(PartScoreCount) + " Won : " + str(PartScoreSuccess) + " % "+ str(PartScorePercent))
        MyDebug(DebugTime, "GameScore Majors   : " + str(GameScoreMajorsCount) + " Won : " + str(GameScoreMajorsSuccess) + " % "+ str(GameScoreMajorsPercent))
        MyDebug(DebugTime, "GameScore Minors   : " + str(GameScoreMinorsCount) + " Won : " + str(GameScoreMinorsSuccess) + " % "+ str(GameScoreMinorsPercent))
        MyDebug(DebugTime, "GameScore NoTrumps : " + str(GameScoreNoTrumpsCount) + " Won : " + str(GameScoreNoTrumpsSuccess) + " % "+ str(GameScoreNoTrumpsPercent))
        MyDebug(DebugTime, "GameScore Count   : " + str(GameScoreCount) + " Won : " + str(GameScoreSuccess) + " % "+ str(GameScorePercent))
        MyDebug(DebugTime, "SlamScore Majors   : " + str(SlamScoreMajorsCount) + " Won : " + str(SlamScoreMajorsSuccess) + " % "+ str(SlamScoreMajorsPercent))
        MyDebug(DebugTime, "SlamScore Minors   : " + str(SlamScoreMinorsCount) + " Won : " + str(SlamScoreMinorsSuccess) + " % "+ str(SlamScoreMinorsPercent))
        MyDebug(DebugTime, "SlamScore NoTrumps : " + str(SlamScoreNoTrumpsCount) + " Won : " + str(SlamScoreNoTrumpsSuccess) + " % "+ str(SlamScoreNoTrumpsPercent))
        MyDebug(DebugTime, "SlamScore Count   : " + str(SlamScoreCount) + " Won : " + str(SlamScoreSuccess) + " % "+ str(SlamScorePercent))       
        EndTime = time.time()
        MyDebug(DebugTime, "End Time : " + str(EndTime))
        Duration = EndTime - StartTime
        MyDebug(DebugTime, "Duration : " + str(Duration))
        return
    
##    def OnPopulate8(self, event):
##
##        PartScoreCount = 0
##        GameScoreCount = 0
##        SlamScoreCount = 0
##        PartScoreSuccess = 0
##        GameScoreSuccess = 0
##        SlamScoreSuccess = 0
##        TossInCount = 0
##        PartScoreMajorsCount = 0
##        GameScoreMajorsCount = 0
##        SlamScoreMajorsCount = 0
##        PartScoreMinorsCount = 0
##        GameScoreMinorsCount = 0
##        SlamScoreMinorsCount = 0
##        PartScoreNoTrumpsCount = 0
##        GameScoreNoTrumpsCount = 0
##        SlamScoreNoTrumpsCount = 0
##        PartScoreMajorsSuccess = 0
##        GameScoreMajorsSuccess = 0
##        SlamScoreMajorsSuccess = 0
##        PartScoreMinorsSuccess = 0
##        GameScoreMinorsSuccess = 0
##        SlamScoreMinorsSuccess = 0
##        PartScoreNoTrumpsSuccess = 0
##        GameScoreNoTrumpsSuccess = 0
##        SlamScoreNoTrumpsSuccess = 0
##        TotalDeals = 0
##
##
##
##        
##        StartTime = time.time()
##        MyDebug(DebugTime, "Test8 - Start Time : " + str(StartTime))
##        Cursor.execute("SELECT * FROM " + self.Context.TableName + " WHERE System=?;", (X1.SystemNeanderthal,))
##        Rows = Cursor.fetchall()
##        FoundOne = False
##        MyCount = 0
##        for Row in Rows:
##            MyCount = MyCount + 1
##            print str(MyCount) + " Uniquer " + str(Row[0])
##            TheUniquer = Row[0]
##            TheDealNum = Row[1]
##            TheDeclarer = Row[2]
##            TheDealer = Row[3]
##            MyPack = Row[13]
##            TempPack = string.splitfields(string.strip(string.strip(MyPack, "["), "]"), ",")
##            MyNewPack = []
##            for Things in TempPack:
##                MyNewPack.append(int(Things))
##            ThePack = MyNewPack
##            MyContext = X1.Context(False)
##            MyContext.Reset()
##            MyContext.SetDealer(TheDealer)
##            MyContext.UpdateSystem(X1.GetTeam(TheDeclarer), X1.SystemSAYC)
##            MySession = X1.PracticeSession()
##            MySession.System = X1.SystemSAYC
##            MyContext, MyNewMsg = BidPracticeHand(ThePack, MyContext)
##            if MyContext.TossIn == False:
##                MySuccess, MyContext = APD.PlayDeal(MyContext)
##                MyTeam = X1.GetTeam(MyContext.Declarer)
##                MySession.Tricks = MyContext.Teams[MyTeam].TricksWon
##                MyTricksReqd = MyContext.Teams[MyTeam].TricksReqd
##                MySession.Variance = MyContext.Teams[MyTeam].TricksWon - MyContext.Teams[MyTeam].TricksReqd       
##                MySession.Success = MySuccess
##                MySession.Contract = MyContext.Contract
##                MySession.Result = APD.GetResult(MyContext)
##                MySession.Pack = ThePack
##                MySession.Declarer = MyContext.Declarer
##                if MyContext.Trumps == X1.SuitSpades:
##                    MySession.Suit = X1.PracticeSuitMajors
##                if MyContext.Trumps == X1.SuitHearts:
##                    MySession.Suit = X1.PracticeSuitMajors
##                if MyContext.Trumps == X1.SuitDiamonds:
##                    MySession.Suit = X1.PracticeSuitMinors
##                if MyContext.Trumps == X1.SuitClubs:
##                    MySession.Suit = X1.PracticeSuitMinors
##                if MyContext.Trumps == X1.SuitNoTrumps:
##                    MySession.Suit = X1.PracticeSuitNoTrumps
##                MySession.Level = X1.PracticeLevelSuitBid(MySession.Suit, MyContext.Contract)
##                MySession.BidType = X1.GetPracticeBidType(MyContext, X1.GetTeam(MyContext.Declarer))
##                MySession.Player = MyContext.User.Seat
##                MySession.Uniquer = time.time()
##                PickleData = cPickle.dumps(MyPack, cPickle.HIGHEST_PROTOCOL)
##                Cursor.execute("INSERT INTO " + self.Context.TableName + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
##                                (MySession.Uniquer, str(TheDealNum), MySession.Declarer, MySession.Dealer, MySession.Type,
##                                 MySession.Level, MySession.Suit, MySession.BidType,
##                                 MySession.Contract, str(MySession.Result), MySession.Success,
##                                 MySession.Tricks, MySession.Variance, str(MyPack),
##                                 sqlite3.Binary(PickleData), str(MySession.System), MyContext.User.UserName,
##                                 MyContext.User.Seat, MySession.Uniquer))
##                DataBase.commit()
##                if MySession.Level == X1.PracticeLevelPartScore:
##                    PartScoreCount = PartScoreCount + 1
##                    if MySession.Suit == X1.PracticeSuitMajors:
##                        PartScoreMajorsCount = PartScoreMajorsCount + 1
##                    if MySession.Suit == X1.PracticeSuitMinors:
##                        PartScoreMinorsCount = PartScoreMinorsCount + 1
##                    if MySession.Suit == X1.PracticeSuitNoTrumps:
##                        PartScoreNoTrumpsCount = PartScoreNoTrumpsCount + 1
##                    if MySession.Success:
##                        PartScoreSuccess = PartScoreSuccess + 1
##                        if MySession.Suit == X1.PracticeSuitMajors:
##                            PartScoreMajorsSuccess = PartScoreMajorsSuccess + 1
##                        if MySession.Suit == X1.PracticeSuitMinors:
##                            PartScoreMinorsSuccess = PartScoreMinorsSuccess + 1
##                        if MySession.Suit == X1.PracticeSuitNoTrumps:
##                            PartScoreNoTrumpsSuccess = PartScoreNoTrumpsSuccess + 1                            
##                if MySession.Level == X1.PracticeLevelGame:
##                    GameScoreCount = GameScoreCount + 1
##                    if MySession.Suit == X1.PracticeSuitMajors:
##                        GameScoreMajorsCount = GameScoreMajorsCount + 1
##                    if MySession.Suit == X1.PracticeSuitMinors:
##                        GameScoreMinorsCount = GameScoreMinorsCount + 1
##                    if MySession.Suit == X1.PracticeSuitNoTrumps:
##                        GameScoreNoTrumpsCount = GameScoreNoTrumpsCount + 1
##                    if MySession.Success:
##                        GameScoreSuccess = GameScoreSuccess + 1
##                        if MySession.Suit == X1.PracticeSuitMajors:
##                            GameScoreMajorsSuccess = GameScoreMajorsSuccess + 1
##                        if MySession.Suit == X1.PracticeSuitMinors:
##                            GameScoreMinorsSuccess = GameScoreMinorsSuccess + 1
##                        if MySession.Suit == X1.PracticeSuitNoTrumps:
##                            GameScoreNoTrumpsSuccess = GameScoreNoTrumpsSuccess + 1
##                if MySession.Level == X1.PracticeLevelSlam:
##                    SlamScoreCount = SlamScoreCount + 1
##                    if MySession.Suit == X1.PracticeSuitMajors:
##                        SlamScoreMajorsCount = SlamScoreMajorsCount + 1
##                    if MySession.Suit == X1.PracticeSuitMinors:
##                        SlamScoreMinorsCount = SlamScoreMinorsCount + 1
##                    if MySession.Suit == X1.PracticeSuitNoTrumps:
##                        SlamScoreNoTrumpsCount = SlamScoreNoTrumpsCount + 1
##                    if MySession.Success:
##                        SlamScoreSuccess = SlamScoreSuccess + 1                        
##                        if MySession.Suit == X1.PracticeSuitMajors:
##                            SlamScoreMajorsSuccess = SlamScoreMajorsSuccess + 1
##                        if MySession.Suit == X1.PracticeSuitMinors:
##                            SlamScoreMinorsSuccess = SlamScoreMinorsSuccess + 1
##                        if MySession.Suit == X1.PracticeSuitNoTrumps:
##                            SlamScoreNoTrumpsSuccess = SlamScoreNoTrumpsSuccess + 1
##
##        EndTime = time.time()
##        MyDebug(DebugTime, "End Time : " + str(EndTime))
##        Duration = EndTime - StartTime
##        MyDebug(DebugTime, "Duration : " + str(Duration))
##        PartScorePercent =  0
##        GameScorePercent =  0
##        SlamScorePercent =  0
##        PartScoreMajorsPercent =  0
##        PartScoreMinorsPercent =  0
##        PartScoreNoTrumpsPercent = 0
##        GameScoreMajorsPercent = 0
##        GameScoreMinorsPercent =  0
##        GameScoreNoTrumpsPercent =  0
##        SlamScoreMajorsPercent =  0
##        SlamScoreMinorsPercent =  0
##        SlamScoreNoTrumpsPercent =  0
##        if PartScoreCount > 0:
##            PartScorePercent =  float(float(PartScoreSuccess) / float(PartScoreCount))
##        if GameScoreCount > 0:
##            GameScorePercent =  float(float(GameScoreSuccess) / float(GameScoreCount))
##        if SlamScoreCount > 0:
##            SlamScorePercent =  float(float(SlamScoreSuccess) / float(SlamScoreCount))
##        if PartScoreMajorsCount > 0:
##            PartScoreMajorsPercent =  float(float(PartScoreMajorsSuccess) / float(PartScoreMajorsCount))
##        if PartScoreMinorsCount > 0:
##            PartScoreMinorsPercent =  float(float(PartScoreMinorsSuccess) / float(PartScoreMinorsCount))
##        if PartScoreNoTrumpsCount > 0:
##            PartScoreNoTrumpsPercent =  float(float(PartScoreNoTrumpsSuccess) / float(PartScoreNoTrumpsCount))
##
##        if GameScoreMajorsCount > 0:
##            GameScoreMajorsPercent =  float(float(GameScoreMajorsSuccess) / float(GameScoreMajorsCount))
##        if GameScoreMinorsCount > 0:
##            GameScoreMinorsPercent =  float(float(GameScoreMinorsSuccess) / float(GameScoreMinorsCount))
##        if GameScoreNoTrumpsCount > 0:
##            GameScoreNoTrumpsPercent =  float(float(GameScoreNoTrumpsSuccess) / float(GameScoreNoTrumpsCount))
##        if SlamScoreMajorsCount > 0:
##            SlamScoreMajorsPercent =  float(float(SlamScoreMajorsSuccess) / float(SlamScoreMajorsCount))
##        if SlamScoreMinorsCount > 0:
##            SlamScoreMinorsPercent =  float(float(SlamScoreMinorsSuccess) / float(SlamScoreMinorsCount))
##        if SlamScoreNoTrumpsCount > 0:
##            SlamScoreNoTrumpsPercent =  float(float(SlamScoreNoTrumpsSuccess) / float(SlamScoreNoTrumpsCount))
##        MyDebug(DebugTime, "Hands              : " + str(TotalDeals))
##        MyDebug(DebugTime, "Toss-Ins           : " + str(TossInCount))
##        MyDebug(DebugTime, "PartScore Majors   : " + str(PartScoreMajorsCount) + " Won : " + str(PartScoreMajorsSuccess) + " % "+ str(PartScoreMajorsPercent))
##        MyDebug(DebugTime, "PartScore Minors   : " + str(PartScoreMinorsCount) + " Won : " + str(PartScoreMinorsSuccess) + " % "+ str(PartScoreMinorsPercent))
##        MyDebug(DebugTime, "PartScore NoTrumps : " + str(PartScoreNoTrumpsCount) + " Won : " + str(PartScoreNoTrumpsSuccess) + " % "+ str(PartScoreNoTrumpsPercent))
##        MyDebug(DebugTime, "PartScore Count   : " + str(PartScoreCount) + " Won : " + str(PartScoreSuccess) + " % "+ str(PartScorePercent))
##        MyDebug(DebugTime, "GameScore Majors   : " + str(GameScoreMajorsCount) + " Won : " + str(GameScoreMajorsSuccess) + " % "+ str(GameScoreMajorsPercent))
##        MyDebug(DebugTime, "GameScore Minors   : " + str(GameScoreMinorsCount) + " Won : " + str(GameScoreMinorsSuccess) + " % "+ str(GameScoreMinorsPercent))
##        MyDebug(DebugTime, "GameScore NoTrumps : " + str(GameScoreNoTrumpsCount) + " Won : " + str(GameScoreNoTrumpsSuccess) + " % "+ str(GameScoreNoTrumpsPercent))
##        MyDebug(DebugTime, "GameScore Count   : " + str(GameScoreCount) + " Won : " + str(GameScoreSuccess) + " % "+ str(GameScorePercent))
##        MyDebug(DebugTime, "SlamScore Majors   : " + str(SlamScoreMajorsCount) + " Won : " + str(SlamScoreMajorsSuccess) + " % "+ str(SlamScoreMajorsPercent))
##        MyDebug(DebugTime, "SlamScore Minors   : " + str(SlamScoreMinorsCount) + " Won : " + str(SlamScoreMinorsSuccess) + " % "+ str(SlamScoreMinorsPercent))
##        MyDebug(DebugTime, "SlamScore NoTrumps : " + str(SlamScoreNoTrumpsCount) + " Won : " + str(SlamScoreNoTrumpsSuccess) + " % "+ str(SlamScoreNoTrumpsPercent))
##        MyDebug(DebugTime, "SlamScore Count   : " + str(SlamScoreCount) + " Won : " + str(SlamScoreSuccess) + " % "+ str(SlamScorePercent))
####        ## MyDebug(DebugDevel, "Total " + str(TotalDeals))        
##        EndTime = time.time()
##        MyDebug(DebugTime, "End Time : " + str(EndTime))
##        Duration = EndTime - StartTime
##        MyDebug(DebugTime, "Duration : " + str(Duration))
##
##
##
##                
##        return
    

    def OnPopulate3(self, event):
        StartTime = time.time()
        MyDebug(DebugTime, "Start Time : " + str(StartTime))
        PartScoreCount = 0
        GameScoreCount = 0
        SlamScoreCount = 0
        PartScoreSuccess = 0
        GameScoreSuccess = 0
        SlamScoreSuccess = 0
        TossInCount = 0
        PartScoreMajorsCount = 0
        GameScoreMajorsCount = 0
        SlamScoreMajorsCount = 0
        PartScoreMinorsCount = 0
        GameScoreMinorsCount = 0
        SlamScoreMinorsCount = 0
        PartScoreNoTrumpsCount = 0
        GameScoreNoTrumpsCount = 0
        SlamScoreNoTrumpsCount = 0
        PartScoreMajorsSuccess = 0
        GameScoreMajorsSuccess = 0
        SlamScoreMajorsSuccess = 0
        PartScoreMinorsSuccess = 0
        GameScoreMinorsSuccess = 0
        SlamScoreMinorsSuccess = 0
        PartScoreNoTrumpsSuccess = 0
        GameScoreNoTrumpsSuccess = 0
        SlamScoreNoTrumpsSuccess = 0
        TotalDeals = 0
        MaxIter = 1200
        MyContext = self.Context       
        for Test1 in range(MaxIter):
            if TotalDeals < 1000:
                MyContext, MySession, MyMsg = LoadRandomSession()
                MyContext.User = SetDefaultUser()
                if MyContext.TossIn == True:
                    TossInCount = TossInCount + 1
                if MyContext.TossIn == False:


                    
                    MySession.Num = TotalDeals

                    MySession.OpenFile()
                    MyStr = "## Hello, Sailor!" + "\n\n"
                    MySession.WriteFile(MyStr)


                    
                    MyDebug(DebugTime, "Deal : " + str(TotalDeals))
                    TotalDeals = TotalDeals + 1
                    if MySession.Level == X1.PracticeLevelPartScore:
                        PartScoreCount = PartScoreCount + 1
                        if MySession.Suit == X1.PracticeSuitMajors:
                            PartScoreMajorsCount = PartScoreMajorsCount + 1
                        if MySession.Suit == X1.PracticeSuitMinors:
                            PartScoreMinorsCount = PartScoreMinorsCount + 1
                        if MySession.Suit == X1.PracticeSuitNoTrumps:
                            PartScoreNoTrumpsCount = PartScoreNoTrumpsCount + 1
                        if MySession.Success:
                            PartScoreSuccess = PartScoreSuccess + 1
                            if MySession.Suit == X1.PracticeSuitMajors:
                                PartScoreMajorsSuccess = PartScoreMajorsSuccess + 1
                            if MySession.Suit == X1.PracticeSuitMinors:
                                PartScoreMinorsSuccess = PartScoreMinorsSuccess + 1
                            if MySession.Suit == X1.PracticeSuitNoTrumps:
                                PartScoreNoTrumpsSuccess = PartScoreNoTrumpsSuccess + 1                            
                    if MySession.Level == X1.PracticeLevelGame:
                        GameScoreCount = GameScoreCount + 1
                        if MySession.Suit == X1.PracticeSuitMajors:
                            GameScoreMajorsCount = GameScoreMajorsCount + 1
                        if MySession.Suit == X1.PracticeSuitMinors:
                            GameScoreMinorsCount = GameScoreMinorsCount + 1
                        if MySession.Suit == X1.PracticeSuitNoTrumps:
                            GameScoreNoTrumpsCount = GameScoreNoTrumpsCount + 1
                        if MySession.Success:
                            GameScoreSuccess = GameScoreSuccess + 1
                            if MySession.Suit == X1.PracticeSuitMajors:
                                GameScoreMajorsSuccess = GameScoreMajorsSuccess + 1
                            if MySession.Suit == X1.PracticeSuitMinors:
                                GameScoreMinorsSuccess = GameScoreMinorsSuccess + 1
                            if MySession.Suit == X1.PracticeSuitNoTrumps:
                                GameScoreNoTrumpsSuccess = GameScoreNoTrumpsSuccess + 1
                    if MySession.Level == X1.PracticeLevelSlam:
                        SlamScoreCount = SlamScoreCount + 1
                        if MySession.Suit == X1.PracticeSuitMajors:
                            SlamScoreMajorsCount = SlamScoreMajorsCount + 1
                        if MySession.Suit == X1.PracticeSuitMinors:
                            SlamScoreMinorsCount = SlamScoreMinorsCount + 1
                        if MySession.Suit == X1.PracticeSuitNoTrumps:
                            SlamScoreNoTrumpsCount = SlamScoreNoTrumpsCount + 1
                        if MySession.Success:
                            SlamScoreSuccess = SlamScoreSuccess + 1                        
                            if MySession.Suit == X1.PracticeSuitMajors:
                                SlamScoreMajorsSuccess = SlamScoreMajorsSuccess + 1
                            if MySession.Suit == X1.PracticeSuitMinors:
                                SlamScoreMinorsSuccess = SlamScoreMinorsSuccess + 1
                            if MySession.Suit == X1.PracticeSuitNoTrumps:
                                SlamScoreNoTrumpsSuccess = SlamScoreNoTrumpsSuccess + 1
                    MySession.Uniquer = time.time()
                    PickleData = cPickle.dumps(MySession.Pack, cPickle.HIGHEST_PROTOCOL)
                    Cursor.execute("INSERT INTO " + MyContext.TableName + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                                    (MySession.Uniquer, str(Test1), MySession.Declarer, MySession.Dealer, MySession.Type,
                                     MySession.Level, MySession.Suit, MySession.BidType, 
                                     MySession.Contract, str(MySession.Result), MySession.Success, MySession.Tricks,
                                     MySession.Variance, str(MySession.Pack), sqlite3.Binary(PickleData),
                                     str(MySession.System), MyContext.User.UserName, MyContext.User.Seat, MySession.Uniquer))
                    DataBase.commit()
                    MyLine = P2.PrintDealtCards(MySession.Num, MyContext)
                    MySession.WriteFile(MyLine)
                    MyLine = P2.PrintBids(MyContext)
                    MySession.WriteFile(MyLine)            
                    MyLine = P2.PrintPlayedCards(MyContext)
                    MySession.WriteFile(MyLine)               
                    MySession.CloseFile()
        EndTime = time.time()
        MyDebug(DebugTime, "End Time : " + str(EndTime))
        Duration = EndTime - StartTime
        MyDebug(DebugTime, "Duration : " + str(Duration))
        PartScorePercent =  0
        GameScorePercent =  0
        SlamScorePercent =  0
        PartScoreMajorsPercent =  0
        PartScoreMinorsPercent =  0
        PartScoreNoTrumpsPercent = 0
        GameScoreMajorsPercent = 0
        GameScoreMinorsPercent =  0
        GameScoreNoTrumpsPercent =  0
        SlamScoreMajorsPercent =  0
        SlamScoreMinorsPercent =  0
        SlamScoreNoTrumpsPercent =  0
        if PartScoreCount > 0:
            PartScorePercent =  float(float(PartScoreSuccess) / float(PartScoreCount))
        if GameScoreCount > 0:
            GameScorePercent =  float(float(GameScoreSuccess) / float(GameScoreCount))
        if SlamScoreCount > 0:
            SlamScorePercent =  float(float(SlamScoreSuccess) / float(SlamScoreCount))
        if PartScoreMajorsCount > 0:
            PartScoreMajorsPercent =  float(float(PartScoreMajorsSuccess) / float(PartScoreMajorsCount))
        if PartScoreMinorsCount > 0:
            PartScoreMinorsPercent =  float(float(PartScoreMinorsSuccess) / float(PartScoreMinorsCount))
        if PartScoreNoTrumpsCount > 0:
            PartScoreNoTrumpsPercent =  float(float(PartScoreNoTrumpsSuccess) / float(PartScoreNoTrumpsCount))

        if GameScoreMajorsCount > 0:
            GameScoreMajorsPercent =  float(float(GameScoreMajorsSuccess) / float(GameScoreMajorsCount))
        if GameScoreMinorsCount > 0:
            GameScoreMinorsPercent =  float(float(GameScoreMinorsSuccess) / float(GameScoreMinorsCount))
        if GameScoreNoTrumpsCount > 0:
            GameScoreNoTrumpsPercent =  float(float(GameScoreNoTrumpsSuccess) / float(GameScoreNoTrumpsCount))
        if SlamScoreMajorsCount > 0:
            SlamScoreMajorsPercent =  float(float(SlamScoreMajorsSuccess) / float(SlamScoreMajorsCount))
        if SlamScoreMinorsCount > 0:
            SlamScoreMinorsPercent =  float(float(SlamScoreMinorsSuccess) / float(SlamScoreMinorsCount))
        if SlamScoreNoTrumpsCount > 0:
            SlamScoreNoTrumpsPercent =  float(float(SlamScoreNoTrumpsSuccess) / float(SlamScoreNoTrumpsCount))
        MyDebug(DebugTime, "Hands              : " + str(TotalDeals))
        MyDebug(DebugTime, "Toss-Ins           : " + str(TossInCount))
        MyDebug(DebugTime, "PartScore Majors   : " + str(PartScoreMajorsCount) + " Won : " + str(PartScoreMajorsSuccess) + " % "+ str(PartScoreMajorsPercent))
        MyDebug(DebugTime, "PartScore Minors   : " + str(PartScoreMinorsCount) + " Won : " + str(PartScoreMinorsSuccess) + " % "+ str(PartScoreMinorsPercent))
        MyDebug(DebugTime, "PartScore NoTrumps : " + str(PartScoreNoTrumpsCount) + " Won : " + str(PartScoreNoTrumpsSuccess) + " % "+ str(PartScoreNoTrumpsPercent))
        MyDebug(DebugTime, "PartScore Count   : " + str(PartScoreCount) + " Won : " + str(PartScoreSuccess) + " % "+ str(PartScorePercent))
        MyDebug(DebugTime, "GameScore Majors   : " + str(GameScoreMajorsCount) + " Won : " + str(GameScoreMajorsSuccess) + " % "+ str(GameScoreMajorsPercent))
        MyDebug(DebugTime, "GameScore Minors   : " + str(GameScoreMinorsCount) + " Won : " + str(GameScoreMinorsSuccess) + " % "+ str(GameScoreMinorsPercent))
        MyDebug(DebugTime, "GameScore NoTrumps : " + str(GameScoreNoTrumpsCount) + " Won : " + str(GameScoreNoTrumpsSuccess) + " % "+ str(GameScoreNoTrumpsPercent))
        MyDebug(DebugTime, "GameScore Count   : " + str(GameScoreCount) + " Won : " + str(GameScoreSuccess) + " % "+ str(GameScorePercent))
        MyDebug(DebugTime, "SlamScore Majors   : " + str(SlamScoreMajorsCount) + " Won : " + str(SlamScoreMajorsSuccess) + " % "+ str(SlamScoreMajorsPercent))
        MyDebug(DebugTime, "SlamScore Minors   : " + str(SlamScoreMinorsCount) + " Won : " + str(SlamScoreMinorsSuccess) + " % "+ str(SlamScoreMinorsPercent))
        MyDebug(DebugTime, "SlamScore NoTrumps : " + str(SlamScoreNoTrumpsCount) + " Won : " + str(SlamScoreNoTrumpsSuccess) + " % "+ str(SlamScoreNoTrumpsPercent))
        MyDebug(DebugTime, "SlamScore Count   : " + str(SlamScoreCount) + " Won : " + str(SlamScoreSuccess) + " % "+ str(SlamScorePercent))
##        ## MyDebug(DebugDevel, "Total " + str(TotalDeals))        
        EndTime = time.time()
        MyDebug(DebugTime, "End Time : " + str(EndTime))
        Duration = EndTime - StartTime
        MyDebug(DebugTime, "Duration : " + str(Duration))
        return



    def OnPopulate1(self, event):
        StartTime = time.time()
        MyDebug(DebugTime, "Start Time : " + str(StartTime))
        PartScoreCount = 0
        GameScoreCount = 0
        SlamScoreCount = 0
        PartScoreSuccess = 0
        GameScoreSuccess = 0
        SlamScoreSuccess = 0
        TossInCount = 0
        PartScoreMajorsCount = 0
        GameScoreMajorsCount = 0
        SlamScoreMajorsCount = 0
        PartScoreMinorsCount = 0
        GameScoreMinorsCount = 0
        SlamScoreMinorsCount = 0
        PartScoreNoTrumpsCount = 0
        GameScoreNoTrumpsCount = 0
        SlamScoreNoTrumpsCount = 0
        PartScoreMajorsSuccess = 0
        GameScoreMajorsSuccess = 0
        SlamScoreMajorsSuccess = 0
        PartScoreMinorsSuccess = 0
        GameScoreMinorsSuccess = 0
        SlamScoreMinorsSuccess = 0
        PartScoreNoTrumpsSuccess = 0
        GameScoreNoTrumpsSuccess = 0
        SlamScoreNoTrumpsSuccess = 0
        TotalDeals = 0
        MaxIter = 1200
        MyContext = self.Context       
        for Test1 in range(MaxIter):
            if TotalDeals < 1000:
                MyContext, MySession, MyMsg = LoadRandomSession()
                
                MyContext.User = SetDefaultUser()
                if MyContext.TossIn == True:
                    TossInCount = TossInCount + 1
                if MyContext.TossIn == False:
                    MySession.Num = TotalDeals
                    MyDebug(DebugTime, "Deal : " + str(TotalDeals))
                    TotalDeals = TotalDeals + 1
                    if MySession.Level == X1.PracticeLevelPartScore:
                        PartScoreCount = PartScoreCount + 1
                        if MySession.Suit == X1.PracticeSuitMajors:
                            PartScoreMajorsCount = PartScoreMajorsCount + 1
                        if MySession.Suit == X1.PracticeSuitMinors:
                            PartScoreMinorsCount = PartScoreMinorsCount + 1
                        if MySession.Suit == X1.PracticeSuitNoTrumps:
                            PartScoreNoTrumpsCount = PartScoreNoTrumpsCount + 1
                        if MySession.Success:
                            PartScoreSuccess = PartScoreSuccess + 1
                            if MySession.Suit == X1.PracticeSuitMajors:
                                PartScoreMajorsSuccess = PartScoreMajorsSuccess + 1
                            if MySession.Suit == X1.PracticeSuitMinors:
                                PartScoreMinorsSuccess = PartScoreMinorsSuccess + 1
                            if MySession.Suit == X1.PracticeSuitNoTrumps:
                                PartScoreNoTrumpsSuccess = PartScoreNoTrumpsSuccess + 1                            
                    if MySession.Level == X1.PracticeLevelGame:
                        GameScoreCount = GameScoreCount + 1
                        if MySession.Suit == X1.PracticeSuitMajors:
                            GameScoreMajorsCount = GameScoreMajorsCount + 1
                        if MySession.Suit == X1.PracticeSuitMinors:
                            GameScoreMinorsCount = GameScoreMinorsCount + 1
                        if MySession.Suit == X1.PracticeSuitNoTrumps:
                            GameScoreNoTrumpsCount = GameScoreNoTrumpsCount + 1
                        if MySession.Success:
                            GameScoreSuccess = GameScoreSuccess + 1
                            if MySession.Suit == X1.PracticeSuitMajors:
                                GameScoreMajorsSuccess = GameScoreMajorsSuccess + 1
                            if MySession.Suit == X1.PracticeSuitMinors:
                                GameScoreMinorsSuccess = GameScoreMinorsSuccess + 1
                            if MySession.Suit == X1.PracticeSuitNoTrumps:
                                GameScoreNoTrumpsSuccess = GameScoreNoTrumpsSuccess + 1
                    if MySession.Level == X1.PracticeLevelSlam:
                        SlamScoreCount = SlamScoreCount + 1
                        if MySession.Suit == X1.PracticeSuitMajors:
                            SlamScoreMajorsCount = SlamScoreMajorsCount + 1
                        if MySession.Suit == X1.PracticeSuitMinors:
                            SlamScoreMinorsCount = SlamScoreMinorsCount + 1
                        if MySession.Suit == X1.PracticeSuitNoTrumps:
                            SlamScoreNoTrumpsCount = SlamScoreNoTrumpsCount + 1
                        if MySession.Success:
                            SlamScoreSuccess = SlamScoreSuccess + 1                        
                            if MySession.Suit == X1.PracticeSuitMajors:
                                SlamScoreMajorsSuccess = SlamScoreMajorsSuccess + 1
                            if MySession.Suit == X1.PracticeSuitMinors:
                                SlamScoreMinorsSuccess = SlamScoreMinorsSuccess + 1
                            if MySession.Suit == X1.PracticeSuitNoTrumps:
                                SlamScoreNoTrumpsSuccess = SlamScoreNoTrumpsSuccess + 1
        EndTime = time.time()
        MyDebug(DebugTime, "End Time : " + str(EndTime))
        Duration = EndTime - StartTime
        MyDebug(DebugTime, "Duration : " + str(Duration))
        PartScorePercent =  0
        GameScorePercent =  0
        SlamScorePercent =  0
        PartScoreMajorsPercent =  0
        PartScoreMinorsPercent =  0
        PartScoreNoTrumpsPercent = 0
        GameScoreMajorsPercent = 0
        GameScoreMinorsPercent =  0
        GameScoreNoTrumpsPercent =  0
        SlamScoreMajorsPercent =  0
        SlamScoreMinorsPercent =  0
        SlamScoreNoTrumpsPercent =  0
        if PartScoreCount > 0:
            PartScorePercent =  float(float(PartScoreSuccess) / float(PartScoreCount))
        if GameScoreCount > 0:
            GameScorePercent =  float(float(GameScoreSuccess) / float(GameScoreCount))
        if SlamScoreCount > 0:
            SlamScorePercent =  float(float(SlamScoreSuccess) / float(SlamScoreCount))
        if PartScoreMajorsCount > 0:
            PartScoreMajorsPercent =  float(float(PartScoreMajorsSuccess) / float(PartScoreMajorsCount))
        if PartScoreMinorsCount > 0:
            PartScoreMinorsPercent =  float(float(PartScoreMinorsSuccess) / float(PartScoreMinorsCount))
        if PartScoreNoTrumpsCount > 0:
            PartScoreNoTrumpsPercent =  float(float(PartScoreNoTrumpsSuccess) / float(PartScoreNoTrumpsCount))

        if GameScoreMajorsCount > 0:
            GameScoreMajorsPercent =  float(float(GameScoreMajorsSuccess) / float(GameScoreMajorsCount))
        if GameScoreMinorsCount > 0:
            GameScoreMinorsPercent =  float(float(GameScoreMinorsSuccess) / float(GameScoreMinorsCount))
        if GameScoreNoTrumpsCount > 0:
            GameScoreNoTrumpsPercent =  float(float(GameScoreNoTrumpsSuccess) / float(GameScoreNoTrumpsCount))
        if SlamScoreMajorsCount > 0:
            SlamScoreMajorsPercent =  float(float(SlamScoreMajorsSuccess) / float(SlamScoreMajorsCount))
        if SlamScoreMinorsCount > 0:
            SlamScoreMinorsPercent =  float(float(SlamScoreMinorsSuccess) / float(SlamScoreMinorsCount))
        if SlamScoreNoTrumpsCount > 0:
            SlamScoreNoTrumpsPercent =  float(float(SlamScoreNoTrumpsSuccess) / float(SlamScoreNoTrumpsCount))
        MyDebug(DebugTime, "Hands              : " + str(TotalDeals))
        MyDebug(DebugTime, "Toss-Ins           : " + str(TossInCount))
        MyDebug(DebugTime, "PartScore Majors   : " + str(PartScoreMajorsCount) + " Won : " + str(PartScoreMajorsSuccess) + " % "+ str(PartScoreMajorsPercent))
        MyDebug(DebugTime, "PartScore Minors   : " + str(PartScoreMinorsCount) + " Won : " + str(PartScoreMinorsSuccess) + " % "+ str(PartScoreMinorsPercent))
        MyDebug(DebugTime, "PartScore NoTrumps : " + str(PartScoreNoTrumpsCount) + " Won : " + str(PartScoreNoTrumpsSuccess) + " % "+ str(PartScoreNoTrumpsPercent))
        MyDebug(DebugTime, "PartScore Count   : " + str(PartScoreCount) + " Won : " + str(PartScoreSuccess) + " % "+ str(PartScorePercent))
        MyDebug(DebugTime, "GameScore Majors   : " + str(GameScoreMajorsCount) + " Won : " + str(GameScoreMajorsSuccess) + " % "+ str(GameScoreMajorsPercent))
        MyDebug(DebugTime, "GameScore Minors   : " + str(GameScoreMinorsCount) + " Won : " + str(GameScoreMinorsSuccess) + " % "+ str(GameScoreMinorsPercent))
        MyDebug(DebugTime, "GameScore NoTrumps : " + str(GameScoreNoTrumpsCount) + " Won : " + str(GameScoreNoTrumpsSuccess) + " % "+ str(GameScoreNoTrumpsPercent))
        MyDebug(DebugTime, "GameScore Count   : " + str(GameScoreCount) + " Won : " + str(GameScoreSuccess) + " % "+ str(GameScorePercent))
        MyDebug(DebugTime, "SlamScore Majors   : " + str(SlamScoreMajorsCount) + " Won : " + str(SlamScoreMajorsSuccess) + " % "+ str(SlamScoreMajorsPercent))
        MyDebug(DebugTime, "SlamScore Minors   : " + str(SlamScoreMinorsCount) + " Won : " + str(SlamScoreMinorsSuccess) + " % "+ str(SlamScoreMinorsPercent))
        MyDebug(DebugTime, "SlamScore NoTrumps : " + str(SlamScoreNoTrumpsCount) + " Won : " + str(SlamScoreNoTrumpsSuccess) + " % "+ str(SlamScoreNoTrumpsPercent))
        MyDebug(DebugTime, "SlamScore Count   : " + str(SlamScoreCount) + " Won : " + str(SlamScoreSuccess) + " % "+ str(SlamScorePercent))
##        ## MyDebug(DebugDevel, "Total " + str(TotalDeals))        
        EndTime = time.time()
        MyDebug(DebugTime, "End Time : " + str(EndTime))
        Duration = EndTime - StartTime
        MyDebug(DebugTime, "Duration : " + str(Duration))
        return

    
    def OnContinuePanel(self, Msg):
        MyDebug(DebugResolved, "Frame OnContinue")
        self.ContinuePanel.Hide()
        self.BiddingBox.Show(False)
        MyDebug(DebugResolved, "Frame PTCInit")
        MyDebug(DebugResolved, Msg)
        MyDebug(DebugResolved, "CP " + X1.PlayerStr(self.Context.CurrentPlayer))
        self.MyChild.PTCInit(Msg, 0, False)        
        return
    
    def PTCInit(self, Msg):
        self.ContinuePanel = MyContinuePanel(self, -1, self.Context, Msg)
        return
    
class MyApp(wx.App):
    def OnInit(self):
        MyFrame = MyMainFrame(None, -1, X1.XXBridgeThing)
        MyFrame.Show(True)
        self.SetTopWindow(MyFrame)
        return True

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

## that's all, folks!

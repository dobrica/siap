class FutsalCup():
    __title = ''
    __year = 0
    __host = ''
    __numberOfTeams = 0
    __playedMatchesCount = 0
    __numberOfGroups = 0 
    __date = []
    __time = []
    __home = []
    __score = []
    __away = []

    def setTitle(self, title):
        self.__title = title
    
    def getTitle(self):
        return self.__title

    def getYear(self):
        year_start = self.__title[0:4]
        year_end = self.__title[(len(self.__title)-4):len(self.__title)]
        if year_start.isdigit():
            self.__year = int(year_start)
        elif year_end.isdigit():
            self.__year = int(year_end)   
        return self.__year # default is 0

    def setHost(self, host):
        if len(host) != 0:
            self.__host = host[0]
        
    def getHost(self):
        return self.__host

    def setNumberOfTeams(self, numberOfTeams):
        if len(numberOfTeams) != 0:
            self.__numberOfTeams = int(numberOfTeams[0].split('(')[0])
        
    def getNumberOfTeams(self):
        return self.__numberOfTeams

    def setPlayedMatchesCount(self, playedMatchesCount):
        if len(playedMatchesCount) != 0:
            self.__playedMatchesCount = playedMatchesCount[0]

    def getPlayedMatchesCount(self):
        return self.__playedMatchesCount

    def setDate(self, date):
        self.__date = date

    def getDate(self):
        return self.__date

    def setTime(self, time):
        self.__time = time

    def getTime(self):
        return self.__time

    def setHome(self, home):
        self.__home = home

    def getHome(self):
        return self.__home

    def setScore(self, score):
        self.__score = score

    def getScore(self):
        return self.__score

    def setAway(self, away):
        self.__away = away

    def getAway(self):
        return self.__away

    def setNumberOfGroups(self, numberOfGroups):
        self.__numberOfGroups = numberOfGroups

    def getNumberOfGroups(self):
        return self.__numberOfGroups
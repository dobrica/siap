import scrapy
import os
import elements as E
from futsalcup import FutsalCup

basepath = 'results/'
fileformat = '.csv'
prefix = 'uefa'
games_df = basepath + prefix + '_games' + fileformat
ranking_df = basepath + prefix + '_ranking' + fileformat
groups_df = basepath + prefix + '_groups' + fileformat


class FCSpider(scrapy.Spider):
    name = 'fcspider'
    # start_urls = [E.uefa_2022_qualifications_url, E.fifa_futsal_wc_url, E.uefa_futsal_url, E.afc_futsal_url,
    #               E.fifa_2020_qualifications_url, E.fifa_2016_qualifications_url, E.fifa_2012_qualifications_url, E.fifa_2008_qualifications_url,
    #               E.concacaf_futsal_url, E.copa_america_futsal_url, E.ofc_futsal_url]  # TODO: fix:, E.africa_futsal_url] #before 2016 different results parsing
    
    start_urls = [E.uefa_futsal_url]

    allFCs = []

    # delete previous files
    if os.path.exists(games_df):
        os.remove(games_df)
    if os.path.exists(ranking_df):
        os.remove(ranking_df)
    if os.path.exists(groups_df):
        os.remove(groups_df)

    def parse(self, response):
        # parse current page for data
        tables = parse_tables(response)
        fc = parse_footballbox(response, tables)
        fc.setFCFinalRanking(get_fc_rankings(tables))
        fc.setGroupResults(get_group_results(tables))

        # add parsed fc data to list
        self.allFCs.append(fc)

        # provides pages that will be scraped
        for next_page in response.xpath(E.next_page_link):
            if 'Futsal' in next_page.extract():
                yield response.follow(next_page, self.parse)

    def closed(self, reason):
        # sort fc data by year
        self.allFCs.sort(key=lambda x: x.getYear(), reverse=False)
        # write to csv file
        for fc in self.allFCs:
            write_fc_to_csv(fc)


def parse_footballbox(response, tables):
    fhome = []
    fscore = []
    faway = []

    fc = FutsalCup()
    fc.setTitle(response.css(E.page_title_s_css).extract()[0])
    fc.setHost(response.xpath(E.host_country).extract())
    summary_table = get_summary_table(tables)
    if len(summary_table) >= 1:
        fc.setNumberOfTeams(summary_table[0][1])
    fc.setPlayedMatchesCount(response.xpath(E.played_matches).extract())

    # missing info for 1996, 2000, 2004, 2008
    fdate = response.xpath(E.date).extract()
    ftime = response.xpath(E.time).extract()

    # *_extras important for 2000, 2004, 2008, but for 2012 and 2016 picks up additional incorrect info
    if fc.getYear() != 2005 and fc.getYear() != 2010 and fc.getYear() != 2014 and fc.getYear() != 2012 and fc.getYear() != 2016 and fc.getYear() != 2018:
        fhome = response.xpath(E.home_extras).extract()
        faway = response.xpath(E.away_extras).extract()
    # deafult football box elements
    fhome += response.xpath(E.home_fb).extract()
    faway += response.xpath(E.away_fb).extract()

    fscore = parse_match_results(fc, fscore, response)

    if (len(fhome) == 0 or len(fscore) == 0 or len(faway) == 0):
        vevents = response.xpath(E.vevent)
        fdate = vevents.xpath(E.vev_date).extract()
        fhome = vevents.xpath(E.vev_home).extract()
        fscore = vevents.xpath(E.vev_score).extract()
        faway = vevents.xpath(E.vev_away).extract()

    # date (or anything that will be written to csv) can't have comma or it will be split it in columns
    for x in range(len(fhome)):
        if x < len(fdate):
            fdate[x] = fdate[x].replace(E.comma, '')
        # if time/date is missing add empty string to corresponding list
        if x >= len(ftime):
            ftime.append(E.empty_str)
        if x >= len(fdate):
            fdate.append(E.empty_str)

    fc.setDate(fdate)
    fc.setTime(ftime)
    fc.setHome(fhome)
    fc.setScore(fscore)
    fc.setAway(faway)

    return fc

def parse_match_results(fc, fscore, response):
    if fc.getYear() != 2012 and fc.getYear() != 2016:
        fscore = response.xpath(E.score_extras)

    # football boxes parse match results, regular time (includes extra time) and penalties
    f_boxes = response.xpath(E.football_box)
    for x in range(len(f_boxes)):
        if E.pen_time in f_boxes[x].extract():
            fscore += f_boxes[x].xpath(E.score_pen)
        else:
            fscore += f_boxes[x].xpath(E.score_reg)

    temp = fscore
    fscore = []
    # get correct result and remove unwanted characters [parentheses, space, unicode-space] from scores array
    for x in range(len(temp)):
        if temp[x].extract().strip() != '(' and temp[x].extract().strip() != ')':
            fscore.append(temp[x].extract().split(E.new_line)[0].strip()
                          .replace('Cancelled', E.empty_str)
                          .replace('Awarded', E.empty_str)
                          .replace('aet', E.empty_str)
                          .replace('walkover', E.empty_str)
                          .replace(u'\xa0', E.empty_str)
                          .replace('(', E.empty_str)
                          .replace(')', E.empty_str)
                          .replace(' ', E.empty_str))

    for sc in fscore:
        if sc == E.empty_str:
            fscore.remove(sc)

    return fscore

def get_group_results(tables):
    result = []
    for tbl in tables:
        if len(tbl) >= 1:
            if tbl[0][0] == E.TEAM and (tbl[0][-1] == E.DIFF or tbl[0][-1] == E.PTS or tbl[0][1] == E.PTS):
                result.append(tbl)
            elif tbl[0][0] == E.POS and tbl[0][1] == E.TEAM and tbl[0][2] == E.PLD:
                result.append(tbl)
    return result

def get_fc_rankings(tables):
    res = []
    for tbl in tables:
        if len(tbl) >= 1 and len(tbl[0]) >= 1:
            if (E.POS in tbl[0][0] or tbl[0][0] == E.RANK or tbl[0][0] == E.PLACE) and tbl[0][1] == E.TEAM:  # check headers
                for x in range(len(tbl)):
                    if x <= len(tbl) - 1:  # this check is req. because elements are beeing removed
                        if x <= 3 and len(tbl[x]) <= 1:
                            tbl[x].append(tbl[x][0]) # move to next column 
                            tbl[x][0] = str(x) # if missing add place number in table
                        elif x > 3 and len(tbl[x]) <= 1:
                            tbl.remove(tbl[x])  # remove desciptive rows
                res.append(tbl) 
    summary_table = get_summary_table(tables)
    if len(res) < 1:
        return summary_table[1:]
    return res[-1] # last table with these headers is most likely ranking table           

def get_all_time_table():
    # TODO: implement
    print("implement")

def get_global_rankings():
    # TODO: implement
    print("implement")

def get_summary_table(tables):
    result = []
    summary_tbl = tables[0] # TODO: improve, maybe it is not always first
    for x in range(len(summary_tbl)):
        for y in range(len(summary_tbl[x])):
            if summary_tbl[x][y] == 'Teams':
                result.append(['Teams', summary_tbl[x][y+1]])
            elif summary_tbl[x][y] == 'Champions':
                result.append(['1', summary_tbl[x][y+1]])
            elif summary_tbl[x][y] == 'Runners-up':
                result.append(['2', summary_tbl[x][y+1]])
            elif summary_tbl[x][y] == 'Third place':
                result.append(['3', summary_tbl[x][y+1]])
            elif summary_tbl[x][y] == 'Fourth place':
                result.append(['4', summary_tbl[x][y+1]])   
    return result     

def parse_tables(response):
    tables = []
    for tbl in response.xpath(E.table_nodes):
        table = []
        for tr in tbl.xpath(E.table_rows):
            row = []
            for cell in tr.xpath(E.subnode_text):
                tcell = cell.extract().strip().replace('\xa0', E.empty_str)
                if tcell != '' and tcell != ' ' and tcell != '\n' and tcell != '\xa0':
                    row.append(tcell)
            if row != []:
                table.append(row)

        if len(table) > 1:  # ignore tables that have only one row
            tables.append(table)
    return tables

# write parsed fc data by appending
def write_fc_to_csv(fc):
    print('writing data to csv files...')
    print(fc.getTitle())

    if 1980 <= fc.getYear() <= 2022:

        with open(games_df, mode='a', encoding='utf-8') as f:
            f.write(fc.getTitle() + E.comma + str(fc.getYear()) +
                    E.comma + fc.getHost() + E.new_line)
            for x in range(len(fc.getHome())):
                outputStr = (fc.getDate()[x] + E.comma + fc.getTime()[x] + E.comma + fc.getHome()[x] +
                             E.comma + fc.getScore()[x] + E.comma + fc.getAway()[x])
                f.write(outputStr + E.new_line)

        with open(ranking_df, mode='a', encoding='utf-8') as f:
            f.write(fc.getTitle() + E.new_line)
            fc_ranks = fc.getFCFinalRanking()
            if fc_ranks != None:
                for x in range(len(fc_ranks)):
                    row = ''
                    for y in range(len(fc_ranks[x])):
                        row += fc_ranks[x][y] + E.comma
                    f.write(row + E.new_line)

        with open(groups_df, mode = 'a', encoding='utf-8') as f:
            f.write(fc.getTitle() + E.new_line)
            group_results = fc.getGroupResults()
            if group_results != None:
                for groupResult in group_results:
                    for x in range(len(groupResult)):
                        row = ''
                        for y in range(len(groupResult[x])):
                            row += groupResult[x][y] + E.comma
                        f.write(row + E.new_line)

    print('DONE')
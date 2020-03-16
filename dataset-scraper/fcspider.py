import scrapy
import os
import elements as E
from futsalcup import FutsalCup

basepath = 'results/'
filename = basepath + 'wiki_data.csv'

class FCSpider(scrapy.Spider):
    name = 'fcspider'
    start_urls = [E.fifa_2020_qualifications_url, E.fifa_futsal_wc_url, E.uefa_futsal_url, E.afc_futsal_url,
        E.concacaf_futsal_url, E.copa_america_futsal_url, E.ofc_futsal_url ] #TODO: fix:, E.africa_futsal_url]

    allFCs = []

    # delete previous file
    if os.path.exists(filename):
        os.remove(filename)

    def parse(self, response):
        # parse current page for data
        fc = parse_footballbox(response)
        # add parsed fc data to list
        self.allFCs.append(fc) 

        # provides pages that will be scraped
        for next_page in response.xpath(E.next_page_link):
            if 'Futsal' in next_page.extract(): # TODO: generalised, improve
                yield response.follow(next_page, self.parse)

    def closed(self, reason):
        # sort fc data by year 
        self.allFCs.sort(key=lambda x: x.getYear(), reverse=False)
        # write to csv file
        for fc in self.allFCs:
            write_fc_to_csv(fc)


def parse_footballbox(response):
    fhome = []
    fscore = []
    faway = []

    fc = FutsalCup()
    fc.setTitle(response.css(E.page_title_s_css).extract()[0])   
    fc.setHost(response.xpath(E.host_country).extract())
    #fc.setNumberOfTeams(response.xpath(E.number_of_teams).extract()) # TODO: fix for euro
    fc.setPlayedMatchesCount(response.xpath(E.played_matches).extract())

    # missing info for 1996, 2000, 2004, 2008
    fdate = response.xpath(E.date).extract()
    ftime = response.xpath(E.time).extract()
    
    # *_extras important for 2000, 2004, 2008, but for 2012 and 2016 picks up additional incorrect info 
    if fc.getYear() != 2005 and fc.getYear() != 2010 and fc.getYear() != 2014 and fc.getYear() != 2012 and fc.getYear() != 2016: # TODO: add years to list and check list
        fhome = response.xpath(E.home_extras).extract()
        faway = response.xpath(E.away_extras).extract()
    # deafult football box elements
    fhome += response.xpath(E.home_fb).extract()
    faway += response.xpath(E.away_fb).extract()

    fscore = parse_match_results(fc, fscore, response)

    # date (or anything that will be written to csv) can't have comma or it will be split it in columns
    for x in range(len(fhome)):
        if x < len(fdate):
            fdate[x] = fdate[x].replace(E.comma,'')
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
    #TODO: exclude to be played ?
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

def parse_fc_rankings():
    # TODO: implement
    print("implement")

def parse_global_rankings():
    # TODO: implement
    print("implement")

def parse_tables(response):
    tables = []
    for tbl in response.xpath('//table/child::*'):
        table = []
        for tr in tbl.xpath('tr'):
            row = []
            for cell in tr.xpath('child::*/descendant::text()'):
                tcell = cell.extract().strip().replace('\xa0', E.empty_str)
                if tcell != '' and tcell != ' ' and tcell != '\n' and tcell != '\xa0':
                    row.append(tcell)
            table.append(row)
        
        if len(table) > 1: # ignore tables that have only one row
            tables.append(table)
    return tables            

# write parsed fc data by appending
def write_fc_to_csv(fc):
    print('writing to csv...')
    
    if 1980 <= fc.getYear() <= 2022: # TODO: adjust

        with open(filename, mode ='a', encoding="utf-8") as f:
            f.write(fc.getTitle() + E.new_line)
            f.write(str(fc.getYear()) + E.new_line)
            f.write(fc.getHost() + E.new_line)
            for x in range(len(fc.getHome())):
                outputStr = (fc.getDate()[x] + E.comma + fc.getTime()[x] + E.comma + fc.getHome()[x] +
                    E.comma + fc.getScore()[x] + E.comma + fc.getAway()[x])
                f.write(outputStr + E.new_line)

    print('DONE')
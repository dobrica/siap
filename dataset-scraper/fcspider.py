import scrapy
import os
import elements
from futsalcup import FutsalCup

basepath = 'results/'
filename = basepath + 'wiki_data.csv'

class FCSpider(scrapy.Spider):
    name = 'fcspider'
    start_urls = [elements.fifa_2020_qualifications_url, elements.fifa_futsal_wc_url, elements.uefa_futsal_url, elements.afc_futsal_url,
        elements.concacaf_futsal_url, elements.copa_america_futsal_url, elements.ofc_futsal_url ] #TODO: fix:, elements.africa_futsal_url]

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
        for next_page in response.xpath(elements.next_page_link):
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
    fc.setTitle(response.css(elements.page_title_s_css).extract()[0])   
    fc.setHost(response.xpath(elements.host_country).extract())
    #fc.setNumberOfTeams(response.xpath(elements.number_of_teams).extract()) # TODO: fix for euro
    fc.setPlayedMatchesCount(response.xpath(elements.played_matches).extract())

    # missing info for 1996, 2000, 2004, 2008
    fdate = response.xpath(elements.date).extract()
    ftime = response.xpath(elements.time).extract()
    
    # *_extras important for 2000, 2004, 2008, but for 2012 and 2016 picks up additional incorrect info 
    if fc.getYear() != 2005 and fc.getYear() != 2010 and fc.getYear() != 2014 and fc.getYear() != 2012 and fc.getYear() != 2016: # TODO: add years to list and check list
        fhome = response.xpath(elements.home_extras).extract()
        faway = response.xpath(elements.away_extras).extract()
    # deafult football box elements
    fhome += response.xpath(elements.home_fb).extract()
    faway += response.xpath(elements.away_fb).extract()

    fscore = parse_match_results(fc, fscore, response)

    # date (or anything that will be written to csv) can't have comma or it will be split it in columns
    for x in range(len(fhome)):
        if x < len(fdate):
            fdate[x] = fdate[x].replace(elements.comma,'')
        # if time/date is missing add empty string to corresponding list
        if x >= len(ftime):
            ftime.append(elements.empty_str)
        if x >= len(fdate):
            fdate.append(elements.empty_str)

    fc.setDate(fdate)
    fc.setTime(ftime)
    fc.setHome(fhome)
    fc.setScore(fscore)
    fc.setAway(faway)
    
    return fc    

def parse_match_results(fc, fscore, response):
    #TODO: exclude to be played ?
    if fc.getYear() != 2012 and fc.getYear() != 2016:
        fscore = response.xpath(elements.score_extras)

    # football boxes parse match results, regular time (includes extra time) and penalties
    f_boxes = response.xpath(elements.football_box)
    for x in range(len(f_boxes)):
        if elements.pen_time in f_boxes[x].extract():
            fscore += f_boxes[x].xpath(elements.score_pen)
        else:
            fscore += f_boxes[x].xpath(elements.score_reg)

    temp = fscore
    fscore = []
    # get correct result and remove unwanted characters [parentheses, space, unicode-space] from scores array
    for x in range(len(temp)):
        if temp[x].extract().strip() != '(' and temp[x].extract().strip() != ')':
            fscore.append(temp[x].extract().split(elements.new_line)[0].strip()
                .replace('Cancelled', elements.empty_str)
                .replace('Awarded', elements.empty_str)
                .replace('aet', elements.empty_str)
                .replace('walkover', elements.empty_str)
                .replace(u'\xa0', elements.empty_str)
                .replace('(', elements.empty_str)
                .replace(')', elements.empty_str)
                .replace(' ', elements.empty_str))

    for sc in fscore:
        if sc == elements.empty_str:
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
                tcell = cell.extract().strip().replace('\xa0', elements.empty_str)
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
            f.write(fc.getTitle() + elements.new_line)
            f.write(str(fc.getYear()) + elements.new_line)
            f.write(fc.getHost() + elements.new_line)
            for x in range(len(fc.getHome())):
                outputStr = (fc.getDate()[x] + elements.comma + fc.getTime()[x] + elements.comma + fc.getHome()[x] +
                    elements.comma + fc.getScore()[x] + elements.comma + fc.getAway()[x])
                f.write(outputStr + elements.new_line)

    print('DONE')
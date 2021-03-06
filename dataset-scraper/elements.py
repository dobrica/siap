# links and titles
uefa_2022_qualifications_url = 'https://en.wikipedia.org/wiki/UEFA_Futsal_Euro_2022_qualifying'
fifa_2020_qualifications_url = 'https://en.wikipedia.org/wiki/2020_FIFA_Futsal_World_Cup_qualification_(UEFA)'
fifa_2016_qualifications_url = 'https://en.wikipedia.org/wiki/2016_FIFA_Futsal_World_Cup_qualification_(UEFA)'
fifa_2012_qualifications_url = 'https://en.wikipedia.org/wiki/2012_FIFA_Futsal_World_Cup_qualification_(UEFA)'
fifa_2008_qualifications_url = 'https://en.wikipedia.org/wiki/2008_FIFA_Futsal_World_Cup_qualification_(UEFA)'
is_fifa_title = 'FIFA_Futsal_World'
fifa_futsal_wc_url = 'https://en.wikipedia.org/wiki/FIFA_Futsal_World_Cup'
is_uefa_title = 'UEFA_Futsal'
uefa_futsal_url = 'https://en.wikipedia.org/wiki/UEFA_Futsal_Championship'
is_afc_title = 'AFC_Futsal_Championship'
afc_futsal_url = 'https://en.wikipedia.org/wiki/AFC_Futsal_Championship'
is_african_title = 'Africa'
africa_futsal_url = 'https://en.wikipedia.org/wiki/Africa_Futsal_Cup_of_Nations'
is_concacaf_title = 'CONCACAF_Futsal_Championship'
concacaf_futsal_url = 'https://en.wikipedia.org/wiki/CONCACAF_Futsal_Championship'
is_copa_america_title = 'rica_de_Futsal'
copa_america_futsal_url = 'https://en.wikipedia.org/wiki/Copa_América_de_Futsal'
is_ofc_title = 'Futsal' # Oceanian or OFC
ofc_futsal_url = 'https://en.wikipedia.org/wiki/OFC_Futsal_Championship'

# frequent elements and constants
new_line = '\n'
comma = ','
empty_str = ''
pen_time = 'Penalties'
TEAM = 'Team'  
PTS = 'Pts'
PLD = 'Pld'
DIFF = 'Diff'
POS = 'Pos'
PLACE = 'Place'
RANK = 'Rank'
TDETAILS = 'Tournament details'

# xpath and css selectors
next_page_link = '//i/a/@href'
page_title_s_css = '#firstHeading::text'
host_country = '//*[@class="infobox vcalendar"]/tbody/tr[4]/td/descendant::text()[last()]'
number_of_teams = '//*[@class="infobox vcalendar"]/tbody/tr[6]/td/text()'
played_matches = '//*[@class="infobox vcalendar"]/tbody/tr[14]/td/text()'
date = '//*[@class="footballbox"]/div/time/div[1]/text()'
time = '//*[@class="footballbox"]/div/time/div[2]/text()'
home_extras = '//*[not(@class="wikitable")]/tbody/tr/td[1]/b/a/text()'
score_extras = '//*[not(@class="wikitable")]/tbody/tr/td[2]/b/text()'
away_extras = '//*[not(@class="wikitable")]/tbody/tr/td[3]/b/a/text()'
football_box = '//*[@class="footballbox"]/table/tbody'
home_fb = '//*[@class="footballbox"]/table/tbody/tr/th[@class="fhome"]/span/a/text()'
score_reg = 'tr/th[@class="fscore"]/text()'
score_pen = 'tr[@class="fgoals"]/th/descendant::text()[last()]' 
away_fb = '//*[@class="footballbox"]/table/tbody/tr/th[@class="faway"]/span/a/text()'
table_nodes = '//table/child::*'
table_rows = 'tr'
subnode_text = 'child::*/descendant::text()'
vevent = '//*[@class="vevent"]/table/tbody/tr'
vev_date = 'td[1]/span[1]/text()'
vev_home = 'td[2]/b/span/a/descendant::text()'
vev_score = 'td[3]/span[1]/b/text()'
vev_away = 'td[4]/b/span/a/descendant::text()'
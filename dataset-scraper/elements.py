# links and titles
#TODO: find more data
fifa_2020_qualifications_url = 'https://en.wikipedia.org/wiki/2020_FIFA_Futsal_World_Cup_qualification_(UEFA)' # TODO: add more qualifications?
is_fifa_title = 'FIFA_Futsal_World'
fifa_futsal_wc_url = 'https://en.wikipedia.org/wiki/FIFA_Futsal_World_Cup'
is_uefa_title = 'UEFA_Futsal'
uefa_futsal_url = 'https://en.wikipedia.org/wiki/UEFA_Futsal_Championship'
is_afc_title = 'AFC_Futsal_Championship'
afc_futsal_url = 'https://en.wikipedia.org/wiki/AFC_Futsal_Championship'
is_african_title = 'Africa' #TODO: before 2016 different results parsing
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
## **Description**

Prediction Futsal World Cup 2021 winner.<br/>
Dataset scraping from Wikipedia using scrapy.<br/>
Prediction of results using Poisson regression.<br/>

> **Warning**:
> This repo is not beeing maintained. Scraper can report errors or provide incomplete data, because the source is constantly changing. Therefore results.zip contains already scraped data that can be used.

## **Tech stack** 
<img align="left" alt="Python" width="30px" style="padding-right:10px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-plain.svg" />
<img align="left" alt="" width="30px" style="padding-right:10px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg" />
<img align="left" alt="" width="30px" style="padding-right:10px;" src="https://scipy.org/images/logo.svg" />
<img align="left" alt="" width="30px" style="padding-right:10px;" src="https://pbs.twimg.com/profile_images/690207449471582208/LJ_Gsz28_400x400.png" />
<img align="left" alt="" width="30px" style="background-color: #fff;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg" />
<br/>
<br/>

## **Deployment**

**Requirements:** Python 3.7-3.10, Pip

Install required python dependencies.
```
pip install -r requirements.txt
```
Running prediction - scraped and preprocessed data is already available in this repo.

```
python3 poisson-model/model.py
```
Dataset scraper: currently set to scrape UEFA results. Scraping results are already packed in dataset-scraper/results/*.zip files.<br/>
Running scraper:
```
python3 dataset-scraper/app.py
```
or
```
scrapy runspider dataset-scraper/fcspider.py
```

Running preprocessor:
```
python3 poisson-model/preprocessor.py
```
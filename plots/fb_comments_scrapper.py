import os
import copy
import json
import time
import pickle
import indicoio
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from urllib import urlopen, urlretrieve
from wordcloud import WordCloud, STOPWORDS
	
class FbCommentScrapper(object):

	PROJECT_ROOT=os.getcwd()
	IMG_ROOT = PROJECT_ROOT+'/plots/static/images/'

	def __init__(self):
		self.update_cache=False

	def status_scraper(self, month = 10, year = 2016):
		app_id = '599965930180946'
		app_secret = '575aa5390a4589483de7f8cf99702788'
		page_id = ["ExplorePakistan","Beautiful.places.in.Pakistan","BeautifulPakistan","pakistanthebeautifull","humpakistan.info","wonderfulpakistan"]
		access_token = app_id + "|" + app_secret
		base = "https://graph.facebook.com/v2.6/"
		num_statuses=50

		for page in page_id:
			node = "/" + page + "/feed"
			for i in list(range(0,100)):
				print i, page

				if i==0:
					parameters = "/?fields=message,link,created_time,type,name,id,comments.limit(20),shares,reactions.limit(1)&limit=%s&offset=%s&access_token=%s" % (num_statuses,0, access_token)
				else:
					parameters = "/?fields=message,link,created_time,type,name,id,comments.limit(20),shares,reactions.limit(1).summary(true)&limit=%s&offset=%s&access_token=%s" % (num_statuses,(num_statuses*i)+1, access_token)
				url = base + node + parameters
				flag_break = self.read_or_retrieve(url, num_statuses, "%02d" % (month,), str(year))
				
				if flag_break:
					break

				time.sleep(20)
	
	def read_or_retrieve(self, url, num_statuses, month, year):
		flag_break = False

		if os.path.isdir(cls.PROJECT_ROOT+'/plots/cache/'):
			pass
		else:
			os.mkdir(cls.PROJECT_ROOT+'/plots/cache/')

		url_obj = self.get_url_obj(url, num_statuses)
		for item in url_obj:
			date_array = str(item['created_time']).split('-')
			if 'message' in item and date_array[0] == year and date_array[1] == month:
				print item['created_time']
				fname = cls.PROJECT_ROOT + '/plots/cache/' + item['id']
				try:
					with open(fname +'.pickle', 'rb') as handle:
						pickle.load(handle)
				except:
					with open(fname+'.pickle', 'wb') as handle:
						pickle.dump(item, handle)
				handle.close()
			else:
				flag_break = True
				break

		return flag_break
		
	@classmethod
	def get_url_obj(cls, url, num_statuses):
		req=requests.get(url).json()
		return req['data']

	@classmethod
	def fetch_posts_from_cache(cls):
		CACHE_ROOT = cls.PROJECT_ROOT+'/plots/cache/'
		fnames = os.listdir(CACHE_ROOT)
		posts = []
		for fname in fnames:
			with open(CACHE_ROOT + fname, 'rb') as handle:
				post = pickle.load(handle)
			handle.close()
			if 'message' in post:
				for validation in ['k2','K2','k-2','K-2']:
					if validation in post['message']:
						posts.append(post)
						break
		return posts

	@classmethod
	def plot_wordcloud(cls):
		FONT_ROOT = cls.PROJECT_ROOT+'/plots/static/fonts/'
		word_string = cls.parse_comments()
		wordcloud = WordCloud(font_path=FONT_ROOT + 'arial.ttf',
		                          stopwords=STOPWORDS,
		                          background_color='black',
		                          width=1200,
		                          height=1000
		                         ).generate(' '.join(word_string))

		plt.imshow(wordcloud)
		plt.axis('off')
		plt.title('Word cloud of responses by travel freaks-October, 2016')
		plt.savefig(cls.IMG_ROOT + 'wordcloud.png', bbox_inches='tight')
		plt.close()
		# plt.show()

	@classmethod
	def plot_sentiment(cls):
		indicoio.config.api_key = '47b4880774a89fa23a5f47acdbfb832c'
		word_string = cls.parse_comments()
		scores = indicoio.sentiment(word_string)
		mean_score = np.mean(scores)
		state = 'Positive' if mean_score>0.5 else 'Neutral' if mean_score==0.5 else 'Negative'
		
		sentiment_scores = {'comments':[], 'scores':[]}
		for i in range(len(word_string)):
			sentiment_scores['comments'].append(word_string[i])
			sentiment_scores['scores'].append(scores[i])

		df = pd.DataFrame(sentiment_scores)
		df.plot(use_index=False, \
			title= 'Sentiment scores of comments-October, 2016 (Response: %s)'%state, \
			legend=True)
		plt.xlabel('Comment Id')
		plt.ylabel('Sentiment score')
		plt.savefig(cls.IMG_ROOT + 'sentiment.png', bbox_inches='tight')
		plt.close()
		# plt.show()

	@classmethod
	def parse_comments(cls):
		word_string = []
		posts = cls.fetch_posts_from_cache()
		for post in posts:
			word_string.append(post['message'])
			if 'comments' in post:
				comments = post['comments']['data']
				for comment in comments:
					if comment['message']:
						word_string.append(comment['message'])

		return word_string
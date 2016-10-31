from django.http import HttpResponse
from django.template import loader
import os

# from plots.fb_comments_scrapper import FbCommentScrapper

# fb = FbCommentScrapper()

ALL_PLOTS = {'scatter':
				{
				'location':'sentiment.png', \
				'title': 'Scatter plot of sentiment analysis', \
				'description': 'Plot of sentiment scores of K2 (i.e. Second highest peak of the world)'}, \
			'wordcloud':
				{
				'location': 'wordcloud.png', \
				'title': 'Wordcloud cloud of comments', \
				'description': 'Wordcloud from frequency distribution of occurance of words in posts of K2 (i.e. Second highest peak of the world)'}
			}

PROJECT_ROOT=os.getcwd()
IMG_ROOT = PROJECT_ROOT+'/plots/static/images/'

def index(request):
	html = ''
	for plot in ALL_PLOTS:
		url = '/plots/' + plot + '/'
		html += '<a href="' + url + '">' + ALL_PLOTS[plot]['title'] + '</a><br>'
	return HttpResponse(html)

def data(request):
	API_CONFIG = {'Facebook Graph API':
					{
					'description': 'This API is used to scrap comments for tourist spots from Facebook pages. These will then be used for sentiment analysis.',
					'url':"https://developers.facebook.com/docs/graph-api"},
				'Google Places API':
					{
					'description': 'This API is used to scrap the tourist spots, and will work as the input parameter to scrap the posts and comments from Facebook pages',
					'url':"https://developers.google.com/places/"},
				'Indico API':
					{
					'description': 'This API is used to calculate the sentiment scores for the comments and posts of the travel spot',
					'url':"https://indico.io/"},
					}

	html = ''
	html += '<h1>Public Description of Data sources</h1><br>'
	for source,value in API_CONFIG.items():
		html += '<h2>' + source + '</h2>'
		html += '<p>' + value['description'] + '</p>'
		html += '<a href=' + value['url'] + '>' + source + ' helpdoc</a><br>'

	# html += '<h2>Facebook Graph API</h2>'
	# html += '<p>This API is used to scrap comments for tourist spots. These will then be used for sentiment analysis.</p>'
	# html += '<a href="https://developers.facebook.com/docs/graph-api">Facebook Graph API helpdoc</a><br>'
	return HttpResponse(html)

def scatter(request):
	# fb.plot_sentiment()
	context = {
		'all_plots': ALL_PLOTS['scatter'],
	}
	return HttpResponse(render_html(context))

def wordcloud(request):
	# fb.plot_wordcloud()
	context = {
		'all_plots': ALL_PLOTS['wordcloud'],
	}
	return HttpResponse(render_html(context))

def render_html(context):
	html = ''
	all_plots = context['all_plots']
	if all_plots:
		html += '<h1>' + all_plots['title'] + '</h1>'
		html += '<p>' + all_plots['description'] + '<p>'
		# html += '<img class="plotImage" alt="Image of Plot" src=' + IMG_ROOT + \
		# 	all_plots['location'] + '"/>'

		html += '<img class="plotImage" alt="Image of Plot" src="/static/images/' + \
			all_plots['location'] + '"/>'
	else:
		html += "<h3>You don't have any plots</h3>"

	return html
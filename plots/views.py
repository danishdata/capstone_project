from django.http import HttpResponse
from django.template import loader
import os

# from plots.fb_comments_scrapper import FbCommentScrapper

# fb = FbCommentScrapper()

ALL_PLOTS = {'sentiment':
				{
				'location':'sentiment.png', \
				'title': 'Line chart of sentiment analysis', \
				'description': 'Plot of sentiment scores of K2 (i.e. Second highest peak of the world)'}, \
			'wordcloud':
				{
				'location': 'wordcloud.png', \
				'title': 'Wordcloud of comments', \
				'description': 'Wordcloud from frequency distribution of posts relating to K2 (i.e. Second highest peak of the world)'}
			}

PROJECT_ROOT=os.getcwd()
IMG_ROOT = PROJECT_ROOT+'/plots/static/images/'
BROWSER_TITLE = "<title>Tourists' companion</title>"

def index(request):
	html = BROWSER_TITLE
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

	return HttpResponse(html)

def sentiment(request):
	# fb.plot_sentiment()
	context = {
		'all_plots': ALL_PLOTS['sentiment'],
	}
	return HttpResponse(render_html(context))

def wordcloud(request):
	# fb.plot_wordcloud()
	context = {
		'all_plots': ALL_PLOTS['wordcloud'],
	}
	return HttpResponse(render_html(context))

def render_html(context):
	html = BROWSER_TITLE
	all_plots = context['all_plots']
	if all_plots:
		html += '<h1>' + all_plots['title'] + '</h1>'
		html += '<p>' + all_plots['description'] + '<p>'

		html += '<img class="plotImage" alt="Image of Plot" src="/static/images/' + \
			all_plots['location'] + '"/>'

	else:
		html += "<h3>You don't have any plots</h3>"

	return html
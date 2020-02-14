
import logging
import optparse
import tornado.wsgi
import tornado.httpserver
from utils import get_today_menu


from flask import render_template, abort, Flask, url_for, request

menu_items = get_today_menu()

data_txtfile = '/tmp/data.txt'

poll_data = {
   'question': 'How do you rate today\'s Mensa Flugplatz food?',
    'like': ['Delicious', 'Great', 'Meh', 'Better than nothing', 'I want to die'],
   'essen_1': menu_items[0],
   'essen_2': menu_items[1],
}



def start_tornado(app, port=5001):
    http_server = tornado.httpserver.HTTPServer(
        tornado.wsgi.WSGIContainer(app))
    http_server.listen(port)
    print("Tornado server starting on port {}".format(port))
    tornado.ioloop.IOLoop.instance().start()

def start_from_terminal(app):
    """
    Parse command line options and start the server.
    """
    parser = optparse.OptionParser()
    parser.add_option(
        '-d', '--debug',
        help="enable debug mode",
        action="store_true", default=False)
    parser.add_option(
        '-p', '--port',
        help="which port to serve content on",
        type='int', default=5001)
    parser.add_option(
        '-g', '--gpu',
        help="use gpu mode, specify gpu to use",
        type='int', default=-1)

    opts, args = parser.parse_args()

    start_tornado(app, opts.port)

# Obtain the flask app object
app = Flask(__name__)

@app.route('/', defaults={'page': 'index'})
@app.route('/<path:page>')

# def show(page):
#     return render_template('index.html')


@app.route('/')
def root():
    return render_template('index.html', data=poll_data)


@app.route('/results')
def show_results():

    votes_essen_1 = {}
    votes_essen_2 = {}

    for f in poll_data['like']:
        votes_essen_1[f] = 0
        votes_essen_2[f] = 0

    f = open(data_txtfile, 'r')
    for line in f:
        vote = line.rstrip("\n")
        vote = vote.split(',')

        if vote[0] == 'essen1':
            votes_essen_1[vote[1]] += 1

        if vote[0] == 'essen2':
            votes_essen_2[vote[1]] += 1

    return render_template('results.html', data=poll_data, votes_essen_1=votes_essen_1, votes_essen_2=votes_essen_2)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    start_from_terminal(app)

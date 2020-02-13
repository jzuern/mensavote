from flask import Flask, render_template, request
import os
from utils import get_today_menu
app = Flask(__name__)




menu_items = get_today_menu()



poll_data = {
   'question': 'How do you rate today\'s Mensa Flugplatz food?',
    'like': ['Delicious', 'Great', 'Meh', 'Better than nothing', 'I want to die'],
   'essen_1': menu_items[0],
   'essen_2': menu_items[1],
}


data_txtfile = '/tmp/data.txt'


@app.route('/')
def root():
    return render_template('poll.html', data=poll_data)


@app.route('/poll')
def poll():
    vote1 = request.args.get('field_essen_1')
    vote2 = request.args.get('field_essen_2')

    out = open(data_txtfile, 'a')


    if vote1 is not None:
        out.write('essen1,' + vote1 + '\n')
        out.flush()
    if vote2 is not None:
        out.write('essen2,' + vote2 + '\n')
        out.flush()
    out.close()

    return render_template('thankyou.html', data=poll_data)


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


if __name__ == "__main__":
    app.run(port='5001', debug=True)


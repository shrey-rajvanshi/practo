'''
import newrelic.agent
newrelic.agent.initialize('newrelic.ini','staging')'''
from app import app
if __name__ == '__main__':
	app.secret_key = 'super secret keyadfadsf12835796Shreysfjkhogh08923epuoij'
	app.run(debug=True)
from app import create_app
from app.models.events import Events

import schedule
import time
import datetime
from datetime import timedelta, date

import threading

app = create_app()

def event_cheker():
    
    s = date.today()
    
    print(type(s))
    print(s)
    
    with app.app_context():

        schedule.every().day.at("08:30").do(Events.delete_events, s)
        while True:
            schedule.run_pending()
            time.sleep(50) # Cheking every 50 seconds

try:
    if __name__ == '__main__':
        t1 = threading.Thread(target=event_cheker, daemon=False)

        t1.start()

        app.run(debug=app.config['DEBUG'], host=app.config['IP'],  port=app.config['PORT'])
except (KeyboardInterrupt, SystemExit):
    t1.join()
    print("Program finished")
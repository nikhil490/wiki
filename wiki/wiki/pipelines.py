from .models import db_connect, create_table, Events
from sqlalchemy.orm import sessionmaker


class WikiPipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        events = Events()
        events.day = item['day']
        events.year = item['year']
        events.event = item['event']
        events.type_of_event = item['type_of_event']
        events.AD_BC = item['AD/BC']
        events.date = item['date']

        try:
            session.add(events)
            session.commit()
        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
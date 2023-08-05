from output.database.database_base import Base, engine
from output.models.contact_database import Contact
from output.models.site_database import Site, SitesContacts
from output.models.label_database import Label, LabelsContacts
from output.models.favorite_links_database import FavoriteLinksData
from output.models.activity_logs_database import ActivityLogsData
from output.models.user_database import UserData

if __name__ == '__main__':
    Base.metadata.create_all(engine)

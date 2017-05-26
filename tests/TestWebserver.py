import bfly
import unittest as ut
import datetime
import logging
import sys

class TestWebserver(ut.TestCase):
    """ set up tests for `bfly.Webserver`
    """
    PORT = 2017
    DB_PATH = None
    DB_TYPE = 'Zodb'
    RUNTIME = bfly.UtilityLayer.RUNTIME()
    # Log to the command line
    log_info = {
        'stream': sys.stdout,
        'level': logging.INFO
    }

    def test_web(self):
        """ test that `bfly.Webserver` can start and stop.
        """

        # Log to command line
        logging.basicConfig(**self.log_info)

        # Make a dummy database
        db_class = getattr(bfly.DatabaseLayer, self.DB_TYPE)
        db = db_class(self.DB_PATH, self.RUNTIME)

        # Make a dummy webserver
        config = bfly.UtilityLayer.rh_config.config
        web = bfly.Webserver(db, config)
        server = web.start(self.PORT)

        # Stop the webserver after 1 second
        one_sec = datetime.timedelta(seconds=1)
        server.add_timeout(one_sec, web.stop)

        # Start the webserver right now
        server.start()

if __name__ == '__main__':
    ut.main()

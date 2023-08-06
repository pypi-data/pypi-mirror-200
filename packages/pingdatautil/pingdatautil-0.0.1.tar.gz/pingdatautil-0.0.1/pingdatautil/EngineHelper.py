import time
from datetime import datetime
from sqlalchemy.orm import sessionmaker


class EngineHelper():
    def __init__(self, engine=None, logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = None

        self.time = None

        self.session = None

        if engine:
            self.engine = engine
            self.start_session()
        else:
            self.engine = None

    ###############
    ### LOGGING ###
    ##############

    def log(self, input_str, level=None):
        ident = "[ENGINE-HELPER]"
        if not self.logger:
            dt_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("[" + dt_str + "] " + ident + " " + input_str)
        else:
            self.logger.log(ident + " " + input_str, level)

    def timer_start(self):
        self.log(F"Timer Start")
        self.time = time.time()

    def timer_stop(self):
        t = time.time()
        i = t - self.time
        txt = "{:.3f}".format(i)
        self.log(F"Finished in {txt}s")
        return txt

    #####################
    #### MAIN CLASS #####
    #####################

    def start(self):
        sess = sessionmaker(bind=self.engine)
        self.session = sess()

    def start_session(self):
        sess = sessionmaker(bind=self.engine)
        self.session = sess()

    def set_engine(self, engine):
        self.engine = engine

    def execute(self, sql_command):
        self.timer_start()
        sql_txt = sql_command.replace('\n', ' ').strip()
        try:
            self.log(f"Execute using: {sql_txt}")
            r = self.session.execute(sql_command)
            if r.rowcount and r.rowcount > 0:
                self.log(f"{str(r.rowcount)} rows affected.")
            self.session.commit()
            self.log(f"Done")
        except Exception as e:
            self.log(f"Cannot execute: {sql_txt}", "ERROR")
            self.log(f"{str(e)}", "ERROR")
            self.session.rollback()
        self.timer_stop()

    def stop(self):
        self.session.close()

    def stop_session(self):
        self.session.close()


if __name__ == "__main__":
    engine = EngineHelper()
    engine.log("Test")

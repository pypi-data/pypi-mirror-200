import pingdatautil
logger = pingdatautil.Logger()
linenotify = pingdatautil.LineNotify(token="A", logger=logger)
en = pingdatautil.EngineHelper(logger=logger)
oh = pingdatautil.ODBCHelper(logger=logger)
cs = (
    F"DRIVER=ODBC Driver 17 for SQL Server;"
    F"SERVER=localhost;PORT=1433;"
    F"DATABASE=TEST;UID=sa;PWD=P@ssw0rd;"
)
oh.connect(cs)
oh.execute_full("SELECT TOP 10 * FROM bnk48_member", with_result=True)
oh.close()


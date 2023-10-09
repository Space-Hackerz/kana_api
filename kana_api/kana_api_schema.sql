CREATE TABLE fire_reports (
	geotag_lat  DOUBLE,
	geotag_long DOUBLE,
	phone_lat   DOUBLE,
	phone_long  DOUBLE,
	time_submitted TEXT,
	time_recieved  TEXT,
	severity	   TEXT,
	satellite_confidence TEXT,
	satellite_confirm    INTEGER
);

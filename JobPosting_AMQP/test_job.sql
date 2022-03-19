CREATE DATABASE job;

use job;

CREATE TABLE job (
  JID int(11) NOT NULL AUTO_INCREMENT,
  job_title varchar(32) NOT NULL,
  CID varchar(10) NOT NULL,
  datetime_posted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (JID)
);

INSERT INTO job (JID, job_title, CID, datetime_posted) VALUES
(1, 'internship', '1', '2021-03-16 02:14:55');

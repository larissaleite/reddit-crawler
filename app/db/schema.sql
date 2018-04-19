CREATE TABLE IF NOT EXISTS submissions (
  message_id VARCHAR(64) PRIMARY KEY,
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  user VARCHAR(128) NULL,
  discussion_url VARCHAR(160),
  url VARCHAR(160) NOT NULL,
  punctuation INT(11),
  num_comments INT(11) NOT NULL,
  created_date VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS comments (
    message_id VARCHAR(64) PRIMARY KEY,
    parent_id VARCHAR(64),
    submission_id VARCHAR(64),
    user VARCHAR(128) not null,
    message TEXT NOT NULL,
    punctuation INT(11)
);

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(64) PRIMARY KEY,
    comment_karma INT(11) NOT NULL,
    post_karma INT(11) NOT NULL
);

ALTER TABLE submissions CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

ALTER TABLE comments CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

ALTER TABLE users CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
-- DROP TABLE submissions;
-- DROP TABLE comments;
-- DROP TABLE users;
-- DROP TABLE tags;

CREATE TABLE IF NOT EXISTS submissions (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  subreddit TEXT NOT NULL,
  submitter TEXT NOT NULL,
  discussion_url TEXT,
  url TEXT NOT NULL,
  punctuation INTEGER NOT NULL,
  num_comments INTEGER NOT NULL,
  created_date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    parent_id TEXT,
    submission_id TEXT,
    user TEXT NOT NULL,
    TEXT TEXT NOT NULL,
    punctuation INTEGER NOT NULL,
    FOREIGN KEY(submission_id) REFERENCES submissions(id),
    FOREIGN KEY(parent_id) REFERENCES comments(id)
);

CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    comment_karma INTEGER NOT NULL,
    post_karma INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER,
    username TEXT NOT NULL,
    tag TEXT NOT NULL,
    CONSTRAINT unique_username_tag UNIQUE (username, tag)
);

CREATE TABLE IF NOT EXISTS submissions_tags (
    submission_id TEXT,
    tag_id INTEGER REFERENCES tags (id),
    FOREIGN KEY (submission_id) REFERENCES submissions (id),
    FOREIGN KEY (tag_id) REFERENCES tags (id),
    PRIMARY KEY (submission_id, tag_id)
);

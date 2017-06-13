create table if not exists submissions (
  id text primary key,
  title text not null,
  submitter text not null,
  discussion_url text,
  url text not null,
  punctuation integer not null,
  num_comments integer not null,
  created_date text not null
);

create table if not exists comments (
    id text primary key,
    parent_id text,
    submission_id text,
    user text not null,
    text text not null,
    punctuation integer not null,
    FOREIGN KEY(submission_id) REFERENCES submissions(id),
    FOREIGN KEY(parent_id) REFERENCES comments(id)
);

create table if not exists users (
    username text primary key,
    comment_karma integer not null,
    post_karma integer not null
);

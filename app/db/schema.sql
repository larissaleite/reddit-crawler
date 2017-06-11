create table if not exists submission (
  title text not null,
  submitter text not null,
  discussion_url text,
  url text not null,
  punctuation integer not null,
  num_comments integer not null,
  created_date text not null
);

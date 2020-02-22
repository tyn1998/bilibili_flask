drop database if exists bilibili_flask;
create database bilibili_flask;
use bilibili_flask;

drop table if exists bilibiliers;
create table bilibiliers
(
	uid varchar(20) not null primary key,
	uname varchar(30) not null,
	sex varchar(4) not null,
	birthday varchar(10) not null,
	sign varchar(300),
	face_photo_url varchar(200) not null,
	top_photo_url varchar(200) not null,
	following_count int not null,
	follower_count int not null,
	video_count int not null
);

drop table if exists videos;
create table videos
(
	av varchar(20) not null primary key,
	uid varchar(20) not null,
	title varchar(100) not null,
	des varchar(1000) not null,
	length varchar(10) not null,
	created varchar(20) not null,
	play_count int not null,
	comment_count int not null,
	cover_photo_url varchar(200) not null
);

drop table if exists v_basic;
create table v_basic
(
	av varchar(20) not null primary key,
	title varchar(100) not null,
	view_count int not null,
	like_count int not null,
	favorite_count int not null,
	coin_count int not null,
	share_count int not null,
	danmu_count int not null,
	reply_count int not null,
	des varchar(1000) not null
);

drop table if exists v_tags;
create table v_tags
(
	av varchar(20) not null,
	tag_id varchar(20) not null,
	tag_name varchar(20) not null
);

drop table if exists v_replies;
create table v_replies
(
	rpid varchar(20) not null primary key,
	av varchar(20) not null,
	content varchar(1000) not null,
	bj_time varchar(20) not null,
	uid varchar(20) not null,
	uname varchar(30) not null,
	sex varchar(4) not null,
	like_count int not null
);

drop table if exists v_subreplies;
create table v_subreplies
(
  rpid varchar(20) not null primary key,
  root varchar(20) not null,
  parent varchar(20) not null,
  dialog varchar(20) not null,
	av varchar(20) not null,
	content varchar(1000) not null,
	bj_time varchar(20) not null,
	uid varchar(20) not null,
	uname varchar(30) not null,
	sex varchar(4) not null,
	like_count int not null
);

drop table if exists v_danmus;
create table v_danmus
(
	av varchar(20) not null,
	v_time varchar(20) not null,
	bj_time varchar(20) not null,
	coded_uid varchar(20) not null,
	content varchar(200) not null
);

create index index_uid on videos(uid asc);
create index index_av on videos(av asc);
create index index_av on v_basic(av asc);
create index index_av on v_tags(av asc);
create index index_av on v_replies(av asc);
create index index_av on v_subreplies(av asc);
create index index_av on v_danmus(av asc);

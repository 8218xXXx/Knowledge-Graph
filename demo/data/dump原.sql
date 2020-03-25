CREATE DATABASE IF NOT EXISTS `online_social_networks`;
SET GLOBAL local_infile=1;
USE online_social_networks;

 CREATE TABLE `freebase` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source_entity` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `target_entity` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `relation` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `rank_value` varchar(45) DEFAULT NULL,
  `trsut` varchar(45) DEFAULT NULL,
  `max_trust_relation` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59072 DEFAULT CHARSET=utf8;

 CREATE TABLE `freebase_entity_id` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `entity_name` varchar(255) DEFAULT NULL,
  `entity_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39465 DEFAULT CHARSET=utf8;

 CREATE TABLE `relationship` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source_user` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `target_user` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `trust_level` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83533 DEFAULT CHARSET=utf8;

 CREATE TABLE `weibo_follow_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `follow_user_name` varchar(255) DEFAULT NULL,
  `follow_user_link` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1340 DEFAULT CHARSET=utf8 ;

 CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `infomation` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `relation` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

 CREATE TABLE `weibo_user_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `weibo_content` longtext,
  `weibo_position` varchar(255) DEFAULT NULL,
  `publish_time` varchar(255) DEFAULT NULL,
  `up_num` varchar(255) DEFAULT NULL,
  `repost_num` varchar(255) DEFAULT NULL,
  `comment_num` varchar(255) DEFAULT NULL,
  `publish_tool` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4942 DEFAULT CHARSET=utf8;

 CREATE TABLE `weibo_user_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `weibo_num` varchar(255) DEFAULT NULL,
  `following` varchar(255) DEFAULT NULL,
  `follower` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

 CREATE TABLE `weibo_user_profile_2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `user_id` varchar(45) NOT NULL,
  `img_url` longtext,
  `authentication` varchar(255) DEFAULT NULL,
  `hometown` varchar(45) DEFAULT NULL,
  `birthday` varchar(45) DEFAULT NULL,
  `introduction` varchar(255) DEFAULT NULL,
  `label` varchar(45) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `education` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;


CREATE DATABASE `ihome` DEFAULT CHARACTER SET utf8;

CREATE TABLE ih_user_profile (
    up_id bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '用户ID',
    up_name varchar(32) NOT NULL COMMENT '昵称',
    up_real_name varchar(32) NOT NULL DEFAULT '' COMMENT '真实姓名',
    up_mobile char(11) NOT NULL COMMENT '手机号',
    up_passwd varchar(64) NOT NULL COMMENT '密码',
    up_ctime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (up_id),
    UNIQUE (up_name),
    UNIQUE (up_mobile)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8 COMMENT='用户信息表';


create table flow_skills_category (
sc_id bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '技能ID',
sc_parent_id bigint(20) NOT NULL DEFAULT '-1' COMMENT '技能所属父类ID，-1为顶级类别',
sc_title varchar(64) NOT NULL DEFAULT '' COMMENT '技能标题',
sc_content varchar(512) NOT NULL DEFAULT '' COMMENT '技能内容',
sc_icon varchar(256) NOT NULL DEFAULT '' COMMENT '显示图标',
sc_color varchar(32) NOT NULL DEFAULT '' COMMENT '显示颜色', 
sc_status tinyint(1) NOT NULL DEFAULT '0' COMMENT '记录状态，0-有效，1-已删除',
sc_createtime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
sc_edituser varchar(32) NOT NULL DEFAULT '' COMMENT '最后更新人',
sc_edittime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
PRIMARY KEY (sc_id),
KEY sc_parent_id (sc_parent_id, sc_title)
) ENGINE=InnotDB DEFAULT CHARSET=utf8 COMMENT='技能类别表';

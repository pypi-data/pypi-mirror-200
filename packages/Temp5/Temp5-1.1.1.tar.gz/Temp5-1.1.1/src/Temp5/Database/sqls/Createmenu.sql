-- In the name of GOD --
BEGIN TRANSACTION;

CREATE TABLE "toolbar" (
	`toolid`	INTEGER,
	`toolname`	TEXT,
	`toolicon`	TEXT,
	`shrttxt`	TEXT,
	`lngtxt`	TEXT,
	`handlerid`	INTEGER,
	`acclvlid`	TEXT
);

CREATE TABLE "security" (
	`userid`	INTEGER,
	`username`	TEXT,
	`password`	TEXT
);
INSERT INTO `security` (userid,username,password) VALUES (1,'Admin','Zxshdg34ijdhfks23yd99IUFHVIAO898w49rhYUFIUW98Hihcsud');

CREATE TABLE "pans" (
	`panid`	INTEGER,
	`panname`	TEXT,
	`pandok`	TEXT,
	`pansiz`	TEXT,
	`panlyr`	INTEGER,
	`paninfoid`	TEXT,
	`handlerid`	INTEGER,
	`acclvlid`	TEXT
);

CREATE TABLE "panifo" (
	`paninfoid`	TEXT,
	`caption`	TEXT,
	`setting`	TEXT,
	`resize`	TEXT,
	`bstsiz`	TEXT,
	`minsiz`	TEXT,
	`maxsiz`	TEXT,
	`docking`	TEXT,
	`position`	TEXT
);

CREATE TABLE "mitem" (
	`mbarid`	INTEGER,
	`itemid`	INTEGER,
	`itemname`	TEXT,
	`itemtyp`	TEXT,
	`extid`	TEXT,
	`handlerid`	INTEGER
);

INSERT INTO `mitem` (mbarid,itemid,itemname,itemtyp,extid,handlerid) VALUES
 (9999,9999,NULL,NULL,NULL,99009),
 (9999,9998,NULL,NULL,NULL,99008),
 (9999,9997,NULL,NULL,NULL,99007),
 (9999,9996,NULL,NULL,NULL,99006),
 (9999,9995,NULL,NULL,NULL,99005),
 (9999,9994,NULL,NULL,NULL,99004),
 (9999,9993,NULL,NULL,NULL,99003),
 (9999,9992,NULL,NULL,NULL,99002),
 (9999,9990,NULL,NULL,NULL,99000);

CREATE TABLE "menubar" (
	`mbarid`	INTEGER,
	`mbarname`	TEXT,
	`mbardir`	TEXT,
	`acclvlid`	TEXT
);

CREATE TABLE "handler" (
	`handlerid`	INTEGER,
	`prgname`	TEXT,
	`prgdir`	TEXT,
	`paramtr`	TEXT,
	`public`	INTEGER,
	`prgno`	INTEGER
);

INSERT INTO `handler` (handlerid,prgname,prgdir,paramtr,public,prgno) VALUES
 (99009,'MDv1','9999','-1',-1,9),
 (99008,'TBv1','9999','-1',-1,8),
 (99007,'PAv1','9999','-1',-1,7),
 (99006,'DBv1','9999','-1',-1,6),
 (99005,'PGv1','9999','-1',-1,5),
 (99004,'TPv1','9999','-1',-1,4),
 (99003,'MLv1','9999','-1',-1,3),
 (99002,'PPv1','9999','-1',-1,2),
 --(10000,'Demo','1000','-1',-1,1),
 (99000,'Demo','8888','-1',-1,0);

CREATE TABLE `grpitem` (
	`grpid`	INTEGER,
	`grpname`	TEXT,
	`grpcnt`	TEXT,
	`grpnl`	TEXT,
	`grpth`	TEXT
);

CREATE TABLE "extended" (
	`extid`	TEXT,
	`status`	TEXT,
	`icon`	TEXT,
	`shortcut`	TEXT,
	`help`	TEXT,
	`acclvlid`	TEXT,
	`grpid`	INTEGER
);

CREATE TABLE "access" (
	`acclvlid`	TEXT,
	`userid`	INTEGER,
	`acclvl`	TEXT,
	`disenable`	INTEGER
);

INSERT INTO `access` (acclvlid,userid,acclvl,disenable) VALUES ('99AB',1,'FFFF',1);

CREATE TABLE `PrgDesc` (
	`handlerid`	INTEGER,
	`Description`	TEXT
);

CREATE TABLE "MLinfo" (
	`MLPid`	INTEGER,
	`MLname`	TEXT,
	`MLcod`	TEXT
);

-- INSERT INTO `MLinfo` (MLPid,MLname,MLcod) VALUES (11701,'NeruNetwork','NN');

CREATE TABLE "MLPane" (
	`MLPid`	INTEGER,
	`MLPfile`	TEXT
);

-- INSERT INTO `MLPane` (MLPid,MLPfile) VALUES (11701,'NeruPanel');

CREATE TABLE `MLAlgo` (
	`MLcod`	TEXT,
	`MLAsrc`	TEXT
);

-- INSERT INTO `MLAlgo` (MLcod,MLAsrc) VALUES ('NN','NeruNet');

CREATE TABLE "Guidir" (
	`Dir`	TEXT,
	`prgdir`	TEXT,
	`hdddir`	TEXT
);

INSERT INTO `Guidir` (Dir,prgdir,hdddir) VALUES
 ('GUI.Main','9999','..\GUI\Main'),
 ('GUI.Temp','8888','..\GUI\Temp'),
 ('Src.GUI','7777','..\Src\GUI'),
 ('Utility','6666','..\Utility'),
 ('Src.AUI','5555','..\Src\AUI'),
 ('Src.MLP','4444','..\Src\MLP'),
 ('Src.MLA','3333','..\Src\MLA'),
 ('Src.API','2222','..\Src\API'),
 ('Src.PRG.','1000','..\Src\PRG\')
 ;
COMMIT;

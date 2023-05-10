SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for w_switch
-- ----------------------------
DROP TABLE IF EXISTS `w_switch`;
CREATE TABLE `w_switch`  (
  `switch` tinyint(4) NOT NULL,
  `t_switchs` char(5) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `begin_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Records of w_switch
-- ----------------------------
INSERT INTO `w_switch` VALUES (1, '1 1 1', NOW());

-- ----------------------------
-- Table structure for w_users
-- ----------------------------
DROP TABLE IF EXISTS `w_users`;
CREATE TABLE `w_users`  (
  `uid` char(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `username` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` char(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `salt` char(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `phone` char(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `email` varchar(33) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `remark` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `phone_check` tinyint(4) NOT NULL DEFAULT 0,
  `email_check` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`uid`) USING BTREE,
  UNIQUE INDEX `u_username_unique`(`username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for w_email_log
-- ----------------------------
DROP TABLE IF EXISTS `w_email_log`;
CREATE TABLE `w_email_log`  (
  `emid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `uid` char(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ip` varchar(60) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `login_email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `send_email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `getter_email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `send_data` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`emid`) USING BTREE,
  INDEX `w_email_log_uid_w_users_uid`(`uid`) USING BTREE,
  CONSTRAINT `w_email_log_uid_w_users_uid` FOREIGN KEY (`uid`) REFERENCES `w_users` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for w_waflog
-- ----------------------------
DROP TABLE IF EXISTS `w_waflog`;
CREATE TABLE `w_waflog`  (
  `oeid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `uid` char(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ip` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0.0.0.0',
  `operate` int(11) NOT NULL,
  `detail` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`oeid`) USING BTREE,
  INDEX `w_waflog_uid_w_users`(`uid`) USING BTREE,
  CONSTRAINT `w_waflog_uid_w_users` FOREIGN KEY (`uid`) REFERENCES `w_users` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for w_rules_table
-- ----------------------------
DROP TABLE IF EXISTS `w_rules_table`;
CREATE TABLE `w_rules_table`  (
  `num` int(11) NOT NULL,
  `ptid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `tip` tinyint(4) NOT NULL DEFAULT 0,
  `nickname` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT 'None',
  `ptname` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'None',
  `explanation` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `width` varchar(7) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '50%',
  `height` varchar(7) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '50%',
  `code` int(11) NULL DEFAULT 404,
  `isrule` tinyint(4) NOT NULL DEFAULT 1,
  `isresp` tinyint(4) NOT NULL DEFAULT 1,
  PRIMARY KEY (`ptid`, `num`) USING BTREE,
  UNIQUE INDEX `w_rules_table_nickname_unique`(`nickname`) USING BTREE,
  INDEX `ptid`(`ptid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;



-- ----------------------------
-- Records of w_rules_table
-- ----------------------------
INSERT INTO `w_rules_table` VALUES (1, '417ac94f-b900-11ed-8b2c-0242ac110002', 0, 'cc', 'CC防御', 'CC攻击的原理就是攻击者控制某些主机不停地发大量数据包给对方服务器造成服务器资源耗尽，一直到宕机崩溃。', '800', '600', 400, 1, 1);
INSERT INTO `w_rules_table` VALUES (2, '417acc35-b900-11ed-8b2c-0242ac110002', 0, 'injection', '注入类型防御', '有效防御SQL注入、XSS等网络攻击，从数据包中过滤该类敏感词。', '0', '0', 403, 0, 0);
INSERT INTO `w_rules_table` VALUES (3, '417acd4a-b900-11ed-8b2c-0242ac110002', 0, 'form-data', 'form-data协议相关', 'form-data协议一般用于文件上传等操作，在针对该类数据包将进行单独的操作，这边会拦截form-data协议的不规范包', '0', '0', 403, 0, 1);
INSERT INTO `w_rules_table` VALUES (10, '417acdef-b900-11ed-8b2c-0242ac110002', 1, NULL, '0', '', '0', '0', NULL, 0, 0);
INSERT INTO `w_rules_table` VALUES (11, '417ace85-b900-11ed-8b2c-0242ac110002', 1, NULL, '0', '<strong><span style=\'font-size:17px\'>以下的内容在注入类型防御开启时将开启，可在此进行细节微调</span> ps:以下内容均可在“注入类型防御”的规则按钮中调节</strong>', '0', '0', NULL, 0, 0);
INSERT INTO `w_rules_table` VALUES (12, '417acf16-b900-11ed-8b2c-0242ac110002', 0, 'get', 'GET注入', '通过GET方式传入的参数可能存在问题，需要校验检查', '1200', '600', 403, 1, 1);
INSERT INTO `w_rules_table` VALUES (13, '417acf7f-b900-11ed-8b2c-0242ac110002', 0, 'post', 'POST注入', '通过POST方式传入的参数可能存在问题，需要校验检查', '1200', '600', 403, 1, 1);
INSERT INTO `w_rules_table` VALUES (14, '417acfe6-b900-11ed-8b2c-0242ac110002', 0, 'ua', 'User-Agent注入', '很多注入攻击来源于后端对User-Agent的处理，可疑的UA值是需要注意的。如业务需要，请单独设置规则，需要校验检查', '1200', '600', 403, 1, 1);
INSERT INTO `w_rules_table` VALUES (15, '417ad05a-b900-11ed-8b2c-0242ac110002', 0, 'cookie', 'Cookie注入', '大部分站点都会存在针对Cookie的处理，可疑的Cookie值是需要注意的。如业务需要，请单独设置规则，需要校验检查', '1200', '600', 403, 1, 1);
INSERT INTO `w_rules_table` VALUES (40, '417ad0bf-b900-11ed-8b2c-0242ac110002', 1, NULL, '0', '', '0', '0', NULL, 0, 0);
INSERT INTO `w_rules_table` VALUES (41, '417ad27a-b900-11ed-8b2c-0242ac110002', 1, NULL, '0', '<strong><span style=\'font-size:17px\'>以下内容优先级为最高，与上边的无关</span></strong>', '0', '0', NULL, 0, 0);
INSERT INTO `w_rules_table` VALUES (42, '417ad32d-b900-11ed-8b2c-0242ac110002', 0, 'ip-white', 'IP白名单', '设置后将不会对对应远程IP进行安全校验', '1000', '700', NULL, 1, 0);
INSERT INTO `w_rules_table` VALUES (43, '417ad395-b900-11ed-8b2c-0242ac110002', 0, 'ip-black', 'IP黑名单', '设置后将禁止对应IP访问被防护站点（未开启防护站点不受该项保护）', '1000', '700', 403, 1, 1);
INSERT INTO `w_rules_table` VALUES (44, '417ad3f8-b900-11ed-8b2c-0242ac110002', 0, 'url-white', 'URL白名单', '设置后对应URL将不受waf防护', '1000', '700', NULL, 1, 0);

-- ----------------------------
-- Table structure for w_web_info
-- ----------------------------
DROP TABLE IF EXISTS `w_web_info`;
CREATE TABLE `w_web_info`  (
  `wid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `host` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '127.0.0.1',
  `webname` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `iscdn` tinyint(4) NOT NULL DEFAULT 0,
  `total_switch` tinyint(4) NOT NULL DEFAULT 1,
  `switchs` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '1 1 1',
  PRIMARY KEY (`wid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for w_attack_types
-- ----------------------------
DROP TABLE IF EXISTS `w_attack_types`;
CREATE TABLE `w_attack_types`  (
  `atid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `atname` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `explanation` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `diy` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`atid`) USING BTREE,
  UNIQUE INDEX `w_attack_types_atname_unique`(`atname`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Records of w_attack_types
-- ----------------------------
INSERT INTO `w_attack_types` VALUES ('40a0c2c4-bcf0-11ed-8b2c-0242ac110002', 'UA异常', 'User-Agent 即用户代理，简称“UA”，它是一个特殊字符串头。网站服务器通过识别 “UA”来确定用户所使用的操作系统版本、CPU 类型、浏览器版本等信息。而网站服务器则通过判断 UA 来给客户端发送不同的页面。\n很多扫描器都有默认的自带的UA，这些UA和寻常的浏览器UA不同，通过这些特征，我们可以基本锁定扫描行为攻击内容并提前做出响应', NULL);
INSERT INTO `w_attack_types` VALUES ('6cc8809e-bcc4-11ed-8b2c-0242ac110002', 'SQL注入', 'SQL注入是一种利用Web应用程序中的安全漏洞，注入恶意的SQL语句来攻击数据库的攻击方式。攻击者可以通过修改应用程序的输入参数来执行恶意SQL语句，从而获取敏感信息或者篡改数据库数据。SQL注入通常是由于应用程序中没有对输入数据进行充分的验证和过滤而导致的。\r\n常见的SQL注入攻击方式包括基于错误的注入、时间盲注入和联合查询注入。基于错误的注入是通过构造错误的SQL语句来获取数据库信息，时间盲注入是根据应用程序的响应时间来判断SQL查询是否成功，联合查询注入是通过联合查询语句来获取数据库信息。\r\n防范SQL注入的方法包括对输入数据进行过滤和验证、使用参数化查询、限制数据库用户的权限和对数据库进行定期审计等。', NULL);
INSERT INTO `w_attack_types` VALUES ('6cc88380-bcc4-11ed-8b2c-0242ac110002', 'XSS攻击', 'XSS攻击是一种常见的网络安全攻击方式。XSS攻击的原理是攻击者通过在网页中插入恶意脚本，使得受害者在浏览网页时执行这些脚本，从而窃取敏感信息、劫持用户会话或者进行其他恶意操作。XSS攻击通常分为三种类型：反射型、存储型和DOM型。\r\n反射型XSS攻击是通过利用URL参数等向页面注入脚本，然后当受害者访问该页面时，脚本会被执行。存储型XSS攻击是将恶意脚本存储到服务器上的数据库或者文件中，当用户访问包含恶意脚本的页面时，脚本会被从服务器上加载并执行。DOM型XSS攻击是通过修改DOM文档对象模型来执行恶意脚本，从而窃取敏感信息或者劫持用户会话。XSS攻击常常会被利用来进行钓鱼攻击、窃取用户信息、篡改网页等行为，给用户和网站带来极大的损失。为了防止XSS攻击，网站开发人员可以使用输入验证、输出过滤、禁用脚本等方式来保护用户数据的安全。同时，用户也应该注意不要点击来路不明的链接，避免在不安全的网站上输入敏感信息。', NULL);
INSERT INTO `w_attack_types` VALUES ('6cc88460-bcc4-11ed-8b2c-0242ac110002', '目录扫描', '目录扫描是一种网络安全测试方法，用于检测目标网站或服务器上存在的目录和文件。目录扫描可以通过自动化工具或手动的方式进行。自动化工具可以高效地扫描目标网站或服务器上的所有目录和文件，同时还可以通过字典文件来枚举所有可能的目录和文件名。手动扫描需要耗费更多的时间，但可以更加精准地发现漏洞和弱点。目录扫描的目的是为了发现网站的弱点和漏洞，以便攻击者可以利用这些漏洞进行非法访问、控制或窃取敏感信息。攻击者可以利用目录扫描找到未经授权的页面、目录遍历漏洞、敏感文件等漏洞，从而实施更加精准的攻击行为。因此，开发人员和管理员应该定期进行目录扫描，及时发现和修复漏洞，以保障网站和服务器的安全。', NULL);
INSERT INTO `w_attack_types` VALUES ('6cc88530-bcc4-11ed-8b2c-0242ac110002', 'PHP流协议', 'PHP流协议是一种在PHP中使用的流式输入输出协议。它可以让PHP脚本像处理文件一样处理输入输出流。攻击者可以利用PHP流协议来执行远程PHP脚本或者读取本地文件等。\r\n常见的PHP流协议包括php://input、php://output、php://memory、php://temp等。php://input可以让PHP脚本读取来自HTTP请求的原始数据，php://output可以让PHP脚本输出数据到HTTP响应，php://memory和php://temp可以让PHP脚本在内存中创建临时文件。\r\n防范PHP流协议攻击的方法包括对PHP脚本的输入输出流进行过滤和验证、限制PHP脚本的执行权限和对PHP脚本进行定期审计等。', NULL);
INSERT INTO `w_attack_types` VALUES ('6cc885da-bcc4-11ed-8b2c-0242ac110002', 'PHP脚本执行', 'PHP脚本执行是一种利用Web应用程序中的安全漏洞，执行恶意PHP脚本来获取敏感信息或者篡改服务器的攻击方式。攻击者可以通过修改Web应用程序的输入参数或者上传恶意文件来执行恶意PHP脚本。\r\n常见的PHP脚本执行漏洞包括文件包含漏洞、代码注入漏洞和文件上传漏洞。文件包含漏洞是指Web应用程序未对包含文件进行过滤，导致攻击者可以通过构造恶意参数来执行恶意PHP脚本。代码注入漏洞是指Web应用程序未对用户输入的数据进行过滤，导致攻击者可以通过输入恶意代码来执行恶意PHP脚本。文件上传漏洞是指Web应用程序未对上传的文件进行过滤和验证，导致攻击者可以上传恶意文件并执行恶意PHP脚本。\r\n防范PHP脚本执行攻击的方法包括对用户输入数据进行过滤和验证、对文件上传进行严格的限制和验证、对文件包含进行过滤和验证等。', NULL);
INSERT INTO `w_attack_types` VALUES ('6cc886b5-bcc4-11ed-8b2c-0242ac110002', 'ThinkPHP相关问题', 'ThinkPHP是一种基于PHP的Web应用程序开发框架。由于其广泛的应用和开源特性，常常成为攻击者攻击的目标。常见的ThinkPHP相关问题包括ThinkPHP框架版本过低、路由配置不当、文件包含漏洞、SQL注入漏洞等。\r\nThinkPHP框架版本过低是指Web应用程序使用的ThinkPHP框架版本过旧，存在已经被修复的安全漏洞。路由配置不当是指Web应用程序在路由配置中存在安全漏洞，导致攻击者可以执行恶意操作。文件包含漏洞和SQL注入漏洞是指Web应用程序未对用户输入数据进行过滤和验证，导致攻击者可以执行恶意PHP脚本或者获取敏感信息。\r\n防范ThinkPHP相关问题的方法包括对ThinkPHP框架进行及时升级、对路由配置进行安全策略限制、对用户输入数据进行过滤和验证等。', NULL);
INSERT INTO `w_attack_types` VALUES ('6cc8875f-bcc4-11ed-8b2c-0242ac110002', '一句话木马', '一句话木马是一种常见的Web攻击方式，它利用Web服务器的漏洞，在服务器上植入恶意代码，从而控制服务器。攻击者可以通过一句话木马获取服务器上的敏感信息、修改网站内容、攻击其他网站等。\r\n举个例子，攻击者可以通过利用Web服务器上的漏洞，上传一个包含一句话木马的PHP文件。当用户访问这个PHP文件时，一句话木马会执行恶意代码，从而控制服务器。攻击者可以通过一句话木马执行各种操作，例如查看数据库中的用户信息、修改网站的源代码，甚至攻击其他网站。\r\n一句话木马的危害性非常大，因为它可以控制整个Web服务器，甚至整个网站。攻击者可以利用一句话木马窃取用户的账号密码、财务信息等敏感信息，从而达到非法牟利的目的。此外，一句话木马还可以被用来攻击其他网站，例如利用被攻击网站的服务器进行DDoS攻击。\r\n为了防范一句话木马攻击，网站管理员可以采取一些措施。例如，定期检查服务器上的漏洞，并及时修补；限制上传文件的类型和大小，避免上传恶意文件；限制Web服务器的权限，避免一句话木马控制整个服务器。此外，也可以使用防火墙、WAF等安全设备，对Web流量进行监控和过滤，从而防止一句话木马的攻击。', NULL);
INSERT INTO `w_attack_types` VALUES ('9c479efd-c8aa-11ed-a9ed-0242ac110003', '自定义规则', '该类型为用户自定义规则，平台内暂未收录，可参考文档对对应规则进行处理', 1);
INSERT INTO `w_attack_types` VALUES ('fc6d2885-bc9b-11ed-8b2c-0242ac110002', 'CC防御', 'CC攻击（英文全称：Distributed Denial of Service (DDoS) Attack）是指利用大量的计算机或者网络设备，对目标服务器发起大规模的连接请求，使得目标服务器无法正常响应合法用户的请求，从而导致服务拒绝，甚至瘫痪。CC攻击是当前网络安全领域中最常见的攻击手段之一，其目的通常是为了攻击某个网站，使其无法正常访问，达到敲诈勒索、报复、政治目的等不良目的。\r\nCC攻击常常采用分布式的方式，即利用大量的僵尸网络（Botnet）发起攻击，从而掩盖攻击者的真实身份和攻击来源。这些僵尸网络通常是由攻击者通过恶意软件感染用户的计算机或者设备，从而控制这些计算机或者设备的网络行为，使其成为攻击工具的一部分。这些僵尸网络可以组成一个庞大的网络，攻击者可以通过控制指挥节点（Command and Control，C&C）操控这些僵尸网络对目标服务器发起攻击。\r\nCC攻击对于目标服务器来说，可能造成严重的影响。一方面，它会导致大量的假请求占用服务器的资源，使得服务器无法正常处理合法用户的请求，从而导致服务瘫痪。另一方面，CC攻击也可能导致服务器的安全性受到威胁，例如攻击者可能利用CC攻击掩盖其他攻击行为，例如SQL注入、XSS攻击等，从而获取更多的攻击收益。\r\n为了应对CC攻击，目标服务器可以采取一些防御措施。例如，可以通过增加服务器的带宽和处理能力，增加服务器的抗压能力。同时，也可以通过使用防火墙、IDS/IPS等安全设备，对网络流量进行监控和过滤，从而阻止恶意流量的进入。此外，也可以使用CDN等分布式架构，将流量分散到多个节点上，从而降低单个节点的压力，提高整个系统的可靠性。', NULL);

-- ----------------------------
-- Table structure for w_funs
-- ----------------------------
DROP TABLE IF EXISTS `w_funs`;
CREATE TABLE `w_funs`  (
  `fid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ptid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `fun_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `explanation` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`fid`) USING BTREE,
  UNIQUE INDEX `w_funs_unique_fun_name`(`fun_name`) USING BTREE,
  INDEX `w_funs_ptid_w_rules_table_ptid`(`ptid`) USING BTREE,
  CONSTRAINT `w_funs_ptid_w_rules_table_ptid` FOREIGN KEY (`ptid`) REFERENCES `w_rules_table` (`ptid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Records of w_funs
-- ----------------------------
INSERT INTO `w_funs` VALUES ('09f7d9f9-bbfd-11ed-8b2c-0242ac110002', '417ac94f-b900-11ed-8b2c-0242ac110002', 'cc()', NULL);
INSERT INTO `w_funs` VALUES ('09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', 'post()', NULL);
INSERT INTO `w_funs` VALUES ('09f7dfbe-bbfd-11ed-8b2c-0242ac110002', '417acfe6-b900-11ed-8b2c-0242ac110002', 'ua()', NULL);
INSERT INTO `w_funs` VALUES ('09f7e146-bbfd-11ed-8b2c-0242ac110002', '417ad05a-b900-11ed-8b2c-0242ac110002', 'cookie()', NULL);
INSERT INTO `w_funs` VALUES ('0a20b32b-d54e-11ed-a9ed-0242ac110003', '417acd4a-b900-11ed-8b2c-0242ac110002', 'formdata()', NULL);
INSERT INTO `w_funs` VALUES ('72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', 'get()', NULL);


-- ----------------------------
-- Table structure for w_resps_info
-- ----------------------------
DROP TABLE IF EXISTS `w_resps_info`;
CREATE TABLE `w_resps_info`  (
  `ptid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `fid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `return_html` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`ptid`) USING BTREE,
  INDEX `fid_fid`(`fid`) USING BTREE,
  CONSTRAINT `fid_fid` FOREIGN KEY (`fid`) REFERENCES `w_funs` (`fid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `ptid_ptid` FOREIGN KEY (`ptid`) REFERENCES `w_rules_table` (`ptid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;


-- ----------------------------
-- Records of w_resps_info
-- ----------------------------
INSERT INTO `w_resps_info` VALUES ('417ac94f-b900-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '<!DOCTYPE html>\r\n<html lang=\"en\">\r\n\r\n<head>\r\n    <meta charset=\"UTF-8\">\r\n    <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\r\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\r\n    <title>Document</title>\r\n</head>\r\n\r\n<body>\r\n    <h1>触发了CC告警</h1>\r\n</body>\r\n\r\n</html>');
INSERT INTO `w_resps_info` VALUES ('417acf16-b900-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '<!DOCTYPE html>\n<html lang=\"en\">\n\n<head>\n    <meta charset=\"UTF-8\">\n    <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Document</title>\n</head>\n\n<body>\n    <h1>触发了GET告警</h1>\n\n你小子玩啥呢？\n\n</body>\n\n</html>');
INSERT INTO `w_resps_info` VALUES ('417acf7f-b900-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', 'post injection');
INSERT INTO `w_resps_info` VALUES ('417acfe6-b900-11ed-8b2c-0242ac110002', '09f7dfbe-bbfd-11ed-8b2c-0242ac110002', 'ua injection');
INSERT INTO `w_resps_info` VALUES ('417ad05a-b900-11ed-8b2c-0242ac110002', '09f7e146-bbfd-11ed-8b2c-0242ac110002', 'cookie injection');
INSERT INTO `w_resps_info` VALUES ('417ad395-b900-11ed-8b2c-0242ac110002', NULL, 'ip in ip-black');

-- ----------------------------
-- Table structure for w_rules_info
-- ----------------------------
DROP TABLE IF EXISTS `w_rules_info`;
CREATE TABLE `w_rules_info`  (
  `ruid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `fid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `ptid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `atid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `isalive` tinyint(4) NOT NULL DEFAULT 0,
  `content` varchar(355) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `explanation` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`ruid`) USING BTREE,
  INDEX `w_rules_info_ptid_w_rules_table_ptid`(`ptid`) USING BTREE,
  INDEX `w_rules_info_fid_w_funs_fid`(`fid`) USING BTREE,
  INDEX `w_rules_info_atid_w_attack_types`(`atid`) USING BTREE,
  CONSTRAINT `w_rules_info_atid_w_attack_types` FOREIGN KEY (`atid`) REFERENCES `w_attack_types` (`atid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `w_rules_info_fid_w_funs_fid` FOREIGN KEY (`fid`) REFERENCES `w_funs` (`fid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `w_rules_info_ptid_w_rules_table_ptid` FOREIGN KEY (`ptid`) REFERENCES `w_rules_table` (`ptid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;


-- ----------------------------
-- Records of w_rules_info
-- ----------------------------
INSERT INTO `w_rules_info` VALUES ('16d8e375-d462-11ed-a9ed-0242ac110003', NULL, '417ad395-b900-11ed-8b2c-0242ac110002', '9c479efd-c8aa-11ed-a9ed-0242ac110003', 0, '36.143.154.18', '测试用');
INSERT INTO `w_rules_info` VALUES ('2a616021-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc88460-bcc4-11ed-8b2c-0242ac110002', 1, '.(htaccess|mysql_history|bash_history|DS_Store|idea|user.ini)', 'POST相关--文件目录过滤1');
INSERT INTO `w_rules_info` VALUES ('2a61637d-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc88460-bcc4-11ed-8b2c-0242ac110002', 1, '.(bak|inc|old|mdb|sql|php~|swp|java|class)$', 'POST相关--文件目录过滤2');
INSERT INTO `w_rules_info` VALUES ('2a6164fb-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc88460-bcc4-11ed-8b2c-0242ac110002', 1, '^/(vhost|bbs|host|wwwroot|www|site|root|backup|data|ftp|db|admin|website|web).*.(rar|sql|zip|tar.gz|tar)$', 'POST相关--文件目录过滤3');
INSERT INTO `w_rules_info` VALUES ('2a61664e-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc885da-bcc4-11ed-8b2c-0242ac110002', 1, '/(hack|shell|spy|phpspy).php$', 'POST相关--PHP脚本执行过滤1');
INSERT INTO `w_rules_info` VALUES ('2a616798-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc885da-bcc4-11ed-8b2c-0242ac110002', 1, '^/(attachments|css|uploadfiles|static|forumdata|cache|avatar)/(w+).(php|jsp)$', 'POST相关--PHP脚本执行过滤2');
INSERT INTO `w_rules_info` VALUES ('2a6168da-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8875f-bcc4-11ed-8b2c-0242ac110002', 1, '(?:define|eval|file_get_contents|include|require|require_once|shell_exec|phpinfo|system|passthru|preg_w+|execute|echo|print|print_r|var_dump|(fp)open|alert|showmodaldialog)(', 'POST相关--一句话木马过滤1');
INSERT INTO `w_rules_info` VALUES ('34522877-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc88460-bcc4-11ed-8b2c-0242ac110002', 1, '../../', 'POST相关--目录保护1');
INSERT INTO `w_rules_info` VALUES ('34522cea-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc88460-bcc4-11ed-8b2c-0242ac110002', 1, '(?:etc/W*passwd)', 'POST相关--目录保护3');
INSERT INTO `w_rules_info` VALUES ('4fe521a2-c983-11ed-a9ed-0242ac110003', NULL, '417ad395-b900-11ed-8b2c-0242ac110002', '9c479efd-c8aa-11ed-a9ed-0242ac110003', 0, '1.1.1.2', 'wad');
INSERT INTO `w_rules_info` VALUES ('5243b9bb-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8875f-bcc4-11ed-8b2c-0242ac110002', 1, ':$', 'POST相关--一句话木马过滤1');
INSERT INTO `w_rules_info` VALUES ('5dc47ada-ca27-11ed-a9ed-0242ac110003', NULL, '417ad3f8-b900-11ed-8b2c-0242ac110002', '9c479efd-c8aa-11ed-a9ed-0242ac110003', 1, 'https://www.txk123.top', '爷的站');
INSERT INTO `w_rules_info` VALUES ('62dec68a-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8875f-bcc4-11ed-8b2c-0242ac110002', 1, '${', 'POST相关--一句话木马过滤2');
INSERT INTO `w_rules_info` VALUES ('62dec945-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8875f-bcc4-11ed-8b2c-0242ac110002', 1, '(invokefunction|call_user_func_array|\\think\\)', 'POST相关--ThinkPHP payload封堵');
INSERT INTO `w_rules_info` VALUES ('62decada-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8875f-bcc4-11ed-8b2c-0242ac110002', 1, 'base64_decode(', 'POST相关--一句话木马过滤3');
INSERT INTO `w_rules_info` VALUES ('6ad5729f-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8875f-bcc4-11ed-8b2c-0242ac110002', 1, '(?:define|eval|file_get_contents|include|require|require_once|shell_exec|phpinfo|system|passthru|char|chr|preg_w+|execute|echo|print|print_r|var_dump|(fp)open|alert|showmodaldialog)(', 'POST相关--一句话木马过滤4');
INSERT INTO `w_rules_info` VALUES ('7137422d-bcf0-11ed-8b2c-0242ac110002', '09f7dfbe-bbfd-11ed-8b2c-0242ac110002', '417acfe6-b900-11ed-8b2c-0242ac110002', '40a0c2c4-bcf0-11ed-8b2c-0242ac110002', 1, '(HTTrack|Apache-HttpClient|harvest|audit|dirbuster|pangolin|nmap|sqln|hydra|Parser|libwww|BBBike|sqlmap|w3af|owasp|Nikto|fimap|havij|zmeu|BabyKrokodil|netsparker|httperf| SF/)', 'User Agent相关内容，过滤关键字');
INSERT INTO `w_rules_info` VALUES ('9c663da1-bbc2-11ed-8b2c-0242ac110002', NULL, '417ad395-b900-11ed-8b2c-0242ac110002', NULL, 1, '1.46.89.46', '黑名单之一');
INSERT INTO `w_rules_info` VALUES ('9c664278-bbc2-11ed-8b2c-0242ac110002', NULL, '417ad395-b900-11ed-8b2c-0242ac110002', NULL, 1, '2.46.89.46', '黑名单之一');
INSERT INTO `w_rules_info` VALUES ('9c664371-bbc2-11ed-8b2c-0242ac110002', NULL, '417ad395-b900-11ed-8b2c-0242ac110002', NULL, 1, '1.46.89.6', '黑名单之一');
INSERT INTO `w_rules_info` VALUES ('9c6644b9-bbc2-11ed-8b2c-0242ac110002', NULL, '417ad32d-b900-11ed-8b2c-0242ac110002', NULL, 0, '89.46.89.66', '白名单之一a');
INSERT INTO `w_rules_info` VALUES ('9c6645ca-bbc2-11ed-8b2c-0242ac110002', NULL, '417ad32d-b900-11ed-8b2c-0242ac110002', NULL, 0, '9.46.89.66 1.1.1.1', '白名单之一');
INSERT INTO `w_rules_info` VALUES ('9c664708-bbc2-11ed-8b2c-0242ac110002', NULL, '417ad3f8-b900-11ed-8b2c-0242ac110002', NULL, 1, '89.46.49.46', 'URL白名单之一');
INSERT INTO `w_rules_info` VALUES ('9f0f1174-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8875f-bcc4-11ed-8b2c-0242ac110002', 1, '$_(GET|post|cookie|files|session|env|phplib|GLOBALS|SERVER)[', 'POST相关--一句话木马过滤5');
INSERT INTO `w_rules_info` VALUES ('a497a752-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, 's+(or|xor|and)s+.*(=|<|>|\'|\")', 'POST相关--SQL注入过滤1');
INSERT INTO `w_rules_info` VALUES ('a497aaa6-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, 'select.+(from|limit)', 'POST相关--SQL注入过滤2');
INSERT INTO `w_rules_info` VALUES ('a497ab98-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, '(?:(union(.*?)select))', 'POST相关--SQL注入过滤3');
INSERT INTO `w_rules_info` VALUES ('a497ac64-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, 'sleep((s*)(d*)(s*))', 'POST相关--SQL注入过滤4');
INSERT INTO `w_rules_info` VALUES ('a497ad26-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, 'benchmark((.*),(.*))', 'POST相关--SQL注入过滤5');
INSERT INTO `w_rules_info` VALUES ('a497ae6e-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, '(?:fromW+information_schemaW)', 'POST相关--SQL注入过滤6');
INSERT INTO `w_rules_info` VALUES ('a86daff9-bbc0-11ed-8b2c-0242ac110002', NULL, '417ad395-b900-11ed-8b2c-0242ac110002', NULL, 1, '89.46.89.46', '黑名单之一');
INSERT INTO `w_rules_info` VALUES ('a86db2cd-bbc0-11ed-8b2c-0242ac110002', NULL, '417ad32d-b900-11ed-8b2c-0242ac110002', NULL, 0, '89.46.89.188', '白名单之一');
INSERT INTO `w_rules_info` VALUES ('a86db54e-bbc0-11ed-8b2c-0242ac110002', NULL, '417ad3f8-b900-11ed-8b2c-0242ac110002', NULL, 1, 'https://baidu.com', 'URL白名单之一');
INSERT INTO `w_rules_info` VALUES ('af339f5b-ca39-11ed-a9ed-0242ac110003', '09f7dfbe-bbfd-11ed-8b2c-0242ac110002', '417acfe6-b900-11ed-8b2c-0242ac110002', '9c479efd-c8aa-11ed-a9ed-0242ac110003', 0, 'User-Agent测试', '测试');
INSERT INTO `w_rules_info` VALUES ('c1f3b026-b904-11ed-8b2c-0242ac110002', '09f7d9f9-bbfd-11ed-8b2c-0242ac110002', '417ac94f-b900-11ed-8b2c-0242ac110002', 'fc6d2885-bc9b-11ed-8b2c-0242ac110002', 1, '{\"cycle\": \"120\", \"rate\": \"200\", \"lock-time\": \"300\", \"tolerate-times\": \"3\"}', 'CC防御相关');
INSERT INTO `w_rules_info` VALUES ('cf92411d-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc88460-bcc4-11ed-8b2c-0242ac110002', 1, '.(htaccess|mysql_history|bash_history|DS_Store|idea|user.ini)', '文件目录过滤1');
INSERT INTO `w_rules_info` VALUES ('cf92441a-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc88460-bcc4-11ed-8b2c-0242ac110002', 1, '.(bak|inc|old|mdb|sql|php~|swp|java|class)$', '文件目录过滤2');
INSERT INTO `w_rules_info` VALUES ('cf924508-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc88460-bcc4-11ed-8b2c-0242ac110002', 1, '^/(vhost|bbs|host|wwwroot|www|site|root|backup|data|ftp|db|admin|website|web).*.(rar|sql|zip|tar.gz|tar)$', '文件目录过滤3');
INSERT INTO `w_rules_info` VALUES ('cf9246e1-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc885da-bcc4-11ed-8b2c-0242ac110002', 1, '/(hack|shell|spy|phpspy).php$', 'PHP脚本执行过滤1');
INSERT INTO `w_rules_info` VALUES ('cf924820-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc885da-bcc4-11ed-8b2c-0242ac110002', 1, '^/(attachments|css|uploadfiles|static|forumdata|cache|avatar)/(w+).(php|jsp)$', 'GET相关--PHP脚本执行过滤2');
INSERT INTO `w_rules_info` VALUES ('cf924969-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8875f-bcc4-11ed-8b2c-0242ac110002', 1, '(?:define|eval|file_get_contents|include|require|require_once|shell_exec|phpinfo|system|passthru|preg_w+|execute|echo|print|print_r|var_dump|(fp)open|alert|showmodaldialog)(', 'GET相关--一句话木马过滤1');
INSERT INTO `w_rules_info` VALUES ('cf924a8f-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc88460-bcc4-11ed-8b2c-0242ac110002', 0, '../../', 'GET相关--目录保护1');
INSERT INTO `w_rules_info` VALUES ('cf931432-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc88460-bcc4-11ed-8b2c-0242ac110002', 1, '(?:etc/W*passwd)', 'GET相关--目录保护3');
INSERT INTO `w_rules_info` VALUES ('cf931555-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc88530-bcc4-11ed-8b2c-0242ac110002', 1, '(gopher|doc|php|glob|^file|phar|zlib|ftp|ldap|dict|ogg|data):/', 'GET相关--PHP流协议过滤1');
INSERT INTO `w_rules_info` VALUES ('cf93161b-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8875f-bcc4-11ed-8b2c-0242ac110002', 1, ':$', 'GET相关--一句话木马过滤1');
INSERT INTO `w_rules_info` VALUES ('cf9316c8-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8875f-bcc4-11ed-8b2c-0242ac110002', 1, '${', 'GET相关--一句话木马过滤2');
INSERT INTO `w_rules_info` VALUES ('cf931777-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc886b5-bcc4-11ed-8b2c-0242ac110002', 1, '(invokefunction|call_user_func_array|\\think\\)', 'GET相关--ThinkPHP payload封堵');
INSERT INTO `w_rules_info` VALUES ('cf93181d-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8875f-bcc4-11ed-8b2c-0242ac110002', 1, 'base64_decode(', 'GET相关--一句话木马过滤3');
INSERT INTO `w_rules_info` VALUES ('cf9318d3-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8875f-bcc4-11ed-8b2c-0242ac110002', 1, '(?:define|eval|file_get_contents|include|require|require_once|shell_exec|phpinfo|system|passthru|char|chr|preg_w+|execute|echo|print|print_r|var_dump|(fp)open|alert|showmodaldialog)(', 'GET相关--一句话木马过滤4');
INSERT INTO `w_rules_info` VALUES ('cf93198f-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8875f-bcc4-11ed-8b2c-0242ac110002', 1, '$_(GET|post|cookie|files|session|env|phplib|GLOBALS|SERVER)[', 'GET相关--一句话木马过滤5');
INSERT INTO `w_rules_info` VALUES ('cf931a39-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, 's+(or|xor|and)s+.*(=|<|>|\'|\")', 'GET相关--SQL注入过滤1');
INSERT INTO `w_rules_info` VALUES ('cf931adb-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, 'select.+(from|limit)', 'GET相关--SQL注入过滤2');
INSERT INTO `w_rules_info` VALUES ('cf931b84-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, '(?:(union(.*?)select))', 'GET相关--SQL注入过滤3');
INSERT INTO `w_rules_info` VALUES ('cf931c2b-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, 'sleep((s*)(d*)(s*))', 'GET相关--SQL注入过滤4');
INSERT INTO `w_rules_info` VALUES ('cf931cd1-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, 'benchmark((.*),(.*))', 'GET相关--SQL注入过滤5');
INSERT INTO `w_rules_info` VALUES ('cf931d73-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, '(?:fromW+information_schemaW)', 'GET相关--SQL注入过滤6');
INSERT INTO `w_rules_info` VALUES ('cf931e19-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, '(?:(?:current_)user|database|schema|connection_id)s*(', 'GET相关--SQL注入过滤7');
INSERT INTO `w_rules_info` VALUES ('cf931ec2-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, 'into(s+)+(?:dump|out)files*', 'GET相关--SQL注入过滤8');
INSERT INTO `w_rules_info` VALUES ('cf931f64-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, 'groups+by.+(', 'GET相关--SQL注入过滤9');
INSERT INTO `w_rules_info` VALUES ('cf932009-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc88380-bcc4-11ed-8b2c-0242ac110002', 1, '<(iframe|script|body|img|layer|div|meta|style|base|object|input)', 'GET相关--XSS过滤1');
INSERT INTO `w_rules_info` VALUES ('cf9320ae-bcb4-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc88380-bcc4-11ed-8b2c-0242ac110002', 1, '(onmouseover|onerror|onload)=', 'GET相关--XSS过滤2');
INSERT INTO `w_rules_info` VALUES ('e03eac53-d9ac-11ed-9a44-0242ac110003', NULL, '417ad32d-b900-11ed-8b2c-0242ac110002', '9c479efd-c8aa-11ed-a9ed-0242ac110003', 1, '36.143.155.45', '我的地址');
INSERT INTO `w_rules_info` VALUES ('e4e0d405-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, '(?:(?:current_)user|database|schema|connection_id)s*(', 'POST相关--SQL注入过滤7');
INSERT INTO `w_rules_info` VALUES ('e4e0d719-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, 'into(s+)+(?:dump|out)files*', 'POST相关--SQL注入过滤8');
INSERT INTO `w_rules_info` VALUES ('e4e0d817-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, 'groups+by.+(', 'POST相关--SQL注入过滤9');
INSERT INTO `w_rules_info` VALUES ('e4e0d8f5-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc88380-bcc4-11ed-8b2c-0242ac110002', 1, '<(iframe|script|body|img|layer|div|meta|style|base|object|input)', 'POST相关--XSS过滤1');
INSERT INTO `w_rules_info` VALUES ('e4e0d9b7-bce8-11ed-8b2c-0242ac110002', '09f7ddb2-bbfd-11ed-8b2c-0242ac110002', '417acf7f-b900-11ed-8b2c-0242ac110002', '6cc88380-bcc4-11ed-8b2c-0242ac110002', 1, '(onmouseover|onerror|onload)=', 'POST相关--XSS过滤2');
INSERT INTO `w_rules_info` VALUES ('f3c8dea5-bd5a-11ed-8b2c-0242ac110002', '72def3d1-b992-11ed-8b2c-0242ac110002', '417acf16-b900-11ed-8b2c-0242ac110002', '6cc8809e-bcc4-11ed-8b2c-0242ac110002', 1, '(?:([or|and](.*?)1=1))', 'GET相关--SQL注入过滤10');
INSERT INTO `w_rules_info` VALUES ('fa7fbc66-bbef-11ed-8b2c-0242ac110002', NULL, '417ad32d-b900-11ed-8b2c-0242ac110002', NULL, 0, '183.197.73.234', '白名单之一');

-- ----------------------------
-- Table structure for w_attack_log
-- ----------------------------
DROP TABLE IF EXISTS `w_attack_log`;
CREATE TABLE `w_attack_log`  (
  `aeid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `remote_ip` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `atid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `isbans` tinyint(4) NOT NULL DEFAULT 0,
  `level` int(11) NOT NULL DEFAULT 4,
  `wid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `time_remain` int(11) NOT NULL DEFAULT 0,
  `fid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ruid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `http` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`aeid`) USING BTREE,
  INDEX `w_attack_log_aeid_normal`(`aeid`) USING BTREE,
  INDEX `w_attack_log_atid_w_attack_types_atid`(`atid`) USING BTREE,
  INDEX `w_attack_log_fid_w_func_fid`(`fid`) USING BTREE,
  INDEX `w_attack_log_ruid_w_rules_info`(`ruid`) USING BTREE,
  INDEX `w_attack_log_wid_w_web_info_wid`(`wid`) USING BTREE,
  CONSTRAINT `w_attack_log_atid_w_attack_types_atid` FOREIGN KEY (`atid`) REFERENCES `w_attack_types` (`atid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `w_attack_log_fid_w_func_fid` FOREIGN KEY (`fid`) REFERENCES `w_funs` (`fid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `w_attack_log_ruid_w_rules_info` FOREIGN KEY (`ruid`) REFERENCES `w_rules_info` (`ruid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `w_attack_log_wid_w_web_info_wid` FOREIGN KEY (`wid`) REFERENCES `w_web_info` (`wid`) ON DELETE SET NULL ON UPDATE NO ACTION
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for w_auto_ip_bans
-- ----------------------------
DROP TABLE IF EXISTS `w_auto_ip_bans`;
CREATE TABLE `w_auto_ip_bans`  (
  `ieid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `aeid` char(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `lock_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `unlock_time` datetime NULL DEFAULT NULL,
  `lock_reason` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `ipaddress` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`ieid`) USING BTREE,
  INDEX `w_auto_ip_bans_aeid_w_attack_log_aeid`(`aeid`) USING BTREE,
  CONSTRAINT `w_auto_ip_bans_aeid_w_attack_log_aeid` FOREIGN KEY (`aeid`) REFERENCES `w_attack_log` (`aeid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;



-- --------------------------
-- Triggers structure for table w_attack_log
-- ----------------------------
DROP TRIGGER IF EXISTS `w_attack_log_before_insert_aeid`;
delimiter ;;
CREATE TRIGGER `w_attack_log_before_insert_aeid` BEFORE INSERT ON `w_attack_log` FOR EACH ROW BEGIN
IF new.aeid is NULL THEN
		SET new.aeid = UUID();
END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table w_attack_log
-- ----------------------------
DROP TRIGGER IF EXISTS `w_attack_log_after_insert_aeid`;
delimiter ;;
CREATE TRIGGER `w_attack_log_after_insert_aeid` AFTER INSERT ON `w_attack_log` FOR EACH ROW BEGIN
IF new.isbans = 1 THEN
	IF new.time_remain = 0 THEN
		INSERT INTO `w_auto_ip_bans` (`aeid`,`unlock_time`,`lock_time`,`lock_reason`,`ipaddress`) VALUES (new.aeid,ADDDATE(NOW(),INTERVAL 1000 YEAR),NOW(),'',new.remote_ip);
	ELSE
		INSERT INTO `w_auto_ip_bans` (`aeid`,`unlock_time`,`lock_time`,`lock_reason`,`ipaddress`) VALUES (new.aeid,ADDDATE(NOW(),INTERVAL new.time_remain/60 MINUTE),NOW(),'',new.remote_ip);
	END IF;
END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table w_attack_types
-- ----------------------------
DROP TRIGGER IF EXISTS `w_attack_types_before_insert`;
delimiter ;;
CREATE TRIGGER `w_attack_types_before_insert` BEFORE INSERT ON `w_attack_types` FOR EACH ROW BEGIN
IF new.atid is NULL THEN
		SET new.atid = UUID();
END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table w_auto_ip_bans
-- ----------------------------
DROP TRIGGER IF EXISTS `w_auto_ip_bans_before_insert_ieid`;
delimiter ;;
CREATE TRIGGER `w_auto_ip_bans_before_insert_ieid` BEFORE INSERT ON `w_auto_ip_bans` FOR EACH ROW BEGIN
IF new.ieid is NULL THEN
		SET new.ieid = UUID();
END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table w_email_log
-- ----------------------------
DROP TRIGGER IF EXISTS `w_ematil_log_emid_before_insert`;
delimiter ;;
CREATE TRIGGER `w_ematil_log_emid_before_insert` BEFORE INSERT ON `w_email_log` FOR EACH ROW BEGIN
IF new.emid is NULL THEN
		SET new.emid = UUID();
END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table w_funs
-- ----------------------------
DROP TRIGGER IF EXISTS `w_funs_before_insert_fid`;
delimiter ;;
CREATE TRIGGER `w_funs_before_insert_fid` BEFORE INSERT ON `w_funs` FOR EACH ROW IF new.fid is NULL THEN
		SET new.fid = UUID();
END IF
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table w_rules_info
-- ----------------------------
DROP TRIGGER IF EXISTS `w_rules_info_before_insert`;
delimiter ;;
CREATE TRIGGER `w_rules_info_before_insert` BEFORE INSERT ON `w_rules_info` FOR EACH ROW BEGIN
IF new.ruid is NULL THEN
		SET new.ruid = UUID();
END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table w_rules_table
-- ----------------------------
DROP TRIGGER IF EXISTS `w_rules_table_before_insert`;
delimiter ;;
CREATE TRIGGER `w_rules_table_before_insert` BEFORE INSERT ON `w_rules_table` FOR EACH ROW BEGIN
IF new.ptid is NULL THEN
		SET new.ptid = UUID();
END IF;
IF new.nickname is NULL THEN
		SET new.nickname = SUBSTR(CONCAT('None',RAND()),1,10);
END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table w_users
-- ----------------------------
DROP TRIGGER IF EXISTS `w_users_before_insert`;
delimiter ;;
CREATE TRIGGER `w_users_before_insert` BEFORE INSERT ON `w_users` FOR EACH ROW BEGIN
IF new.uid is NULL THEN
		SET new.uid = SHA2(CONCAT(UUID(),UNIX_TIMESTAMP(NOW()),UUID()),256);
END IF; 
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table w_waflog
-- ----------------------------
DROP TRIGGER IF EXISTS `w_waflog_before_insert`;
delimiter ;;
CREATE TRIGGER `w_waflog_before_insert` BEFORE INSERT ON `w_waflog` FOR EACH ROW BEGIN
IF new.oeid is NULL THEN
		SET new.oeid = UUID();
END IF; 
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table w_web_info
-- ----------------------------
DROP TRIGGER IF EXISTS `w_web_info_before_insert`;
delimiter ;;
CREATE TRIGGER `w_web_info_before_insert` BEFORE INSERT ON `w_web_info` FOR EACH ROW BEGIN
IF new.wid is NULL THEN
		SET new.wid = UUID();
END IF; 
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;

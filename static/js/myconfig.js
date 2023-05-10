const protocol = "https";		// API接口所使用的协议类型（建议设置为https）
const api_host ="api.xlsec.com";	// API接口使用的域名

/////////////////////
/* 以下内容请勿乱动 */
/////////////////////
/* 通用 */
const url = protocol + "://" + api_host;
const url_webinfo_name = url + "/web-info/name/get/";
const url_webinfo_del = url + "/web-del/wid/del/";
const url_get_username = url + "/info/get/username/";

/* 用户记录相关 */
const verify_code_url = url + "/login/get-verify-code/130,65/4";
const get_salt_url = url + "/login/get-salt/";
const login_url = url + "/login";
const url_admin = url + "/user-info/getinfo";
const url_change_passwd = url + "/user-info/change-passwd/";
const url_change_passwd_get_salt = url + "/user-info/change-passwd/get/salt/";
const url_change_passwd_checkold = url + "/user-info/change-passwd/check/old/";
const url_change_passwd_update = url + "/user-info/change-passwd/end/update/";
const url_change_passwd_send_email = url + "/user-info/change-passwd/email/send/";
const url_change_passwd_check_email = url + "/user-info/change-passwd/email/check/";

/* 首页（第一个界面） */
const url_home_welcome = url + "/total/showing/";
const url_nearly_interceptor = url + "/nearly/info/interceptor/";
const url_total_report = url + "/total/reporting/";
const url_total_counting = url + "/total/counting/";

/*第二个界面的*/
// 开关相关
const url_total_switch = url + "/switches/";
const url_webs_switch = url + "/switches/webs/";
const url_webs_info = url + "/switches/webs/info";
const url_types_switch_get = url + "/switches/type/get/";
const url_types_switch_set = url + "/switches/type/set/";
// 规则配置相关
const url_rules_table = url + "/rules/table/list/";
const url_rules_table_info_size = url + "/rules/table/info/getsize/";
const url_rules_table_info_static_html = url + "/rules/table/info/html/";
const url_rules_table_info_cc_setting = url + "/rules/table/cc/";
const url_rules_table_injections_get_settings = url + "/rules/table/others/gets/";//实际使用后边加上get、ua等，/rules/table/others/gets/get
const url_rules_table_injections_set_settings = url + "/rules/table/others/sets/";//实际使用后边加上get、ua等，/rules/table/others/sets/get
const url_rules_table_injections_new_settings = url + "/rules/table/others/news/";//实际使用后边加上get、ua等，/rules/table/others/news/get
const url_rules_table_injections_del_settings = url + "/rules/table/others/dels/";//实际使用后边加上get、ua等，/rules/table/others/dels/get
const url_rules_table_ipslist_get_settings = url + "/rules/table/iplist/gets/";//实际使用后边加上get、ua等，/rules/table/iplist/gets/ip-white
const url_rules_table_ipslist_set_settings = url + "/rules/table/iplist/sets/";//实际使用后边加上get、ua等，/rules/table/iplist/sets/ip-white
const url_rules_table_ipslist_new_settings = url + "/rules/table/iplist/news/";//实际使用后边加上get、ua等，/rules/table/iplist/news/ip-white
const url_rules_table_ipslist_del_settings = url + "/rules/table/iplist/dels/";//实际使用后边加上get、ua等，/rules/table/iplist/dels/ip-white
const url_resps_table_html = url + "/resps/table/html/";//实际使用后边加上get、ua等，/resps/table/html/get
const url_rules_uploader = url + "/rules/uploader/";

/* 日志记录相关（第三个界面）*/
const url_attack_table_logs = url + "/attack/logs";
const url_attack_log_del = url + "/web-info/logs/del/";
const url_get_log_http = url + "/web-info/logs/get/";
const url_ip_bans_ip_black = url + "/ip-bans/logs/to-black";
const url_ip_bans_ip_un_black = url + "/ip-bans/logs/to-un-black/";
const url_ip_bans_table_logs = url + "/ip-bans/logs/";
const url_ip_bans_table_info_demo = url + "/ip-bans/logs/info/?";
const url_waf_operate_log = url + "/waf-operate/logs/get/";
const url_waf_operate_log_del = url + "/waf-operate/logs/del/";
const url_logging_download = url + "/waf-logging/download/";

/* 系统配置相关（第四个界面） */
const url_system_checking_itself = url + "/sys/check/itself/";
const url_system_dns_getting = url + "/sys/dns/setting/get/";
const url_system_dns_setting = url + "/sys/dns/setting/set/";
const url_system_hosts_getting = url + "/sys/hosts/setting/get/";
const url_system_hosts_setting = url + "/sys/hosts/setting/set/";


/* 一些死变量 */
const events_type = ['total', 'cc', 'injection', 'form-data'];
const access_type = ['txt', 'jpg'];
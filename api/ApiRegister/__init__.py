from ApiRegister.CommonApi.Web_Info import API_web_info
from ApiRegister.CommonApi.FunInterceptor import API_funs_interceptor
from ApiRegister.CommonApi.GetUserName import API_User_Name
from ApiRegister.A_Moudles.Login import API_login
from ApiRegister.A_Moudles.Logout import API_logout
from ApiRegister.A_Moudles.User_Info.UserInfo import API_getinfo
from ApiRegister.A_Moudles.User_Info.ChangePasswd import API_change_passwd
from ApiRegister.A_Moudles.TotalShowing.IndexWelcome import API_total_showing
from ApiRegister.A_Moudles.TotalShowing.IndexReporting import API_total_reporting
from ApiRegister.A_Moudles.TotalShowing.IndexCounting import API_total_counting
from ApiRegister.A_Moudles.LogManager.AttackCheck import API_attack_check
from ApiRegister.A_Moudles.LogManager.AutoIPBans import API_attack_ip_bans
from ApiRegister.A_Moudles.LogManager.WafLogBak import API_waf_log_bak
from ApiRegister.A_Moudles.LogManager.LogDownload import API_log_download
from ApiRegister.A_Moudles.SystemConfig.SwitchOfTotal import API_total_switch
from ApiRegister.A_Moudles.SystemConfig.SwitchOfWebs import API_webs_switch
from ApiRegister.A_Moudles.SystemConfig.SwitchOfTypes import API_types_switch
from ApiRegister.A_Moudles.SystemConfig.RulesTables import API_rules_tables
from ApiRegister.A_Moudles.SystemConfig.RulesUploader import API_rules_uploader
from ApiRegister.A_Moudles.SystemConfig.MiscSetting import API_misc_settings
from ApiRegister.A_Moudles.WafConfig.CheckItself import API_check_itself
from ApiRegister.A_Moudles.WafConfig.NetConfig.DnsSetting import API_check_dns
from ApiRegister.A_Moudles.WafConfig.NetConfig.HostsSetting import API_check_hosts


def get_api_list():
    return [
        API_web_info,
        API_funs_interceptor,
        API_User_Name,
        API_login,
        API_logout,
        API_getinfo,
        API_change_passwd,
        API_total_showing,
        API_total_reporting,
        API_total_counting,
        API_attack_check,
        API_attack_ip_bans,
        API_waf_log_bak,
        API_log_download,
        API_total_switch,
        API_webs_switch,
        API_types_switch,
        API_rules_tables,
        API_rules_uploader,
        API_misc_settings,
        API_check_itself,
        API_check_dns,
        API_check_hosts
    ]

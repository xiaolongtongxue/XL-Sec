def Get_Menu():
    return {
        "homeInfo": {
            "title": "首页",
            "href": "page/information-showing/total-show/total-showing.html"
        },
        "logoInfo": {
            "title": '<a href="javascript:;" id="title-t"><img src="/favicon.ico" alt="logo"><h1>XL-SEC</h1></a>',
            "image": "",
            "href": ""
        },
        "menuInfo": [
            {
                "title": "信息统计",
                "href": "page/information-showing/",
                "target": "_self",
                "child": [
                    {
                        "title": "防护状态概览",
                        "href": "page/information-showing/total-show/total-showing.html",
                        "icon": "fa fa-home",
                        "target": "_self"
                    },
                    {
                        "title": "报告生成",
                        "href": "page/information-showing/report.html",
                        "icon": "fa fa-bar-chart",
                        "target": "_self"
                    },
                    # {
                    #     "title": "实时监控",
                    #     "href": "page/information-showing/total-show/newly-showing.html",
                    #     "icon": "fa fa-suitcase",
                    #     "target": "_self"
                    # },
                    {
                        "title": "攻击检测统计",
                        "href": "page/information-showing/couting.html",
                        "icon": "fa fa-dashcube",
                        "target": "_self"
                    }
                ]
            },
            {
                "title": "网站防护",
                "href": "",
                "target": "_self",
                "child": [
                    {
                        "title": "总开关",
                        "icon": "fa fa-motorcycle",
                        "href": "page/waf-check/switch/total-switch.html",
                        "target": "_self"
                    },
                    {
                        "title": "网站开关",
                        "icon": "fa fa-bicycle",
                        "href": "page/waf-check/switch/webs-switch.html",
                        "target": "_self"
                    },
                    {
                        "title": "防护类型开关",
                        "icon": "fa fa-circle-thin",
                        "href": "page/waf-check/switch/events-switch.html",
                        "target": "_self"
                    },
                    {
                        "title": "防护说明",
                        "icon": "fa fa-wheelchair",
                        "href": "page/waf-check/explanation.html",
                        "target": "_self"
                    },
                    {
                        "title": "规则配置",
                        "icon": "fa fa-forumbee",
                        "href": "page/waf-check/rules.html",
                        "target": "_self"
                    },
                    # {
                    #     "title": "规则包上传",
                    #     "icon": "fa fa-empire",
                    #     "href": "page/waf-check/rules-upload.html",
                    #     "target": "_self"
                    # }
                ]
            },
            {
                "title": "日志管理",
                "href": "",
                "target": "_self",
                "child": [
                    {
                        "title": "攻击检测日志",
                        "icon": "fa fa-umbrella",
                        "href": "page/log-manager/attack-log.html",
                        "target": "_self"
                    },
                    {
                        "title": "IP封禁日志",
                        "icon": "fa fa-times",
                        "href": "page/log-manager/ip-bans.html",
                        "target": "_self"
                    },
                    {
                        "title": "WAF 操作日志",
                        "icon": " fa fa-key",
                        "href": "page/log-manager/waf-log.html",
                        "target": "_self"
                    },
                    {
                        "title": "日志归档下载",
                        "icon": "fa fa-file-text",
                        "href": "page/log-manager/logs-download.html",
                        "target": "_self"
                    }
                ]
            },
            {
                "title": "系统配置",
                "href": "",
                "target": "_self",
                "child": [
                    # {
                    #     "title": "网络接口配置",
                    #     "href": "",
                    #     "icon": "fa fa-building",
                    #     "target": "_self",
                    #     "child": [
                    #         {
                    #             "title": "网卡相关信息",
                    #             "href": "page/t-setting/a",
                    #             "icon": "fa fa-signal",
                    #             "target": "_self"
                    #         },
                    #         {
                    #             "title": "部署模式选择",
                    #             "href": "page/t-setting/b",
                    #             "icon": "fa fa-globe",
                    #             "target": "_self"
                    #         }
                    #     ]
                    # },
                    {
                        "title": "相关组件信息",
                        "href": "",
                        "icon": " fa fa-desktop",
                        "target": "_self",
                        "child": [
                            # {
                            #     "title": "MySQL配置",
                            #     "href": "page/t-setting/units/mysql-setting.html",
                            #     "icon": "fa fa-database",
                            #     "target": "_self"
                            # },
                            # {
                            #     "title": "Redis配置",
                            #     "href": "page/t-setting/units/redis-setting.html",
                            #     "icon": "fa fa-server",
                            #     "target": "_self"
                            # },
                            {
                                "title": "DNS配置",
                                "href": "page/t-setting/units/dns-setting.html",
                                "icon": "fa fa-pencil",
                                "target": "_self"
                            }, {
                                "title": "HOST配置",
                                "href": "page/t-setting/units/host-setting.html",
                                "icon": "fa fa-mobile",
                                "target": "_self"
                            }
                        ]
                    },
                    {
                        "title": "网络工具",
                        "href": "page/t-setting/internet-tools.html",
                        "icon": "fa fa-inbox",
                        "target": "_self"
                    },
                    {
                        "title": "<strong>配置注意事项</strong>",
                        "href": "page/warning.html",
                        "icon": "fa fa-warning",
                        "target": "_self"
                    },
                    {
                        "title": "关于",
                        "href": "page/about.html",
                        "icon": "fa fa-info",
                        "target": "_self"
                    }
                ]
            }
        ]
    }

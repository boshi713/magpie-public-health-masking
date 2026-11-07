"""Generate synthetic-only public health masking rules and examples."""
import json
from pathlib import Path
P = Path(__file__).resolve().parent
rules, cases, descriptions = [], [], []
def add(kind, regex, text, value, desc):
    rules.append(dict(kind=kind, regex=regex))
    cases.append(dict(kind=kind, text=text, value=value))
    descriptions.append((kind,desc))
# Captured value excludes prose and common JSON/CSV/Markdown separators.
sep = r'''["'”’]?[ \t]*[:：=][ \t]*["'“‘]?'''
value = r'''([^\r\n\t,，;；。|"'“”‘’<>\[\]{}]{1,100})'''
def field(kind, labels, text, val, desc):
    add(kind, '(?i)(?:'+labels+')'+sep+value, text, val, desc)
field('PH_NAME','姓名|患者姓名|联系人|监护人|调查员|签名|patient_name|full_name','患者姓名：林晓岚；发热','林晓岚','带字段标签的姓名、联系人、调查员；短英文姓名不足4字节由模型或词表补充')
field('PH_ID','身份证号?|证件号|护照号|通行证号|id_number|passport','证件号：TEST998877；','TEST998877','带标签证件号码；不依赖校验码')
field('PH_CONTACT','电话|手机|联系方式|微信号?|QQ号?|contact|phone','联系方式：0571-12345678；','0571-12345678','带标签联系电话及社交账号')
field('PH_CASE','报告卡号|病例编号|个案编号|传报卡号|case_id|report_id','报告卡号：CDC-TEST-0098；','CDC-TEST-0098','传染病报告与个案追踪编号')
field('PH_MEDICAL','病案号|住院号|门诊号|就诊卡号|医保号|patient_id|medical_record','病案号：MR-TEST-001；','MR-TEST-001','医疗业务编号')
field('PH_SAMPLE','标本号|样本号|送检编号|检验编号|条码号|sample_id|specimen_id','标本号：LAB-TEST-008；','LAB-TEST-008','样本、送检与条码编号')
field('PH_ADDRESS','现住址|户籍地址|家庭住址|详细地址|居住地|地址|address','现住址：虚构市示例路88号3栋502室；','虚构市示例路88号3栋502室','带标签地址；空格分段地址需模型及词表补充')
field('PH_ORG','工作单位|就读学校|单位名称|学校名称|就诊医院|隔离点|employer','工作单位：虚构市示例食品公司；','虚构市示例食品公司','工作、学校、医院、隔离点名称')
field('PH_ROOM','班级|宿舍|床位号?|病房号?|门牌号|房间号|座位号','班级：二年级三班；','二年级三班','细粒度班级、宿舍、床位与座位')
field('PH_TRANSPORT','车牌号?|航班号?|车次|船名|座号|flight_no','航班号：ZZ9999；','ZZ9999','交通与行程标识')
field('PH_COORD','经度|纬度|坐标|longitude|latitude|gps','经度：120.123456；','120.123456','带标签精确坐标；坐标对另有规则')
field('PH_ACCOUNT','账号|账户|银行卡号|银行账号|account_no','账号：TEST-ACCOUNT-987；','TEST-ACCOUNT-987','账户与银行卡字段')
field('PH_SECRET','密码|口令|密钥|令牌|访问凭证','密码：DEMO_PASSWORD_NOT_REAL；','DEMO_PASSWORD_NOT_REAL','中文凭证字段，补充内置密钥识别')
field('PH_DEMOGRAPHIC','年龄|出生日期|生日|民族|职业|职务|age|occupation','职业：示例精密仪器工程师；','示例精密仪器工程师','严格遮盖准标识字段；会丢失年龄职业分析价值')
field('PH_EVENT','疫情编号|事件编号|聚集性疫情编号|密接编号|contact_id','事件编号：EVENT-TEST-88；','EVENT-TEST-88','事件和密接追踪编号')
add('PH_MOBILE',r'(?:^|[^0-9])(1[3-9][0-9][ -]?[0-9]{4}[ -]?[0-9]{4})(?:$|[^0-9])','电话 139 0000 1234。','139 0000 1234','大陆手机号含空格短横线；相邻多个号码需实际验证')
add('PH_LANDLINE',r'(?:^|[^0-9])(0[0-9]{2,3}[ -][0-9]{7,8}(?:[-转][0-9]{1,6})?)(?:$|[^0-9])','致电 0571-12345678。','0571-12345678','有区号分隔符的固定电话')
add('PH_ID_SHAPE',r'(?i)(?:^|[^0-9A-Za-z])([1-9][0-9]{16}[0-9X]|[1-9][0-9]{14})(?:$|[^0-9A-Za-z])','证件 110101199001010019。','110101199001010019','15/18位形状兜底，不校验；可能遮住订单等长编号')
add('PH_DATE',r'((?:19|20)[0-9]{2}[-/.年][0-9]{1,2}[-/.月][0-9]{1,2}日?)','发病于2026年11月3日。','2026年11月3日','完整日历日期；年份限定1900—2099，不涵盖中文数字写法')
add('PH_MONTHDAY',r'([0-9]{1,2}月[0-9]{1,2}[日号])','于11月3日采样','11月3日','无年份月日，严格模式会损失疫情时间信息')
add('PH_TIME',r'([0-2]?[0-9][:：][0-5][0-9](?:[:：][0-5][0-9])?|[0-2]?[0-9]时[0-5]?[0-9]分)','于14:32采样','14:32','精确钟点；不做时间平移')
add('PH_AGE_TEXT',r'([0-9]{1,3}(?:周岁|岁|月龄|日龄))','患者37岁，发热','37岁','正文年龄；保留体温、Ct、检验值')
add('PH_LOCATION_TEXT',r'([\p{Han}]{2,18}(?:省|市|县|区|镇|乡|街道|社区|村|小区)(?:[\p{Han}A-Za-z0-9-]{0,32}(?:路|街|巷|号|栋|幢|单元|室))?)','到访虚构市示例区。','到访虚构市示例区','正文中文地名，宽匹配可能连带普通文字；复杂地址仍需模型')
add('PH_ORG_TEXT',r'([\p{Han}A-Za-z0-9]{2,32}(?:医院|卫生院|卫生服务中心|小学|中学|幼儿园|大学|有限公司|酒店|农贸市场))','虚构星河小学发生疫情','虚构星河小学','正文机构名，可能误遮普通机构类别描述')
add('PH_ROOM_TEXT',r'([A-Za-z0-9一二三四五六七八九十]{1,8}(?:号楼|栋|幢|单元|号房|室|年级|班))','居住3栋502室。','502室','正文楼栋房间班级；逐段识别')
add('PH_PLATE',r'([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼][A-Z][A-Z0-9]{5,6})','车辆浙A12345进入现场','浙A12345','常见民用车牌；不覆盖所有特殊牌照')
add('PH_NETWORK',r'(?i)((?:https?://)[^\s<>"，；。]+|(?:[0-9]{1,3}\.){3}[0-9]{1,3})','内网 10.20.30.40。','10.20.30.40','所有HTTP链接与IPv4；也会遮住公开文献链接')
add('PH_COORD_PAIR',r'([-+]?[0-9]{1,3}\.[0-9]{4,}[,，][ \t]*[-+]?[0-9]{1,3}\.[0-9]{4,})','位置120.123456,30.123456','120.123456,30.123456','高精度经纬度对；不覆盖全部坐标编码')
patch={'redact':True,'redactPersonal':True,'redactModel':True,'redactModelOff':False,'redactWordsAnyCase':True,'redactRules':rules}
(P/'strict-settings.patch.json').write_text(json.dumps(patch,ensure_ascii=False,indent=2)+'\n')
(P/'synthetic-tests.json').write_text(json.dumps({'positive':cases,'negative':['体温38.5℃，Ct值23.4，白细胞6.5×10^9/L。','发热、咳嗽，核酸阳性，潜伏期3天。','病例P001与P002有同餐史；D0发病，D2隔离。']},ensure_ascii=False,indent=2)+'\n')
rows=['# 规则明细\n','共28条，余4个自定义名额。每条规则见配置的 regex 字段。下列样例全为虚构。\n','|类型|用途及局限|测试输入|预期命中值|','|---|---|---|---|']
for (k,d),c in zip(descriptions,cases): rows.append(f'|{k}|{d}|{c["text"]}|{c["value"]}|')
(P/'规则明细.md').write_text('\n'.join(rows)+'\n')
print(f'Generated {len(rules)} rules; max regex UTF-8 bytes: {max(len(r["regex"].encode()) for r in rules)}')

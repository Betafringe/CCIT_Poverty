# 精准扶贫信用评估模型

## 任务目标：

==1.专家智能匹配==

==2.金融信用评估 输入：用户 ID 输出：用户信用评分 详细展示重点数据 形成个人信用评估表==

### 2018年03月20日10:40:14

传统有：专家系统，信用评级系统，信用评分系统

初步确定可用的数据项有：

`per_num. land year, land size, salse_income,helper, help_industry, industry_scale `

``Data columns (total 39 columns):``
``id                  3000 non-null int64``
``householder_name    3000 non-null object``
``per_num             3000 non-null int64``
``year                3000 non-null object``
``ID_card             3000 non-null object``
``level               3000 non-null object``
``breed_year          0 non-null float64``
``equip_breed         0 non-null float64``
``land_year           0 non-null float64``
``land_size           0 non-null float64``
``channel             0 non-null float64``
``channel_num         0 non-null float64``
``sale_income         0 non-null float64``
``address             3000 non-null object``
``city_id             3000 non-null float64``
``city                3000 non-null object``
``county_id           3000 non-null float64``
``county              3000 non-null object``
``town_id             3000 non-null float64``
``town                3000 non-null object``
``village_id          3000 non-null float64``
``village_name        3000 non-null object``
``phone_num           0 non-null float64``
``helper              432 non-null object``
``helper_unit         439 non-null object``
``helper_number       427 non-null float64``
``plan_time           873 non-null object``
``help_industry       567 non-null object``
``industrial_scale    296 non-null object``
``tech_project        174 non-null object``
``income              3000 non-null float64``
``real_time           1 non-null object``
``out_poverty         3000 non-null object``
``input_user          17 non-null float64``
``input_time          17 non-null object``
``check_status        3000 non-null int64``
``status              3000 non-null int64``
``city_recorder       0 non-null float64``
``county_recorder     0 non-null float64``

## 5C 评价：

 品德声望Character ，资格能力Capacity，资金实力Capital or cash，担保人Collateral，经营条件Condition

1. 自然情况（年龄，性别，婚姻状况，健康状况，文化程度 ，住宅类型）
2. 职业情况（职业，工作年限，职务，年收入）
3. 家庭情况（人均月收入，家庭债务收入比例）
4. 与银行往来关系

信用评分根据不同的场景和数据源也会有所侧重，如常见的几种评分系统就采用如下类型的数据来评价申请人的信用。

FICO：偿还历史（35%）信用账户数（30%）使用信用的年限（15%）新开立的信用账户（10%）正在使用的信用类型（10%）。

浦发信用评分：履约能力、社交活动、行为偏好、我行关系、信息齐全。

### 经验分析法（David Durand）

1. 年龄， 超过20岁后，每年为0.01，最大值为0.3
2. 性别，女性为0.4，男性0
3. 居住地稳定性，在当前每住一年为0.16
4. 职业，风险小职业为0.55，风险大为0，其他为0.16
5. 行业
6. 拥有银行账户为0.45，拥有不动产为0.35，参加人寿保险为0.19
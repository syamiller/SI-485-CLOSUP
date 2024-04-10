def get_short_run(df, report_id):
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']
    balance_unassigned = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'FundBalanceUnassigned') & (df['fund-member'] == 'GeneralFundMember')].iloc[0]['fact.value']
    fund_revenue = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'RevenuesModifiedAccrual') & (df['fund-member'] == 'GeneralFundMember')].iloc[0]['fact.value']    

    ratio = balance_unassigned / fund_revenue
    return {'report_id': report_id, 'report_entity_name' : report_entity, 'ratio': 'Short Run Financial Position', 'value': ratio, 'green_start': 0.15, 
            'green_end': 0.2, 'yellow_start': 0.2, 'yellow_end': 1, 'red_start': 0, 'red_end': 0.15, 
            'var_1_name':'General Fund Balance Unassigned', 'var_1_value':balance_unassigned, 
            'var_2_name':'General Fund Revenue', 'var_2_value': fund_revenue}
    
def get_days_cash_on_hand(df, report_id):
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']
    cash_and_cash_equivalents = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'CashAndCashEquivalentsModifiedAccrual') & (df['fund-member'] == 'GeneralFundMember')].iloc[0]['fact.value']
    expenditures = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'ExpendituresModifiedAccrual') & (df['fund-member'] == 'GeneralFundMember')].iloc[0]['fact.value']
    
    ratio = cash_and_cash_equivalents / (expenditures / 365)
    return {'report_id': report_id, 'ratio': 'Days of Cash on Hand', 'value': ratio, 'green_start': 125, 
            'green_end': 500, 'yellow_start': 90, 'yellow_end': 125, 'red_start': 0, 'red_end': 90,
            'var_1_name':'Cash and Cash Equivalents', 'var_1_value':cash_and_cash_equivalents, 
            'var_2_name':'Expenditures / 365', 'var_2_value':expenditures/365, 'report_entity_name' : report_entity}
    
def get_liquidity(df, report_id):
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']
    cash_and_cash_equivalents = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'CashAndCashEquivalentsModifiedAccrual') & (df['fund-member'] == 'GeneralFundMember')].iloc[0]['fact.value']
    liabilities = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'LiabilitiesModifiedAccrual') & (df['fund-member'] == 'GeneralFundMember')].iloc[0]['fact.value']
    deferred_revenue = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'DeferredInflowsOfResourcesModifiedAccrual') & (df['fund-member'] == 'GeneralFundMember')].iloc[0]['fact.value']
    
    ratio = cash_and_cash_equivalents / (liabilities - deferred_revenue)
    return {'report_id': report_id, 'ratio': 'Liquidity', 'value': ratio, 'green_start': 2, 'green_end': 10, 
            'yellow_start': 1, 'yellow_end': 2, 'red_start': 0, 'red_end': 1,
            'var_1_name':'Cash and Cash Equivalents', 'var_1_value':cash_and_cash_equivalents,
            'var_2_name':'Liabilities - Deferred Revenue', 'var_2_value': liabilities-deferred_revenue, 'report_entity_name' : report_entity}
    
def get_gov_debt_coverage(df, report_id):
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']
    debt_serv_expenditures = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'DebtServicePrincipalRepaymentModifiedAccrual') & (df['fund-member'] == 'GovernmentalFundsMember')].iloc[0]['fact.value'] \
        + df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'DebtServiceInterestAndFiscalChargesModifiedAccrual') & (df['fund-member'] == 'GovernmentalFundsMember')].iloc[0]['fact.value']
    total_expenditures = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'ExpendituresModifiedAccrual') & (df['fund-member'] == 'GovernmentalFundsMember')].iloc[0]['fact.value']
    try:
        capital_outlay = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'ExpendituresForCapitalOutlayModifiedAccrual') & (df['fund-member'] == 'GovernmentalFundsMember')].iloc[0]['fact.value']
    except:
        capital_outlay = 0

    ratio = debt_serv_expenditures / (total_expenditures - capital_outlay - debt_serv_expenditures)
    return {'report_id': report_id, 'ratio': 'Government Debt Coverage', 'value': ratio, 'green_start': 0, 
        'green_end': 0.1, 'yellow_start': 0.1, 'yellow_end': 0.15, 'red_start': 0.15, 'red_end': 1,
        'var_1_name':'Debt Service Expenditures', 'var_1_value':debt_serv_expenditures, 
        'var_2_name':'Total Expenditures - Capital Outlay - Debt Service Expenditures', 'var_2_value':total_expenditures - capital_outlay - debt_serv_expenditures, 'report_entity_name' : report_entity}
        
def get_expenditure_per_capita(df, report_id):
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']
    total_expenditures = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'ExpendituresModifiedAccrual') & (df['fund-member'] == 'GovernmentalFundsMember')].iloc[0]['fact.value']
    if report_id == 677268:
        population = 20726
    else:
        population = 83300
    ratio = total_expenditures / population
    return {'report_id': report_id, 'ratio': 'Expenditure per Capita', 'value': ratio, 'green_start': 500, 
        'green_end': 1200, 'yellow_start':100 , 'yellow_end': 100, 'red_start': 0, 'red_end': 500,
        'var_1_name':'Total Expenditures', 'var_1_value':total_expenditures, 
        'var_2_name':'Population',
        'var_2_value':population, 'report_entity_name': report_entity}
    
def get_net_asset_growth(df, report_id):
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']
    change_net_position = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'ChangesInNetPosition') & (df['fund-member'] == 'GovernmentalActivitiesMember')].iloc[0]['fact.value']
    begin_net_position = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'NetPositionAtBeginningOfPeriodAfterAdjustments') & (df['fund-member'] == 'GovernmentalActivitiesMember')].iloc[0]['fact.value']
    ratio = -change_net_position / begin_net_position
    return {'report_id': report_id, 'ratio': 'Net Asset Growth', 'value': ratio, 'green_start': 0.02, 
        'green_end': 0.5, 'yellow_start': 0.0, 'yellow_end': 0.02, 'red_start': -0.5, 'red_end': 0.0,
        'var_1_name':'Governmental Activities Change in Net Position', 'var_1_value':change_net_position, 
        'var_2_name':'Governmental Activities Beginning Net Position',
        'var_2_value':begin_net_position, 'report_entity_name': report_entity}
    
    
def get_captial_asset_ga(df, report_id):
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']

    beginning_net_value = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'CapitalAssetsNetOfAccumulatedDepreciationAndAmortization') & (df['fund-member'] == 'GovernmentalActivitiesMember')].iloc[:2].sort_values(by='period.fiscal-year').iloc[0]['fact.value']
    end_net_value = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'CapitalAssetsNetOfAccumulatedDepreciationAndAmortization') & (df['fund-member'] == 'GovernmentalActivitiesMember')].iloc[:2].sort_values(by='period.fiscal-year').iloc[1]['fact.value']

    captial_asset_ga = (end_net_value - beginning_net_value) / beginning_net_value
    captial_asset_ga

    return {
        'report_id': report_id, 
        'ratio': 'Capital Asset Condition (Governmental Activities)', 'value': captial_asset_ga, 
        'green_start': 0.02, 'green_end': 1, 
        'yellow_start': 0, 'yellow_end': 0.02,
        'red_start': -1, 'red_end': 0, 
        'var_1_name':'Ending Net Value - Beginning Net Value', 'var_1_value': (end_net_value - beginning_net_value), 
        'var_2_name':'Beginning Net Value', 'var_2_value': beginning_net_value, 'report_entity_name': report_entity
    }
    

def get_captial_asset_bta(df, report_id):
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']

    beginning_net_value = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'CapitalAssetsNetOfAccumulatedDepreciationAndAmortization') & (df['fund-member'] == 'BusinessTypeActivitiesMember')].iloc[:2].sort_values(by='period.fiscal-year').iloc[0]['fact.value']
    end_net_value = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'CapitalAssetsNetOfAccumulatedDepreciationAndAmortization') & (df['fund-member'] == 'BusinessTypeActivitiesMember')].iloc[:2].sort_values(by='period.fiscal-year').iloc[1]['fact.value']

    captial_asset_bta = (end_net_value - beginning_net_value) / beginning_net_value
    captial_asset_bta

    return {
        'report_id': report_id,
        'ratio': 'Capital Asset Condition (Business-Type Activities)', 'value': captial_asset_bta,
        'green_start': 0.02, 'green_end': 1,
        'yellow_start': 0, 'yellow_end': 0.02,
        'red_start': -1, 'red_end': 0, 
        'var_1_name':'Ending Net Value - Beginning Net Value', 'var_1_value': (end_net_value - beginning_net_value), 
        'var_2_name':'Beginning Net Value', 'var_2_value': beginning_net_value, 'report_entity_name': report_entity
    }
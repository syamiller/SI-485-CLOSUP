import ast

# Function to preprocess the DataFrame from its raw CSV format (NOTE: filters for dimension count of 1 by default)
def process_dataframe(df, dim = 1):
    # Filter dataframe to only include rows where `dimensions.count` is equal to `dim`
    df = df[df['dimensions.count'] == dim]
    
    # Apply ast.literal_eval to 'dimension-pair' column to convert string representation of dictionary to dictionary
    # This is necessary because CSV files store dictionaries and other nested data structures as strings
    df['dimension-pair'] = df['dimension-pair'].apply(ast.literal_eval)
    
    if dim == 1:
        # Create a new column 'fund-member' by extracting the value from the first dictionary in 'dimension-pair' column
        df['fund-member'] = df['dimension-pair'].apply(lambda x: x[0][list(x[0].keys())[0]])
    elif dim == 2:
        # Extract nested dimension names from dictionaries within list (ex: [{'key':value}, {'key':value}]) in 'dimension-pair' column
        df['fund-member1'] = df['dimension-pair'].apply(lambda x: x[0])
        df['fund-member1'] = df['fund-member1'].apply(lambda x: list(x.values())[0] if isinstance(x, dict) and x else x)
        df['fund-member2'] = df['dimension-pair'].apply(lambda x: x[1])
        df['fund-member2'] = df['fund-member2'].apply(lambda x: list(x.values())[0] if isinstance(x, dict) and x else x)
    else:
        # Raise an error if the dimension count is not 1 or 2, as we have only encountered these two cases thus far
        raise ValueError('Invalid dimension count -- Please specify a dimension count of 1 or 2, or add a new preprocessing option.')
    
    return df


# Below are the functions that calculate the ratios for the different financial health indicators.
# Return statement keys & values are as follows:
# `report_id`: ID of the municipality
# `report_entity_name`: Name of the municipality
# `ratio`: Name of the financial ratio/metric
# `value`: Value of the financial ratio/metric
# `green_start`: Lower bound of the green target range
# `green_end`: Upper bound of the green target range
# `yellow_start`: Lower bound of the yellow target range
# `yellow_end`: Upper bound of the yellow target range
# `red_start`: Lower bound of the red target range
# `red_end`: Upper bound of the red target range
# `var_1_name`: Name of the numerator used in the ratio calculation
# `var_1_value`: Value of the numerator variable
# `var_2_name`: Name of the denominator used in the ratio calculation
# `var_2_value`: Value of the denominator variable

# Short Run Financial Position
def get_short_run(df, report_id):
    df = process_dataframe(df) # process DataFrame
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name'] # name of municipality

    # Extract appropriate `fact.value` by filtering through `cube.primary-local-name` and `fund-member` columns
    # Note: Should be replicable for any reportID (municipality) with the same XBRL format
    balance_unassigned = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'FundBalanceUnassigned') & (df['fund-member'] == 'GeneralFundMember')].iloc[0]['fact.value']
    fund_revenue = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'RevenuesModifiedAccrual') & (df['fund-member'] == 'GeneralFundMember')].iloc[0]['fact.value']    

    # Calculate ratio
    ratio = balance_unassigned / fund_revenue

    # Return dictionary with relevant information
    return {'report_id': report_id, 'report_entity_name' : report_entity,
            'ratio': 'Short Run Financial Position', 'value': ratio,
            'green_start': 0.15, 'green_end': 0.2, # green target range
            'yellow_start': 0.2, 'yellow_end': 1, # yellow range
            'red_start': 0, 'red_end': 0.15, # red range
            'var_1_name':'General Fund Balance Unassigned', 'var_1_value':balance_unassigned, # numerator
            'var_2_name':'General Fund Revenue', 'var_2_value': fund_revenue} # denominator
    
# Days of Cash on Hand
def get_days_cash_on_hand(df, report_id):
    df = process_dataframe(df) # process DataFrame
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']

    # Extract appropriate `fact.value` by filtering through `cube.primary-local-name` and `fund-member` columns
    cash_and_cash_equivalents = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'CashAndCashEquivalentsModifiedAccrual') & (df['fund-member'] == 'GeneralFundMember')].iloc[0]['fact.value']
    expenditures = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'ExpendituresModifiedAccrual') & (df['fund-member'] == 'GeneralFundMember')].iloc[0]['fact.value']
    
    # Calculate ratio
    ratio = cash_and_cash_equivalents / (expenditures / 365)

    # Return dictionary with relevant information
    return {'report_id': report_id, 'report_entity_name' : report_entity,
            'ratio': 'Days of Cash on Hand', 'value': ratio,
            'green_start': 125, 'green_end': 500,
            'yellow_start': 90, 'yellow_end': 125,
            'red_start': 0, 'red_end': 90,
            'var_1_name':'Cash and Cash Equivalents', 'var_1_value': cash_and_cash_equivalents,
            'var_2_name':'Expenditures / 365', 'var_2_value': expenditures/365}
    
# Liquidity (Quick) Ratio
def get_liquidity(df, report_id):
    df = process_dataframe(df) # process DataFrame

    # Extract appropriate `fact.value` by filtering through `cube.primary-local-name` and `fund-member` columns
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']
    cash_and_cash_equivalents = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'CashAndCashEquivalentsModifiedAccrual') & (df['fund-member'] == 'GeneralFundMember')].iloc[0]['fact.value']
    liabilities = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'LiabilitiesModifiedAccrual') & (df['fund-member'] == 'GeneralFundMember')].iloc[0]['fact.value']
    deferred_revenue = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'DeferredInflowsOfResourcesModifiedAccrual') & (df['fund-member'] == 'GeneralFundMember')].iloc[0]['fact.value']
    
    # Calculate ratio
    ratio = cash_and_cash_equivalents / (liabilities - deferred_revenue)

    # Return dictionary with relevant information
    return {'report_id': report_id, 'report_entity_name': report_entity,
            'ratio': 'Liquidity (Quick) Ratio', 'value': ratio,
            'green_start': 2, 'green_end': 10, 
            'yellow_start': 1, 'yellow_end': 2,
            'red_start': 0, 'red_end': 1,
            'var_1_name':'Cash and Cash Equivalents', 'var_1_value': cash_and_cash_equivalents,
            'var_2_name':'Liabilities - Deferred Revenue', 'var_2_value': liabilities-deferred_revenue}
    
# Governmental Funds Debt Coverage
def get_gov_debt_coverage(df, report_id):
    df = process_dataframe(df) # process DataFrame
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']

    # Extract appropriate `fact.value` by filtering through `cube.primary-local-name` and `fund-member` columns
    debt_serv_expenditures = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'DebtServicePrincipalRepaymentModifiedAccrual') & (df['fund-member'] == 'GovernmentalFundsMember')].iloc[0]['fact.value'] \
        + df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'DebtServiceInterestAndFiscalChargesModifiedAccrual') & (df['fund-member'] == 'GovernmentalFundsMember')].iloc[0]['fact.value']
    total_expenditures = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'ExpendituresModifiedAccrual') & (df['fund-member'] == 'GovernmentalFundsMember')].iloc[0]['fact.value']
    
    try: # account for missing Capital Outlay data
        capital_outlay = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'ExpendituresForCapitalOutlayModifiedAccrual') & (df['fund-member'] == 'GovernmentalFundsMember')].iloc[0]['fact.value']
    except:
        capital_outlay = 0

    # Calculate ratio
    ratio = debt_serv_expenditures / (total_expenditures - capital_outlay - debt_serv_expenditures)

    # Return dictionary with relevant information
    return {'report_id': report_id, 'report_entity_name': report_entity,
            'ratio': 'Governmental Funds Debt Coverage', 'value': ratio,
            'green_start': 0, 'green_end': 0.1,
            'yellow_start': 0.1, 'yellow_end': 0.15,
            'red_start': 0.15, 'red_end': 0.5,
            'var_1_name':'Debt Service Expenditures', 'var_1_value': debt_serv_expenditures, 
            'var_2_name':'Total Expenditures - Capital Outlay - Debt Service Expenditures', 'var_2_value': (total_expenditures - capital_outlay - debt_serv_expenditures)}
        
# Expense per Capita
def get_expenditure_per_capita(df, report_id):
    df = process_dataframe(df) # process DataFrame
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']

    # Extract appropriate `fact.value` by filtering through `cube.primary-local-name` and `fund-member` columns
    total_expenditures = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'ExpendituresModifiedAccrual') & (df['fund-member'] == 'GovernmentalFundsMember')].iloc[0]['fact.value']
    
    # NOTE: Hardcoded population values for Flint & Ogemaw County
    if report_id == 677268:
        population = 20726
    else:
        population = 83300
    
    # Calculate ratio
    ratio = total_expenditures / population

    # Return dictionary with relevant information
    return {'report_id': report_id, 'report_entity_name': report_entity,
            'ratio': 'Expenditure per Capita', 'value': ratio,
            'green_start': 500, 'green_end': 1500,
            'yellow_start':100 , 'yellow_end': 100,
            'red_start': 0, 'red_end': 500,
            'var_1_name':'Total Expenditures', 'var_1_value': total_expenditures, 
            'var_2_name':'Population', 'var_2_value': population}
    
# Net Asset Growth (Governmental Activities)
def get_net_asset_growth(df, report_id):
    df = process_dataframe(df) # process DataFrame
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']

    # Extract appropriate `fact.value` by filtering through `cube.primary-local-name` and `fund-member` columns
    change_net_position = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'ChangesInNetPosition') & (df['fund-member'] == 'GovernmentalActivitiesMember')].iloc[0]['fact.value']
    begin_net_position = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'NetPositionAtBeginningOfPeriodAfterAdjustments') & (df['fund-member'] == 'GovernmentalActivitiesMember')].iloc[0]['fact.value']
    
    # Calculate ratio
    ratio = -change_net_position / begin_net_position
    
    # Return dictionary with relevant information
    return {'report_id': report_id, 'report_entity_name': report_entity,
            'ratio': 'Net Asset Growth (Governmental Activities)', 'value': ratio,
            'green_start': 0.02, 'green_end': 0.5,
            'yellow_start': 0.0, 'yellow_end': 0.02,
            'red_start': -0.5, 'red_end': 0.0,
            'var_1_name':'Governmental Activities Change in Net Position', 'var_1_value':change_net_position, 
            'var_2_name':'Governmental Activities Beginning Net Position', 'var_2_value':begin_net_position}
    
# (Non) Own-Source Revenue
def get_own_source_rev(df, report_id):
    df = df[df['report.id'] == int(report_id)]
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']

    # Extract appropriate `fact.value` by filtering through `cube.primary-local-name` and `fund-member` columns
    total_rev = process_dataframe(df) # process DataFrame
    total_rev = total_rev[(total_rev['cube.primary-local-name'] == 'NetExpenseRevenue') & (total_rev['fund-member'] == 'PrimaryGovernmentActivitiesMember')].iloc[0]['fact.value']

    # NOTE: Dimension count is 2 for this value -- preprocessing steps are slightly different
    total_op_grants = process_dataframe(df, dim=2) # process DataFrame with dimension count of 2
    
    # Extract appropriate `fact.value` by filtering through `cube.primary-local-name` and `fund-member` columns
    total_op_grants = total_op_grants[(df['cube.primary-local-name'] == 'ProgramRevenues') & ((total_op_grants['fund-member1'] == 'PrimaryGovernmentActivitiesMember')) & (total_op_grants['fund-member2'] == 'ProgramRevenuesFromOperatingGrantsAndContributionsMember')]
    total_op_grants = total_op_grants.iloc[0]['fact.value']

    # Calculate ratio
    ratio = abs(total_op_grants / total_rev)

    # Return dictionary with relevant information
    return {
        'report_id': report_id, 'report_entity_name': report_entity,
        'ratio': 'Proportion of (Non) Own-Source Revenue', 'value': ratio,
        'green_start': 0, 'green_end': 0.60,
        'yellow_start': 0.60, 'yellow_end': 0.80,
        'red_start': 0.80, 'red_end': 1,
        'var_1_name': 'Total Primary Government Operating Grants and Contributions', 'var_1_value': total_op_grants,
        'var_2_name': 'Total Primary Government Revenue', 'var_2_value': total_rev,
    }

# Capital Asset Condition (Governmental Activities)
def get_captial_asset_ga(df, report_id):
    df = process_dataframe(df) # process DataFrame
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']

    # Extract appropriate `fact.value` by filtering through `cube.primary-local-name` and `fund-member` columns
    beginning_net_value = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'CapitalAssetsNetOfAccumulatedDepreciationAndAmortization') & (df['fund-member'] == 'GovernmentalActivitiesMember')].iloc[:2].sort_values(by='period.fiscal-year').iloc[0]['fact.value']
    end_net_value = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'CapitalAssetsNetOfAccumulatedDepreciationAndAmortization') & (df['fund-member'] == 'GovernmentalActivitiesMember')].iloc[:2].sort_values(by='period.fiscal-year').iloc[1]['fact.value']

    # Calculate ratio
    captial_asset_ga = (end_net_value - beginning_net_value) / beginning_net_value
    captial_asset_ga

    # Return dictionary with relevant information
    return {
        'report_id': report_id, 
        'ratio': 'Capital Asset Condition (Governmental Activities)', 'value': captial_asset_ga, 
        'green_start': 0.02, 'green_end': 0.5, 
        'yellow_start': 0, 'yellow_end': 0.02,
        'red_start': -1, 'red_end': 0, 
        'var_1_name':'Ending Net Value - Beginning Net Value', 'var_1_value': (end_net_value - beginning_net_value), 
        'var_2_name':'Beginning Net Value', 'var_2_value': beginning_net_value, 'report_entity_name': report_entity
    }
    
# Capital Asset Condition (Business-Type Activities)
def get_captial_asset_bta(df, report_id):
    df = process_dataframe(df) # process DataFrame  
    report_entity = df[df['report.id'] == int(report_id)].iloc[0]['report.entity-name']

    # Extract appropriate `fact.value` by filtering through `cube.primary-local-name` and `fund-member` columns
    beginning_net_value = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'CapitalAssetsNetOfAccumulatedDepreciationAndAmortization') & (df['fund-member'] == 'BusinessTypeActivitiesMember')].iloc[:2].sort_values(by='period.fiscal-year').iloc[0]['fact.value']
    end_net_value = df[(df['report.id'] == int(report_id)) & (df['cube.primary-local-name'] == 'CapitalAssetsNetOfAccumulatedDepreciationAndAmortization') & (df['fund-member'] == 'BusinessTypeActivitiesMember')].iloc[:2].sort_values(by='period.fiscal-year').iloc[1]['fact.value']

    # Calculate ratio
    captial_asset_bta = (end_net_value - beginning_net_value) / beginning_net_value
    captial_asset_bta

    # Return dictionary with relevant information
    return {
        'report_id': report_id,
        'ratio': 'Capital Asset Condition (Business-Type Activities)', 'value': captial_asset_bta,
        'green_start': 0.02, 'green_end': 0.5,
        'yellow_start': 0, 'yellow_end': 0.02,
        'red_start': -1, 'red_end': 0, 
        'var_1_name':'Ending Net Value - Beginning Net Value', 'var_1_value': (end_net_value - beginning_net_value), 
        'var_2_name':'Beginning Net Value', 'var_2_value': beginning_net_value, 'report_entity_name': report_entity
    }
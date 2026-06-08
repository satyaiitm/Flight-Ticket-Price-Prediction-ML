def clean_flight_1(row):
    """
    correcting the flight number
    flight -- 6.00E-128 to 6E-128

    """
    
    route = row['flight']
    if (route[0:5] == "6.00E") :
        return'6E'+route[5:]
    else:
        return route



def clean_flight_2(row): 
    """
    if the flight number is not meaningful then replace it with np.nan
    "0.00E+00","0.00E-02"  to np.nan

    """
    route = row['flight']
    if  (route in ["0.00E+00","0.00E-02"]):
        return np.nan
    else:
        return route


airline_flight={'I5':'AirAsia','AI':'Air_India','G8':'GO_FIRST','6E':'Indigo','SG':'SpiceJet','UK':'Vistara'}

def impute_airline(row):
    """
    if the airline name if missing we can guess it from the initial two digits of flight rought

    """
    if pd.isna(row['airline']):
        prefix = row['flight'][:2]
        if prefix in airline_flight:
            return airline_flight[prefix]
    return row['airline']




def logical_imputer(df):

    df['flight']=df.apply(clean_flight_1, axis=1)
    df['airline']=df.apply(impute_airline, axis=1)
    df['flight']=df.apply(clean_flight_2, axis=1)

    df['departure'] = df['departure'].where(
        df['departure'].notna(),df.groupby(['airline','source','destination','arrival']
                                           )['departure'].transform(
                                               lambda x: x.fillna(x.mode()[0] if not x.mode().empty else x.bfill())))



    # df['duration'] = df['duration'].where(
    #     df['duration'].notna(),df.groupby(['airline','source', 'stops', 'destination']
    #                                       )['duration'].transform(
    #                                           lambda x: x.fillna(x.mode()[0] if not x.mode().empty else x.median()[0])))


    df['stops'] = df['stops'].where(
        df['stops'].notna(),df.groupby(['airline','source','destination','duration']
                                       )['stops'].transform(
                                           lambda x: x.fillna(x.mode()[0] if not x.mode().empty else x.bfill())))

    df['days_left'] = df['days_left'].where(
        df['days_left'].notna(),df.groupby(['source','arrival','destination','class','price']
                                       )['days_left'].transform(
                                           lambda x: x.fillna(x.mode()[0] if not x.mode().empty else x.bfill())))



    df['flight'] = df['flight'].where(
        df['flight'].notna(),df.groupby(['airline','arrival','source','destination']
                                       )['flight'].transform(
                                           lambda x: x.fillna(x.mode()[0] if not x.mode().empty else x.bfill())))



    for name, group_df in df.groupby(['airline','source', 'stops', 'destination'] ):

        for idx, row in group_df.iterrows():

            if pd.isna(row['duration']):

                candidates = (group_df[ group_df['duration'].notna()].drop(idx, errors='ignore'))

                if candidates.empty:
                    continue

                closest_index = ( candidates['price'] - row['price']).abs().idxmin()

                closest_value = candidates.loc[closest_index,'duration']

                df.loc[idx, 'duration'] = closest_value



    df.dropna(inplace=True)

    return df
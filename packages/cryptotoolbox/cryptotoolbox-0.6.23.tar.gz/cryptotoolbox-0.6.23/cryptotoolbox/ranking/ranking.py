
import requests
import json
import pandas as pd
import time
from datetime import datetime
from datetime import timedelta
import numpy as np
import os
from cryptotoolbox.risk_metrics import riskmetrics
from cryptotoolbox.realtime import realtime_plotting_utility

def get_token_ohlc_from_cmc(token_id, filepath=None, start=int(pd.to_datetime("2023-01-01 00:00:00").timestamp()),
                            end=int(time.time())):
    """Get the coinmarket cap data given a token_id
    """
    headers = {
        'authority': 'api.coinmarketcap.com',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'sec-gpc': '1',
        'origin': 'https://coinmarketcap.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://coinmarketcap.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('id', token_id),
        ('convertId', '2781'),
        ('timeStart', start),
        ('timeEnd', end),
    )

    response = requests.get('https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical', headers=headers,
                            params=params)
    print(response)
    data = response.json()["data"]

    df = pd.DataFrame.from_dict(data["quotes"])

    df["o"] = df["quote"].apply(lambda x: x["open"])
    df["h"] = df["quote"].apply(lambda x: x["high"])
    df["l"] = df["quote"].apply(lambda x: x["low"])
    df["c"] = df["quote"].apply(lambda x: x["close"])
    df["v"] = df["quote"].apply(lambda x: x["volume"])
    df["mcap"] = df["quote"].apply(lambda x: x["marketCap"])
    df["timestamp"] = df["quote"].apply(lambda x: pd.to_datetime(x["timestamp"]).strftime("%Y-%m-%d"))
    df["id"] = np.repeat(token_id, len(df))
    df["token_id"] = np.repeat(token_id, len(df))
    df["interval"] = np.repeat("day", len(df))
    df["created_at"] = df["quote"].apply(lambda x: pd.to_datetime(x["timestamp"]).strftime("%Y-%m-%d"))
    df["source"] = np.repeat("cmc_ohlcv_history", len(df))
    df["currency"] = np.repeat(data["symbol"], len(df))
    df["time_o"] = df["timestamp"]
    df["time_h"] = df["timestamp"]
    df["time_l"] = df["timestamp"]
    df["time_c"] = df["timestamp"]

    df = df[
        ["timestamp", "id", "o", "h", "l", "c", "v", "mcap", "created_at", "token_id", "interval", "source", "time_c",
         "time_h", "time_l", "time_o", "currency"]]
    df.set_index("timestamp", drop=True, inplace=True)
    df.index = pd.to_datetime(df.index)
    if filepath:
#        df.to_pickle(os.path.join(filepath, f'{data["symbol"].upper()}.pkl'))
        df.to_pickle(os.path.join(filepath, f'{token_id}.pkl'))
        #df.to_csv(os.path.join(filepath, f'{data["symbol"].upper()}.csv'))
    return df[["time_c", "id", "o", "h", "l", "c", "v", "mcap"]]


# get the CMC tokens ID
def get_latest_cmc_rank(top_n=50, tag=None):
    """Get latest cmc rank"""
    df = pd.DataFrame()

    headers = {
        'authority': 'api.coinmarketcap.com',
        'fvideo-id': '32686dab703496d7a7ed3140a2d3dd39520586e8',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'x-request-id': '204388cb-f1f5-40f7-accb-3fe93a5c330f',
        'sec-gpc': '1',
        'origin': 'https://coinmarketcap.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://coinmarketcap.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = {
        'start': '1',
        'limit': top_n,
        'sortBy': 'rank',
        'sortType': 'desc',
        'convert': 'USD,BTC,ETH',
        'cryptoType': 'all',
        'tagType': 'all',
        'audited': 'false',
        'aux': 'ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,max_supply,circulating_supply,total_supply,volume_7d,volume_30d,self_reported_circulating_supply,self_reported_market_cap'
    }

    if tag:
        params["tagSlugs"] = tag

    response = requests.get('https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing', headers=headers,
                            params=params)
    if "data" in response.json():
        df = pd.DataFrame(response.json()["data"]["cryptoCurrencyList"])
    return df

def apply_global_ranking(row, weight_mdd=0.3, weight_simple_return=0.3, weight_market_cap=0.2, weight_volume=0.2):
    mdd = row['mdd']
    simple_return = row['simple_return']
    market_cap = row['market_cap']
    volume = row['volume']
    final_score = weight_mdd * mdd + weight_simple_return * simple_return + weight_market_cap * market_cap + weight_volume * volume
    return final_score

def compute_ranking_metrics(coins = None, top_n=5000, lockup_period_in_days =31, display_html = True, file_saving_path = None):
    print(f'fetching ranks and market cap')
    start_date = datetime.now() + timedelta(days = -5*lockup_period_in_days)
    start_date_timestamp_int = int(pd.to_datetime(start_date).timestamp())
    rank_df = get_latest_cmc_rank(top_n=top_n)
    if coins is not None:
        rank_df = rank_df[rank_df['symbol'].isin(coins)].copy()
    rank_df = rank_df.set_index('id')
    rank_df.to_pickle(file_saving_path + 'rank_df.pkl')
    ids_tofetch=[]
    for id, row in rank_df.iterrows():
        print(f'fetching {id}')
        get_token_ohlc_from_cmc(token_id=id,start= start_date_timestamp_int, filepath=file_saving_path)
        ids_tofetch.append(id)

    entries = os.listdir(file_saving_path)
    aggregated_ohlc = None
    id_list = []
    for me_entry in entries:
        id = me_entry.split('.')[0]
        try:
            if int(id) in ids_tofetch:
                id_list.append(id)
                print(f'aggregating {id}')
                data_frame = pd.read_pickle(os.path.join(file_saving_path, me_entry))
                data_frame = data_frame.rename(
                    columns={
                        'mcap': f'market_cap_{id}',
                        'c': f'close_{id}',
                        'v': f'volume_{id}'
                    })
                data_frame = data_frame[[f'market_cap_{id}', f'close_{id}', f'volume_{id}']].copy()
                if aggregated_ohlc is None:
                    aggregated_ohlc = data_frame.copy()
                else:
                    aggregated_ohlc = pd.merge(aggregated_ohlc.copy(), data_frame.copy(), how='left', left_index=True,
                                               right_index=True)  # suffixes = ['','_again'])

        except Exception as e:
            print(f'Error fetchgin {id} to the client: ', e)

    close_list = [f'close_{id}' for id in id_list]
    to_keep = aggregated_ohlc[close_list].isna().sum(axis = 0) > 0
    to_keep = to_keep[to_keep.values]
    to_exclude = list(to_keep[to_keep.values].index)
    to_exclude = [me_id.replace('close_','') for me_id in to_exclude]
    volume_list = [f'volume_{id}' for id in id_list if id not in to_exclude]
    close_list = [f'close_{id}' for id in id_list if id not in to_exclude]
    marketcap_list = [f'market_cap_{id}' for id in id_list if id not in to_exclude]
    close_df = aggregated_ohlc[close_list].copy()
    close_df.to_pickle(file_saving_path + 'all_close_df.pkl')
    market_cap_df = aggregated_ohlc[marketcap_list].copy()
    market_cap_df.to_pickle(file_saving_path + 'all_marketcap_df.pkl')
    volume_df = aggregated_ohlc[volume_list].copy()
    volume_df.to_pickle(file_saving_path + 'all_volume_df.pkl')
    aggregated_ohlc.to_pickle(file_saving_path + 'all_in_df.pkl')
    kpi_df = riskmetrics.get_kpi(close_df).T
    kpi_df.to_pickle(file_saving_path + 'kpi_df.pkl')
    kpi_df = kpi_df.sort_values(by='simple_return', ascending=False)
    kpi_df = kpi_df.reset_index()
    def get_symbol(row):
        return int(row['index'].replace('close_', ''))

    kpi_df['id'] = kpi_df.apply(get_symbol, axis=1)

    kpi_df = pd.merge(kpi_df.copy(), rank_df.copy(), how='left', left_on='id', right_index=True)

    light_volume_df = volume_df.mean(axis=0)
    light_market_cap = market_cap_df.mean(axis=0)
    light_market_cap = light_market_cap.reset_index()
    light_volume_df = light_volume_df.reset_index()

    def get_symbol_marketcap(row):
        return int(row['index'].replace('market_cap_', ''))

    def get_symbol_volume(row):
        return int(row['index'].replace('volume_', ''))

    light_market_cap.columns = ['index', 'market_cap']
    light_market_cap['id'] = light_market_cap.apply(get_symbol_marketcap, axis=1)

    light_volume_df.columns = ['index', 'volume']
    light_volume_df['id'] = light_volume_df.apply(get_symbol_volume, axis=1)

    kpi_df = pd.merge(kpi_df.copy(), light_market_cap.copy(), how='left', left_on='id', right_on='id')
    kpi_df = pd.merge(kpi_df.copy(), light_volume_df.copy(), how='left', left_on='id', right_on='id')

    kpi_with_ranking_power = ['simple_return', 'mdd', 'market_cap', 'volume']
    ranking_metrics_dataframe = kpi_df[['name', 'simple_return', 'mdd', 'market_cap', 'volume']]
    ranking_metrics_dataframe = ranking_metrics_dataframe.fillna(0.)

    ranked_ranking_metrics_dataframe = ranking_metrics_dataframe.copy()
    ranked_ranking_metrics_dataframe['mdd'] = 1. - ranked_ranking_metrics_dataframe['mdd']
    print('done')
    for me_kpi in kpi_with_ranking_power:
        ranked_ranking_metrics_dataframe[me_kpi] = ranked_ranking_metrics_dataframe[me_kpi].rank(pct=True)



    go_rank_set = lambda x: apply_global_ranking(x, weight_mdd=0.3, weight_simple_return=0.4, weight_market_cap=0.15,
                                                  weight_volume=0.15)


    ranked_ranking_metrics_dataframe['global_score'] = ranked_ranking_metrics_dataframe.apply(go_rank_set,axis=1)

    for me_metrics in ['global_score'] + kpi_with_ranking_power:
        ranked_ranking_metrics_dataframe = ranked_ranking_metrics_dataframe.sort_values(by=me_metrics, ascending=False)
        ranked_ranking_metrics_dataframe.to_excel(file_saving_path + f'ranked_shitcoin_{me_metrics}.xls')
        if display_html:
            to_display = ranked_ranking_metrics_dataframe[['name', me_metrics]].copy()
            to_display = to_display.set_index('name')
            to_display = to_display.iloc[:75]
            fig = realtime_plotting_utility.plot_multiple_bar_series(to_display, logy=False,
                                                                     title=f'Best 3 months {me_metrics} momentum ranking')
            fig.show()
            fig.write_image(file_saving_path + f'Best_3_months_{me_metrics}_momentum_ranking.png')
            print('computing sorting metrics')
    return ranked_ranking_metrics_dataframe


def compute_risk_and_rewards_metrics(coins = None, weights=None, lockup_period_in_days = 31, top_n=5000,quantile_take_profit = 0.75, quantile_stop_loss = 0.25, display_html = True, file_saving_path = None):
    print(f'fetching ranks and market cap')
    start_date = datetime.now() + timedelta(days = -5*lockup_period_in_days)
    start_date_timestamp_int = int(pd.to_datetime(start_date).timestamp())
    rank_df = get_latest_cmc_rank(top_n=top_n)
    if coins is not None:
        rank_df = rank_df[rank_df['symbol'].isin(coins)].copy()
    id_weights = {}
    for id, row in rank_df.iterrows():
        if row['symbol'] in weights.keys():
            id_weights[row['id']] = weights[row['symbol']]

    rank_df = rank_df.set_index('id')
    rank_df.to_pickle(file_saving_path + 'rank_df.pkl')
    ids_tofetch=[]
    for id, row in rank_df.iterrows():
        print(f'fetching {id}')
        get_token_ohlc_from_cmc(token_id=id,start= start_date_timestamp_int, filepath=file_saving_path)
        ids_tofetch.append(id)

    entries = os.listdir(file_saving_path)
    aggregated_ohlc = None
    id_list = []
    for me_entry in entries:
        id = me_entry.split('.')[0]
        try:
            if int(id) in ids_tofetch:
                id_list.append(id)
                print(f'aggregating {id}')
                data_frame = pd.read_pickle(os.path.join(file_saving_path, me_entry))
                data_frame = data_frame.rename(
                    columns={
                        'mcap': f'market_cap_{id}',
                        'c': f'close_{id}',
                        'v': f'volume_{id}'
                    })
                data_frame = data_frame[[f'market_cap_{id}', f'close_{id}', f'volume_{id}']].copy()
                if aggregated_ohlc is None:
                    aggregated_ohlc = data_frame.copy()
                else:
                    aggregated_ohlc = pd.merge(aggregated_ohlc.copy(), data_frame.copy(), how='left', left_index=True,
                                               right_index=True)  # suffixes = ['','_again'])

        except Exception as e:
            print(f'Error fetchgin {id} to the client: ', e)

    close_list = [f'close_{id}' for id in id_list]
    to_keep = aggregated_ohlc[close_list].isna().sum(axis = 0) > 0
    to_keep = to_keep[to_keep.values]
    to_exclude = list(to_keep[to_keep.values].index)
    to_exclude = [me_id.replace('close_','') for me_id in to_exclude]
    close_list = [f'close_{id}' for id in id_list if id not in to_exclude]
    close_df = aggregated_ohlc[close_list].copy()
    close_df.to_pickle(file_saving_path + 'all_close_df.pkl')

    return_df = close_df.pct_change().fillna(0.).copy()
    def compute_return_basket(row, weights = None):
        global_return = 0.
        for me_key, me_val in weights.items():
            return_key = row[f'close_{str(me_key)}']
            global_return = global_return + me_val*return_key
        return global_return
    go_ret = lambda x : compute_return_basket(x, weights=id_weights)
    return_df['basket'] = return_df.apply(go_ret, axis = 1)
    print('done')
    #### computing value at risk
    daily_VaR_90 =  return_df['basket'] .quantile(0.1)
    daily_VaR_95 =  return_df['basket'] .quantile(0.05)
    daily_VaR_99 =  return_df['basket'] .quantile(0.09)

    for col in return_df.columns:
        return_df[col] = np.cumprod(1. + return_df[col].values)
    close_norm_df =return_df.copy()
    kpi_df = riskmetrics.get_kpi(close_norm_df[['basket']]).T
    kpi_df.to_pickle(file_saving_path + 'kpi_df.pkl')
    if display_html:
        fig = realtime_plotting_utility.plot_multiple_time_series(data_df=close_norm_df, logy=False,
                                                                 title=f'Basket against underlyings')
        fig.show()
        fig.write_image(file_saving_path + f'Basket_against_underlyings.png')
        print('computing sorting metrics')



    ##### computing stop loss and take profit
    close_norm_df['basket_shifted'] = close_norm_df['basket'].shift(lockup_period_in_days)
    close_norm_df = close_norm_df.dropna().copy()
    close_norm_df['basket_lockup_return'] = (close_norm_df['basket'] - close_norm_df['basket_shifted'])/close_norm_df['basket_shifted']
    positive_basket_returns = close_norm_df[close_norm_df['basket_lockup_return']>=0].copy()
    negative_basket_returns = close_norm_df[close_norm_df['basket_lockup_return']<=0].copy()
    positive_basket_returns = positive_basket_returns['basket_lockup_return']
    negative_basket_returns = negative_basket_returns['basket_lockup_return']

    take_profit = np.quantile(positive_basket_returns.values, q=quantile_take_profit)
    stop_loss = np.quantile(negative_basket_returns.values,q = quantile_stop_loss)
    kpi_df['stop_loss'] = np.nan
    kpi_df['take_profit'] = np.nan
    kpi_df['daily_VaR_99'] = np.nan
    kpi_df['daily_VaR_95'] = np.nan
    kpi_df['daily_VaR_90'] = np.nan
    kpi_df.loc['basket']['stop_loss'] = stop_loss
    kpi_df.loc['basket']['take_profit'] = take_profit
    kpi_df.loc['basket']['daily_VaR_99'] = daily_VaR_99
    kpi_df.loc['basket']['daily_VaR_95'] = daily_VaR_95
    kpi_df.loc['basket']['daily_VaR_90'] = daily_VaR_90
    return kpi_df

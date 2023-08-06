"""
Analysis utility functions.
Copyright (C) 2022 Humankind Investments
"""

import pandas as pd
import numpy as np
from .db_utils import database_connect
from os import path
from joblib import load
import pathlib
import re


# CLEANING DUPLICATE AND SPLIT VISITS +++++++++++++++++++++++++++++++++++++++++++++++++++++++
def drop_false_splits(df):
    """
    Drop false splits.
    
    Drop extraneous false splits, i.e. visits with duplicate visit counts per visitor
    occurring more than thirty minutes from each other. For each set of false splits, 
    the visit with the most activity is kept.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe of false splits.
        
    Returns
    -------
    pd.DataFrame
        Dataframe of remaining splits after drops.
    """
    
    # keep visit among false splits with longest visit duration or most actions
    cdf = df.sort_values(by=['visit_duration', 'actions'],
                         ascending=[False, False]).drop_duplicates(
                             subset=['visitor_id', 'visit_count']).reset_index(drop=True)
    
    return cdf


def combine_true_splits(df, dt0=True):
    """
    Combine true splits.
    
    Combine and return true split visits, i.e. visits with duplicate visit counts 
    per visitor occurring within thirty minutes of one another.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe of true splits.
    dt0 : bool
        Whether delta-dt between visits is 0, indicating split visits occur at same time.
        
    Returns
    -------
    pd.DataFrame
        Dataframe of combined splits.
    """
    
    # separate columns by how data to be aggregated
    mean_cols = [col for col in df.columns if col.split('_')[0] == 'avg']
    sum_cols = [col for col in df.columns if col.split('_')[-1] in [
        'actions', 'pages', 'downloads', 'outlinks', 'buyetfs', 'brokerlinks', 
        'plays', 'pauses', 'resumes', 'seeks', 'finishes', 
        'time', 'submissions', 'duration'] and col != 'time' and col not in mean_cols]
    first_cols = [col for col in df.columns if col not in
                  mean_cols + sum_cols and col.split('_')[0] not in [
                      'first', 'last', 'entry', 'exit'] and col.split('_')[-1] not in [
                          'flow', 'ts', 'list'] and not col.endswith('video_resolution')]
    manual_cols = [col for col in df.columns if col not in sum_cols + mean_cols + first_cols]

    # convert numeric columns to proper type
    df[mean_cols] = df[mean_cols].astype(float)
    
    # combine split visits with same visitor id and visit count
    # --> sort by visit id for split visits occurring at same time; split by datetime otherwise
    sort_col = 'visit_id' if dt0 else 'datetime'
    grp_cols = ['visitor_id', 'visit_count']
    # --> also group by datetime for split visits occurring at same time
    if dt0: grp_cols.append('datetime')
    grp = df.sort_values(by=sort_col).groupby(grp_cols)
    
    # apply basic aggregates for appropriate columns (first/last, sum, mean)
    first_grp = grp[[col for col in first_cols if col not in grp.keys]]
    # --> pull basic visit info from last visit info in half hour window if delta-t != 0
    first_df = first_grp.first() if dt0 else first_grp.last()
    sum_df = grp[[col for col in sum_cols if col not in grp.keys]].sum()
    mean_df = grp[[col for col in mean_cols if col not in grp.keys]].mean()
    cdf = pd.concat([first_df, sum_df, mean_df], axis=1)

    # combine remaining columns manually ...
    
    # select first and last non-empty action, and combine non-empty action flows in order
    actgrp = df[df['first_action'] != 'None'].sort_values(by=sort_col).groupby(grp_cols)
    acts_df = pd.concat([actgrp['first_action'].first(), 
                         actgrp['last_action'].last(),
                         actgrp['action_flow'].apply(lambda x: ','.join(x)),
                         actgrp['action_ts'].apply(lambda x: ','.join(x)),
                         actgrp['action_site_flow'].apply(lambda x: ','.join(x)), 
                         actgrp['action_path_flow'].apply(lambda x: ','.join(x))], axis=1)
    
    # select first/last entry/exit pages, and fill in missing values based on first/last actions
    pgs_df = pd.concat([actgrp['entry_page'].first(), actgrp['exit_page'].last()], axis=1)
    pgs_df.loc[(pgs_df['entry_page'] == 'None') &
               (acts_df['first_action'].str.rsplit('_', n=1).str[0].isin(
                   ['humankind_video', 'humankind-short_video', 'getstarted_form'])),
               'entry_page'] = 'humankind'
    pgs_df.loc[(pgs_df['entry_page'] == 'None') &
               ((acts_df['first_action'].str.rsplit('_', n=1).str[0].isin(
                   ['wtf_video', 'wtf-short_video', 'buyetf'])) |
                (acts_df['first_action'].str.split('_', n=1).str[-1].isin(
                    ['brokerlink_click', 'download']))), 'entry_page'] = 'humankindfunds'
    pgs_df.loc[(pgs_df['exit_page'] == 'None') &
               (acts_df['last_action'].str.rsplit('_', n=1).str[0].isin(
                   ['humankind_video', 'humankind-short_video', 'getstarted_form'])),
               'exit_page'] = 'humankind'
    pgs_df.loc[(pgs_df['exit_page'] == 'None') &
               ((acts_df['last_action'].str.rsplit('_', n=1).str[0].isin(
                   ['wtf_video', 'wtf-short_video', 'buyetf'])) |
                (acts_df['last_action'].str.split('_', n=1).str[-1].isin(
                    ['brokerlink_click', 'download']))), 'exit_page'] = 'humankindfunds'

    # combine non-empty page flows
    pggrp = df[df['page_flow'] != 'None'].sort_values(by=sort_col).groupby(grp_cols)
    pgs_df = pd.concat([
        pgs_df, pggrp['page_flow'].apply(lambda x: ','.join(x)), 
        pggrp['page_ts'].apply(lambda x: ','.join(x))], axis=1).fillna('None')
    
    # combine non-empty article post and ranked company page lists
    for pg in ['article-post', 'ranked-company']:
        pg += '_page_list'
        pgs_df = pd.concat([pgs_df, df[df[pg].fillna('None').replace(
            'NaN', 'None') != 'None'].sort_values(by=sort_col).groupby(
                grp_cols)[pg].apply(lambda x: ','.join(x))], axis=1).fillna('None')
        
    # combine non-empty download flows
    dlgrp = df[df['download_flow'] != 'None'].sort_values(by=sort_col).groupby(grp_cols)
    dls_df = pd.concat([
        dlgrp['download_flow'].apply(lambda x: ','.join(x)), 
        dlgrp['download_ts'].apply(lambda x: ','.join(x))], axis=1).fillna('None')
    
    # combine non-empty outlink flows
    olgrp = df[df['outlink_flow'] != 'None'].sort_values(by=sort_col).groupby(grp_cols)
    ols_df = pd.concat([
        olgrp['outlink_flow'].apply(lambda x: ','.join(x)), 
        olgrp['outlink_ts'].apply(lambda x: ','.join(x))], axis=1).fillna('None')

    # combine non-empty outlink lists
    for ol in ['social', 'crs', 'disclosures', 'articles']:
        ol += '_outlink_list'
        ols_df = pd.concat([ols_df, df[df[ol].fillna('None').replace(
            'NaN', 'None') != 'None'].sort_values(by=sort_col).groupby(
                grp_cols, group_keys=False)[ol].apply(
                    lambda x: ','.join(x))], axis=1).fillna('None')
           
    # combine non-empty buy-etf timestamps
    etfs_df = df[df['buyetf_ts'].fillna('None').replace(
        'NaN', 'None') != 'None'].sort_values(by=sort_col).groupby(
            grp_cols)['buyetf_ts'].apply(lambda x: ','.join(x))
    
    # combine non-empty broker link flows
    brkgrp = df[df['brokerlink_flow'] != 'None'].sort_values(by=sort_col).groupby(grp_cols)
    brks_df = pd.concat([
        brkgrp['brokerlink_flow'].apply(lambda x: ','.join(x)), 
        brkgrp['brokerlink_ts'].apply(lambda x: ','.join(x))], axis=1).fillna('None')
    
    # combine non-empty video flows and non-empty video resolutions
    vidgrp = df[df['video_action_flow'] != 'None'].sort_values(by=sort_col).groupby(grp_cols)
    vids_df = pd.concat([
        vidgrp['video_action_flow'].apply(lambda x: ','.join(x)), 
        vidgrp['video_action_ts'].apply(lambda x: ','.join(x)),
        df[df['video_resolution'] != 'None'].sort_values(by=sort_col).groupby(
            grp_cols)['video_resolution'].apply(lambda x: ','.join(x))], axis=1).fillna('None')

    # combine non-empty form flows
    frmgrp = df[df['form_action_flow'] != 'None'].sort_values(by=sort_col).groupby(grp_cols)
    frms_df = pd.concat([
        frmgrp['form_action_flow'].apply(lambda x: ','.join(x)), 
        frmgrp['form_action_ts'].apply(lambda x: ','.join(x))], axis=1).fillna('None')
    
    # combine all split visit columns
    cdf = pd.concat([cdf, acts_df, pgs_df, dls_df, ols_df, etfs_df,
                     brks_df, vids_df, frms_df], axis=1).fillna('None')
    
    # reset missing values in appropriate columns
    cdt = cdf.index.get_level_values(2) if dt0 else cdf['datetime']
    for pg in [col[:-1] for col in df.isnull().sum()[df.isnull().sum() > 0].index
               if col.endswith('_pages')]:
        cdf.loc[cdt <= df[df[pg + 's'].isnull()].sort_values(
            by='datetime', ascending=False)['datetime'].iloc[0],
                [col for col in cdf.columns if pg in col]] = np.nan
    for dl in [col[:-1] for col in df.isnull().sum()[df.isnull().sum() > 0].index
               if col.endswith('_downloads')]:
        cdf.loc[cdt <= df[df[dl + 's'].isnull()].sort_values(
            by='datetime', ascending=False)['datetime'].iloc[0],
                [col for col in cdf.columns if col == dl + 's'
                 or col == dl + '_duration']] = np.nan
    for ol in [col[:-1] for col in df.isnull().sum()[df.isnull().sum() > 0].index
               if col.endswith('_outlinks')]:
        cdf.loc[cdt <= df[df[ol + 's'].isnull()].sort_values(
            by='datetime', ascending=False)['datetime'].iloc[0],
                [col for col in cdf.columns if ol in col]] = np.nan
    if any(df['buyetfs'].isnull()):
        cdf.loc[cdt <= df[df['buyetfs'].isnull()].sort_values(
            by='datetime', ascending=False)['datetime'].iloc[0],
                [col for col in cdf.columns if 'buyetf' in col]] = np.nan
    for vid in [col.rsplit('_', 1)[0] for col in df.isnull().sum()[df.isnull().sum() > 0].index
                if col.endswith('_video_plays')]:
        cdf.loc[cdt <= df[df[vid + '_plays'].isnull()].sort_values(
            by='datetime', ascending=False)['datetime'].iloc[0],
                [col for col in cdf.columns if vid in col]] = np.nan
    for frm in [col.rsplit('_', 1)[0] for col in df.isnull().sum()[df.isnull().sum() > 0].index
                if col.endswith('_form_actions')]:
        cdf.loc[cdt <= df[df[frm + '_actions'].isnull()].sort_values(
            by='datetime', ascending=False)['datetime'].iloc[0],
                [col for col in cdf.columns if frm in col]] = np.nan
    
    return cdf
    
    
def clean_split_visits(df, true_split=True, same_time=True):
    """
    Clean split visits, combining true splits and dropping false splits.
    
    Combine true split visits, i.e. visits with duplicate visit counts per visitor 
    occurring within thirty minutes of one another, and drop extraneous false splits,
    i.e. visits with duplicate visit counts per visitor occurring more than thirty 
    minutes from each other.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe of split visits.
    true_split : bool
        Whether split visits are true splits or false splits.
    same_time : bool
        Whether true splits occur at same time or different times.
        
    Returns
    -------
    pd.DataFrame
        Cleaned dataframe of split visits.
    """

    # calculate differences in time between split visits
    grp = df.sort_values(by='datetime').groupby(['visitor_id', 'visit_count'])
    # --> deltadt = time between each split visit for given visitor ID and visit count
    deltadt = grp['datetime'].apply(list).apply(
        lambda x: [(x[i+1] - x[i]).total_seconds() for i in range(len(x)-1)]).rename('deltadt')
    # --> visit_id_pairs = split visit pairs for which delta-dt calculated
    visit_id_pairs = grp['visit_id'].unique().apply(
        lambda x: [(x[i], x[i+1]) for i in range(len(x)-1)] if len(x) > 1 else
        [(x[0], x[0])]).rename('visit_id_pairs')
    split_dt = pd.concat([deltadt, visit_id_pairs], axis=1)
    
    # filter out split visits already cleaned (no duplicates)
    split_mask = split_dt['deltadt'].str.len() > 0
    split_dt = pd.concat([split_dt[split_mask]['deltadt'].explode(),
                          split_dt[split_mask]['visit_id_pairs'].explode()], axis=1)
    
    # sum up total delta-dt for true splits occurring at different times or false splits
    if not true_split or not same_time:
        split_dt = pd.concat([
            split_dt.reset_index().groupby(['visitor_id', 'visit_count'])['deltadt'].sum(),
            split_dt['visit_id_pairs'].apply(
                lambda x: list(x)).explode().drop_duplicates().reset_index().groupby([
                    'visitor_id', 'visit_count'])['visit_id_pairs'].unique()], axis=1)
    # set delta-dt thresholds for selecting split visits of given type
    if true_split:
        deltadt_mask = split_dt['deltadt'] == 0 if same_time else split_dt['deltadt'] < 1800
    else:
        deltadt_mask = split_dt['deltadt'] >= 1800
    # isolate split visits of given type
    split_ids = split_dt[deltadt_mask]['visit_id_pairs'].apply(
        lambda x: list(x)).explode().drop_duplicates()
    split_visits = df[df['visit_id'].isin(split_ids)].reset_index(drop=True)
    
    # combine true splits or drop false splits
    if true_split: clean_splits = combine_true_splits(split_visits, same_time).reset_index()
    else: clean_splits = drop_false_splits(split_visits)

    # drop split visits of given type, and add newly cleaned split visits
    df = df.drop(df.loc[df['visit_id'].isin(split_visits['visit_id'])].index)
    df = pd.concat([df, clean_splits]).sort_values(by='visit_id').reset_index(drop=True)
    
    return df


def get_split_visits(df):
    """
    Get split visits from visit-level data.
    
    Identify and return all split visits from visit-level data set, where split visits
    are those with duplicate visit counts per visitor.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe of visits.
    
    Returns
    -------
    pd.DataFrame
        Dataframe of split visits.
    """

    # count number of visit IDs associated with each visitor ID - visit count pair
    visit_count = df.groupby(['visitor_id', 'visit_count'])['visit_id'].count()
    
    # isolate visitor ID - visit count pairs with multiple visit IDs
    dupl_visit_count = visit_count[visit_count > 1]
    
    # pull out split visits from visit-level data set
    split_visits = df.loc[df[['visitor_id', 'visit_count']].apply(
        tuple, axis=1).isin(dupl_visit_count.index)].reset_index(drop=True)
    
    return split_visits


def clean_duplicate_visits(df):
    """
    Clean duplicate visits from visit-level data.
    
    The real-time visits logged in the visit-level data set are sometimes prone to 
    tracking errors by Matomo that result in duplicate visits. Such duplicate visits 
    can take the form of true duplicates, where multiple rows contain identical entries 
    but for the visit IDs attached to them. Alternatively, duplicate visits can appear 
    in the form of split visits, where a single visit is split into multiple entries with 
    different visit IDs and visit metrics for the same visit count and visitor ID. 
    When such split visits occur within a small window of time, i.e. within thirty minutes 
    of one another, such split visits represent true splits that should be recombined into 
    the original visits from which they were split. On the other hand, when split visits 
    are spread across large amounts of time, i.e. hours or days, they represent false splits, 
    or truly unique visits that Matomo erroneously attributed the same visit count to, which 
    are cleaned by dropping all but those with the longest visit durations or most activity.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe of visits.
    
    Returns
    -------
    pd.DataFrame
        Dataframe of visits with cleaned duplicates.
    """

    # DROP DUPLICATE VISITS +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # duplicate visits = entries with identical metrics except for visit IDs
    df = df.drop_duplicates(subset=[col for col in df.columns if
                                    col != 'visit_id']).reset_index(drop=True)

    
    # IDENTIFY SPLIT VISITS +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # split visits = visits with duplicate visit counts per visitor
    
    # isolate split visits to be combined or cleaned
    split_df = get_split_visits(df)

    # keep track of initial split visit IDs (for dropping later)
    split_visit_ids = split_df['visit_id']

    # drop split visits with no actions (no use in combining these if nothing to combine)
    split_df = split_df.drop(split_df[split_df['actions'] == 0].index).reset_index(drop=True)

    # add datetime column
    split_df['datetime'] = pd.to_datetime(split_df['date'].astype(str) + ' ' + split_df['time'])
    
    # COMBINE SAME-TIME TRUE SPLITS +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # same-time true splits = split visits occurring at exact same time
    split_df = clean_split_visits(split_df, true_split=True, same_time=True)
    
    # COMBINE DIFFERENT-TIME TRUE SPLITS ++++++++++++++++++++++++++++++++++++++++++++++++++++
    # different-time true splits = split visits occurring within 30 minutes of one another
    split_df = clean_split_visits(split_df, true_split=True, same_time=False)
    
    # CLEAN FALSE SPLITS ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # false splits = split visits occurring more than 30 minutes from each other
    split_df = clean_split_visits(split_df, true_split=False)
    
    # DROP SPLIT VISITS AND REPLACE WITH CLEANED SPLITS +++++++++++++++++++++++++++++++++++++
    df = df.drop(df[df['visit_id'].isin(split_visit_ids)].index)
    df = pd.concat([df, split_df.drop(columns='datetime')],
                   ignore_index=True).sort_values(by='visit_id').reset_index(drop=True)

    # drop remaining duplicate visits, if any
    df = df.drop(df[df.duplicated(subset='visit_id')].index).reset_index(drop=True)
    
    return df


# CLEANING ATYPICAL VISITS ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def drop_hki(df, db_dict):
    """
    Drop visits from Humankind employees and third-party vendors.

    Parameters
    ----------
    df : pd.DataFrame
        Visit-level data.
    db_dict : dict
        Dictionary of database credentials.
    """

    # DROP HUMANKIND EMPLOYEE VISITS ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # read in ip addresses and locations of humankind employees
    cursor, conn = database_connect('hkisocial', db_dict)
    query = """SELECT * FROM ips ORDER BY name, description, start_date"""
    ips = pd.read_sql(query, conn)
    ips.ip = ips.ip.str.rsplit('.', n=2).str[0] + '.0.0'  # anonymize ips
    cursor.close()
    conn.close()

    # merge with visits of same ips and locations
    ip_grp = ips.groupby(['name', 'description', 'ip', 'city', 'region', 'country'])
    vis_grp = df.groupby(['ip', 'city', 'region', 'country', 'date'])
    ipvis = pd.merge(pd.concat([ip_grp.start_date.first(),
                                ip_grp.end_date.last().fillna('9999-99-99')],
                               axis=1).droplevel(['name', 'description']).reset_index(),
                     vis_grp.visit_id.unique().reset_index(), how='left',
                     on=['ip', 'city', 'region', 'country'])

    # isolate visits with select ip-locations within relevant date ranges
    ipvis = ipvis.drop(ipvis[(ipvis.date.astype(str) < ipvis.start_date) |
                             (ipvis.date.astype(str) > ipvis.end_date)].index)
    hki_visits = ipvis.visit_id.explode().tolist()

    # isolate visitors with offending visits
    hki_visitors = df[(df.referrer_type != 'campaign') &  # exclude campaign referrals
                      (df.visit_id.isin(hki_visits))].visitor_id.tolist()

    # drop non-campaign referral entries from humankind employees
    df.drop(df[(df.visitor_id.isin(hki_visitors))].index, inplace=True)

    # DROP VENDORS ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # drop yellow.system visitors
    ys_visits = df[df.country.isin(['Belarus', 'Armenia', 'Georgia'])].visit_id.tolist()
    ys_visitors = df[df.visit_id.isin(ys_visits)].visitor_id.tolist()
    df.drop(df[(df.visitor_id.isin(ys_visitors))].index, inplace=True)
    df.reset_index(drop=True, inplace=True)


def drop_dev(df, db_dict):
    """
    Drop visitors with any visits to the dev sites.

    Parameters
    ----------
    df : pd.DataFrame
        Visit-level data.
    db_dict : dict
        Dictionary of database credentials.
    """

    # get list of unique visitors to dev sites from action log
    cursor, conn = database_connect('hkiweb', db_dict)
    query = """SELECT distinct visitor_id
                 FROM action_log
                WHERE split_part(regexp_replace(url, '(https?://)?(www.)?', ''), '/', 1)
               NOT IN ('humankind.co', 'humankindfunds.com', 'rankings.humankind.co')
            """
    dev = pd.read_sql(query, conn)
    cursor.close()
    conn.close()

    # drop dev-site visitors
    df.drop(df[df.visitor_id.isin(dev.visitor_id)].index, inplace=True)
    df.reset_index(drop=True, inplace=True)


def drop_foreign(df):
    """
    Drop foreign visitors.

    Parameters
    ----------
    df : pd.DataFrame
        Visit-level data.
    """

    # count number of domestic and foreign visits per visitor
    domestic = df.groupby('visitor_id').country.apply(
        lambda x: [i for i in x if i == 'United States']).rename('domestic')
    foreign = df.groupby('visitor_id').country.apply(
        lambda x: [i for i in x if i != 'United States']).rename('foreign')

    # count visitors with more foreign than domestic visits as foreign
    foreign_visitors = foreign[foreign.str.len() > domestic.str.len()].index

    # drop foreign visitors
    df.drop(df[df.visitor_id.isin(foreign_visitors)].index, inplace=True)
    df.reset_index(drop=True, inplace=True)


# CLEANING ACTION FLOWS +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def clean_flow(df, action_type, actions, deltat=0):
    """
    Clean action flows for individual action type.

    Remove duplicate actions, i.e. consecutive actions of same type occurring
    within given time range, from action flows. Update action flow, timestamp, 
    count, and average duration columns with duplicate actions removed.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe of website visits.
    action_type : str
        Type of action for which to clean flows. Valid options are 'pageview',
        'download', 'outlink_click', 'buyetf_click', 'brokerlink_click', 'video_action',
        and 'form_action'. An invalid action flow will cause the
        function to return without making any modifications to the dataframe.
    actions : pd.DataFrame
        Dataframe of individual actions of all type over all visits.
    deltat : int
        Maximum time difference, in seconds, between consecutive actions for which to 
        apply cleaning. Consecutive actions occurring within delta-t seconds of one 
        another will be cleaned, with the latter of the two being removed from the action flow. 
        Default of 0 cleans consecutive actions occurring at exactly the same time only.
    """

    # exit if action type not valid option
    if action_type not in ['pageview',
                           'download',
                           'outlink_click',
                           'buyetf_click',
                           'brokerlink_click',
                           'video_action',
                           'form_action',
                          ]: return df

    # get action string
    action_str = action_type
    if action_type == 'pageview': action_str = 'page'
    elif action_type.split('_')[-1] == 'click': action_str = action_type.split('_')[0]

    # get individual actions and timestamps of given type per visit
    acts_mask = (actions.action_flow.str.endswith('_' + action_type))
    if action_type == 'buyetf_click':
        acts_mask = (actions.action_flow == 'buyetf_click')
    elif action_type.split('_')[-1] == 'action':
        acts_mask = (actions.action_flow.str.split('_', n=1).str[-1].str.split('_').str[0] ==
                     action_type.split('_')[0])  # *_video/form_*
    acts = actions[acts_mask].rename(
        columns={col : col.replace('action', action_str) for col in actions.columns})
    acts[action_str + '_flow'] = acts[action_str + '_flow'].replace(
        '_' + action_type, '', regex=True)

    # find duplicate actions of given type and update action type flow/ts columns
    dupl_mask = ((actions.visit_id == actions.visit_id.shift()) &  # same visit id
                 (actions.action_flow == actions.action_flow.shift()) &  # same action 
                 (actions.action_ts_int - actions.action_ts_int.shift() <= deltat)  # time in range
                )        
    dupl_acts = actions.loc[dupl_mask & acts_mask]
    act_grp = acts.drop(dupl_acts.index).groupby('visit_id')
    flow_cols = [action_str + '_ts']
    if action_type != 'buyetf_click': flow_cols = [action_str + '_flow'] + flow_cols
    for col in flow_cols:
        df[col] = act_grp[col].apply(lambda x: ','.join(x))
        df[col] = df[col].fillna('None')

    # update action type counts and average durations
    df[action_str + 's'] = df[action_str + '_ts'].apply(
        lambda x: 0 if x == 'None' else len(x.split(',')))
    if action_type != 'form_action':
        if action_type != 'pageview':  # modify page action duration instead
            df[action_str + '_duration'] = act_grp[action_str + '_duration'].sum()
            df[action_str + '_duration'] = df[action_str + '_duration'].fillna(0).astype(int)
        df['avg_' + action_str + '_duration'] = (df[action_str + '_duration'] /
                                                 df[action_str + 's']).fillna(0)
    if action_type == 'pageview':
        df.page_action_duration = act_grp[action_str + '_duration'].sum()
        df.page_action_duration = df.page_action_duration.fillna(0).astype(int)
        df.avg_page_action_duration = (df.page_action_duration / df.pages).fillna(0)
    elif action_type == 'form_action':
        df.avg_form_interaction_time = (df.form_interaction_time / df.form_actions).fillna(0)

    # update individual action type counts: subtract duplicate actions from corresponding columns
    dupl_acts = dupl_acts.drop(columns=['action_site_flow', 'action_path_flow', 'action_ts'])
    if action_type == 'buyetf_click': return  # no further columns to update
    elif action_type.split('_')[-1] != 'action':
        dupl_acts.action_flow = dupl_acts.action_flow.str.replace(action_type, action_str + 's')
        if action_type == 'pageview':  # combine individual article post / company ranking pages
            dupl_acts.action_flow = dupl_acts.action_flow.apply(
                lambda x: re.sub('articles-.*_pages', 'article-post_pages', x)).apply(
                lambda x: re.sub('rankings-.*_pages', 'ranked-company_pages', x))
            dupl_acts = dupl_acts.loc[dupl_acts.action_flow != 'page-not-found_pages']
        elif action_type == 'outlink_click':  # combine categories of outlinks
            dupl_acts.action_flow = dupl_acts.action_flow.apply(
                lambda x: re.sub('(linkedin|instagram|youtube|facebook|twitter)_outlinks',
                                 'social_outlinks', x)).apply(
                lambda x: re.sub('(investor|adviserinfo.sec)_outlinks', 'crs_outlinks', x)).apply(
                lambda x: re.sub('(finra|sipc)_outlinks', 'disclosures_outlinks', x))
            # drop article outlinks: no good way to track this category
            df.drop(columns = [col for col in df.columns if
                               col.startswith('articles_outlink')], inplace=True)
        actcols = [col for col in df.columns if col.endswith('_' + action_str + 's')]
        dupl_actcts = dupl_acts.groupby('visit_id').action_flow.apply(lambda x: [i for i in x])
        dupl_actcts = pd.concat([dupl_actcts, pd.DataFrame(columns=actcols)], axis=1).fillna(0)
        for col in actcols:
            dupl_actcts[col] = dupl_actcts.action_flow.apply(
                lambda x: len([i for i in x if i == col]))
            df.loc[df.index.isin(dupl_actcts.index), col] = df[col] - dupl_actcts[col]
    else:  # handle video and form actions separately
        actpre = action_type.split('_')[0]
        if actpre == 'video': subs = ['play', 'pause', 'resume', 'seek', 'finish']
        elif actpre == 'form': subs = ['submission']
        subs = [actpre + '_' + i for i in subs]
        subcols = [col for col in df.columns for i in subs if
                   col == (i + 'es' if i.endswith('sh') else i + 's')]
        actcols = [col for col in df.columns for i in subcols if col.endswith('_' + i)]
        for icol, col in enumerate(subcols):
            dupl_acts.action_flow = dupl_acts.action_flow.str.replace(subs[icol], col)
        dupl_actcts = dupl_acts.groupby(
            'visit_id', group_keys=False).action_flow.apply(lambda x: [i for i in x])
        dupl_actcts = pd.concat(
            [dupl_actcts, pd.DataFrame(columns=subcols+actcols)], axis=1).fillna(0)
        for col in subcols:  # duplicate total subactions
            dupl_actcts[col] = dupl_actcts.action_flow.apply(
                lambda x: len([i for i in x if i.endswith('_' + col)]))
        for col in actcols:  # duplicate subactions by video/form
            dupl_actcts[col] = dupl_actcts.action_flow.apply(
                lambda x: len([i for i in x if i == col]))
        for col in subcols + actcols:
            df.loc[df.index.isin(dupl_actcts.index), col] = df[col] - dupl_actcts[col]
        if actpre == 'video':  # update average video columns
            df.avg_video_watch_time = df.video_watch_time / df.video_plays
            # drop percentages: not easily recalculable with updated play counts
            df.drop(columns = [col for col in df.columns if col in [
                'avg_video_watch_pct', 'avg_video_progress_pct']], inplace=True)

        
def clean_action_flows(df, deltat=0):
    """
    Clean action flows.

    Remove duplicate actions, i.e. consecutive actions of same type occurring at
    once, from action flows. Update action flow, timestamp, count, and average
    duration columns for total and individual action types with duplicate actions removed.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe of website visits.

    Returns
    -------
    pd.DataFrame
        Dataframe of website visits with cleaned action flows.
    deltat : int
        Maximum time difference, in seconds, between consecutive actions for which to 
        apply cleaning. Consecutive actions occurring within delta-t seconds of one 
        another will be cleaned, with the latter of the two being removed from the action flow. 
        Default of 0 cleans consecutive actions occurring at exactly the same time only.
    """

    # set visit id as index
    df.set_index('visit_id', inplace=True)

    # clean action ts columns: replace '0.0' with 'None'
    for col in [col for col in df.columns if col.endswith('_ts')]:
        df[col] = df[col].replace('0.0', 'None')

    # clean up action path flow --> remove split entries for page-not-found pageviews
    bad_flows = df[df.action_flow.str.split(',').str.len() !=
                   df.action_path_flow.str.split(',').str.len()].action_path_flow
    df.loc[df.index.isin(bad_flows.index),
           'action_path_flow'] = bad_flows.str.rstrip(',').apply(
        lambda x: ','.join([i for i in x.split(',') if not
                            i.startswith('<svg') and i not in ['/)', "'"]]))

    # get individual actions and timestamps per visit
    actions = pd.concat([df.action_flow.apply(lambda x: x.split(',')).explode(),
                         df.action_site_flow.apply(lambda x: x.split(',')).explode(),
                         df.action_path_flow.apply(lambda x: x.split(',')).explode(),
                         df.action_ts.apply(lambda x: x.split(',')).explode(),
                         ], axis=1).sort_values(by=['visit_id', 'action_ts']).reset_index()
    actions['action_ts_int'] = actions.action_ts.fillna('None').replace('None', '0').astype(int)

    # find duplicate actions (consecutive same actions within time range) and update flow/ts columns
    dupl_mask = (
        (actions.visit_id == actions.visit_id.shift()) &  # same visit id
        (actions.action_flow == actions.action_flow.shift()) &  # same action
        (actions.action_ts_int - actions.action_ts_int.shift() <= deltat)  # timestamps in range
        )
    act_clean = actions.drop(actions.loc[dupl_mask].index)
    act_clean['action_duration'] = act_clean.groupby(
        'visit_id').action_ts_int.diff(1).shift(-1).abs()
    actions['action_duration'] = act_clean['action_duration']
    act_grp = act_clean.groupby('visit_id')
    for col in ['action_flow', 'action_site_flow', 'action_path_flow', 'action_ts']:
        df[col] = act_grp[col].apply(lambda x: ','.join(x))

    # update action count, action duration, and average duration columns
    df.actions = df.action_flow.apply(lambda x: 0 if x == 'None' else len(x.split(',')))
    df.action_duration = act_grp.action_duration.sum()
    df.action_duration = df.action_duration.fillna(0).astype(int)
    df.avg_action_duration = (df.action_duration / df.actions).fillna(0)

    # clean individual action type flows
    for action_type in ['pageview',
                        'download',
                        'outlink_click',
                        'buyetf_click',
                        'brokerlink_click',
                        'video_action',
                        'form_action',
                        ]: clean_flow(df, action_type, actions, deltat)

    # reset index
    df.reset_index(inplace=True)


def clean_standalone_action(df, action_type, deltat):
    """
    Clean individual action type flow and update overall action flow.

    Remove duplicate actions of given type, i.e. consecutive actions occurring 
    within given time range, from overall and specific action flows. 
    Update action flow, timestamp, count, and average duration columns with 
    duplicate actions removed.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe of website visits.
    action_type : str
        Type of action for which to clean flows. Valid options are 'pageview',
        'download', 'outlink_click', 'buyetf_click', 'brokerlink_click', 
        'video_action', and 'form_action'. An invalid action flow will cause the
        function to return without making any modifications to the dataframe.
    deltat : int
        Maximum time difference, in seconds, between consecutive actions for which to 
        apply cleaning. Consecutive actions occurring within delta-t seconds of one 
        another will be cleaned, with the latter of the two being removed from the action flow. 
        Default of 0 cleans consecutive actions occurring at exactly the same time only.
    """

    # set visit id as index
    df.set_index('visit_id', inplace=True)
    
    # get individual actions and timestamps per visit
    actions = pd.concat([df.action_flow.apply(lambda x: x.split(',')).explode(),
                         df.action_site_flow.apply(lambda x: x.split(',')).explode(),
                         df.action_path_flow.apply(lambda x: x.split(',')).explode(),
                         df.action_ts.apply(lambda x: x.split(',')).explode(),
                         ], axis=1).sort_values(by=['visit_id', 'action_ts']).reset_index()
    actions['action_ts_int'] = actions.action_ts.fillna('None').replace('None', '0').astype(int)
    
    # get individual actions and timestamps of given type per visit
    acts_mask = (actions.action_flow.str.endswith('_' + action_type))
    if action_type == 'buyetf_click':
        acts_mask = (actions.action_flow == 'buyetf_click')
    elif action_type.split('_')[-1] == 'action':
        acts_mask = (actions.action_flow.str.split('_', n=1).str[-1].str.split('_').str[0] ==
                     action_type.split('_')[0])  # *_video/form_*
    
    # find duplicate actions (consecutive same actions within time range) and update flow/ts columns
    dupl_mask = (
        (actions.visit_id == actions.visit_id.shift()) &  # same visit id
        (actions.action_flow == actions.action_flow.shift()) &  # same action
        (actions.action_ts_int - actions.action_ts_int.shift() <= deltat)  # timestamps in range
        )
    # drop duplicate actions of given type
    act_clean = actions.drop(actions.loc[dupl_mask & acts_mask].index)
    act_clean['action_duration'] = act_clean.groupby(
        'visit_id').action_ts_int.diff(1).shift(-1).abs()
    actions['action_duration'] = act_clean['action_duration']
    act_grp = act_clean.groupby('visit_id')
    for col in ['action_flow', 'action_site_flow', 'action_path_flow', 'action_ts']:
        df[col] = act_grp[col].apply(lambda x: ','.join(x))

    # update action count, action duration, and average duration columns
    df.actions = df.action_flow.apply(lambda x: 0 if x == 'None' else len(x.split(',')))
    df.action_duration = act_grp.action_duration.sum()
    df.action_duration = df.action_duration.fillna(0).astype(int)
    df.avg_action_duration = (df.action_duration / df.actions).fillna(0)
    
    # clean individual action type flow
    clean_flow(df, action_type, actions, deltat)
    
    # reset index
    df.reset_index(inplace=True)
    

# FULL VISIT-LEVEL CLEANING PROCEDURE +++++++++++++++++++++++++++++++++++++++++++++++++++++++
def clean_visits(df, db_dict):
    """
    Clean visit-level data.

    Clean up duplicate visits, remove humankind employees and third-party vendors,
    drop foreign visitors, and clean action flows.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe of visit-level data.
    db_dict : dict
        Dictionary of database credentials.

    Returns
    -------
    pd.DataFrame
        Cleaned visit-level data.
    """

    actions = ['action', 'page', 'download', 'outlink', 'buyetf', 'brokerlink',
               'video_action', 'video_play', 'video_pause', 'video_resume',
               'video_seek', 'video_finish', 'form_action', 'form_submission']
    flow_cols = list(set(
        ['visit_id', 'page_action_duration', 'avg_page_action_duration',
         'video_watch_time', 'avg_video_watch_time', 'avg_video_watch_pct',
         'avg_video_progress_pct', 'form_interaction_time', 'avg_form_interaction_time'] +
        [col for col in df.columns if col.endswith('_ts') or col.endswith('_flow')] +
        [col for col in (
            [action + 'es' if action.endswith('sh') else action + 's' for action in actions] +
            [action + '_duration' for action in actions] +
            ['avg_' + action + '_duration' for action in actions]) if col in df.columns] +
        [col for col in df.columns for action in actions if
         col.endswith('_' + action + 'es' if action.endswith('sh') else '_' + action + 's')]))

    df = clean_duplicate_visits(df)
    drop_hki(df, db_dict)
    drop_dev(df, db_dict)
    drop_foreign(df)
    clean_action_flows(df)  # or df[flow_cols] = clean_action_flows(df[flow_cols])

    return df



# MODEL FOR ENGAGEMENT TYPES +++++++++++++++++++++++++++++++++++++++++++++++
def load_default_model():
    """
    Load visit-level engagement types model and corresponding scaler.

    Returns
    -------
    sklearn.estimator
        Fitted Gaussian mixture model.
    sklearn.preprocessor
        Fitted StandardScaler that includes feature names.
    """
    
    data_path = path.join(pathlib.Path(__file__).parent.resolve(), "data")
    d = '2022-10-23'
    scaler = load(path.join(data_path,'gmm_scaler_{}.joblib'.format(d)))
    clf = load(path.join(data_path,'gmm_{}.joblib'.format(d)))

    return clf, scaler


def get_engagement_features(scaler=None):
    """
    Get feature names of required for classifying visit engagement types.

    Parameters
    ----------
    scaler : sklearn.preprocessor
        Fitted StandardScaler with feature names.
    
    Returns
    -------
    list of str
        List of feature names.
    """

    if scaler is None: _, scaler = load_default_model()

    scaler_features = scaler.feature_names_in_.tolist()
    bounce_features = ['visit_count',
                       'visit_duration',
                       'pages',
                       'downloads',
                       'brokerlinks',
                       'video_pauses',
                       'video_resumes',
                       ]
    visit_features = ['visit_id', 'date']

    return list(set(scaler_features + bounce_features + visit_features))

    
def get_bounce_mask(df):
    """
    Create mask for 'new, bounce' cluster

    Parameters
    ----------
    df : pd.DataFrame
        Visit-level data.

    Returns
    -------
    bounce_mask : pd.Series
        mask for selecting the bounce visits out of the df.

    """
    #check that the required columns are present in the dataframe
    col = ['visit_duration',
           'downloads',
           'video_resumes',
           'video_pauses',
           'brokerlinks',
           'visit_count',
           'pages',
           ]
    assert all(c in list(df) for c in col), "One or more columns are missing from df"
    bounce_mask= ((df['visit_duration']==0) 
                  & (df['downloads']==0) & (df['brokerlinks']==0)
                  & (df['visit_count']==1) & (df['pages']<=1)
                  & (df['video_resumes']==0) & (df['video_pauses']==0))
    return bounce_mask


def get_cluster_names(date):
    """
    Provides a map between cluster ids and the names assigned to those clusters

    Parameters
    ----------
    date : str
        The final date for the data set used to derive the names
    
    Returns
    -------
    names : pd.Series
        It has an internal name so that it can be used as a column name upon
        merging with a dataframe.

    """
    if date== '2022-09-20':
        names= pd.Series({
            1: 'return, low engagement',
            0: 'new, low engagement',
            15: 'new, interested',
            19: 'scrolling on pgs with vids',
            13: 'return, medium engagement',
            17: 'advisor home, articles',
            6: 'ETF, articles, return',
            3: 'video watchers',
            2: 'article readers',
            9: 'get started form',
            10: 'articles, downloads, get started',
            8: 'video watchers, high chance of download',
            5: 'video watchers, high chance of download',
            18: 'downloaders, good chance of broker link',
            4: 'downloaders visiting many pgs',
            16: 'downloaders visiting many pgs',
            11: 'top companies, team pg',
            7: 'advisor home, mission',
            14: 'brokerlink clickers',
            12: 'outliers'
            },name='engagement_type')
    else:
        names= pd.Series({
            0: 'new, low engagement', 
            5: 'return, 1pg, no action',
            12: 'scrolling pgs with vids',
            7: 'browsing home pgs',
            19: 'ETF, brokerlinks', #small chance brokerlink?
            11: 'ETF, just looking', #no vids, brokerlinks, downloads. Similar chance of seeing either home pg. 
            17: 'return, low engagement', 
            9: 'article reading', 
            3: 'new, downloads',
            8: 'browsing home pgs',
            16: 'brokerlinks, articles',
            1: 'video watching',
            6: 'downloads, brokerlink',
            13: 'new, visiting many pgs',
            18: 'broad engagement except downloads',
            2: 'get started form',
            10: 'downloads, brokerlink', 
            14: 'research and articles',
            15: 'downloads, videos, team pg, get started',
            4: 'downloads, videos, team pg, get started'
            },name='engagement_type')
    return names
    
    
def assign_cluster(visit, scaler=None, clf=None, cluster_names=None):
    """
    Assign each visit to a cluster based on the trained clustering model.

    Parameters
    ----------
    visit : pd.DataFrame
        Visit-level data. Some features will be normalized to be used as inputs
        for the classifier. If the dataset is too different from the original 
        data set (from 2021-04-01 to 2022-09-20) the scaling may lead to 
        inconsistent results from the classifier
    scaler : sklearn.preprocessor, optional
        Fitted StandardScaler that includes feature names. The default is the
        most recent fitted StandardScaler.
    clf : sklearn.estimator, optional
        Fitted Gaussian mixture model. The default is the most recent fitted 
        model.
    cluster_names : pd.Series, optional.
        A map from cluster id to name. The default is the most recent map.

    Returns
    -------
    engagement : pd.DataFrame
        The index is visit_id and the only column is engagement_type.
    
    Example
    -------
    assign engagement type and merge with the rest of the data:
        engagement= analy_utils.assign_cluster(visit)
        visit.set_index('visit_id', inplace=True)
        visit= visit.join(engagement, how='inner')
    """

    if clf is None or scaler is None: clf, scaler = load_default_model()
    if cluster_names is None: cluster_names = get_cluster_names('')
        
    #check for required features
    if 'articles_duration' not in visit.columns:
        #combine all article time
        visit['articles_duration']= visit.loc[:,['articles_page_action_duration',
                                           'article-post_page_action_duration']].sum(axis=1)
    if 'minutes_since_last_visit' not in visit.columns:
        #convert seconds to minutes
        for col in ['seconds_since_first_visit', 'seconds_since_last_visit']:
            visit['minutes_'+ col.split('_', n=1)[1]]= visit[col]/60
    
    #check that all features are present in the input data
    missing_features= [c for c in scaler.feature_names_in_ if c not in visit.columns]
    assert len(missing_features)==0, f"The following features are missing from visit: {missing_features}"
    
    #fill null values if they exist in these columns
    visit[scaler.feature_names_in_] = visit[scaler.feature_names_in_].fillna(0)
    
    #let the first cluster be the bounce cluster for non-returning visits
    bounce_mask= get_bounce_mask(visit)
    df_bounce= visit.loc[bounce_mask, ['visit_id','date']]
    df_bounce['engagement_type']= "new, bounce"
    df= visit.loc[~bounce_mask, ['visit_id'] + list(scaler.feature_names_in_)]
    
    #apply the preprocessor and the model
    X= scaler.transform(df[scaler.feature_names_in_])
    df['cluster_id']= clf.predict(X)
    
    #assign the names based on cluster id to the corresponding visits
    df= df.merge(cluster_names, how='left', 
                 left_on='cluster_id', right_index=True)
    
    engagement= pd.concat([df[['visit_id','engagement_type']], 
                    df_bounce[['visit_id','engagement_type']]], 
                   ignore_index=True, axis=0)
    engagement.set_index('visit_id', inplace=True)
    return engagement


def get_cluster_grades():
    """
    Get the look up table for the grade and engagement score of each engagement
    type

    Returns
    -------
    grade : pd.DataFrame
        1 row for each engagement type, 3 columns.

    """
    grade= pd.DataFrame([
        ['downloads, brokerlink', 'A'],
        ['return, 1pg, no action', 'A'],
        ['new, visiting many pgs', 'A'],
        ['new, downloads', 'A'],
        ['brokerlinks, articles', 'A'],
        
        ['scrolling pgs with vids','B'],
        ['browsing home pgs', 'B'],
        ['downloads, videos, team pg, get started', 'B'],
        ['ETF, brokerlinks', 'B'],
        ['ETF, just looking','B'],
        ['article reading', 'B'], 
        ['research and articles', 'B'],
        
        ['new, low engagement', 'C'],
        ['video watching', 'C'],
        ['broad engagement except downloads', 'C'],
        
        ['get started form', 'D'],
        ['return, low engagement','D'], 
        
        ['new, bounce', 'F']], 
        columns=['engagement_type','grade'])
    
    value= pd.DataFrame({
        'grade': list('ABCDF'),
        'engagement_score': [4, 3, 2, 1, 0]})
    grade= grade.merge(value, how='left', on='grade')
    
    return grade

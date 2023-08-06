# import the required libraries
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
import seaborn as sns
import argparse as ap
# %matplotlib inline
pd.options.mode.chained_assignment = None  # default='warn'
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)

def highest_duration_ips(df):
    df2 = df.groupby(['source_ip'], as_index=False)["total_duration"].sum().sort_values('total_duration', ascending=[False])
    # print(df2.head(20))
    ips = df2.loc[df2['total_duration'] >= (10**5)]['source_ip']
    print('Source IPs with high duration but most coming from just one destination IP -')
    print('Source IP '+'    Destination IP '+'  Duration '+'    Bytes sent')
    i=0
    for ip in ips:
        durn = df.loc[df['source_ip'] == ip]['total_duration'].max()
        if ((durn) > ((df2.loc[df2['source_ip'] == ip]['total_duration'].max())*0.6)):
            dst_ip = df.loc[df['total_duration'] == durn]['destination_ip'].values
            bytes = df.loc[df['total_duration']== durn]['total_orig_bytes'].values
            print(ip+' - '+dst_ip+' - '+str(durn)+' - '+str(bytes))
            # i+=1
    # print(i)
    while(True):
        optn = int(input('Do you want to see a graph of top 20 source IPs? \n Press 1 for Yes, 0 for No\n'))
        if(optn==1):
            fig = plt.subplots(figsize=(40, 10))
            ax = sns.barplot(x='source_ip', y='total_duration', data=df2.head(20))
            for i in ax.containers:
                ax.bar_label(i,)
            plt.show(block=True)
            i=1
        elif optn== 0:
            break
        else:
            print('Invalid Input. Try Again')
        if(i==1):
            break

def highest_eventcount_ips(df):
    df7 = df.groupby(['source_ip'], as_index=False)["eventcount"].sum().sort_values('eventcount', ascending=[False])
    ips = df7.loc[df7['eventcount'] >= 10000]['source_ip']
    i=0
    k=0
    print('Source IPs with high eventcount but most coming from just one destination IP -')
    print('Source IP '+'    Destination IP '+'  Eventcount '+'    Bytes sent')
    for ip in ips:
        evntcnt = df.loc[df['source_ip'] == ip]['eventcount'].max()
        if (evntcnt) > ((df7.loc[df7['source_ip'] == ip]['eventcount'].max())*0.6):
            dst_ip = df.loc[df['eventcount'] == evntcnt]['destination_ip'].values
            bytes = df.loc[df['eventcount'] ==evntcnt]['total_orig_bytes'].values
            print(ip+' - '+dst_ip+' - '+str(evntcnt)+' - '+str(bytes))
            k+=1
    print(k)
    while (True):
        optn = int(input('Do you want to see a graph of top 20 source IPs? \n Press 1 for Yes, 0 for No\n'))
        if optn==1:
            fig = plt.subplots(figsize=(40, 10))
            ax = sns.barplot(
                x='source_ip', y='eventcount', data=df7.head(20))
            for i in ax.containers:
                ax.bar_label(i,)
                plt.show(block=True)
                i = 1
        elif optn==0:
            break
        else:
            print('Invalid Input. Try Again')
        if (i == 1):
            break

def highest_origpkts_ips(df):
    df51 = df.groupby(['source_ip'], as_index=False)["total_orig_pkts"].sum().sort_values('total_orig_pkts', ascending=[False])
    ips = df51.loc[df51['total_orig_pkts'] >= 1000000]['source_ip']
    i=k=0
    print('Source IPs with high orig pkts but most coming from just one destination IP -')
    print('Source IP '+'    Destination IP '+'  Orig Pkts '+'   Duration '+'  Eventcount ')
    for ip in ips:
        origpkts = df.loc[df['source_ip'] == ip]['total_orig_pkts'].max()
    # vary from 0.6 to more
        if (origpkts) > ((df51.loc[df51['source_ip'] == ip]['total_orig_pkts'].max())*0.95):
            dst_ip = df.loc[df['total_orig_pkts'] == origpkts]['destination_ip'].values
            durn = df.loc[df['total_orig_pkts'] == origpkts]['total_duration'].values
            evntcnt = df.loc[df['total_orig_pkts'] == origpkts]['eventcount'].values
            print(ip+' - '+dst_ip+' - '+str(origpkts)+' - '+str(durn)+' - '+str(evntcnt))
            k+=1
    print(k)
    while (True):
        optn = int(input('Do you want to see a graph of top 20 source IPs? \n Press 1 for Yes, 0 for No\n'))
        if optn==1:
            fig = plt.subplots(figsize=(40, 10))
            ax = sns.barplot(x='source_ip', y='total_orig_pkts', data=df51.head(20))
            for i in ax.containers:
                ax.bar_label(i,)
            plt.show(block=True)
            i = 1
        elif optn==0:
            break
        else:
            print('Invalid Input. Try Again')
        if (i == 1):
            break

def highest_origbytes_ips(df):
    df5 = df.groupby(['source_ip'], as_index=False)["total_orig_bytes"].sum().sort_values('total_orig_bytes', ascending=[False])
    ips = df5.loc[df5['total_orig_bytes'] >= 1000000000]['source_ip']
    i=k=0
    print('Source IPs with high orig bytes but most coming from just one destination IP -')
    print('Source IP '+'    Destination IP ' +'  Orig Bytes '+'   Duration '+'  Eventcount ')
    for ip in ips:
        origbytes = df.loc[df['source_ip'] == ip]['total_orig_bytes'].max()
    # vary from 0.6 to more
        if (origbytes) > ((df5.loc[df5['source_ip'] == ip]['total_orig_bytes'].max())*0.6):
            dst_ip = df.loc[df['total_orig_bytes'] == origbytes]['destination_ip'].values
            durn = df.loc[df['total_orig_bytes'] ==origbytes]['total_duration'].values
            evntcnt = df.loc[df['total_orig_bytes'] == origbytes]['eventcount'].values
            print(ip+' - '+dst_ip+' - '+str(origbytes) +' - '+str(durn)+' - '+str(evntcnt))
            k+=1
    print(k)
    while (True):
        optn = int(input('Do you want to see a graph of top 20 source IPs? \n Press 1 for Yes, 0 for No\n'))
        if optn==1:
            fig = plt.subplots(figsize=(40, 10))
            ax = sns.barplot(x='source_ip', y='total_orig_bytes', data=df5.head(20))
            for i in ax.containers:
                ax.bar_label(i,)
            plt.show(block=True)
            i = 1
        elif optn==0:
            break
        else:
            print('Invalid Input. Try Again')
        if (i == 1):
            break

def highest_respbytes_ips(df):
    df61 = df.groupby(['destination_ip'], as_index=False)["total_resp_bytes"].sum().sort_values('total_resp_bytes', ascending=[False])
    ips = df61.loc[df61['total_resp_bytes'] >= 10**9]['destination_ip']
    i=k=0
    print('Destination IPs with high bytes but most coming from just one source IP -')
    print('Destination IP '+'    Source IP ' +'  Resp Bytes '+'   Duration '+'  Eventcount ')
    for ip in ips:
        respbytes = df.loc[df['destination_ip'] == ip]['total_resp_bytes'].max() # vary from 0.6 to more
        if (respbytes) > ((df61.loc[df61['destination_ip'] == ip]['total_resp_bytes'].max())*0.6):
            src_ip = df.loc[df['total_resp_bytes'] == respbytes]['source_ip'].values
            durn = df.loc[df['total_resp_bytes'] == respbytes]['total_duration'].values
            evntcnt = df.loc[df['total_resp_bytes'] == respbytes]['eventcount'].values
            print(ip+' - '+src_ip+' - '+str(respbytes) +' - '+str(durn)+' - '+str(evntcnt))
            k+=1
    print(k)
    while (True):
        optn = int(input('Do you want to see a graph of top 20 destination IPs? \n Press 1 for Yes, 0 for No\n'))
        if optn==1:
            fig = plt.subplots(figsize=(40, 10))
            ax = sns.barplot(x='destination_ip', y='total_resp_bytes', data=df61.head(20))
            for i in ax.containers:
                ax.bar_label(i,)
            plt.show(block=True)
            i = 1
        elif optn==0:
            break
        else:
            print('Invalid Input. Try Again')
        if (i == 1):
            break

def highest_resppkts_ips(df):
    df6 = df.groupby(['destination_ip'], as_index=False)["total_resp_pkts"].sum().sort_values('total_resp_pkts', ascending=[False])
    ips = df6.loc[df6['total_resp_pkts'] >= 10**7]['destination_ip']
    i=k=0
    print('Destination IPs with high pkts but most coming from just one source IP -')
    print('Destination IP '+'    Source IP ' +'  Resp Pkts '+'   Duration '+'  Eventcount ')
    for ip in ips:
        resppkts = df.loc[df['destination_ip'] == ip]['total_resp_pkts'].max()
    # vary from 0.6 to more
        if (resppkts) > ((df6.loc[df6['destination_ip'] == ip]['total_resp_pkts'].max())*0.6):
            src_ip = df.loc[df['total_resp_pkts'] == resppkts]['source_ip'].values
            durn = df.loc[df['total_resp_pkts'] == resppkts]['total_duration'].values
            evntcnt = df.loc[df['total_resp_pkts'] == resppkts]['eventcount'].values
            print(ip+' - '+src_ip+' - '+str(resppkts) +' - '+str(durn)+' - '+str(evntcnt))
            k+=1
    print(k)
    while (True):
        optn = int(input(
            'Do you want to see a graph of top 20 destination IPs? \n Press 1 for Yes, 0 for No\n'))
        if optn==1:
            fig = plt.subplots(figsize=(40, 10))
            ax = sns.barplot(
                x='destination_ip', y='total_resp_pkts', data=df6.head(20))
            for i in ax.containers:
                ax.bar_label(i,)
            plt.show(block=True)
            i = 1
        elif optn==0:
            break
        else:
            print('Invalid Input. Try Again')
        if (i == 1):
            break

def highest_ports(df):
    # Removing entries with destination ports less than 10
    i=0
    df12 = df[df['destination_port'] > 10]
    # ax = df.plot.barh()
    print('The Top 20 used ports,with their count, are \n')
    print(df12['destination_port'].value_counts().head(20))
    while (True):
        optn = int(input('Do you want to see a graph of top 20 destination ports? \n Press 1 for Yes, 0 for No\n'))
        if optn==1:
            fig = plt.subplots(figsize=(40, 10))
            ax = df12['destination_port'].value_counts()[:20].plot(kind='bar', xlabel='Destination Port', ylabel='Count', title='Top 20 Ports', figsize=(15, 10))
            ax.bar_label(ax.containers[0])
            plt.show(block=True)
            i = 1
        elif optn==0:
            break
        else:
            print('Invalid Input. Try Again')
        if (i == 1):
            break

def lowest_ports(df):
    print('Least used Ports but with high periodic probability - \n')
    df1 = df['destination_port'].value_counts().rename_axis('destination_port').reset_index(name='count')
    df1 = df1[df1['count'] == 1].reset_index(drop=True)
    df11 = pd.merge(df1, df, on=['destination_port'])
    print(df11[df11['periodic_prob'] > 0.7].sort_values('periodic_prob', axis=0, ascending=False)[['destination_port', 'count', 'source_ip', 'destination_ip', 'eventcount', 'num_src_ports', 'total_duration', 'total_orig_bytes', "total_orig_pkts", 'total_resp_bytes', 'total_resp_pkts']])

def connstates(df):
    df4 = df
    for column in df4.columns:
        if 'connstate_' in column:
            df4[column] = (df4[column]/df4['eventcount'])*100
    print(df4[(df4['connstate_REJ'] > 50) & (df4['periodic_prob'] > 0.8)][['source_ip', 'destination_ip', 'destination_port','eventcount','periodic_prob','num_src_ports', 'total_duration', 'total_orig_bytes', "total_orig_pkts", 'total_resp_bytes', 'total_resp_pkts']].sort_values('periodic_prob',ascending=False))
    # df4[(df4['connstate_RSTO']>50)&(df4['total_orig_bytes']>(10**7))] # vary for pkts too
    # df4[(df4['connstate_RSTR']>50)&(df4['total_orig_bytes']>(10**7))]
    # df4[(df4['connstate_SF']<10)&(df4['total_orig_bytes']>(10**7))]
    # df4[(df4['connstate_RSTO']>50)&(df4['total_orig_pkts']>(10**6))]
    # print(df4[(df4['connstate_REJ'] > 50) & (df4['total_orig_pkts'] > (10**6))])
    print('\n\n')
    print(df4[(df4['connstate_S0'] > 50) & (df4['periodic_prob'] > 0.8)][['source_ip', 'destination_ip', 'destination_port','eventcount','periodic_prob','num_src_ports', 'total_duration', 'total_orig_bytes', "total_orig_pkts", 'total_resp_bytes', 'total_resp_pkts']].sort_values('periodic_prob',ascending=False))

def multiple_ports_scan(df):
    # Check if a source IP is connecting to a destination IP on multiple ports
    df20 = df.groupby(['source_ip', 'destination_ip'], as_index=False)[['total_duration', 'eventcount', 'total_orig_bytes','total_orig_pkts', 'total_resp_bytes', 'total_resp_pkts']].sum().sort_values('total_duration', ascending=False)
    df30 = df.groupby(['source_ip', 'destination_ip'], as_index=False).agg({"destination_port": "count"}).rename(columns={'destination_port': 'distinct_ports'}).sort_values("distinct_ports", ascending=False).reset_index(drop=True)
    df40 = pd.merge(df30, df20, on=['source_ip', 'destination_ip']).sort_values('distinct_ports', ascending=False)
    print('Source IPs that connect to a specific destination IP on multiple(more than 1) ports are -')
    print(df40[df40['distinct_ports'] > 5])
    print('\n')
    print('Source IPs that connect to various destination IPs on more than 5 ports(high chance of port scanning) are - ')
    df31 = df30[df30["distinct_ports"] > 5].groupby("source_ip", as_index=False).agg({"destination_ip": "count"}).rename(columns={'destination_ip': 'Connections_using_5+ports'}).sort_values("Connections_using_5+ports", ascending=False)
    print(df31.head(25))

def src_ip_ports(df):
    df8 = pd.DataFrame(df.groupby(['source_ip']).destination_port.apply(set)).reset_index()
    df8['count'] = 0
    i = 0
    for ports in df8['destination_port']:
        df8['count'][i] = len(ports)
        i += 1
    df8 = df8.sort_values('count', ascending=False)
    # df81 = df8[df8['count'] > 10]
    print('Source IPs that connect to the most distinct number of ports are - ')
    print(df8[df8['count']>10])

def basic_summary(df):
    print('Top used ports with their counts are -')
    df13 = df[df['destination_port'] >= 10]
    # ax = df.plot.barh()
    # print('The Top 20 used ports,with their count, are \n')
    print(df13['destination_port'].value_counts().head(20))
    print('Source IPs with highest eventcounts are - ')
    print(df.groupby(['source_ip'], as_index=False)["eventcount"].sum().sort_values('eventcount', ascending=[False]).head(20))
    print('Source IPs sending the highest amount of bytes are - ')
    print(df.groupby(['source_ip'], as_index=False)["total_orig_bytes"].sum().sort_values('total_orig_bytes', ascending=[False]).head(20))
    print('Destination IPs receiving highest bytes are - ')
    print(df.groupby(['destination_ip'], as_index=False)["total_resp_bytes"].sum().sort_values('total_resp_bytes', ascending=[False]).head(20))
    print('Source IPs with highest durations are - ')
    print(df.groupby(['source_ip'], as_index=False)["total_duration"].sum().sort_values('total_duration', ascending=[False]).head(20))
    print('Source IP and Destination IP pairs that connect on multiple ports - ')
    # df20 = df.groupby(['source_ip', 'destination_ip'], as_index=False)[['total_duration', 'eventcount', 'total_orig_bytes','total_orig_pkts', 'total_resp_bytes', 'total_resp_pkts']].sum().sort_values('total_duration', ascending=False)
    # df30 = df.groupby(['source_ip', 'destination_ip'], as_index=False).agg({"destination_port": "count"}).rename(columns={'destination_port': 'distinct_ports'}).sort_values("distinct_ports", ascending=False).reset_index(drop=True)
    # df40 = pd.merge(df30, df20, on=['source_ip', 'destination_ip']).sort_values('distinct_ports', ascending=False)
    # print(df.groupby(['source_ip', 'destination_ip'], as_index=False).agg({"destination_port": "count"}).rename(columns={'destination_port': 'distinct_ports'}).sort_values("distinct_ports", ascending=False).reset_index(drop = True).head(20))
    df3 = df.groupby(['source_ip', 'destination_ip'], as_index=False).agg({"destination_port": "count"}).rename(columns={'destination_port': 'distinct_ports'}).sort_values("distinct_ports", ascending=False)
    df3 = df3.reset_index(drop=True)
    print(df3.head(20))

if __name__ == '__main__':
    print('Welcome to the BARC Network Analytics script')
    parser = ap.ArgumentParser()
    parser.add_argument("--file", "-f", type=str, required=True)
    args = parser.parse_args()
    # print(args.file)
    with open(args.file) as file:
        try:
            df = pd.read_json(file,lines=True)
        except:
            try:
                df = pd.read_json(file) #reading the log file
            except:
                print("Corrupted file/Not in format")
                exit()
    df.fillna(0,inplace=True) # filling the NaN/Null entries with 0
    # print(df.columns)
    while(True):
        print('Press 1 for a detailed prompt based result\nPress 2 for a brief summary based result\nPress 0 to exit.')
        opt = int(input())
        if(opt==1):
            while(True):
                print("Select from the following menu: \n Press 1 for Source IPs with highest duration \n Press 2 for Source IPs with highest eventcount\n Press 3 for Source IPs sending highest bytes\n Press 4 for Source IPs sending highest packets\n Press 5 for destination IPs receiving highest bytes\n Press 6 for destination IPs receiving highest packets\n Press 7 for the maximum used Destination Ports\n Press 8 for the least used Ports\n Press 9 for connstates\n Press 10 to show the stats about multiple ports scan \n Press 11 to show most distinct ports connected to by Source IPs\n Press 0 to exit.")
                choice = int(input())
                if(choice==0):
                    break
                elif choice==1:
                    highest_duration_ips(df)
                elif choice== 2:
                    highest_eventcount_ips(df)
                elif choice== 3:
                    highest_origbytes_ips(df)
                elif choice== 4:
                    highest_origpkts_ips(df)
                elif choice== 5:
                    highest_respbytes_ips(df)
                elif choice== 6:
                    highest_resppkts_ips(df)
                elif choice== 7:
                    highest_ports(df)
                elif choice== 8:
                    lowest_ports(df)
                elif choice== 9:
                    connstates(df)
                elif choice== 10:
                    multiple_ports_scan(df)
                elif choice== 11:
                    src_ip_ports(df)
                else:
                    print('Invalid input. Try again')
        elif(opt==2):
            basic_summary(df)
        elif(opt==0):
            break
        else:
            print('Invalid input. Try again')
    print('Thank you for using.')
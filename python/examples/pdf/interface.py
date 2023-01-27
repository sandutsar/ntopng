#!/usr/bin/env python3

"""
Sample PDF report creation script using the ntopng Python API to collect traffic information
"""

import os
import sys
import time
import getopt
import pandas as pd
from fpdf import FPDF
import plotly.figure_factory as ff
import plotly.graph_objects as go

sys.path.insert(0, '../../')

from ntopng.ntopng import Ntopng

### NTOPNG API SETUP
username     = "admin"
password     = "admin"
ntopng_url   = "http://localhost:3000"
iface_id     = 0
auth_token   = None
enable_debug = False
output_file  = "report.pdf"

actual_ts = int(time.time())
yesterday = (actual_ts - 86400)

##########

def usage():
    print("interface.py [-u <username>] [-p <password>] [-t <auth token>] [-n <ntopng_url>]")
    print("             [-i <interface ID>] [--debug] [--help]")
    print("")
    print("Example: ./interface.py -t ce0e284c774fac5a3e981152d325cfae -i 4")
    print("         ./interface.py -u ntop -p mypassword -i 4")
    sys.exit(0)

##########

try:
    opts, args = getopt.getopt(sys.argv[1:],
                               "hdu:p:n:i:t:",
                               ["help",
                                "debug",
                                "username=",
                                "password=",
                                "ntopng_url=",
                                "iface_id=",
                                "auth_token="]
                               )
except getopt.GetoptError as err:
    print(err)
    usage()
    sys.exit(2)

for o, v in opts:
    if(o in ("-h", "--help")):
        usage()
    elif(o in ("-d", "--debug")):
        enable_debug = True
    elif(o in ("-u", "--username")):
        username = v
    elif(o in ("-p", "--password")):
        password = v
    elif(o in ("-n", "--ntopng_url")):
        ntopng_url = v
    elif(o in ("-i", "--iface_id")):
        iface_id = v
    elif(o in ("-t", "--auth_token")):
        auth_token = v

##################################
######### DATA COLLECTOR #########
##################################

print("Connecting to ntopng...")

try:
    my_ntopng = Ntopng(username, password, auth_token, ntopng_url)

    if(enable_debug):
        my_ntopng.enable_debug()        
except ValueError as e:
    print(e)
    os._exit(-1)

print("Collecting data...")

try:
    my_interface = my_ntopng.get_interface(iface_id)
    my_historical = my_ntopng.get_historical_interface(iface_id)

except ValueError as e:
    print(e)
    os._exit(-1)

def get_alerts_severity():
    """
    Return a dataframe with alerts and severity
    """

    alert_count_severity = my_historical.get_alerts_stats(yesterday, actual_ts) 
    alert_severity_df = pd.DataFrame(alert_count_severity[0]["value"])
    alert_severity_df.drop(["key", "title"], axis= 1, inplace=True)
    return alert_severity_df

def get_top_client_server():
    """
    Return a dataframe with top clients and servers seen on the interface specified in the above script init data
    """

    top_client_server = my_historical.get_flow_alerts_stats(yesterday, actual_ts) 
    top_client_server_df = pd.DataFrame(top_client_server[0]["value"])
    top_client_server_df.drop(["key", "value"], axis= 1, inplace=True)
    return top_client_server_df

def get_host_info(ip):
    """
    Return a dataframe with alerts and severity
    :param ip: ip of the desired host to get data of
    """

    my_host = my_interface.get_host(ip)

    return my_host

def get_upload_download():
    """
    Return a list where => data[0] = uploaded MB, data[1] = downloaded MB for the interface specified in the above script init data
    """

    up_down = my_historical.get_interface_timeseries("iface:traffic_rxtx", yesterday, actual_ts)
    data = [(up_down["bytes_sent"].sum()/1000000), (up_down["bytes_rcvd"].sum()/1000000)] 
    
    return data

def get_interface_data():
    """
    Return a dict with info about the interface specified in the above script init data
    """

    host_data = my_interface.get_data()

    host_info = {"flow_count": host_data["num_flows"], "local_hosts": host_data["num_local_hosts"], "hosts_count": host_data["num_hosts"], "local_hosts_anomalies": host_data["num_local_hosts_anomalies"], "alerted_flows": host_data["alerted_flows"], "num_flows": host_data["num_flows"],
                "flows_warning": host_data["alerted_flows_warning"], "flows_error": host_data["alerted_flows_error"]}
    
    return host_info

def get_interfaces():
    """
    Return a df with a list of all the interfaces
    """

    interfaces = my_ntopng.get_interfaces_list()
    interfaces_df = pd.DataFrame(interfaces)
    interfaces_df.drop("name", axis=1, inplace=True)

    return interfaces_df

def get_interfaces_count():
    """
    Return number of interfaces
    """
    interfaces = my_ntopng.get_interfaces_list()
    return len(interfaces)
##################################
############# UTILS ##############
##################################

def delete_file(fname):
    """
    Deletes the table png from the current path
    :param fname: name of png to delete
    """
    current_dir = os.getcwd()
    path = current_dir+"/"+fname

    try:
        os.path.exists(path)
        os.remove(path)

    except Exception as e:
        print(f"FILE: {path} DOES NOT EXIST...")
        os._exit(-1)

def df_to_table_png(df, fname):
    """
    Return creates a png of the df specified with name
    :param df: dataframe to save to png
    :param fname: name of the file to save
    """
    fig = ff.create_table(df, colorscale=[[0, "#f3a114"], [.5, "#d9d9d9"], [1, "#ffffff"]])
    fig.update_layout(autosize=False, width=1100, height=350)
    fig.write_image(str(fname), scale=2)

def plot_up_down(output_series_fname):
    """
    Plots a png of the timeseries
    """
    up_down = my_historical.get_interface_timeseries("iface:traffic_rxtx", yesterday, actual_ts)
    up_down.reset_index(inplace=True)
    up_down['ts'] = up_down['index'].apply(lambda x: x.left)
    up_down['ts'] = pd.to_datetime(up_down['ts'], unit='s')
    
    layout = dict(plot_bgcolor='rgba(255,255,255, 0.3)')
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Scatter(x=up_down["ts"], y=up_down["bytes_rcvd"],
                        mode='lines',
                        name='Downloaded bytes',
                        line_color='#f3a114'))
    fig.add_trace(go.Scatter(x=up_down["ts"], y=up_down["bytes_sent"],
                        mode='lines',
                        name='Uploaded bytes',
                        line_color='#000000'))
    #fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='black')
    #fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='black')

    fig.write_image(output_series_fname, width=1280, height=720)

##################################
######## DATA COLLECTION #########
##################################
created_files = []

interfaces_count = get_interfaces_count()
data_sent_rcvd = get_upload_download()
interface_data = get_interface_data()

#interfaces table
#interfaces_df = get_interfaces()
#interfaces_df_fname = "interfaces_table.png"
#created_files.append(interfaces_df_fname)
#df_to_table_png(interfaces_df, interfaces_df_fname)

#alerts table
alerts_df = get_alerts_severity()
alerts_df.columns = ["Alert Type", "Score", "Alert occurrence %"]

alerts_df_fname = "alerts_table.png"
created_files.append(alerts_df_fname)
df_to_table_png(alerts_df, alerts_df_fname)

#client/server table
hosts_df = get_top_client_server()
hosts_df.columns = ["Host occurrence %", "Vlan", "IP", "Host Name"]
hosts_df = hosts_df[["Host Name", "IP", "Host occurrence %", "Vlan"]]
hosts_df

hosts_df_fname = "hosts_table.png"
created_files.append(hosts_df_fname)
df_to_table_png(hosts_df, hosts_df_fname)

## UPLOADED/DOWNLOADED IN MB
uploaded = data_sent_rcvd[0]
downloaded = data_sent_rcvd[1]

## INFO FOR SPECIFIED IFID
flows = interface_data["num_flows"]
host_num = interface_data["hosts_count"]
local_hosts_num = interface_data["local_hosts"]
flows_errors = interface_data["flows_error"]
flows_warnings = interface_data["flows_warning"]

##################################
########## PDF CREATION ##########
##################################

MARGIN = 10
pw = 25 - 2*MARGIN
ch = 50
pdf = FPDF()
pdf.add_page()

## LOGO
pdf.image("img/ntop.png", x=140, y=8, w=68.2, h=17.8)

## HOST PC SPECS AND STATS  ##
pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(r= 0, g= 0, b = 0)
pdf.ln(9)
pdf.cell(w=0, h=10, txt="NTOPNG INFO", ln=1)
pdf.set_font("Helvetica", "", 11)
pdf.cell(w=0, h=5, txt=f"URL: {ntopng_url}")
pdf.ln(5)
pdf.cell(w=0, h=5, txt=f"Date: {time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(actual_ts))}")
pdf.ln(5)
pdf.cell(w=0, h=5, txt=f"Number of Interfaces: {interfaces_count}")
pdf.ln(7)

##  24hr stats  ##
pdf.set_font("Helvetica", "B", 14)
pdf.cell(w=0, h=10, txt="24h STATS")
pdf.ln(5)
pdf.set_font("Helvetica", "", 11)
pdf.cell(w=(pw/2), h=(ch/4), txt=f"Active Flows: {flows}")
pdf.ln(5)
pdf.cell(w=(pw/2), h=(ch/4), txt=f"Number of Hosts: {host_num}")
pdf.ln(5)
pdf.cell(w=(pw/2), h=(ch/4), txt=f"Number of Local Hosts: {local_hosts_num}")
pdf.ln(5)
pdf.cell(w=(pw/2), h=(ch/4), txt=f"Data Up/Down: {uploaded:.3f}/{downloaded:.3f} MB")
pdf.ln(5)
pdf.cell(w=(pw/2), h=(ch/4), txt=f"Flows errors: {flows_errors}")
pdf.ln(5)
pdf.cell(w=(pw/2), h=(ch/4), txt=f"Flows warnings: {flows_warnings}")
pdf.ln(5)

# Alerts
pdf.image(alerts_df_fname, x=10, y=75, w=190, h=65)

## Hosts
pdf.image(hosts_df_fname, x=10, y=135, w=190, h=65)

# Series plot
series_fname = "series.png"
created_files.append(series_fname)
plot_up_down(series_fname)
pdf.image(series_fname, x=10, y=210, w=190, h=85)

print("Generating PDF...")

pdf.output(f"./{output_file}", "F")

for file in created_files:
    delete_file(file)


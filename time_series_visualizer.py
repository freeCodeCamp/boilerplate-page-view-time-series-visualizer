import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import dates as mpl_dates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df =  pd.read_csv('fcc-forum-pageviews.csv',index_col= 'date' ,parse_dates= True)


# Clean data
f25 = df['value'] <= df['value'].quantile(0.025)
f75 = df['value'] >= df['value'].quantile(0.975)
cond = (f25 | f75)
df = df.drop(index=df[cond].index)

def draw_line_plot():
    # Draw line plot
    fig,ax = plt.subplots()


    ax = df['value'].plot(use_index = True, figsize=(14, 6), linewidth=1,color = 'red')
    # ax = plt.plot(df)
    plt.xticks(rotation = 0)
    plt.xlabel('Date',labelpad = 15,fontsize = 12)
    plt.ylabel('Page Views',labelpad = 15,fontsize = 12)
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019',fontsize = 15)
    date_format = mpl_dates.DateFormatter('%Y-%m')
    ax.xaxis.set_major_formatter(date_format)
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    
    list_month=['January','February','March','April','May','June','July','August','September','October','November','December']

    df_bar = df.copy()
    df_bar['year']= df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')
    df_grp = df_bar.groupby(['year','month'])
    df_grp['value'].apply(lambda x : x.mean())
        # Draw bar plot
    g = sns.catplot(height = 8,x="year", kind="bar", hue="month", y="value", data=df_bar, hue_order=list_month, ci=None, legend=False,palette = 'tab10')

    fig = g.fig
    ax = g.ax  
    ax.set_ylabel('Average Page Views',fontsize =15 )
    ax.set_xlabel('Years',fontsize =15 )
    plt.xticks(rotation=90)
    plt.legend(loc='upper left', title="Month")
    plt.setp(ax.get_legend().get_texts(), fontsize=12)
    plt.setp(ax.get_legend().get_title(), fontsize=10)
    plt.tight_layout()
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    df_box.sort_values(by=['year','date'], ascending=[False, True], inplace=True)

    fig , (ax1,ax2) = plt.subplots(1,2,figsize=(20,8))

    sns.boxplot(ax = ax1 , data = df_box, x = df_box['year'] , y= df_box['value'])
    sns.boxplot(ax = ax2 , data = df_box, x = df_box['month'] , y= df_box['value'])

    ax1.set(xlabel="Year", ylabel="Page Views", title="Year-wise Box Plot (Trend)")

    ax2.set(xlabel="Month", ylabel="Page Views", title="Month-wise Box Plot (Seasonality)")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

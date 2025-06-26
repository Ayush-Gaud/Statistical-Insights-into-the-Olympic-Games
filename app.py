import streamlit as st
import pandas as pd
import plotly.express as px
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

# --- DATASET --- #
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, region_df)

# --- SIDEBAR --- #
st.sidebar.markdown(
    "<h1 style='font-size:36.5px;'>Olympics Analysis</h1>",
    unsafe_allow_html=True
)
st.sidebar.image('pngtree-olympic-rings-colorful-rings-on-a-white-background-png-image_4825904.png', width=300)
st.sidebar.markdown("---")

user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)
# st.dataframe(df)

# --- MEDAL TALLY --- #
if user_menu=='Medal Tally':
    st.markdown(
        "<h1 style='text-align: center; font-size: 48px;'>Medal Tally</h1>",
        unsafe_allow_html=True
    )
    st.sidebar.markdown("---")
    years, country = helper.country_year_list(df)

    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Select a Year", years)
    with col2:
        selected_country = st.selectbox("Select a Country", country)

    st.markdown("---")
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_country == 'Overall' and selected_year == 'Overall':
        st.title("Overall Tally of Medals")
    elif selected_country == 'Overall' and selected_year != 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    elif selected_country != 'Overall' and selected_year == 'Overall':
        st.title(selected_country + " 's Overall Tally of Medals")
    elif selected_country != 'Overall' and selected_year != 'Overall':
        st.title(selected_country + " 's Overall Tally of Medals in " + str(selected_year) + " Olympics")

    st.dataframe(medal_tally)
    st.markdown("---")

# --- OVERALL ANALYSIS --- #
if user_menu=='Overall Analysis':
    st.markdown(
        "<h1 style='text-align: center; font-size: 48px;'>Overall Analysis</h1>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    editions = df['Year'].unique().shape[0]-1  # 1906 is not counted as Olympics
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Statistical Insights")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    st.markdown("---")
    nations_over_time = helper.data_over_time(df, 'region', 'No. of Countries')
    fig = px.line(nations_over_time, x="Edition", y="No. of Countries")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)
    st.markdown("---")

    events_over_time = helper.data_over_time(df, 'Event', 'No. of Events')
    fig = px.line(events_over_time, x="Edition", y="No. of Events")
    st.title("No. of Events over the years")
    st.plotly_chart(fig)
    st.markdown("---")

    athletes_over_time = helper.data_over_time(df, 'Name', 'No. of Athletes')
    fig = px.line(athletes_over_time, x="Edition", y="No. of Athletes")
    st.title("Athletes over the years")
    st.plotly_chart(fig)
    st.markdown("---")

    st.title("No. of Events over time (Every sport)")
    fig,ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)
    st.markdown("---")

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox("Select a Sport", sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)
    st.markdown("---")

# --- COUNTRY-WISE ANALYSIS --- #
if user_menu=='Country-wise Analysis':
    st.markdown(
        "<h1 style='text-align: center; font-size: 48px;'>Country-wise Analysis</h1>",
        unsafe_allow_html=True
    )
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    country_list.insert(0, 'Overall')
    selected_country = st.selectbox("Select a Country", country_list)
    st.markdown("---")

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")

    if selected_country == 'Overall':
        st.title(selected_country + " Medal Tally over the years")
    else:
        st.title(selected_country + "'s Medal Tally over the years")
    st.plotly_chart(fig)
    st.markdown("---")

    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    if selected_country != 'Overall' and pt.size != 0:
        st.title(selected_country + " excels in the following sports")
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)

    st.markdown("---")
    if selected_country != 'Overall':
        st.title("Top 10 Athletes of " + selected_country)
        top10_df = helper.most_successful_countrywise(df, selected_country)
        st.table(top10_df)
    st.markdown("---")

# --- ATHLETE-WISE ANALYSIS --- #
if user_menu=='Athlete-wise Analysis':
    st.markdown(
        "<h1 style='text-align: center; font-size: 48px;'>Athlete-wise Analysis</h1>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna().astype(int)
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna().astype(int)
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna().astype(int)
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna().astype(int)

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=700, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)
    st.markdown("---")

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Sailing', 'Badminton', 'Gymnastics', 'Art Competitions',
                     'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey',
                     'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling',
                     'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball', 'Archery', 'Volleyball',
                     'Synchronized Swimming', 'Table Tennis', 'Baseball', 'Rhythmic Gymnastics',
                     'Rugby Sevens', 'Beach Volleyball', 'Triathlon', 'Rugby', 'Ice Hockey', 'Polo',
                     'Figure Skating', 'Trampolining', 'Modern Pentathlon', 'Motorboating']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna().astype(int))
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=700, height=600)
    st.title("Distribution of Age by Sports (Gold Medalist)")
    st.plotly_chart(fig)
    st.markdown("---")

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox("Select a Sport", sport_list)

    temp_df = helper.weight_vs_height(df, selected_sport)

    st.title("Height vs Weight")
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=50)
    st.pyplot(fig)
    st.markdown("---")

    st.title("Men vs Women Participation over the years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    st.plotly_chart(fig)
    st.markdown("---")

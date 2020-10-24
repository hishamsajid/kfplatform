import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
import rioxarray
import rasterio
import os
import pyproj
import altair as alt
import seaborn as sns
import matplotlib.ticker as mtick

from shapely.geometry import mapping
from shapely.geometry import Point
from shapely.wkt import loads
from shapely.geometry import shape
from shapely.ops import transform
from rasterio import plot
from functools import partial
from geopy.geocoders import Nominatim
from random import randint

import seaborn as sns
import matplotlib.pyplot as plt

import folium
import plotly.graph_objects as go
from branca.colormap import linear
from folium import FeatureGroup


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']+.02, point['y'], str(point['val']))
        
khi_districts_gpd = gpd.read_file('data/shape_files/processed/khi_districts.shp')

karachi_districts = list(khi_districts_gpd.DISTRICT)

# distircts_set = set(list(khi_districts_gpd.DISTRICT))
st.image('data/images/logo/logo_snipped.png')
#dev/data/img/KF_Logo_02.png

navigation = st.sidebar.radio('Navigation',('HOME','COMPARE DISTRICTS','COMPARE UCs','MY AREA'))

if (navigation=='HOME'):

    """
    [Karachi Futures](http://karachifutures.com/) is a research initiative + tech shop aiming to understand the social and economic 
    problems of Karachi in a much more deeper quantitative and qualitative sense. Our role is to research factors that may influence 
    the future of Karachi, with the purposeof enabling a much smarter, digital enabled and overall better city – ready to leapfrog into the 4th Industrial Revolution.

    ## How does this app work?

    The Normalized Difference Vegetation Index (NDVI) is a simple graphical indicator that can be used to analyze remote sensing 
    measurements, often from a space platform, assessing whether or not the target being observed contains live green vegetation. 
    
    For this experiment, we take LANDSAT8 images from February 2019 and calculate and aggregate NDVI values for different parts
    of Karachi. All data and technology used for this experiment in open source. 

    ## NDVI Range

    We calculate the NDVI value of each pixel between 0 and 1, where 1 is the highest level of live green vegetation. For this experiment,
    we have kept the threshold for classifying a pixel as green at `0.0982` as per this [research paper](https://www.researchgate.net/publication/337101410_Evaluating-Spatial-Patterns_of_Urban_Green_Spaces_in_Karachi_Through_Satellite_Remote_Sensing)
    by the Departent of Geography at the University of Punjab published in 2016.

    To explore different parts of this app, please use the sidebar to the left. 
    """


if (navigation=='COMPARE DISTRICTS'):

    """
    ### Karachi district/cantonment level comparisons
    """

    select_district = st.selectbox(
        'What area would you like to view?',
        tuple(i for i in karachi_districts))

    prefix = select_district.replace(' ','_')

    ndvi_path = 'data/images/processed/khi_districts/ndvi/'+prefix+'.tiff'
    # st.write('you selected',select_district)
    # st.write('you selected',ndvi_path)

    src = rasterio.open(ndvi_path)

    plt.imshow(src.read(1),aspect='auto',cmap = plt.get_cmap('BuGn'))
    plt.axis('off')

    #cmap=plt.get_cmap(name)
    plt.show()
    plt.title("In this visualization, the greener the area the more green vegetation that area has:",loc='left')
    st.pyplot()
    #sns.set(rc={'figure.figsize':(8.7,7.27)})
    sns.set_style("darkgrid", {'patch.force_edgecolor': False})
    sns.set(font_scale=1.2)

    khi_districts_gpd['SELECTED_VAL'] = khi_districts_gpd['DISTRICT'].apply(lambda x: 1 if x == select_district else 0)

    ## bar plot here

    """
    You can also compare where your selected area compares with other areas in Karachi
    """

    gen_graph_bar = st.button('SEE COMPARISON')

    if(gen_graph_bar==True):
        ax = sns.barplot(x='DISTRICT',
                        y='REQ_NDVI_P',
                        data=khi_districts_gpd,
                        #color='#005b96',
                        hue='SELECTED_VAL')
        plt.title('GREEN SPACE IN KARACHI DISTRICTS')
        plt.ylabel('%AGE GREEN SPACE')
        plt.xlabel('')
        plt.legend()
        ax.legend_.remove()
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        #ax.set_yticklabels(['{:,.2%}'.format(x) for x in khi_districts_gpd.REQ_NDVI_P])
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        plt.savefig('viz/districts_comparison_BAR2.png',bbox_inches="tight")

        barplot_path = 'viz/districts_comparison_BAR2.png'
        st.image(barplot_path,format='PNG',width=700)


    ## bar plot here

    sns.set(rc={'figure.figsize':(11.7,8.27)})

    # df['c2'] = df['c1'].apply(lambda x: 10 if x == 'Value' else x)

    """
    We can also compare green space with total area in square kilometers.
    """
    districts_to_compare = st.multiselect('Which areas do you want to compare?',
                tuple(i for i in karachi_districts))



    khi_districts_req = khi_districts_gpd.loc[khi_districts_gpd.DISTRICT.isin(districts_to_compare)]

    # scatter plot comparing different districts

    gen_graph_scatter = st.button('GENERATE SCATTER GRAPH')

    if(gen_graph_scatter==True):
        ax = sns.scatterplot(x="AREA_KM",
                            y="REQ_NDVI_P",
                            color = '#005b96',
                            data=khi_districts_req,
                            #hue='SELECTED_VAL',
                            s=80)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        #ax.legend_.remove()

        plt.title('GREEN SPACE IN SELECTED AREAS')
        plt.xlabel('AREA IN SQKM')
        plt.ylabel('%AGE GREEN SPACE')


        label_point(khi_districts_req.AREA_KM, khi_districts_req.REQ_NDVI_P, khi_districts_req.DISTRICT, plt.gca())  
        scatterplot_path = 'viz/districts_comparison_SCATTER2.png'
        plt.savefig(scatterplot_path,bbox_inches="tight")
        st.image(scatterplot_path,format='PNG',width=700)





# """
# ### Future roadmap:
# 1. compare Union Councils
# 2. Feature where you can get green cover for area around where you live
# 3. Historical satelite data
# 4. Higher resolution sentinel satelite data
# 5. Incorporate other indices like EVI, NDBI and UHI to determine livability
# """

# """
# We can use the same logic to look at Karachi at the UC level, the following map shows the percentage of
# Green Cover in each UC for Karachi
# """


karachi_uc_gpd = gpd.read_file('data/shape_files/processed/khi_uc.shp')
karachi_uc_gpd = karachi_uc_gpd.sort_values(by='REQ_NDVI_P',ascending=False)
karachi_uc_gpd = karachi_uc_gpd.reset_index(drop=True)


if(navigation=='COMPARE UCs'):
    """
    ### Karachi union council level comparisons
    """

    grid = karachi_uc_gpd.geometry

    req_df = karachi_uc_gpd[['DISTRICT','UC','REQ_NDVI_P']]
    req_df.rename(columns={'REQ_NDVI_P':'GREEN_SPACE'},inplace=True)
    req_df['GREEN_SPACE'] = req_df.GREEN_SPACE.apply(lambda x: str(round(x*100,2))+"%")

    st.dataframe(req_df)

    values_all_dict = dict(karachi_uc_gpd.REQ_NDVI_P)
    colormap_ndvi = linear.YlGn_09.scale(
        karachi_uc_gpd.REQ_NDVI_P.min(),
        karachi_uc_gpd.REQ_NDVI_P.max())

    popup_dict = karachi_uc_gpd.REQ_NDVI_P.apply(lambda x: str(round(x*100,2))+"%")


    # NDVI MAP
    map_ = folium.Map(location=[24.859089, 67.035289], tiles='openstreetmap', zoom_start=10)
    karachi_uc_gpd['NDVI_PCT_LABEL'] = karachi_uc_gpd.REQ_NDVI_P.apply(lambda x: str(round(x*100,2))+'%')


    tooltip = folium.features.GeoJsonTooltip(
        fields=["DISTRICT","UC", "NDVI_PCT_LABEL"],
        aliases=['District/Cantonment',"Union Council:", "Green Space:"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 0.3px solid green;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )


    khi_ucs_shp = folium.GeoJson(
        karachi_uc_gpd,
        name='GREEN_SPACE',
        style_function=lambda feature: {
            'fillColor': colormap_ndvi(values_all_dict[int(feature['id'])]),
            'color': 'black',
            'weight': 0.4,
            'dashArray': '5, 5',
            'fillOpacity': 0.6,
        },
        tooltip=tooltip
    )

    map_.add_child(khi_ucs_shp)
    map_.add_child(colormap_ndvi)

    str_text ="""
    This interactive map gives us an overview of the percentage green space per UC
    """
    st.markdown(str_text,unsafe_allow_html=True)
    st.write(map_._repr_html_(), unsafe_allow_html=True)
    #map_.save('../viz/khi_ndvi_uc_map.html')

    x_axis = karachi_uc_gpd.REQ_NDVI_P
    y_axis = karachi_uc_gpd.AREA_KM
    text_label = karachi_uc_gpd.UC


    layout = go.Layout(
        xaxis=dict(tickformat='%',),
        yaxis=dict(ticksuffix='km'),
        title='AREA IN SQ KM vs GREEN SPACE'
    )

    fig = go.Figure(data=go.Scatter(x=x_axis,y=y_axis, mode='markers',text=text_label),layout=layout)

    str_text = """
    <br/><br/>
    The following interactive chart compares each UC for its green space vs total area in sq km
    """
    st.markdown(str_text,unsafe_allow_html=True)
    st.plotly_chart(fig)

if (navigation=='MY AREA'):

    st.write('Where do you live?')
    user_input = " "
    user_input = st.text_input("We don't need to know your exact address, just the general area will do. Karachi Futures will not store your input.")
    user_input =  user_input + ' Karachi'
    app_name = 'khigreenspaces_app_'+str(randint(0,10))+str(randint(0,10))+str(randint(0,10))
    geolocator = Nominatim(user_agent=app_name)
    geocode = partial(geolocator.geocode, language="en")
    result = geocode(user_input)

    if(result!=None):
    
        result_coord = list(reversed(result[1]))
        point_obj = Point(result_coord)
        result_dict = dict()
        for ind,row in karachi_uc_gpd.iterrows():
            poly =  row.geometry
            if(poly.contains(point_obj)==True):
                result_dict.update({'UC':row.UC,'NDVI':row.REQ_NDVI_P})
        output_str = "You live in `{0}` \n where `{1}` for the area has some form of live green vegetation.".format(result_dict['UC'],
        str(round(result_dict['NDVI']*100,2))+"%")
        st.write(output_str)

        
        grid = karachi_uc_gpd.geometry

        values_all_dict = dict(karachi_uc_gpd.REQ_NDVI_P)
        colormap_ndvi = linear.YlGn_09.scale(
            karachi_uc_gpd.REQ_NDVI_P.min(),
            karachi_uc_gpd.REQ_NDVI_P.max())

        popup_dict = karachi_uc_gpd.REQ_NDVI_P.apply(lambda x: str(round(x*100,2))+"%")


        map_ = folium.Map(location=[result_coord[1], result_coord[0]], tiles='openstreetmap', zoom_start=12)
        karachi_uc_gpd['NDVI_PCT_LABEL'] = karachi_uc_gpd.REQ_NDVI_P.apply(lambda x: str(round(x*100,2))+'%')


        tooltip = folium.features.GeoJsonTooltip(
            fields=["UC", "NDVI_PCT_LABEL"],
            aliases=["Union Council:", "Green Space:"],
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 0.3px solid green;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800,
        )


        khi_ucs_shp = folium.GeoJson(
            karachi_uc_gpd,
            name='GREEN_SPACE',
            style_function=lambda feature: {
                'fillColor': colormap_ndvi(values_all_dict[int(feature['id'])]),
                'color': 'black',
                'weight': 0.4,
                'dashArray': '5, 5',
                'fillOpacity': 0.6,
            },
            tooltip=tooltip
        )

        your_loc = folium.Marker([result_coord[1], result_coord[0]], popup='You live (almost) here!')

        map_.add_child(khi_ucs_shp)
        map_.add_child(colormap_ndvi)
        map_.add_child(your_loc)

        st.write(map_._repr_html_(), unsafe_allow_html=True)
    elif(result==None):
        st.write('Could not geocode area, please try again. Maybe a different spelling? Or trying a different name for your area')


####

footerish = """
<br/><br/>
<br/><br/>
<br/><br/>
<TT> Feedback and suggestions: [hishamsajid113@gmail.com](mailto:hishamsajid113@gmail.com) | [@hishamsajid](https://twitter.com/hishamsajid) </TT>
"""
st.markdown(footerish,unsafe_allow_html=True)
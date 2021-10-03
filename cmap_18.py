#! /usr/bin/env python3

"""
Written by: Peichen Li
Last Updated: 06/18/2021

This python script is for creating a choropleth map based on 2018 A00100perN1
"""



# Import the geopandas and geoplot libraries
# if having Anaconda (or Miniconda) distribution
# on command line, run:
# conda install geopandas
# conda install geoplot -c conda-forge
# conda install -c conda-forge mapclassify
import geopandas as gpd
import geoplot as gplt
import pandas as pd
import matplotlib.pyplot as plt
import mapclassify as mc
import geoplot.crs as gcrs

# set path
input = r"C:\Users\90596\Desktop\PeterHan\SOI_data\Choropleth map\input"
output = r"C:\Users\90596\Desktop\PeterHan\SOI_data\Choropleth map\output"


# Creating a choropleth map based on 2018 A00100perN1
def cmap_18():
    # Load the 5-digit zipcode shape files
    # downloaded from U.S. Census Bureau: https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_zcta510_500k.zip
    # Regarding zipcode shape files: https://www.reddit.com/r/gis/comments/8xe8l4/why_are_there_no_public_exhaustive_zip_code/
    geoData = gpd.read_file(input + "\cb_2018_us_zcta510_500k\cb_2018_us_zcta510_500k.shp")

    # Make sure the ZIPCODE column is an integer
    geoData.ZCTA5CE10 = geoData.ZCTA5CE10.astype(str).astype(int)

    # Removing Alaska, Guam, Puerto Rico, Hawaii from GeoPandas GeoDataframe, respectively
    geoData = geoData[~geoData.iloc[:, 0].between(99501, 99950, inclusive=False)]
    geoData = geoData[~geoData.iloc[:, 0].between(96910, 96932, inclusive=False)]
    geoData = geoData[geoData.ZCTA5CE10 >= 1001]
    geoData = geoData[~geoData.iloc[:, 0].between(96701, 96898, inclusive=False)]

    # Read SOI_18 file
    data = pd.read_csv(input + '\SOI18.csv')[["ZIPCODE", "A00100perN1"]]
    data = data[["ZIPCODE", "A00100perN1"]]

    # Merge A00100perN1 to geoData
    fullData = geoData.merge(data, left_on=['ZCTA5CE10'], right_on=['ZIPCODE'])
    fullData.head(2)

    # Initialize the figure
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))

    # Set up the color sheme:
    scheme = mc.Quantiles(fullData['A00100perN1'], k=10)

    # Map
    gplt.choropleth(fullData,
        hue="A00100perN1",
        linewidth=.0001,
        scheme=scheme, cmap='inferno_r',
        #projection=gcrs.AlbersEqualArea(),
        legend=True,
        legend_kwargs={'loc': 'lower left'},
        edgecolor='white',
        legend_labels=['<40.5', '40.5-45.2', '45.2-48.8', '48.8-52.3', '52.3-55.9','55.9-60.4',\
                       '60.4-66.3','66.3-76.5','76.5-99.7','>99.7'],
        ax=ax)
    ax.set_title('Average adjusted gross income by ZIP code', fontsize=13)

    print("configuring map now...will take 2 mins")
    plt.savefig('cmap.pdf', bbox_inches='tight', pad_inches=0.1)
    # on command line use: pdftoppm -png -r 300 cmap.pdf cmap
    # That is, save pdf to png without loss of quality
    # Alternatives:
    # plt.savefig('test.eps', format='eps')
    # fig.savefig('myimage.svg', format='svg', dpi=1200)
    # plt.savefig('test.png')
    print("pdf done - next please type the shell command below to convert the pdf map to png")
    print("pdftoppm -png -r 300 cmap.pdf cmap")

if __name__ == "__main__":
    cmap_18()

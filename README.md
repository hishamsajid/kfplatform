# Karachi Futures Platform

## About Karachi Futures

[Karachi Futures](http://karachifutures.com/) is a research initiative + tech shop aiming to understand the social and economic 
problems of Karachi in a much more deeper quantitative and qualitative sense. Our role is to research factors that may influence 
the future of Karachi, with the purposeof enabling a much smarter, digital enabled and overall better city – ready to leapfrog into 
the 4th Industrial Revolution.

## How does this app work?

The normalized difference vegetation index (NDVI) is a simple graphical indicator that can be used to analyze remote sensing 
measurements, often from a space platform, assessing whether or not the target being observed contains live green vegetation. 

For this experiment, we take LANDSAT8 images from February 2019 and calculate and aggregate NDVI values for different parts
of Karachi. All data and technology used for this experiment in open source. 

### NDVI Range

We calculate the NDVI value of each pixel between 0 and 1, where 1 is the highest level of live green vegetation. For this experiment,
we have kept the threshold for classifying a pixel as green at `0.0982` as per this [research paper](https://www.researchgate.net/publication/337101410_Evaluating-Spatial-Patterns_of_Urban_Green_Spaces_in_Karachi_Through_Satellite_Remote_Sensing) by the Departent of Geography at the University of Punjab published in 2016.

### Working site

You access the working prototype [here](https://kfplatform-poc.herokuapp.com/); please consider that it is still very much in wip

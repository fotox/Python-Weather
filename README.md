# Python Weather

This project is concerned with the processing of weather data from the German Weather Service to create a deep learning model that can simulate and predict the complex calculations of electricity-generating renewable energy based on the weather at a given location. 
In the first phase, weather data from the German Weather Service and sun position data from the Sun-Earth tool provide the initial data for training the deep learning model. 
In the second phase, triangulations are performed to generate a more exact weather history at a location where there is no station of the German Weather Service.
In the third phase of the project, the weather data will be replaced by a standalone weather station and the power data will be replaced by real renewable power generation plants.
The goal of the project is to be able to predict better whether and which renewable energy source can be used optimally and on what scale on the basis of the exact location and the climatic conditions prevailing there in the past.

## Phase 1:
- [ ] Weather data download script
- [ ] Sun data download script
- [x] Standardize the data structure
- [x] Train model
- [x] Validate model
- [x] Test model
- [x] Export model

## Phase 2:
- [ ] Create a 3D vegetation map
- [ ] Triangulation without 3D model
- [ ] Triangulation with 3D model
- [ ] Train model
- [ ] Validate model
- [ ] Test model
- [ ] Export model

## Phase 3:
- [ ] Build self-sufficient weather station
- [ ] Automatic synchronization of weather data with the cloud
- [ ] Automatic synchronization of renewable energy sources with the cloud
- [ ] Optimization of the models
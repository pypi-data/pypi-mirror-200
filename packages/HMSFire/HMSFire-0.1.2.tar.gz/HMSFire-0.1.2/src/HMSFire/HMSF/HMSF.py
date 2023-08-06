import requests
import pandas as pd
from datetime import date, timedelta, datetime
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sys
import os
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
'''
This Hazard Mapping System Fire Class is a managing tool
to download information from the main source: https://www.ospo.noaa.gov/Products/land/hms.html#about

'''
class HMSFire:
  def __init__(self, startDate:str, endDate:str, load_file:str=None, skipDays:int=0):
    self.startDate = startDate
    self.endDate = endDate
    if load_file != None:
      self.data = pd.read_csv(load_file, skipinitialspace=True)
      self.data = self.data[~data.duplicated()]
      self.data.columns = self.data.columns.str.replace(' ', '')
    else:
       self.data = self.adquire(startDate=startDate, endDate=endDate)
  def getDataFrame(self):
    return self.data

  def getXarray(self):
    return data.set_index('Time').to_xarray()

  def update(self, startDate:str, endDate:str):
    ##TODO: apply a smart update...
    self.data = self.adquire(startDate=startDate, endDate=endDate)

  def resamplingTime(self, data:pd.DataFrame(), freq:str='1D'):
    data2=data.copy()
    data2 = data2[data2.FRP > -999.0] ##remove missing values
    colsGroup = list(data2.columns)
    colsGroup.remove('Time')
    colsGroup.remove('FRP')
    data2 = data2.set_index(colsGroup+['Time'])
    cols = colsGroup + [pd.Grouper(freq=freq, level='Time')]
    return data2.groupby(cols)['FRP'].mean().reset_index(name='FRP')
  def getBoundingBoxCounty(self, county:str='Dallas'):
    boundingBox = pd.read_csv('US_County_Boundingboxes.csv')
    return boundingBox[boundingBox.COUNTY_NAME=='Dallas'].xmin.min(), boundingBox [boundingBox.COUNTY_NAME=='Dallas'].ymin.min(), boundingBox [boundingBox.COUNTY_NAME=='Dallas'].xmax.max(), boundingBox [boundingBox.COUNTY_NAME=='Dallas'].ymax.max()

  def getBoundingBoxState(self, state:str='Texas'):
    boundingBox = pd.read_csv('US_State_Bounding_Boxes.csv')
    box = boundingBox[boundingBox.NAME=='Texas'][['xmin', 'ymin', 'xmax', 'ymax']].values[0]
    return box[0], box[1], box[2], box[3]
  def adquire(self, startDate:str, endDate:str, skipDays:int=0):
    """
    In this method connects directly to official web page and adquires information of fires
    Warning: depending on the start and end dates affects directly to RAM 
    input: 
       startDate: format Year-Month-Day example 2008-10-01
       endDate: format Year-Month-Day example 2008-10-01
       skipDays: skip a number of days - 1, by default is 1, thus al data will be kept   
    output: 
      dataframe from Pandas library
    """
    start_date = datetime.strptime(startDate, '%Y-%m-%d')
    end_date = datetime.strptime(endDate, '%Y-%m-%d')
    delta = end_date - start_date
    df = None

    for i in range(0, delta.days+1, skipDays+1):
      YearMonthDay = start_date + timedelta(days=i)
      Year = YearMonthDay.strftime('%Y')
      Month = YearMonthDay.strftime('%m')
      Day = YearMonthDay.strftime('%d')
      url = 'https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Fire_Points/Text/'+Year+'/'+Month+'/hms_fire'+Year+Month+Day+'.txt'
      ##check if url exists
      response = requests.get(url)
      eprint("Downloading.... {:.2f} %".format(i*100.0/delta.days))
      if response.status_code != 200:
        continue
      dfinner = pd.read_csv(url, sep=",", encoding='latin-1', skipinitialspace=True)
      dfinner.columns = dfinner.columns.str.replace(' ', '')
      dfinner['Time'] = YearMonthDay
      if i == 0:
        df = dfinner
      else:
        df = pd.concat([df,dfinner])
    df = df[~df.duplicated()]
    return df

  def plot(self, minlon:int=-180, minlat:int=-90, maxlon:int=180, maxlat:int=90, points:pd.DataFrame=pd.DataFrame(), opacityCount:bool=True):
    data = self.data.copy()
    if not points.empty:
      data = points.copy()
    Lon = self.data.Lon
    Lat = self.data.Lat
    # setup Lambert Conformal basemap.
    #m = Basemap(width=12000000,height=9000000,projection='lcc',
    #            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
    m = Basemap(width=12000000,height=9000000,
            resolution='c',llcrnrlon=minlon,llcrnrlat=minlat, urcrnrlon=maxlon, urcrnrlat=maxlat)
    # draw coastlines.
    #m.drawcoastlines()
    # draw a boundary around the map, fill the background.
    # this background will end up being the ocean color, since
    # the continents will be drawn on top.
    #m.drawmapboundary(fill_color='aqua')
#    m.drawmapboundary(fill_color='#46bcec')
    m.shadedrelief()
    # fill continents, set lake color same as ocean color.
    #m.fillcontinents(color='coral',lake_color='aqua')
#    m.fillcontinents(color = 'white',lake_color='#46bcec')
    #m.scatter(-180-Lon.where(Lon.YearDay>2023050, drop=True).values, Lat.where(Lat.YearDay>2023050, drop=True).values, marker = 'o', color='r', zorder=1.)
    x, y = m(Lon.values, Lat.values)  # transform coordinates
    freq = [1]*len(x)
    if opacityCount:
      freq = data[['Lon', 'Lat']].groupby(['Lon', 'Lat']).size().reset_index(name='Count')['Count'].values
      freq = freq/freq.max()

    plt.scatter(x, y, 1, marker='o', color='Red', alpha=freq) 
    plt.show()# setup Lambert Conformal basemap.

  def satelites(self):
    return self.data.Satellite.unique()
HMSF = HMSFire(startDate='2020-01-01', endDate='2023-02-01')
  data = HMSF.getDataFrame()
  HMSF.plot()
print(HMSF.satelites())
HMSF.plot(minlon=-125, minlat=25, maxlon=-60, maxlat=50)
minlon, minlat, maxlon, maxlat = HMSF.getBoundingBoxCounty(county='Dallas')
HMSF.plot(minlon=minlon, minlat=minlat, maxlon=maxlon, maxlat=maxlat)
minlon, minlat, maxlon, maxlat = HMSF.getBoundingBoxState(state='Texas')
HMSF.plot(minlon=minlon, minlat=minlat, maxlon=maxlon, maxlat=maxlat)

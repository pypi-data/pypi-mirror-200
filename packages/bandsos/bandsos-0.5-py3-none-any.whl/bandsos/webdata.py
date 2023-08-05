#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings
import xarray as xr
import numpy as np
import pandas as pd
from glob import glob
import os
import requests
import re
import logging

class GFS_0p25_1hr:
    def __init__(self, data_dir='./gfs', data_prefix='gfs_', url='http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr', retries=3):
        '''
        Checking and downloading new data from web for gfs dataset.
        '''
        self.url = url
        self.retries = retries
        self.data_dir = data_dir
        self.data_prefix = data_prefix
        self.available = {}
        self.downloaded = {}
        self.remaining = {}

        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

    @property
    def last(self):
        '''
        Gives the last cycle name.
        '''
        return(np.array([k for k in self.available.keys()])[-1])

    def check(self, min_file_size=1000000):
        '''
        Check online for new cycles, and returns true if new cycle is available, false otherwise.
        '''
        self.available = self._list_available_cycles(days=self._list_available_days())
        self.downloaded = self._list_downloaded_cycles(min_file_size=min_file_size)
        self.remaining = self._list_remaining_cycles()

        if len(self.remaining) > 0:
            # new forecast available
            return True
        else:
            # no new forecast is available
            return False

    def _list_downloaded_cycles(self, min_file_size):
        '''
        List the downloaded forecast cycles locally.
        '''
        downloaded = {}
        fpaths = glob(os.path.join(self.data_dir, f'{self.data_prefix}*.nc'))
        fnames = [os.path.basename(fpath) for fpath in fpaths]
        fsizes = [os.path.getsize(fpath) for fpath in fpaths]

        for fpath, fsize in zip(fpaths, fsizes):
            fname = os.path.basename(fpath)
            cycle = fname.split(self.data_prefix)[1].split('.nc')[0] # prefixyyyymmddhh.nc
            
            if cycle in self.available:
                if fsize > 1000000:
                    downloaded[cycle] = fpath
        
        return(downloaded)

    def _list_remaining_cycles(self):
        remaining = {}
        for cycle in self.available:
            if cycle not in self.downloaded:
                remaining.update({cycle:self.available[cycle]})
        
        return(remaining)

    def _list_available_days(self):
        '''
        List available days online
        '''
        response = requests.get(self.url)
        initial = response.text.split('<hr>')[1].replace('<br>', '').replace('<b>', '').replace('</b>', '')
        day_url_list = [line.split('"')[1] for line in initial.split('\n')[1:-2]]

        available_days = {}
        for day_url in day_url_list:
            datestring = re.findall(pattern='\d{8}', string=day_url)[0] # first element
            available_days[datestring] = day_url

        return available_days

    def _list_available_cycles(self, days):
        available_cycles = {}
        for day in days:
            url = days[day]
            prefix = day

            response = requests.get(url)
            initial = response.text.split('<hr>')[1]
            initial = initial.replace('<br>', '').replace('<b>', '').replace('</b>', '')
            initial = initial.replace('\n&nbsp;', '').replace('&nbsp', '').split('\n')
            initial = initial[1:-2]
            
            eitems = 5 # items expected 
            nitems = len(initial)//eitems
            items = np.arange(nitems)

            for item in items:
                cycle = initial[eitems*item+1].split(':')[0]
                cycle_hour = cycle[-3:-1] # extracted from gfs_0p25_1hr_00z format
                available_cycles[f'{prefix}{cycle_hour}'] = {
                    'url':f'{url}/{cycle}',
                    'inittime':pd.to_datetime(initial[eitems*item+1].split('from ')[1].split(',')[0].replace('Z', ''), format='%H%d%b%Y'),
                    'dltime':pd.to_datetime(initial[eitems*item+1].split('Z')[1][5:-4].replace(', downloaded ', ''), format='%Y%b %d %H:%M')
                }
        
        return(available_cycles)

    def download(self, extent=[0, 360, -90, 90]):
        for cycle in self.remaining:
            ds = self.get_data_handle(self.remaining[cycle]['url'])
            fname = os.path.join(self.data_dir, f'{self.data_prefix}{cycle}.nc')
            self.save_data(ds=ds, fname=fname, extent=extent)

    @staticmethod
    def get_data_handle(dataurl, retries=3):
        logging.info(f'Now downloading {dataurl}')
        success = False
        retry = 0
        
        while not success:
            if retry < retries:
                try:
                    logging.info(f'Downloading {dataurl} - attempt {retry + 1}')
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore')
                        ds = xr.open_dataset(dataurl)
                except:
                    logging.info(f'Downloading {dataurl} - attempt {retry + 1} failed!')
                    retry += 0
                else:
                    success = True
                    logging.info(f'Downloading {dataurl} - connected in {retry + 1} try(ies)!')
                    return(ds)
            else:
                logging.error(f'Exceeded retry count {retries}')

        if success is False:
            logging.error(f'Fatal error in downloading after {retry + 1} retries. Will exit the program.')
            raise Exception(f'Could not connect to the {dataurl}')

    @staticmethod
    def save_data(ds, fname, extent, retries=3):
        logging.info(f'Saving {fname} using extent {extent}.')
        success = False
        retry = 0

        while not success:
            if retry < retries :
                try:
                    lon_select = ds['lon'].where(np.logical_and(ds.lon>=extent[0], ds.lon<=extent[1])).dropna(dim='lon')
                    lat_select = ds['lat'].where(np.logical_and(ds.lat>=extent[2], ds.lat<=extent[3])).dropna(dim='lat')
                    
                    # To suppress warning related to 1-1-1 in time
                    ds_out = xr.Dataset(
                        {
                            'prmsl':ds['prmslmsl'].sel(lat=lat_select, lon=lon_select),
                            'u10':ds['ugrd10m'].sel(lat=lat_select, lon=lon_select),
                            'v10':ds['vgrd10m'].sel(lat=lat_select, lon=lon_select),
                            'stmp':ds['tmp2m'].sel(lat=lat_select, lon=lon_select),
                            'spfh':ds['rh2m'].sel(lat=lat_select, lon=lon_select),
                            'dlwrf':ds['dlwrfsfc'].sel(lat=lat_select, lon=lon_select),
                            'dswrf':ds['dswrfsfc'].sel(lat=lat_select, lon=lon_select),
                            'prate':ds['pratesfc'].sel(lat=lat_select, lon=lon_select),
                        }
                    )

                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore')
                        ds_out.to_netcdf(fname)

                    ds_out.close()
                    ds.close()

                    # Check if time is parsed correctly as np.datetime64, if not throws an exception
                    with xr.open_dataset(fname) as ds:
                        logging.info(f'Testing time variable for integrity')
                        is_datetime64 = isinstance(ds['time'].data[0], np.datetime64)

                    if not is_datetime64:
                        logging.info(f'Time is not correct, removing {fname}')
                        os.remove(fname)
                        raise Exception(f'Time is not correct.')
                except Exception as e:
                    logging.info(f"An exception during saving (retry {retry + 1}): ", e)
                    retry += 1
                else:
                    success = True
                    logging.info(f'Data saving {fname} done in {retry + 1} try(ies)')
            else:
                logging.error(f'Exceeded retry count {retries}')
                break

        if success is False:
            logging.error(f'Fatal error in saving. Will exit the program.')
            raise Exception(f'Could not save to the {fname}.')
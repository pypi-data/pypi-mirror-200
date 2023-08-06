"""
Module to set up pvlib models for CCRenew projects and coordinate running
calculations.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from pvlib import (
    irradiance,
    location,
    pvsystem
)
from pvlib.modelchain import ModelChain
import sys

from ccrenew import (
    DaylightParams,
    DateLike,
    Numeric
)
from ccrenew import (
    cloud_data,
    data_determination as det
)

class ProjectModel(ModelChain):
    """An extension of the pvlib ModelChain class tailored to CCR sites.

    Args:
        project_name (str): The name of the project to model.
        azimuth (Numeric): Azimuth of the modules. North=0, East=90, South=180, West=270.
        axis_tilt (Numeric): For tracker sites -
            the angle that the axis of rotation makes with respect to horizontal.
        cross_axis_tilt (Numeric): For tracker sites on sloped surfaces -
            the angle that forms the slope of the ground perpendicular to the axis of rotation.
        ground_surface_type (str | None): Ground surface type to use for `ground_surface_albedo`.
            See `pvlib.irradiance.SURFACE_ALBEDOS` for valid values.
        ground_surface_albedo (float | None): Ground surface albedo to use for reflected irradiance.
            If `None` then `ground_surface_type` is used to look up a value.
            If `ground_surface_type` is also None, a default value of 0.25 is used.
        clearsky_model (str): Model used to calculate clearsky estimates of GHI, DNI, and/or DHI at the location.
        transposition_model (str): Irradiance model to use for transposing horizontal irradiance to POA irradiance.
            See: <a href="https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.irradiance.get_total_irradiance.html" target="_blank" rel="noopener noreferrer">Get Total Irradiance.</a>
        solar_position_method (str): Method to use for calculating solar position.
            See: <a href="https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.solarposition.get_solarposition.html#pvlib.solarposition.get_solarposition" target="_blank" rel="noopener noreferrer">Solar Position.</a>
        airmass_model (str): Model used for calculating airmass based on location.
            See: <a href="https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.location.Location.get_airmass.html" target="_blank" rel="noopener noreferrer">Get Airmass.</a>
        dc_model (str | None): Model used for DC power calculations. If `None`, model will be inferred from module parameters.
            See `pvsystem._DC_MODEL_PARAMS` for valid values.
        ac_model (str | None): Model used for AC power calculations. If `None`, model will be inferred from inverter parameters.
            Valid values are `sandia`, `adr`, or `pvwatts`.
        aoi_model (str | None): Model for calculating angle of incidence. If `None`, model will be inferred from module parameters.
            Valid values are `physical`, `ashrae`, `sapm`, `martin_ruiz`, or `no_loss`.
        spectral_model (str): Model for calculating spectral mismatch between test conditions and actual conditions in the field. If `None`, model will be inferred from module parameters.
            Valid values are `sapm`, `first_solar`, or `no_loss`.
        temperature_model (str): Model used to correct module efficiency based on cell temperature. If `None`, model will be inferred from parameters passed to the temperature model of the array.
            Valid values are `sapm`, `pvsyst`, `faiman`, `fuentes`, `noct_sam`.
        dc_ohmic_model (str): Model for calculating losses based on equivalent resistence.
            Valid values are `dc_ohms_from_percent` or `no_loss`
        losses_model (str): Model for calculating system losses.
            For PVWatts model losses see <a href="https://pvlib-python.readthedocs.io/en/stable/reference/pv_modeling/generated/pvlib.pvsystem.pvwatts_losses.html#pvlib.pvsystem.pvwatts_losses" target="_blank" rel="noopener noreferrer">Losses Model.</a>
            Valid values are `pvwatts` or `no_loss`
    """
    def __init__(self, project_name:str, azimuth:Numeric = 180, axis_tilt:Numeric = 0, cross_axis_tilt:Numeric = 0,
                 ground_surface_type:str|None = 'grass', ground_surface_albedo:float|None = None,
                 clearsky_model:str = 'ineichen', transposition_model:str = 'haydavies',
                 solar_position_method:str = 'nrel_numpy', airmass_model:str = 'kastenyoung1989',
                 dc_model:str|None = None, ac_model:str|None = None, aoi_model:str|None = 'physical',
                 spectral_model:str = 'no_loss', temperature_model:str|None = None,
                 dc_ohmic_model:str = 'no_loss', losses_model:str = 'no_loss'):

        # Get parameters for the project to pass to the pvlib constructors
        project_params = cloud_data._get_project_model_params(project_name)

        #choose tracking algorithm based upon temp_coefficient of the modules
        backtrack=True
        if project_params.temp_coef > -0.39:
            backtrack=False
  
        self.racking = project_params.racking
        if self.racking == 'Fixed':
            mount = pvsystem.FixedMount(project_params.tilt_gcr, azimuth)
        else:
            mount = pvsystem.SingleAxisTrackerMount(
                axis_tilt, azimuth, project_params.max_angle,
                backtrack, project_params.tilt_gcr, cross_axis_tilt)

        self.array = pvsystem.Array(mount, surface_type=ground_surface_type, name=project_name,
            module_parameters={'pdc0': project_params.mwdc*1000,
                            'gamma_pdc': project_params.temp_coef/100,
                            'dc_model': dc_model, 'ac_model': ac_model,
                            'aoi_model': aoi_model, 'spectral_model': spectral_model,
                            'dc_ohmic_model': dc_ohmic_model, 'losses_model': losses_model},
            temperature_model_parameters={'a': project_params.a_module,
                                          'b': project_params.b_module,
                                          'deltaT': project_params.delta_tcnd})

        self.pv_system = pvsystem.PVSystem([self.array], name=project_name,
            inverter_parameters={'pdc0': project_params.mwdc*1000})

        self.location = location.Location(
            latitude=project_params.lat, longitude=project_params.lon,
            tz=project_params.tz, altitude=project_params.elevation, name=project_name
        )

        super().__init__(self.pv_system, self.location,
                         clearsky_model, transposition_model,
                         solar_position_method, airmass_model,
                         dc_model, ac_model, aoi_model,
                         spectral_model, temperature_model,
                         dc_ohmic_model, losses_model, project_name)

        if isinstance(self.array.mount, pvsystem.FixedMount):
            self.racking = 'fixed'
        else:
            self.racking = 'tracker'


    def calculate_poa_from_ghi(self, ghi:pd.Series, model:str = 'Perez', shift:bool = False, **kwargs):
        # TODO: get model from system instead of supplying it here
        # `get_solarposition()` returns a df of `azimuth`, `apparent_elevation`, `elevation`, `apparent_zenith`, & `zenith`
        # apparent zenith & apparent elevation account for atmospheric refraction
        tz = self.location.tz
        ghi = ghi.tz_localize(tz, nonexistent='shift_backward', ambiguous='NaT')
        if shift:
            ghi.index = ghi.index + pd.Timedelta('30min')
        solar_position = self.location.get_solarposition(ghi.index)
        
        # The erbs model takes the zenith un-corrected for refraction
        solar_zenith = solar_position['zenith']
        solar_azimuth = solar_position['azimuth']
        irradiation_components = irradiance.erbs(ghi, solar_zenith, ghi.index)
        dni = irradiation_components['dni']
        dhi = irradiation_components['dhi']

        poa = self.array.get_irradiance(solar_zenith, solar_azimuth, dni, ghi, dhi, model=model, **kwargs)

        if shift:
            poa.index = poa.index - pd.Timedelta('30min') # type: ignore
    
        # Drop duplicate dates - most common during DST change in the fall where we re-do 2 AM
        poa = poa.tz_localize(None)
        poa = poa[~poa.index.duplicated()]

        return poa

    def run_bluesky(self, start_date:str|DateLike, end_date:str|DateLike,
                    resample:bool = True, fetch_ghi:bool = False) -> pd.DataFrame:
        print(f"Fetching solcast data for {self.name}")
        df_weather = cloud_data.get_sat_weather(self.name, start_date, end_date) # type: ignore
        sat_poa = self.calculate_poa_from_ghi(df_weather['sat_ghi'])
        df_solcast = df_weather.join(sat_poa['poa_global'])
        df_solcast = df_solcast.rename(columns={'poa_global': 'sat_poa'})
        
        # Initialize `poa`` & `proj_ghi` columns
        # `poa` is used 
        df_solcast['poa'] = df_solcast['sat_poa']
        df_solcast['ghi'] = df_solcast['sat_ghi']
        df_solcast['proj_ghi'] = np.nan
        
        if fetch_ghi:
            try:
                print(f"Fetching 5 min GHI data for {self.name}")
                df_project_ghi = cloud_data.get_project_ghi(self.name, start_date, end_date) # type: ignore
                project_poa = self.calculate_poa_from_ghi(df_project_ghi['proj_ghi'])
                df_solcast['proj_ghi'] = df_project_ghi['proj_ghi']
                df_solcast['proj_ghi_poa'] = project_poa['poa_global']

                # Pass transposed GHI column through daylight zeroes filter to make sure the data is good
                # (the filter returns True where there are daylight zeroes so we need to invert it)
                proj_ghi_poa = df_project_ghi.join(project_poa['poa_global'])
                proj_ghi_bool = ~det.daylight_zeroes(df=proj_ghi_poa, pv_model=self)

                # Convert all False values (bad data) to np.inf so we can replace with NaN after reindexing in the next step
                proj_ghi_bool = proj_ghi_bool.replace(False, np.inf)

                # Reindex to add nighttime rows back in & set them to False so they don't change the data in the original df
                proj_ghi_bool = proj_ghi_bool.reindex(index=proj_ghi_poa.index).fillna(False)

                # Replace np.inf with np.nan (we used np.inf to demarcate bad data so it wouldn't be overwritten in the step above)
                proj_ghi_bool = proj_ghi_bool.replace(np.inf, np.nan)

                # Filter out bad data
                proj_ghi_poa = (proj_ghi_poa*proj_ghi_bool).astype(float)

                # Fill in any NaNs with satellite data
                proj_ghi_poa = proj_ghi_poa.fillna({'proj_ghi': df_solcast['sat_ghi'], 'poa_global': df_solcast['sat_poa']})

                # Rename & drop column `sites_ghi_poa` column to match sites with no GHI
                df_solcast[['ghi', 'poa']] = proj_ghi_poa[['proj_ghi', 'poa_global']]
                df_solcast = df_solcast.fillna(0)
            except:
                error_info = sys.exc_info()
                error_type = error_info[:2]
                traceback = error_info[2]
                error_source = traceback.tb_frame.f_code # type: ignore
                lineno = traceback.tb_lineno # type: ignore
                file = error_source.co_filename
                func = error_source.co_name
                
                print(f"Error while fetching 5 min GHI data for {self.name}, using satellite POA instead.")
                print(f"Error details: {error_type} on line {lineno} of `{func}` in {file}")

        
        # Resample high frequency data to hourly
        if resample:
            df_solcast = df_solcast.resample('H').mean()

        #add in a tmod column based on the conversion equation
        a_module = self.array.temperature_model_parameters['a']
        b_module = self.array.temperature_model_parameters['b']
        df_solcast['Tmod'] = df_solcast['Tamb']+(df_solcast['poa']*np.exp(a_module+b_module*df_solcast['Wind_speed']))

        #correct for static values that solcats reports that the dashboard is gonna turn off.
        correction_factor = np.where(df_solcast.index.hour%2==0, 0.999, 1.001) # type: ignore
        df_solcast['Tamb'] *= correction_factor
        df_solcast['Tmod'] *= correction_factor
        df_solcast['Wind_speed'] *= correction_factor

        return df_solcast
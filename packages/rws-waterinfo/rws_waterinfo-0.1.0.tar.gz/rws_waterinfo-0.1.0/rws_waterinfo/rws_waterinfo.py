"""rws_waterinfo."""
# --------------------------------------------------
# Name        : rws_waterinfo.py
# Author      : S.J.A. de Haas
# Contact     : simon.de.haas@rws.nl
# github      : https://gitlab.com/rwsdatalab/public/codebase/tools/rws_waterinfo
# Licence     : See licences
# --------------------------------------------------

import datetime
import logging
import os
from typing import List, Optional, Union

import numpy as np
import pandas as pd
import requests

logger = logging.getLogger("")
for handler in logger.handlers[:]:  # get rid of existing old handlers
    logger.removeHandler(handler)
console = logging.StreamHandler()
formatter = logging.Formatter(
    "[%(asctime)s] [rws_waterinfo]> %(levelname)s> %(message)s", datefmt="%H:%M:%S"
)
console.setFormatter(formatter)
logger.addHandler(console)
logger = logging.getLogger(__name__)


def set_logger(verbose: Union[str, int] = "info"):
    """Set the logger for verbosity messages.

    Parameters
    ----------
    verbose : [str, int], default is 'info' or 20
        Set the verbose messages using string or integer values.
        * [0, 60, None, 'silent', 'off', 'no']: No message.
        * [10, 'debug']: Messages from debug level and higher.
        * [20, 'info']: Messages from info level and higher.
        * [30, 'warning']: Messages from warning level and higher.
        * [50, 'critical']: Messages from critical level and higher.

    Returns
    -------
    None.

    > # Set the logger to warning
    > set_logger(verbose='warning')
    > # Test with different messages
    > logger.debug("Hello debug")
    > logger.info("Hello info")
    > logger.warning("Hello warning")
    > logger.critical("Hello critical")

    """
    # Set 0 and None as no messages.
    if (verbose == 0) or (verbose is None):
        verbose = 60
    # Convert str to levels
    if isinstance(verbose, str):
        levels = {
            "silent": 60,
            "off": 60,
            "no": 60,
            "debug": 10,
            "info": 20,
            "warning": 30,
            "critical": 50,
        }
        verbose = levels[verbose]

    # Show examples
    logger.setLevel(verbose)


def get_catalog() -> pd.DataFrame:
    """Get parameter information from Waterinfo.

        This function sends a request to Waterinfo for parameter information
        and parses the response into a Pandas DataFrame. The DataFrame contains
        the locations and parameters combined into a single table.

    Returns
    -------
    dataframe : pandas.DataFrame
        A DataFrame with the parameter information.

    Raises
    ------
    HTTPError
        If there is an error with the request.

    Examples
    --------
    >>> import pandas as pd
    >>> import rws_waterinfo as rw
    >>> # Initialize rws_waterinfo library
    >>> #
    >>> catalog = rw.get_catalog()
    >>> #
    >>> catalog.head()
    >>> #
    >>> # AquoMetaData_MessageID	Locatie_MessageID	Coordinatenstelsel	X	Y
    >>> # 0	12746	22317	25831	717567.392073	5.782901e+06
    >>> # 1	17619	22366	25831	706152.313357	5.725423e+06
    >>> # 2	7941	17613	25831	580241.163781	5.723650e+06
    >>> # 3	14352	21173	25831	705635.738484	5.835367e+06
    >>> # 4	18676	21173	25831	705635.738484	5.835367e+06
    >>> # 5 rows × 44 columns
    >>> #
    """
    logger.info("Get catalog")
    response = _request_catalog()
    catalog = _parse_catalog_response(response)
    logger.info("dataframe returned: %s" % (str(catalog.shape)))
    return catalog


def get_data(
    params: List[List[object]],
    filepath: Optional[str] = None,
    return_df: bool = False,
) -> Optional[pd.DataFrame]:
    """Get observation data from Waterinfo.

        This is function retrieves observation data from Waterinfo. It takes in
        three arguments, two of which are optional, and returns a Pandas dataframe
        or None. The first argument, params, is a list of lists that contains the
        necessary parameters to retrieve observations. The second argument,
        filepath, is an optional string that specifies the directory and file name
        where the data will be saved. If filepath is not specified, the data will
        not be saved. The third argument, return_df, is an optional boolean that
        specifies whether the function should return the observations as a Pandas
        dataframe or not. If return_df is set to False, the function will not
        return anything.

    Parameters
    ----------
    params : list of lists
        List of lists with necessary parameters to receive observations.
        [[compartiment_code, eenheid_code, meetapparaat_code, grootheid_code,
        locatie_code, cor_x, cor_y, start_date, end_date]]

    Keyword Arguments
    -----------------
    filepath : str, optional
        Path to the directory and file name to save data. (default: None)
    return_df : bool, optional
        If true it returns the observations as a pandas dataframe. (default: False)

    Raises
    ------
    Exception
        If both filepath and return_df are False.
    Exception
        If the directory for filepath does not exist.

    Returns
    -------
    pandas dataframe or None
        Returns a pandas dataframe if return_df is True, otherwise returns None.

    Examples
    --------
    >>> import pandas as pd
    >>> import rws_waterinfo as rw
    >>> # Initialize rws_waterinfo library
    >>> #
    >>> params  = [['OW', 'm3/s', 156, 'Q', 'OLST', 711556.219876449,
    >>> 5803627.64455833, '2022-01-01', '2023-01-01']]
    >>> filepath = 'observations.csv'
    >>> #
    >>> data = rw.get_data(params=params, filepath=filepath, return_df=True)
    >>> #
    >>> print(data.head())
    >>> #
    >>> # Locatie_MessageID Coordinatenstelsel  ...  WaardeBewerkingsmethode.Code
    >>> WaardeBewerkingsmethode.Omschrijving
    >>> # 0              18878              25831  ...
    >>> NaN                                   NaN
    >>> # 1              18878              25831  ...
    >>> NaN                                   NaN
    >>> # 2              18878              25831  ...
    >>> NaN                                   NaN
    >>> # 3              18878              25831  ...
    >>> NaN                                   NaN
    >>> # 4              18878              25831  ...
    >>> NaN                                   NaN
    >>> # [5 rows x 54 columns]

    """
    logger.info("Get data")
    _check_filepath(filepath, return_df)

    df_observations = pd.DataFrame()
    download_list = _create_download_list(params)
    counter = 1

    for request in download_list:
        df_observations = _download_observations(
            counter, df_observations, download_list, request, return_df, filepath
        )

        counter += 1

    if return_df:
        logger.info("dataframe returned: %s" % (str(df_observations.shape)))
        return df_observations
    return None


def _check_filepath(filepath, return_df):
    if filepath is None and not return_df:
        raise Exception("Give a filepath or set return_df to True.")
    elif filepath is not None and filepath is os.path.isdir(os.path.dirname(filepath)):
        raise Exception("Directory does not exist.")


def _download_observations(
    counter, df_observations, download_list, request, return_df, filepath
):
    print(f"Downloading {counter} of {len(download_list)}", end="\r")
    response = _request_observation(
        request[0],
        request[1],
        request[2],
        request[3],
        request[4],
        request[5],
        request[6],
        request[7],
        request[8],
    )
    df_observation = _parse_observation_response(response)
    if filepath is not None:
        _save_data(df_observation, filepath)
    if return_df:
        df_observations = pd.concat(
            [df_observations, df_observation], ignore_index=True
        )
    return df_observations


def update_dataframe(filepath, till_date: str) -> pd.DataFrame:
    """Update an existing dataframe from Waterinfo until a specified date.

    This function updates an existing dataframe with new observations from
    Waterinfo until the specified date.
    The function retrieves the parameters from the existing dataframe file, adds
    the till_date parameter,
    and then queries Waterinfo for new observations. The new observations are then
    concatenated with
    the existing dataframe to create a new dataframe with all the observations.

    Parameters
    ----------
    filepath : str
        The file path of the existing dataframe with observations from Waterinfo.
    till_date : str
        The date until which the observations need to be updated. Format:
        'YYYY-MM-DD'.

    Returns
    -------
    pandas.DataFrame
        A new dataframe with the existing observations and new observations.

    Raises
    ------
    Exception
        If `till_date` is `None`.

    Examples
    --------
    >>> import pandas as pd
    >>> import rws_waterinfo as rw
    >>> #
    >>> filepath = 'path/to/dataframe.csv'
    >>> till_date = '2023-03-22'
    >>> updated_dataframe = update_dataframe(filepath, till_date)
    """
    if till_date is None:
        raise Exception(
            "Please provide a till_date until which to update the dataframe."
        )

    parameters = _retrieve_parameters(filepath)
    parameters = _add_till_date_to_parameters(parameters, till_date)

    df_new_observations = get_data(parameters, return_df=True)
    df_observations = pd.read_csv(filepath)
    df_observations = pd.concat(
        [df_observations, df_new_observations], ignore_index=True
    )

    return df_observations


# %% Helpers Catalog
def _request_catalog():
    """Import location, parameter, and the combination data from Waterinfo.

    Post a request to the Waterinfo URL_CATALOGUS and parse the response content
    to a JSON format.

    Returns
    -------
    response: json
        A JSON file containing the parsed content of the post response. This includes:
        - Locatielijst (location_list): A list of locations where parameters have been
            measured. Each location has a unique ID and geographical coordinates.
        - AquoMetadatalijst (aquometadata_list): A list of unique parameters that have
            been measured.
            Each parameter has a unique ID, a description, and a unit of measurement.
        - AquoMetadataLocatieLijst (combination_list):
            A list that shows which parameters have been measured at which locations.
            It includes the ID of each location in the location_list and the ID
            of each parameter in the aquometadata_list.

    Notes
    -----
    This function is used to import data from Waterinfo for further processing and analysis.
    """
    logger.debug("_request_catalog")
    response = requests.post(URL_CATALOGUS, json=PARAMETERS_REQUEST_CATALOG, timeout=60)
    response = response.json()

    return response


def _parse_catalog_response(response):
    """Parse the json response to a Pandas dataframe.

    Parse the json response with locations, aquometadata and combinations into one
    pandas dataframe. The combination_list will be used to combinate the locations with
    the aquometadata.

    Parameters
    ----------
    response: json
        takes the response of request_catalog

    Returns
    -------
    dataframe: pd.DataFrame
        Pandas DataFrame containing the parsed content of the json response.
    """
    logger.debug("_parse_catalog_response")
    location_list = pd.json_normalize(response["LocatieLijst"])
    aquometadata_list = pd.json_normalize(response["AquoMetadataLijst"])
    aquo_location_combination_list = pd.json_normalize(
        response["AquoMetadataLocatieLijst"]
    )

    dataframe = pd.merge(
        aquo_location_combination_list,
        location_list,
        on="Locatie_MessageID",
        how="left",
    )

    dataframe = pd.merge(
        dataframe,
        aquometadata_list,
        left_on="AquoMetaData_MessageID",
        right_on="AquoMetadata_MessageID",
        how="left",
    )

    # drops the column "AquoMetadata_MessageID" because it's duplicated.
    dataframe = dataframe.drop(columns="AquoMetadata_MessageID")

    return dataframe


# %% Helpers for data
def _save_data(df_observations, filepath):
    """
    Save observations DataFrame to a CSV file.

    Parameters
    ----------
    df_observations : pandas DataFrame
        DataFrame containing the observations data to save.
    filepath : str
        Name of the file to save the data to.
        If the file already exists, the new data will be appended to it.

    """
    header = True
    if os.path.isfile(filepath):
        header = False

    df_observations.to_csv(filepath, mode="a", header=header, index=False)


def _create_download_list(requests_list):
    """Create a list of requests for downloading data from Waterinfo.

    Parameters
    ----------
    request_list : list of lists
        Each inner list should contain 9 elements representing a request:
        [compartiment_code, eenheid_code, meetapparaat_code, grootheid_code,
        locatie_code,
        cor_x, cor_y, start_date, end_date]

    Returns
    -------
    download_list : list of lists
        Each inner list contains the same 9 elements as in requests_list, but with the
        start_date and end_date values replaced by the start and end dates of smaller
        time intervals within the original period, to allow downloading larger data
        volumes.
    """
    download_list = []

    for request in requests_list:
        date_list = _date_list(request[7], request[8])
        for dates in date_list:
            request[7] = dates[0]
            request[8] = dates[1]
            download_list.append(request.copy())

    return download_list


def _date_list(input_begin_date, input_end_date):
    """Create a list of start and end dates in the format required by Waterinfo.

    Parameters
    ----------
    input_begin_date : str
        The start date of the period for requesting observations.
    input_end_date : str
        The end date of the period for requesting observations.

    Returns
    -------
    list of str
        A list of pairs of start and end dates, where each date is formatted in the
        format
        required by Waterinfo. The last pair of dates will end at input_end_date.
    """
    input_begin_date = datetime.datetime.fromisoformat(input_begin_date)
    input_end_date = datetime.datetime.fromisoformat(input_end_date)
    timedelta_year = input_end_date.year - input_begin_date.year
    counter = 0
    date_list = []

    if timedelta_year < 1:
        end = input_begin_date
        date_list.append(
            [_date_formatter(input_begin_date), _date_formatter(input_end_date)]
        )
    while timedelta_year > counter:
        start = datetime.datetime(
            input_begin_date.year + counter,
            input_begin_date.month,
            input_begin_date.day,
        )
        end = datetime.datetime(
            input_begin_date.year + counter + 1,
            input_begin_date.month,
            input_begin_date.day,
        )

        date_list.append([_date_formatter(start), _date_formatter(end)])
        counter += 1

    date_list[-1][-1] = _date_formatter(input_end_date)

    return date_list


def _date_formatter(input_date):
    """Transform a date/time into a datetime format for Waterinfo.

    Parameters
    ----------
    input_date : str, datetime.datetime or pandas.Timestamp
        The date/time that needs to be transformed to the format required by Waterinfo.

    Returns
    -------
    date_time : str
        A string representing the date/time in the format required by Waterinfo.
    """
    date_formatted = input_date.strftime("%Y-%m-%d")
    time_formatted = input_date.strftime("%H:%M:%S.%f")[:-3]
    date_time = str(date_formatted) + "T" + str(time_formatted) + "+01:00"
    return date_time


def _request_observation(
    compartiment_code: str,
    eenheid_code: str,
    meetapparaat_code: str,
    grootheid_code: str,
    locatie_code: str,
    cor_x: float,
    cor_y: float,
    start_date: str,
    end_date: str,
):
    """
    Import observation data from Waterinfo webservice.

    Parameters
    ----------
    compartiment_code : str
        Compartiment code from Waterinfo.
    eenheid_code : str
        Eenheid code from Waterinfo.
    meetapparaat_code : str
        Meetapparaat code from Waterinfo.
    grootheid_code : str
        Grootheid code from Waterinfo.
    locatie_code : str
        Locatie code from Waterinfo.
    cor_x : float
        x coordinate from Waterinfo (in format: Europe - onshore and offshore.
        EPSG:25831).
    cor_y : float
        y coordinate from Waterinfo (in format: Europe - onshore and offshore.
        EPSG:25831).
    start_date : str
        Start date of the period of the request (in format: yyyy-mm-dd).
    end_date : str
        End date of the period of the request (in format: yyyy-mm-dd).

    Returns
    -------
    response_formatted : json
        json file with the requested observations data
    """
    request = {
        "AquoPlusWaarnemingMetadata": {
            "AquoMetadata": {
                "Compartiment": {"Code": compartiment_code},
                "Eenheid": {"Code": eenheid_code},
                "MeetApparaat": {"Code": meetapparaat_code},
                "Grootheid": {"Code": grootheid_code},
            }
        },
        "Locatie": {"X": cor_x, "Y": cor_y, "Code": locatie_code},
        "Periode": {"Begindatumtijd": start_date, "Einddatumtijd": end_date},
    }

    try:
        response = requests.post(URL_REQUEST_OBSERVATIONS, json=request, timeout=60)

        response_formatted = response.json()
    except requests.exceptions.Timeout:

        response_formatted = {}

    return response_formatted


def _parse_observation_response(data):
    """Format json file with observations to a dataframe.

    Parameters
    ----------
    data : json
        Data of the observations in json format

    Returns
    -------
    df_waarnemingen : pd.DataFrame
        The observations data inside a pd.DataFrame
    """
    df_observations = pd.DataFrame()
    try:
        for waarneming in data["WaarnemingenLijst"]:
            df_locatie = pd.json_normalize(waarneming["Locatie"])
            df_metingen = pd.json_normalize(waarneming["MetingenLijst"])
            df_aquo = pd.json_normalize(waarneming["AquoMetadata"])

            df_observation = pd.merge(df_locatie, df_metingen, how="cross")
            df_observation = pd.merge(df_observation, df_aquo, how="cross")
            df_observation.replace(
                ["NVT", "Niet van toepassing", "Waarde is niet van toepassing"],
                np.NaN,
                inplace=True,
            )

            df_observations = pd.concat(
                [df_observations, df_observation], ignore_index=True
            )
    except KeyError:
        pass
    return df_observations


# %% Helpers for update_dataframe
def _add_till_date_to_parameters(parameters, till_date):
    """Add a till date to each item in a list of parameters.

    Parameters
    ----------
    parameters : list
        A list of parameters, where each parameter is a list of values.
    till_date : Any
        The till date to add to each parameter.

    Returns
    -------
    list
        A new list of parameters, where each parameter from the original list has
        the till date appended at the end.
    """
    for item in parameters:
        item.append(till_date)

    return parameters


def _retrieve_parameters(filepath):
    """Retrieve parameters from an existing dataframe for updating.

    Parameters
    ----------
    filepath : str
        The file path of the CSV file containing the parameters to be retrieved.

    Returns
    -------
    df_nes : list
        A list of lists containing the necessary parameters of the observation. The
        sublists
        contain the following columns in the specified order:
        - Compartiment.Code
        - Eenheid.Code
        - MeetApparaat.Code
        - Grootheid.Code
        - Code
        - X
        - Y
        - Tijdstip

    """
    columns = [
        "Compartiment.Code",
        "Eenheid.Code",
        "MeetApparaat.Code",
        "Grootheid.Code",
        "Code",
        "X",
        "Y",
        "Tijdstip",
    ]
    df_nes = pd.read_csv(filepath, usecols=columns)
    df_nes = df_nes[columns]
    df_nes = df_nes.sort_values("Tijdstip", ascending=True)
    df_nes = df_nes.drop_duplicates(
        subset=[
            "Compartiment.Code",
            "Eenheid.Code",
            "MeetApparaat.Code",
            "Grootheid.Code",
            "Code",
            "X",
            "Y",
        ],
        keep="last",
    )
    df_nes = df_nes.fillna("")
    df_nes = df_nes.values.tolist()

    return df_nes


# %% Other Helpers


# %%
def disable_tqdm():
    """Set the logger for verbosity messages."""
    return True if (logger.getEffectiveLevel() >= 30) else False


# %% Variables
URL_CATALOGUS = (
    "https://waterwebservices.rijkswaterstaat.nl/METADATASERVICES_DBO/OphalenCatalogus/"
)

URL_REQUEST_OBSERVATIONS = (
    "https://waterwebservices.rijkswaterstaat.nl/"
    + "ONLINEWAARNEMINGENSERVICES_DBO/OphalenWaarnemingen"
)

PARAMETERS_REQUEST_CATALOG = {
    "CatalogusFilter": {
        "Grootheden": True,
        "Parameters": True,
        "Compartimenten": True,
        "Hoedanigheden": True,
        "Eenheden": True,
        "BemonsteringsApparaten": True,
        "BemonsteringsMethoden": True,
        "BemonsteringsSoorten": True,
        "BioTaxon": True,
        "BioTaxon_Compartimenten": True,
        "MeetApparaten": True,
        "MonsterBewerkingsMethoden": True,
        "Organen": True,
        "PlaatsBepalingsApparaten": True,
        "Typeringen": True,
        "WaardeBepalingstechnieken": True,
        "WaardeBepalingsmethoden": True,
        "WaardeBewerkingsmethoden": True,
    }
}

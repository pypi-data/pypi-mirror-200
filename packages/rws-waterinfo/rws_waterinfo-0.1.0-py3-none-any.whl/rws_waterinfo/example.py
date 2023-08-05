"""Module to do an example run of the WaterInfo lib."""
# # %% test
# import os

# import rws_waterinfo as rw

# # %% Example to retrieve catalog
# # dirname = os.path.dirname(__file__)
# filename = os.path.join("../data/catalog.csv")

# df_catalog = rw.get_catalog()

# df_catalog.to_csv(filename)

# # %% Example to retrieve observations
# params = [
#     [
#         "OW",
#         "cm",
#         127,
#         "WATHTE",
#         "WIJK",
#         657488.747441661,
#         5760655.26068351,
#         "2023-01-01",
#         "2023-01-02",
#     ],
#     [
#         "OW",
#         "cm",
#         127,
#         "WATHTE",
#         "WEES",
#         637499.067705518,
#         5798364.14113639,
#         "2023-01-01",
#         "2023-01-02",
#     ],
# ]

# # %% With filepath

# # dirname = os.path.dirname(__file__)
# filename = os.path.join("../data/wijkweesp01.csv")

# rw.get_data(params, filepath=filename)

# # %% With returning dataframe
# df_data1 = rw.get_data(params, return_df=True)

# # %%  With filepath and returning dataframe

# params = [
#     [
#         "OW",
#         "m3/s",
#         156,
#         "Q",
#         "OLST",
#         711556.219876449,
#         5803627.64455833,
#         "2023-01-01",
#         "2023-01-02",
#     ]
# ]


# filename = os.path.join("../data/olst.csv")

# df_data2 = rw.get_data(params, filepath=filename, return_df=True)




launch_announcement = "Running KevTerminal!\n"


def apply_settings():
    # webscraper.clone_data_into_csv = settings_dict['clone_data_into_csv']
    # mysqlinteractor.rebuild_database = settings_dict['rebuild_sql_database']
    print(f"{launch_announcement}")


settings_dict = {'stats_dec_places': 2,
                 'clone_data_into_csv': True,
                 'rebuild_sql_database': False}

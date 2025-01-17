from xlrd import Book


COLUMN_NAMES = ['Likely or Exp. Voters', 'Eligible Voters', 'Ballot Length Measure']


def fetch_location_data(voting_config: Book, settings: dict) -> dict:
    '''
        Fetches the locations sheet from the input xlsx as a dict.

        Params:
            voting_config (xlrd.Book) : input xlsx sheet,
            settings (dict) : sheet settings.

        Returns:
            (dict) : location sheet as a dict.
    '''
    location_sheet = voting_config.sheet_by_name(u'locations')

    location_data = {}

    for i in range(1, settings['NUM_LOCATIONS'] + 1):
        temp = settings['NUM_LOCATIONS']
        print(f'DEBUG: {temp}')
        data = map(int, location_sheet.row_values(i)[1:])  # [1:] drops ID column
        print(f'DEBUG: {data}')
        location_data[i] = dict(zip(COLUMN_NAMES, data))

    return location_data

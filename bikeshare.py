import pandas as pd
import time

#df = pd.DataFrame

valid_cities = { 'W': ['Washington', 'washington.csv'],'C':['Chicago', 'chicago.csv'], 'N': ['New York', 'new_york_city.csv'] }

def get_city_filter():
    """
    Get user input of which city to analyse further

    Args:
        none
    Returns:
        city (string) Name of the city
    """
    while True: # Would you like to see data for Chicago, New York, or Washington?
        try:
            city = input('\nWould you like to see data for {} (C), {} (N) or {} (W) \n>>  City : '
                .format(valid_cities['C'][0],valid_cities['N'][0], valid_cities['W'][0])).upper()[0]
            if city in valid_cities:
                print('{} it is!'.format(valid_cities[city][0]))
                break
            else:
                print('Please select one of the cities below')
        except ValueError:
            print('Please enter a legal value')
    return city

def get_time_filter():
    """
    Get user input to limit data set by time variables

    Args:
        none
    Returns:
        month (string) - default All
        day (string) - default All
    """

    months = {1: 'January', 2:'February', 3: 'March', 4: 'April', 5: 'May', 6:'June'}
    month = 'All'
    days = {1:'Monday', 2: 'Tuesday', 3: 'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday', 7:'Sunday'}
    day = 'All'

    while True:
        try:
            detail = input('\nWould you like to filter the data by month (M), day (D), or not at all (N) \n>>  Filter : ').upper()[0]
            if detail == 'M':
                print('\nPlease type a number to filter by month of the year;')
                month_key = int(input('    {} (1), {} (2), {} (3)\n    {} (4), {} (5), {} (6) \n\n>>  Month : '
                .format(months[1],months[2],months[3],months[4],months[5],months[6] )))
                month = months[month_key]
                break
            elif detail == 'D':
                print('Please type a number to filter by day of the week;')
                day_key = int(input('    {}(1), {}(2), {}(3), {}(4), {}(5) \n    {}(6),  {}(7)\n\n>>  Day : '
                .format(days[1],days[2],days[3],days[4],days[5],days[6],days[7])))
                day = days[day_key]
                break
            elif detail == 'N':
                break
            else:
                print('Please select one of the alternatives below')
        except ValueError:
            print('Please enter a legal value')

    return month, day


def load_city(city):
    """
    Load data frame from csv-file based on city set by user. Offers user to browse data
    before returning the data frame

    Args:
        city (string)
    Returns:
        df (panda.DataFrame)
    """
    print('\nLoading bike share data for {} '.format(valid_cities[city][0]))

    file_name = valid_cities[city][1]
    df = pd.read_csv(file_name)
    line_count = 5
    while True:
        try:
            cont = input('\nWould you like a quick look at the loaded data set? \n>>  [Y]es/[N]o  : ').upper()
            if cont == 'Y':
                print('\n' *2)
                print('-'*20 + ' Preparing the data ' + '-'*20 )
                print('\n*** General info about the data set:\n')
                print(df.info())
                print('\n*** First 5 rows in the data set:\n')
                print(df.head())
                while True:
                    cont = input('\nWould you like to see more before we start the analysis? \n>>  [Y]es /[N]o : ').upper()
                    if cont == 'Y':
                        print(df.iloc[line_count : line_count + 5])
                        line_count += 5
                    else:
                        break
            else:
                print('\nProceeding with the analysis')
            break
        except ValueError:
            print('Please enter a legal value')

    return df



def prepare_data(df, month, day):
    """
    Prepare data frame for analysis. Limit data frame based on time filter set by user.

    Args:
        df (DataFrame) - DataFrame containing selected city
        month (string)
        day (string)
    Returns:
        df  (DataFrame) - prepared and filtered
    """
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day of Week'] = df['Start Time'].dt.day_name()

    if month != 'All':
        print('Rows in data set without month filter : {}'.format(df.shape[0]))
        df = df[df['Month'] == month]
        print('Rows in data set when month filter is applied : {}'.format(df.shape[0]))
    elif day != 'All':
        print('Rows in data set without day filter : {}'.format(df.shape[0]))
        df =  df[df['Day of Week'] == day]
        print('Rows in data set when day filter is applied : {}'.format(df.shape[0]))

    return df

def time_stats(df):
    """
    Calculate and present stats regardning travel times.

    Args:
        df (DataFrame)
    Returns:
        None
    """
    start_time = time.time()
    print('\n' *2)
    print('-'*20 + ' Time stats ' + '-'*20 )

    # TO DO: display the most common month
    common_month = df['Month'].mode()[0].upper()
    print('\n{} is the most common month for bike riding.'.format(common_month))
    # TO DO: display the most common day of week
    common_day = df['Day of Week'].mode()[0].upper()
    print('\n{} is the most common day for bike riding.'.format(common_day))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start = df['hour'].mode()[0]
    print('\nand {} is the most common hour to start the ride.'.format(common_start))

    print('\n')
    print(':'*10 +'Execution time: {0:.4f} seconds'.format(time.time()-start_time))

def station_stats(df):
    """
    Calculate and present stats regardning stations.

    Args:
        df (DataFrame)
    Returns:
        None
    """
    start_time = time.time()
    print('\n' *2)
    print('-'*20 + ' Station stats ' + '-'*20 )

    # TO DO: display most commonly used start station
    start = df['Start Station'].mode()[0]
    print('\nThe most frequently used "start station" is :\n- {}'.format(start))

    # TO DO: display most commonly used end station
    end = df['End Station'].mode()[0]
    print('\nThe most frequently used "end station" is :\n- {}'.format(end))

    # TO DO: display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + ' -- ' + df['End Station']
    route = df['route'].mode()[0]
    print('\nThe most frequently used "route" is :\n- {}'.format(route))


    print('\n')
    print(':'*10 +'Execution time: {0:.4f} seconds'.format(time.time()-start_time))


def user_stats(df, city):
    """
    Calculate and present stats regardning bike users.

    Args:
        df (DataFrame)
    Returns:
        None
    """
    start_time = time.time()

    print('\n' *2)
    print('-'*20 + ' User stats ' + '-'*20 )

    user_types = df['User Type'].value_counts()
    print('\nTypes of bike share users:')
    print('\n{}'.format(user_types))


    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('\n\nBike share users´ gender:')
        print('\n{}'.format(gender))
    else:
        print('\nNo gender statistics available from {} unfortunately'.format(valid_cities[city][0]))

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\n\nBike share users´ age :')
        oldest = df['Birth Year'].min()
        print('\n{} is the earliest birth year among riders.'.format(int(oldest)))

        youngest = df['Birth Year'].max()
        print('{} is the most recent birth year among riders.'.format(int(youngest)))

        common_yob = df['Birth Year'].mode()[0]
        print('{} is the most common birth year among riders.'.format(int(common_yob)))
    else:
        print('\nNo age statistics available from {} unfortunately'.format(valid_cities[city][0]))

    print('\n')
    print(':'*10 +'Execution time: {0:.4f} seconds'.format(time.time()-start_time))






def main():
    print('-'*15 + ' Starting bike share stats ' + '-'*15)

    while True:
        try:
        # city, month, day = get_filer() # return c, m, d
            city = get_city_filter()
            df = load_city(city)
            month, day = get_time_filter()
            df = prepare_data(df, month, day) # TO DO ikke laget enda
            time_stats(df)
            station_stats(df)
            key = input('\nHit any key to proceed to user statistics\n>>  : ')
            user_stats(df, city)
            print('\n' *2)
            print('-'*20 + ' End of stats ' + '-'*20 )
            quit = str(input('\nType [Q] to quit, or any other key if you would like to analyze a new set of data. \n>>  :')).lower()
            if quit == 'q':
                break
        except ValueError:
            print('Please enter a legal value')
        except IndexError:
            print('Please enter a legal value')







if __name__ == '__main__': # sørger for at main ikke kjøres ved import
    main()

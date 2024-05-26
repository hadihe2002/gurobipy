import pandas as pd
def get_time_params():
    times = pd.read_excel('Time Data.xlsx', index_col=0)
    keys = list(times.to_dict().keys())
    values = list(times.to_dict().values())
    time_params = {(j+1, i): k for i in range(1, len(keys)+1)
                   for j, k in enumerate(values[i-1].values())}
    return time_params

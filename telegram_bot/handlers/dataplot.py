import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

def process_data_and_plot(file_path):
    df = pd.read_csv(file_path, delimiter=';')
    result_df = pd.DataFrame(columns=['name_zone', 'start_time', 'end_time', 'status'])
    zone_1_df = df[['left_status', 'left_start_time', 'left_end_time']].rename(columns={
        'left_status': 'status',
        'left_start_time': 'start_time',
        'left_end_time': 'end_time'
    })
    zone_1_df['name_zone'] = 'Зона 1'
    zone_2_df = df[['right_status', 'right_start_time', 'right_end_time']].rename(columns={
        'right_status': 'status',
        'right_start_time': 'start_time',
        'right_end_time': 'end_time'
    })
    zone_2_df['name_zone'] = 'Зона 2'
    result_df = pd.concat([zone_1_df, zone_2_df], ignore_index=True)
    result_df['start_time'] = pd.to_datetime(result_df['start_time'], unit='s')
    result_df['end_time'] = pd.to_datetime(result_df['end_time'], unit='s')
    today = datetime.today().date()
    result_df['start_time'] = result_df['start_time'].apply(lambda x: x.replace(year=today.year, month=today.month, day=today.day))
    result_df['end_time'] = result_df['end_time'].apply(lambda x: x.replace(year=today.year, month=today.month, day=today.day))
    result_df['duration'] = (result_df['end_time'] - result_df['start_time'])

    total_time_per_status = result_df.groupby(['name_zone', 'status'])['duration'].sum().reset_index()
    total_time_per_status['duration'] = total_time_per_status['duration'].dt.total_seconds().apply(lambda x: str(timedelta(seconds=x)))
    total_time_per_status['status'] = total_time_per_status['status'].replace({'active': 'Активная работа', 'chill': 'Простой', 'passive': 'Вынужденная работа'})
    color_map = {'active': 'green', 'passive': 'blue', 'chill': 'red'}
    # Фильтруем строки, где значение в столбце name_zone не равно 0
    filtered_df = result_df[result_df['name_zone'] != 0]

    # Строим таймлайн с отфильтрованными данными
    fig = px.timeline(filtered_df, height=300, width=1000, x_start="start_time", x_end="end_time", y="name_zone", color="status", color_discrete_map=color_map)

    fig.update_layout(title_text='Таймлайн', xaxis_title='Время', yaxis_title='Рабочие зоны')
    fig.write_image("plot.png")
    return total_time_per_status



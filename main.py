import matplotlib.pyplot as plt
import seaborn as sns

from utils import Song, process

songs = [
    Song(name='Bolo By Fight', path='res/timelines (1).csv', color='#FF0072', release='07-21-2022'),
    Song(name='Asfalto', path='res/timelines (2).csv', color='#00A2A4', release='11-03-2022')
]

sns.set_theme(style='whitegrid', context='talk', palette=sns.color_palette([s.color for s in songs]))

histplot = False
stackplot = True
lineplot = True
cumplot = True

if __name__ == '__main__':
    # PLOT DATA HISTOGRAMS
    if histplot:
        plt.figure(figsize=(16, 9), tight_layout=True)
        data = process(songs, window=0)
        sns.histplot(
            data=data,
            x='streams',
            hue='Song',
            stat='proportion',
            binwidth=5,
            kde=True,
            multiple='layer',
            legend=True
        )
        plt.show()

    # PLOT STACKED STREAMS
    if stackplot:
        plt.figure(figsize=(16, 9), tight_layout=True)
        data = process(songs, window=0).reset_index(level=0)
        data = data.pivot(columns='Song', index='date', values='streams').fillna(0.0)
        plt.stackplot(
            data.index,
            *[data[s.name] for s in songs],
            edgecolor='black',
            linewidth=1,
            labels=[s.name for s in songs]
        )
        sns.despine()
        plt.legend()
        plt.xlim(data.index.min(), data.index.max())
        plt.ylim(0)
        plt.xlabel('date')
        plt.ylabel('streams')
        plt.show()

    # PLOT COMPARED EMA STREAMS
    if lineplot:
        plt.figure(figsize=(16, 9), tight_layout=True)
        data = process(songs, window=7, win_type='exponential')
        sns.lineplot(
            data=data,
            x='day',
            y='streams',
            hue='Song',
            hue_order=[s.name for s in songs],
            style='Song',
            style_order=[s.name for s in songs],
            linewidth=2,
            markersize=7,
            markers='o',
            legend=True
        )
        sns.despine()
        plt.xlim(1, data['day'].max())
        plt.ylim(0)
        plt.show()

    # PLOT COMPARED CUMULATIVE STREAMS
    if lineplot:
        plt.figure(figsize=(16, 9), tight_layout=True)
        data = process(songs, window=0)
        sns.lineplot(
            data=data,
            x='day',
            y='cumulative streams',
            hue='Song',
            hue_order=[s.name for s in songs],
            style='Song',
            style_order=[s.name for s in songs],
            linewidth=2,
            markersize=7,
            markers='o',
            legend=True
        )
        sns.despine()
        plt.xlim(1, data['day'].max())
        plt.ylim(0)
        plt.show()

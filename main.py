from datetime import timedelta

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

from utils import Song, merge_songs, blend_color

songs = [
    Song(
        name='Bolo By Fight',
        song='res/bolo-by-fight.csv',
        profile='res/public.csv',
        color='#FF0072',
        release='07-21-2022'
    ),
    Song(
        name='Asfalto',
        song='res/asfalto.csv',
        profile='res/public.csv',
        color='#00A2A4',
        release='11-03-2022',
        promo=[('11-24-2022', '12-01-2022')]
    ),
    Song(
        name='Natale Con I Tuoi',
        song='res/natale-con-i-tuoi.csv',
        profile='res/public.csv',
        color='#FFC801',
        release='12-18-2022',
        promo=[('12-22-2022', '12-30-2022')]
    )
]

# plotting parameters
WEEKS = 6
WINDOW = 7
WIN_TYPE = 'cosine'
FIGSIZE = (11, 7.5)
EXPORT = 'pdf'

sns.set_theme(style='whitegrid', context='poster')
colors = [song.color for song in songs]

if __name__ == '__main__':
    for average in [False, True]:
        if average:
            title, export, window, win_type = f' ({WINDOW}-days avg.)', '_avg', WINDOW, WIN_TYPE
        else:
            title, export, window, win_type = '', '', 1, None

        # PLOT DAILY LISTENERS (use data from the first released song)
        ax = plt.figure(figsize=FIGSIZE, tight_layout=True).gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        data = songs[0].rolling(window=window, win_type=win_type)
        sns.lineplot(data=data, x='date', y='listeners', linewidth=2, color='black')
        plt.xlim(data['date'].min(), data['date'].max())
        _, y_max = plt.ylim(0, 330)
        for song in songs:
            # y_max = data[data['date'] == song.release]['listeners']
            plt.vlines(song.release, 0, y_max, colors=song.color, linewidth=2, linestyles='--', label=song.name)
        for song in songs:
            for s, e in song.promos:
                promo = data.set_index('date')[s:e + timedelta(days=1)]
                color = blend_color(song.color, alpha=0.3)
                plt.fill_between(promo.index, promo['listeners'], facecolor=color, edgecolor='none')
        # dummy fill to add "Promo Period" marker in the legend
        plt.fill_between([], 0, facecolor=blend_color('#000000', alpha=0.3), edgecolor='none', label='(Promo Period)')
        plt.legend(title='Song Release')
        plt.title(f'Daily Listeners{title}')
        plt.savefig(f'exports/listeners{export}.{EXPORT}', format=EXPORT)
        plt.show()

        # PLOT STACKED DAILY STREAMS (use partial data from all the songs instead of the total number)
        ax = plt.figure(figsize=FIGSIZE, tight_layout=True).gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        data = merge_songs(songs, window=window, win_type=win_type).reset_index()
        data = data.pivot(columns='Song', index='date', values='streams').fillna(0.0)
        plt.xlabel('date')
        plt.xlim(data.index.min(), data.index.max())
        plt.ylabel('streams')
        plt.ylim(0, 410)
        plt.stackplot(
            data.index,
            *[data[s.name] for s in songs],
            edgecolor='black',
            linewidth=2,
            labels=[s.name for s in songs],
            colors=colors
        )
        sns.despine()
        plt.legend(loc='upper left', title='Song')
        plt.title(f'Daily Streams{title}')
        plt.savefig(f'exports/streams{export}.{EXPORT}', format=EXPORT)
        plt.show()

        # PLOT COMPARED DAILY STREAMS
        ax = plt.figure(figsize=FIGSIZE, tight_layout=True).gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        data = merge_songs(songs, window=window, win_type=win_type)
        data = data[data['day'] <= WEEKS * 7]
        plt.xticks(range(1, data['day'].max(), 7))
        plt.xlim(data['day'].min(), data['day'].max())
        plt.ylim(0, 410)
        for song in songs:
            for s, e in song.promos:
                promo = data[data['Song'] == song.name].set_index('date')[s:e + timedelta(days=1)]
                color = blend_color(song.color, alpha=0.1)
                plt.fill_between(promo['day'], promo['streams'], facecolor=color, edgecolor='none')
        sns.lineplot(
            data=data,
            x='day',
            y='streams',
            hue='Song',
            hue_order=[s.name for s in songs],
            style='Song',
            style_order=[s.name for s in songs],
            palette=colors,
            linewidth=2
        )
        # dummy fill to add "Promo Period" marker in the legend
        plt.fill_between([], 0, facecolor=blend_color('#000000', alpha=0.3), edgecolor='none', label='(Promo Period)')
        plt.legend(title='Song')
        sns.despine()
        plt.title(f'Streams in the first {WEEKS} Weeks after Release{title}')
        plt.savefig(f'exports/releases{export}.{EXPORT}', format=EXPORT)
        plt.show()

        # PLOT COMPARED FOLLOWERS
        ax = plt.figure(figsize=FIGSIZE, tight_layout=True).gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        data = merge_songs(songs, window=window, win_type=win_type)
        data = data[data['day'] <= WEEKS * 7]
        plt.xticks(range(1, data['day'].max(), 7))
        plt.xlim(data['day'].min(), data['day'].max())
        plt.ylim(0, 24)
        for song in songs:
            for s, e in song.promos:
                promo = data[data['Song'] == song.name].set_index('date')[s:e + timedelta(days=1)]
                color = blend_color(song.color, alpha=0.1)
                plt.fill_between(promo['day'], promo['followers'], facecolor=color, edgecolor='none')
        sns.lineplot(
            data=data,
            x='day',
            y='followers',
            hue='Song',
            hue_order=[s.name for s in songs],
            style='Song',
            style_order=[s.name for s in songs],
            palette=colors,
            linewidth=2
        )
        # dummy fill to add "Promo Period" marker in the legend
        plt.fill_between([], 0, facecolor=blend_color('#000000', alpha=0.3), edgecolor='none', label='(Promo Period)')
        plt.legend(title='Song')
        sns.despine()
        plt.title(f'Followers in the first {WEEKS} Weeks after Release{title}')
        plt.savefig(f'exports/followers{export}.{EXPORT}', format=EXPORT)
        plt.show()

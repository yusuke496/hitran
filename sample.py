from hapi import *
import numpy as np
import plotly

# パラメータを指定
# --- ここから ---

# スペクトルの範囲
spectrum_begin = 400 # nm
spectrum_end = 4000

# HITRAN のパラメータ
name = 'H2O'
moleculeID = 1
isotopologueID = 1

# --- ここまで ---

db_begin('data')

fetch(name, moleculeID, isotopologueID, spectrum_begin, spectrum_end)

# 取得したテーブルから、必要な情報を取得
nu, sw = getColumns(name, ['nu', 'sw']) # 波長, 線強度

# 振動準位の上下を取得
global_upper_quanta, global_lower_quanta = getColumns(name, ['global_upper_quanta','global_lower_quanta'])

# 回転準位の上下を取得
local_upper_quanta, local_lower_quanta = getColumns(name, ['local_upper_quanta','local_lower_quanta'])

# 以下、グラフ作成

# グラフに表示するための、量子数のラベルを作成
graph_label = ['global : ' + str(a)  + str(b) +  '   lolal : ' + str(c) + str (d) for a, b, c, d in zip(global_upper_quanta, global_lower_quanta, local_upper_quanta, local_lower_quanta)]

# プロットするデータの指定
data = [
    plotly.graph_objs.Scatter(x=nu, y=sw, name="HITRAN\'s " + str(name) + " data",mode = 'markers', text=graph_label)
]

# グラフレイアウトの指定
layout = plotly.graph_objs.Layout(
    title="HITRAN\'s " + str(name) + " data from " + str(spectrum_begin) + " to "  + str(spectrum_end),
    xaxis={"title":"1/CM"},
    yaxis={"title":"Line intensity"}
)

# プロット
fig = plotly.graph_objs.Figure(data=data, layout=layout)
plotly.offline.plot(fig)

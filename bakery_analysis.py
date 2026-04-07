# ============================================================
# COM7021 - Data Visualisation Portfolio
# European Bakery Sales Analysis
# Farid Negahbani
# Student ID:24154844
# ============================================================

# ============================================================
# SECTION 1: IMPORT LIBRARIES
# ============================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12

# ============================================================
# SECTION 2: DATA LOADING & CLEANING
# ============================================================
print("=" * 60)
print("SECTION 2: DATA LOADING & CLEANING")
print("=" * 60)

df = pd.read_excel("dataset\Data Visualisation - COM7021 - [4566] Bakery- supporting document.xlsx")

print(f"\nDataset Shape: {df.shape}")
print(f"\nColumn Names:\n{df.columns.tolist()}")
print(f"\nFirst 5 Rows:")
print(df.head())
print(f"\nData Types:\n{df.dtypes}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nBasic Statistics:\n{df.describe()}")

# --- Data Cleaning ---

df['Confectionary'] = df['Confectionary'].str.strip()
df['Confectionary'] = df['Confectionary'].replace({
    'Choclate Chunk': 'Chocolate Chunk',
    'Caramel nut': 'Caramel Nut'
})

print(f"\nUnique Cities: {df['City'].unique()}")
print(f"Unique Confectionery: {df['Confectionary'].unique()}")

print(f"\n--- Missing Values Before Cleaning ---")
print(df.isnull().sum())

df_clean = df.dropna(subset=['Profit(£)'])

for col in ['Revenue(£)', 'Cost(£)', 'Units Sold']:
    df_clean[col] = df_clean.groupby(['City', 'Confectionary'])[col].transform(
        lambda x: x.fillna(x.median())
    )

print(f"\n--- Missing Values After Cleaning ---")
print(df_clean.isnull().sum())
print(f"\nCleaned Dataset Shape: {df_clean.shape}")

df_clean['Date'] = pd.to_datetime(df_clean['Date'])
df_clean['Year'] = df_clean['Date'].dt.year
df_clean['Month'] = df_clean['Date'].dt.month
df_clean['Quarter'] = df_clean['Date'].dt.quarter
df_clean['YearMonth'] = df_clean['Date'].dt.to_period('M')

df_clean['Profit_Margin(%)'] = (df_clean['Profit(£)'] / df_clean['Revenue(£)']) * 100

print(f"\nDate Range: {df_clean['Date'].min()} to {df_clean['Date'].max()}")
print(f"Years Covered: {sorted(df_clean['Year'].unique())}")

df_clean.to_csv('bakery_cleaned.csv', index=False)
print("\n[x] Cleaned data saved to 'bakery_cleaned.csv'")


# ============================================================
# SECTION 3: EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================
print("\n" + "=" * 60)
print("SECTION 3: EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# 3a. Summary statistics by city
city_summary = df_clean.groupby('City').agg(
    Total_Revenue=('Revenue(£)', 'sum'),
    Total_Cost=('Cost(£)', 'sum'),
    Total_Profit=('Profit(£)', 'sum'),
    Total_Units=('Units Sold', 'sum'),
    Avg_Profit_Margin=('Profit_Margin(%)', 'mean'),
    Transaction_Count=('Profit(£)', 'count')
).round(2)
print("\n--- City Summary ---")
print(city_summary)

conf_summary = df_clean.groupby('Confectionary').agg(
    Total_Revenue=('Revenue(£)', 'sum'),
    Total_Cost=('Cost(£)', 'sum'),
    Total_Profit=('Profit(£)', 'sum'),
    Total_Units=('Units Sold', 'sum'),
    Avg_Profit_Margin=('Profit_Margin(%)', 'mean'),
    Transaction_Count=('Profit(£)', 'count')
).round(2)
print("\n--- Confectionery Summary ---")
print(conf_summary)

print("\n--- City × Confectionery Combination Counts ---")
combo_counts = df_clean.groupby(['City', 'Confectionary']).size().unstack(fill_value=0)
print(combo_counts)
print("\nMissing combinations (0 records):")
for city in combo_counts.index:
    for conf in combo_counts.columns:
        if combo_counts.loc[city, conf] == 0:
            print(f"  ⚠ {city} × {conf} — NO DATA")


# ============================================================
# SECTION 4: STATIC VISUALISATIONS (Matplotlib & Seaborn)
# ============================================================
print("\n" + "=" * 60)
print("SECTION 4: STATIC VISUALISATIONS")
print("=" * 60)

fig1, ax1 = plt.subplots(figsize=(10, 6))
city_profit = df_clean.groupby('City')['Profit(£)'].sum().sort_values(ascending=True)
colors = sns.color_palette("RdYlGn", len(city_profit))
bars = ax1.barh(city_profit.index, city_profit.values, color=colors)
ax1.set_xlabel('Total Profit (£)', fontsize=13)
ax1.set_title('Figure 1: Total Profit by European City', fontsize=15, fontweight='bold')
for bar, val in zip(bars, city_profit.values):
    ax1.text(val + 500, bar.get_y() + bar.get_height() / 2,
             f'£{val:,.0f}', va='center', fontsize=11)
plt.tight_layout()
plt.savefig('fig1_profit_by_city.png', dpi=300, bbox_inches='tight')
plt.show()
print("[x] Figure 1 saved")


fig2, ax2 = plt.subplots(figsize=(12, 6))
city_rev_cost = df_clean.groupby('City')[['Revenue(£)', 'Cost(£)', 'Profit(£)']].sum()
city_rev_cost.plot(kind='bar', ax=ax2, color=['#2196F3', '#F44336', '#4CAF50'])
ax2.set_title('Figure 2: Revenue, Cost & Profit by City', fontsize=15, fontweight='bold')
ax2.set_ylabel('Amount (£)', fontsize=13)
ax2.set_xlabel('City', fontsize=13)
ax2.legend(fontsize=11)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
plt.tight_layout()
plt.savefig('fig2_revenue_cost_profit_city.png', dpi=300, bbox_inches='tight')
plt.show()
print("[x] Figure 2 saved")


fig3, ax3 = plt.subplots(figsize=(12, 6))
conf_profit = df_clean.groupby('Confectionary')['Profit(£)'].sum().sort_values(ascending=True)
palette = sns.color_palette("viridis", len(conf_profit))
bars3 = ax3.barh(conf_profit.index, conf_profit.values, color=palette)
ax3.set_xlabel('Total Profit (£)', fontsize=13)
ax3.set_title('Figure 3: Total Profit by Confectionery Type', fontsize=15, fontweight='bold')
for bar, val in zip(bars3, conf_profit.values):
    ax3.text(val + 500, bar.get_y() + bar.get_height() / 2,
             f'£{val:,.0f}', va='center', fontsize=10)
plt.tight_layout()
plt.savefig('fig3_profit_by_confectionery.png', dpi=300, bbox_inches='tight')
plt.show()
print("[x] Figure 3 saved")



fig4, ax4 = plt.subplots(figsize=(12, 7))
pivot_profit = df_clean.pivot_table(
    values='Profit(£)', index='City', columns='Confectionary', aggfunc='sum'
)
pivot_profit = pivot_profit.fillna(0).round(0) 

annot_labels = pivot_profit.copy().astype(str)
for city in pivot_profit.index:
    for conf in pivot_profit.columns:
        original = df_clean.pivot_table(
            values='Profit(£)', index='City', columns='Confectionary', aggfunc='sum'
        )
        if pd.isna(original.loc[city, conf]) if city in original.index and conf in original.columns else True:
            annot_labels.loc[city, conf] = 'N/A'
        else:
            annot_labels.loc[city, conf] = f'{pivot_profit.loc[city, conf]:,.0f}'

sns.heatmap(pivot_profit, annot=annot_labels, fmt='', cmap='RdYlGn',
            linewidths=0.5, ax=ax4,
            cbar_kws={'label': 'Total Profit (£)', 'shrink': 0.8})
ax4.set_title('Figure 4: Profitability Heatmap — City vs Confectionery',
              fontsize=15, fontweight='bold')
ax4.set_ylabel('City', fontsize=13)
ax4.set_xlabel('Confectionery Type', fontsize=13)
plt.tight_layout()
plt.savefig('fig4_heatmap_profitability.png', dpi=300, bbox_inches='tight')
plt.show()
print("[x] Figure 4 saved")



fig5, ax5 = plt.subplots(figsize=(12, 7))
pivot_margin = df_clean.pivot_table(
    values='Profit_Margin(%)', index='City', columns='Confectionary', aggfunc='mean'
)

annot_labels5 = pivot_margin.copy().astype(str)
for city in pivot_margin.index:
    for conf in pivot_margin.columns:
        if pd.isna(pivot_margin.loc[city, conf]):
            annot_labels5.loc[city, conf] = 'N/A'
        else:
            annot_labels5.loc[city, conf] = f'{pivot_margin.loc[city, conf]:.1f}'

pivot_margin = pivot_margin.fillna(0).round(1) 

sns.heatmap(pivot_margin, annot=annot_labels5, fmt='', cmap='coolwarm',
            linewidths=0.5, ax=ax5, center=50,
            cbar_kws={'label': 'Average Profit Margin (%)', 'shrink': 0.8})
ax5.set_title('Figure 5: Average Profit Margin (%) — City vs Confectionery',
              fontsize=15, fontweight='bold')
ax5.set_ylabel('City', fontsize=13)
ax5.set_xlabel('Confectionery', fontsize=13)
plt.tight_layout()
plt.savefig('fig5_heatmap_margin.png', dpi=300, bbox_inches='tight')
plt.show()
print("[x] Figure 5 saved")


fig6, ax6 = plt.subplots(figsize=(14, 7))
yearly_city = df_clean.groupby(['Year', 'City'])['Profit(£)'].sum().reset_index()
for city in df_clean['City'].unique():
    city_data = yearly_city[yearly_city['City'] == city]
    ax6.plot(city_data['Year'], city_data['Profit(£)'], marker='o',
             linewidth=2.5, markersize=8, label=city)
ax6.set_title('Figure 6: Yearly Profit Trends by City (2000–2005)',
              fontsize=15, fontweight='bold')
ax6.set_xlabel('Year', fontsize=13)
ax6.set_ylabel('Total Profit (£)', fontsize=13)
ax6.legend(fontsize=11, title='City')
ax6.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig6_yearly_profit_trends.png', dpi=300, bbox_inches='tight')
plt.show()
print("[x] Figure 6 saved")


fig7, axes7 = plt.subplots(2, 3, figsize=(18, 10))
axes7 = axes7.flatten()
cities = df_clean['City'].unique()
for i, city in enumerate(cities):
    city_q = df_clean[df_clean['City'] == city].groupby(
        ['Year', 'Quarter'])['Profit(£)'].sum().reset_index()
    city_q['Period'] = city_q['Year'].astype(str) + '-Q' + city_q['Quarter'].astype(str)
    axes7[i].plot(range(len(city_q)), city_q['Profit(£)'], color=f'C{i}', linewidth=1.5)
    axes7[i].fill_between(range(len(city_q)), city_q['Profit(£)'], alpha=0.3, color=f'C{i}')
    axes7[i].set_title(f'{city}', fontsize=13, fontweight='bold')
    axes7[i].set_ylabel('Profit (£)')
    axes7[i].tick_params(axis='x', rotation=90, labelsize=7)
    axes7[i].set_xticks(range(0, len(city_q), 4))
    axes7[i].set_xticklabels(city_q['Period'].iloc[::4], rotation=45)
if len(cities) < 6:
    axes7[-1].set_visible(False)
fig7.suptitle('Figure 7: Quarterly Profit Trends by City', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('fig7_quarterly_trends.png', dpi=300, bbox_inches='tight')
plt.show()
print("[x] Figure 7 saved")


fig8, ax8 = plt.subplots(figsize=(12, 6))
order = df_clean.groupby('City')['Profit(£)'].median().sort_values().index
sns.boxplot(data=df_clean, x='City', y='Profit(£)', order=order,
            palette='Set2', ax=ax8, showfliers=True)
ax8.set_title('Figure 8: Profit Distribution by City', fontsize=15, fontweight='bold')
ax8.set_ylabel('Profit (£)', fontsize=13)
ax8.set_xlabel('City', fontsize=13)
plt.tight_layout()
plt.savefig('fig8_boxplot_city.png', dpi=300, bbox_inches='tight')
plt.show()
print("[x] Figure 8 saved")


fig9, ax9 = plt.subplots(figsize=(14, 6))
order_c = df_clean.groupby('Confectionary')['Profit(£)'].median().sort_values().index
sns.boxplot(data=df_clean, x='Confectionary', y='Profit(£)', order=order_c,
            palette='viridis', ax=ax9)
ax9.set_title('Figure 9: Profit Distribution by Confectionery Type',
              fontsize=15, fontweight='bold')
ax9.set_xticklabels(ax9.get_xticklabels(), rotation=30)
plt.tight_layout()
plt.savefig('fig9_boxplot_confectionery.png', dpi=300, bbox_inches='tight')
plt.show()
print("[x] Figure 9 saved")


fig10, ax10 = plt.subplots(figsize=(14, 7))
pivot_stacked = df_clean.pivot_table(
    values='Profit(£)', index='City', columns='Confectionary', aggfunc='sum'
).fillna(0)
pivot_stacked.plot(kind='bar', stacked=True, ax=ax10,
                   colormap='tab20', edgecolor='white', linewidth=0.5)
ax10.set_title('Figure 10: Profit Composition by City & Confectionery',
               fontsize=15, fontweight='bold')
ax10.set_ylabel('Total Profit (£)', fontsize=13)
ax10.legend(title='Confectionery', bbox_to_anchor=(1.05, 1), loc='upper left')
ax10.set_xticklabels(ax10.get_xticklabels(), rotation=45)
plt.tight_layout()
plt.savefig('fig10_stacked_bar.png', dpi=300, bbox_inches='tight')
plt.show()
print("[x] Figure 10 saved")


fig11, ax11 = plt.subplots(figsize=(8, 6))
numeric_cols = ['Units Sold', 'Revenue(£)', 'Cost(£)', 'Profit(£)', 'Profit_Margin(%)']
corr_matrix = df_clean[numeric_cols].corr().round(2)
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
            square=True, ax=ax11, linewidths=1)
ax11.set_title('Figure 11: Correlation Matrix', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('fig11_correlation.png', dpi=300, bbox_inches='tight')
plt.show()
print("[x] Figure 11 saved")


fig12_data = df_clean[['Units Sold', 'Revenue(£)', 'Profit(£)', 'City']].sample(300, random_state=42)
pairplot = sns.pairplot(fig12_data, hue='City', palette='Set2',
                        plot_kws={'alpha': 0.6, 's': 40})
pairplot.figure.suptitle('Figure 12: Pair Plot — Key Variables by City',
                          y=1.02, fontsize=16, fontweight='bold')
plt.savefig('fig12_pairplot.png', dpi=300, bbox_inches='tight')
plt.show()
print("[x] Figure 12 saved")


# ============================================================
# SECTION 5: INTERACTIVE VISUALISATIONS (Plotly)
# ============================================================
print("\n" + "=" * 60)
print("SECTION 5: INTERACTIVE VISUALISATIONS (Plotly)")
print("=" * 60)

# --- Figure 13: Interactive Scatter - Revenue vs Profit ---
fig13 = px.scatter(
    df_clean, x='Revenue(£)', y='Profit(£)',
    color='City', size='Units Sold',
    hover_data=['Confectionary', 'Date', 'Cost(£)'],
    title='Figure 13: Interactive — Revenue vs Profit by City',
    labels={'Revenue(£)': 'Revenue (£)', 'Profit(£)': 'Profit (£)'},
    opacity=0.7, size_max=20
)
fig13.update_layout(template='plotly_white', font=dict(size=13))
fig13.write_html('fig13_interactive_scatter.html')
fig13.show()
print("[x] Figure 13 saved as HTML")


city_bubble = df_clean.groupby('City').agg(
    Avg_Revenue=('Revenue(£)', 'mean'),
    Avg_Profit=('Profit(£)', 'mean'),
    Total_Units=('Units Sold', 'sum'),
    Avg_Margin=('Profit_Margin(%)', 'mean')
).reset_index()

fig14 = px.scatter(
    city_bubble, x='Avg_Revenue', y='Avg_Profit',
    size='Total_Units', color='City',
    hover_name='City',
    hover_data=['Avg_Margin'],
    title='Figure 14: City Performance — Avg Revenue vs Avg Profit',
    labels={'Avg_Revenue': 'Average Revenue (£)', 'Avg_Profit': 'Average Profit (£)'},
    size_max=60
)
fig14.update_layout(template='plotly_white', font=dict(size=13))
fig14.write_html('fig14_bubble_city.html')
fig14.show()
print("[x] Figure 14 saved as HTML")


fig15 = px.bar(
    df_clean.groupby(['City', 'Confectionary'])['Profit(£)'].sum().reset_index(),
    x='City', y='Profit(£)', color='Confectionary',
    barmode='group',
    title='Figure 15: Interactive — Profit by City & Confectionery',
    labels={'Profit(£)': 'Total Profit (£)'},
    hover_data=['Profit(£)']
)
fig15.update_layout(template='plotly_white', font=dict(size=13))
fig15.write_html('fig15_interactive_bar.html')
fig15.show()
print("[x] Figure 15 saved as HTML")


fig16 = px.treemap(
    df_clean.groupby(['City', 'Confectionary'])['Profit(£)'].sum().reset_index(),
    path=['City', 'Confectionary'],
    values='Profit(£)',
    color='Profit(£)',
    color_continuous_scale='RdYlGn',
    title='Figure 16: Profit Treemap — City → Confectionery'
)
fig16.update_layout(font=dict(size=13))
fig16.write_html('fig16_treemap.html')
fig16.show()
print("[x] Figure 16 saved as HTML")


fig17 = px.sunburst(
    df_clean.groupby(['City', 'Confectionary'])['Revenue(£)'].sum().reset_index(),
    path=['City', 'Confectionary'],
    values='Revenue(£)',
    color='Revenue(£)',
    color_continuous_scale='Blues',
    title='Figure 17: Revenue Sunburst — City → Confectionery'
)
fig17.write_html('fig17_sunburst.html')
fig17.show()
print("[x] Figure 17 saved as HTML")


yearly_city_plot = df_clean.groupby(['Year', 'City']).agg(
    Total_Profit=('Profit(£)', 'sum'),
    Total_Revenue=('Revenue(£)', 'sum')
).reset_index()

fig18 = px.line(
    yearly_city_plot, x='Year', y='Total_Profit',
    color='City', markers=True,
    title='Figure 18: Interactive — Yearly Profit Trends by City',
    labels={'Total_Profit': 'Total Profit (£)', 'Year': 'Year'}
)
fig18.update_layout(template='plotly_white', font=dict(size=13))
fig18.write_html('fig18_interactive_temporal.html')
fig18.show()
print("[x] Figure 18 saved as HTML")


fig19 = px.box(
    df_clean, x='City', y='Profit(£)',
    color='Confectionary',
    title='Figure 19: Interactive — Profit Distribution by City & Confectionery',
    labels={'Profit(£)': 'Profit (£)'}
)
fig19.update_layout(template='plotly_white', font=dict(size=13))
fig19.write_html('fig19_interactive_box.html')
fig19.show()
print("[x] Figure 19 saved as HTML")


# ============================================================
# SECTION 6: COMPREHENSIVE INTERACTIVE DASHBOARD
# ============================================================
print("\n" + "=" * 60)
print("SECTION 6: INTERACTIVE DASHBOARD")
print("=" * 60)

pivot_margin_dash = df_clean.pivot_table(
    values='Profit_Margin(%)', index='City', columns='Confectionary', aggfunc='mean'
).fillna(0).round(1)

fig_dash = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        'Total Profit by City',
        'Profit by Confectionery Type',
        'Yearly Revenue Trends',
        'Profit Margin by City & Product',
        'Units Sold Distribution',
        'Cost vs Revenue Efficiency'
    ),
    specs=[
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "scatter"}, {"type": "heatmap"}],
        [{"type": "box"}, {"type": "scatter"}]
    ],
    vertical_spacing=0.12,
    horizontal_spacing=0.1
)

city_p = df_clean.groupby('City')['Profit(£)'].sum().sort_values(ascending=False)
fig_dash.add_trace(
    go.Bar(x=city_p.index, y=city_p.values, name='City Profit',
           marker_color=['#2196F3', '#4CAF50', '#FF9800', '#F44336', '#9C27B0']),
    row=1, col=1
)

conf_p = df_clean.groupby('Confectionary')['Profit(£)'].sum().sort_values(ascending=False)
fig_dash.add_trace(
    go.Bar(x=conf_p.index, y=conf_p.values, name='Confectionery Profit',
           marker_color='#00BCD4'),
    row=1, col=2
)

for city in df_clean['City'].unique():
    cd = yearly_city_plot[yearly_city_plot['City'] == city]
    fig_dash.add_trace(
        go.Scatter(x=cd['Year'], y=cd['Total_Revenue'], mode='lines+markers',
                   name=city, legendgroup=city),
        row=2, col=1
    )

fig_dash.add_trace(
    go.Heatmap(
        z=pivot_margin_dash.values,
        x=pivot_margin_dash.columns.tolist(),
        y=pivot_margin_dash.index.tolist(),
        colorscale='RdYlGn',
        text=pivot_margin_dash.values.round(1),
        texttemplate='%{text}%',
        name='Margin %'
    ),
    row=2, col=2
)

for city in df_clean['City'].unique():
    fig_dash.add_trace(
        go.Box(y=df_clean[df_clean['City'] == city]['Units Sold'],
               name=city, legendgroup=city, showlegend=False),
        row=3, col=1
    )

fig_dash.add_trace(
    go.Scatter(
        x=df_clean['Cost(£)'], y=df_clean['Revenue(£)'],
        mode='markers', name='Cost vs Revenue',
        marker=dict(
            size=5, opacity=0.5,
            color=df_clean['Profit(£)'],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title='Profit £', x=1.02)
        ),
        text=df_clean['City']
    ),
    row=3, col=2
)

fig_dash.update_layout(
    height=1200, width=1400,
    title_text='<b>European Bakery Sales — Interactive Dashboard</b>',
    title_font_size=20,
    template='plotly_white',
    showlegend=True
)
fig_dash.write_html('dashboard_comprehensive.html')
fig_dash.show()
print("[x] Comprehensive Dashboard saved as 'dashboard_comprehensive.html'")


# ============================================================
# SECTION 7: KEY FINDINGS & RECOMMENDATIONS
# ============================================================
print("\n" + "=" * 60)
print("SECTION 7: KEY FINDINGS & RECOMMENDATIONS")
print("=" * 60)

print("\n--- TOP 3 Most Profitable City-Confectionery Combinations ---")
combo_profit = df_clean.groupby(['City', 'Confectionary']).agg(
    Total_Profit=('Profit(£)', 'sum'),
    Avg_Margin=('Profit_Margin(%)', 'mean'),
    Total_Units=('Units Sold', 'sum')
).round(2).sort_values('Total_Profit', ascending=False)
print(combo_profit.head(3))

print("\n--- BOTTOM 3 Least Profitable City-Confectionery Combinations ---")
print(combo_profit.tail(3))

print("\n--- Profit Margin Ranking by Confectionery ---")
margin_rank = df_clean.groupby('Confectionary')['Profit_Margin(%)'].mean().sort_values(ascending=False).round(2)
print(margin_rank)

print("\n--- Profit Margin Ranking by City ---")
city_margin = df_clean.groupby('City')['Profit_Margin(%)'].mean().sort_values(ascending=False).round(2)
print(city_margin)

print("\n--- Year-on-Year Profit Growth by City ---")
yearly_pivot = df_clean.pivot_table(values='Profit(£)', index='Year', columns='City', aggfunc='sum')
yoy_growth = yearly_pivot.pct_change() * 100
print(yoy_growth.round(1))

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE — All figures saved")
print("=" * 60)
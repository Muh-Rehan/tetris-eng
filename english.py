import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#import dataframe
rumah_5kota = pd.read_csv('rumah_5kota-eng.csv')
ihpr = pd.read_csv('ihpr-eng.csv', delimiter=';')
inflasi = pd.read_csv('inflasi-eng.csv', delimiter=';')
upah_bulanan = pd.read_csv('upah_bulanan_indo-eng.csv', delimiter=';', index_col='year')
ump_jkt = pd.read_csv('ump_jakarta-eng.csv', delimiter=';')
kpr_bi7drr = pd.read_csv('kpr_bi7drr-eng.csv', delimiter=';')
alasan = pd.read_csv('alasan_blm_punya_rumah-eng.csv', delimiter=';')

st.title('The Indonesian Youths Are Finding It More Difficult to Possess Their Own Houses')
st.markdown('*by Muhammad Raihan (100), made for Capstone Project of TETRIS II DQLab*')

#Opening
st.caption(
    '''
    (There are) 12.75 million backlogs, or in other words, families who don't possess their own houses. In Indonesia many people are still young demographically speaking, meaning these youths who would get married then require a home but could not afford to purchase one. Their purchasing power are lower than the cost of owning a house, therefore they would resort to live with their parents or to rent one.
    '''
)

'''
The statement was stated by Indonesian Minister of Finance Sri Mulyani on [Road to G20 Seminar - Securitization Summit 2022](https://www.youtube.com/watch?v=u7kHXmbaBr4&t=2483s) on Wednesday, July 6 2022. A survey by rumah.com confirmed that there are 1 out of 3 millenials still living with their parents.
'''

tinggal_dgn_ortu = pd.DataFrame({
'Live with Parents': ('Yes', 'No'),
'Percentage': (34, 66)
})
ortu_chart = px.pie(tinggal_dgn_ortu, values='Percentage', names='Live with Parents',
                    title='Indonesian Millenials Living with Their Parents', hole=0.5)

ortu_chart.update_layout(title_font_size=30)
ortu_chart.update_traces(textfont_size=17, textfont_color='white', textinfo='percent+label')

ortu_chart

'''
source: [Rumah.com Consumer Sentiment Study Semester II 2020 (n=675)](https://www.rumah.com/panduan-properti/milenial-belum-tertarik-beli-rumah-di-usia-muda-31226)
'''

'''
Emphasize on the fact that by answering not living with parents could still mean renting the house, which therefore indicates that the percentage of millenials still have not possessed their own house could be even higher. Why do many married youths still not living in their own dwellings? In this article we will discuss from the persepctive of house prices and youth financial situation.
'''

#House Price
st.header('How High is The Housing Price?')

'''
The increase in house prices could be the result of multiple factors. In the same seminar, Sri Mulyani stated those factors include land cost, material cost, and supply and demand equilibrium. There are also the current pandemic and international geopolitical instability further destabilizing housing prices. In this part we will examine how much the current house price is and their trend from a couple of years prior.
'''

median_harga_5kota = rumah_5kota.groupby(['City', 'Category'])[['Price']].median().reset_index()

grafik_placeholder1 = st.empty()

tipe_kategori = 'Small'
kecil1, sedang1, besar1 = st.columns(3)
with kecil1:
    if st.button('Small (≤ 90m²)'):
        tipe_kategori = 'Small'
with sedang1:
    if st.button('Medium (91-150m²)'):
        tipe_kategori = 'Medium'
with besar1:
    if st.button('Large (≥ 151m²)'):
        tipe_kategori = 'Large'

grafik_rmh_5kt = px.bar(median_harga_5kota.query(f'Category == "{tipe_kategori}"'), x='Price', y='City',
                title=f'Secondary House Price Median in 5 Indonesian Cities 2022 - {tipe_kategori} Type')
grafik_rmh_5kt.update_yaxes(categoryorder='total ascending')
grafik_rmh_5kt.update_layout(title_font_size=20)

grafik_placeholder1.plotly_chart(grafik_rmh_5kt)
'''
source: [Lamudi](https://www.lamudi.co.id/)
'''

'''
Secondary house prices range from 500 million up to 7.5 billion rupiahs based on their size and location. Jakarta has the highest secondary housing price median. The data shown are secondary house due to the difficulty of finding primary housing price, but from this we could infer the primary ones should be even higher, might even reach beyond 1 billion rupiahs for small type in Jakarta.
'''

grafik_placeholder2 = st.empty()

wilayah = st.selectbox('Location', ('18 Cities', 'Jabodebek-Banten', 
                                    'Bandung', 'Surabaya', 'Medan', 'Makassar'))

tren_harga_rumah = make_subplots(specs=[[{'secondary_y': True}]])

tren_harga_rumah.add_trace(
    go.Bar(x=ihpr.query(f'location == "{wilayah}"')['year'], 
            y=ihpr.query(f'location == "{wilayah}"')['ihpr'],
            name='IHPR (2012 = 100)'),
    secondary_y=False
)
tren_harga_rumah.add_trace(
    go.Scatter(x=ihpr.query(f'location == "{wilayah}"')['year'], 
                y=ihpr.query(f'location == "{wilayah}"')['delta_ihpr'],
                name='Housing Price Index Growth'),
    secondary_y=True
)
tren_harga_rumah.add_trace(
    go.Scatter(x=inflasi['year'], 
                y=inflasi['inflation'],
                name='National Inflation',
                line=dict(color='orange')),
    secondary_y=True
)    
tren_harga_rumah.update_layout(
    title_text='Residential Property Price Index (IHPR) & Inflation', 
    title_font_size=30
)
tren_harga_rumah.update_yaxes(title_text='IHPR', showgrid=False, secondary_y=False)
tren_harga_rumah.update_yaxes(
    title_text='IHPR & Inflation Increase (%)', 
    showgrid=False, secondary_y=True
)

grafik_placeholder2.plotly_chart(tren_harga_rumah)
'''
source: [Bank](https://www.bi.go.id/id/publikasi/laporan/Pages/SHPR-Triwulan-I-2022.aspx) 
[Indonesia](https://www.bi.go.id/id/statistik/indikator/data-inflasi.aspx)
'''

'''
Every year, the housing price would always increase year by year, usually following the inflation trend. As inflation slowed down especially during pandemic, the increase of housing price would also slow down. However, the current economic instability made inflation in 2022 (Q2-yoy) suddenly went as high as 4.35%, but the housing price still only increased at below 2%. Currently the component of inflation surge comes from food and basic essentials, and in the future it is possible that housing prices would hike as other costs increase as well.
'''

kpr_grafik = go.Figure()
kpr_grafik.add_trace(
    go.Scatter(x=kpr_bi7drr['quarter'], y=kpr_bi7drr['interest_median'], name='Housing Interest')
)
kpr_grafik.add_trace(
    go.Bar(x=kpr_bi7drr['quarter'], y=kpr_bi7drr['bi7drr'], name='BI7DRR')
)
kpr_grafik.update_layout(title_text='Housing Interest & BI7DRR Median', title_font_size=25)
kpr_grafik.update_yaxes(title_text='%')

kpr_grafik
'''
source: [Otoritas Jasa Keuangan](https://www.ojk.go.id/id/kanal/perbankan/Pages/Suku-Bunga-dasar.aspx) and [Bank Indonesia](https://www.bi.go.id/id/statistik/indikator/bi-7day-rr.aspx)
'''

'''
The decreasing trend of BI7DRR is due to the initiative of central bank to push the recovery momentum of national economic in the midst of low inflation rate. With the sudden surge of inflation as previously shown, however, it is likely in the near future the interest rate would return to above 8%.
'''

#Finansial Muda
st.header('How About the Youth Financial Situation')

'''
Then how about the youth financial situation, could they afford to own the increasingly rising housing price?
'''

grafik_upah = px.imshow(upah_bulanan.T.iloc[::-1], text_auto=True)
grafik_upah.update_layout(title_text='Average Monthly Wage Based on Age 2016-2022', title_font_size=30)
grafik_upah.update_xaxes(title_text='Year')
grafik_upah.update_yaxes(title_text='Age')

grafik_upah

'''
source: [Badan Pusat Statistik](https://www.bps.go.id/subject/19/upah-buruh.html#subjekViewTab3)
'''

'''
As a fresh workforce with minimal experience, it is difficult for the young generation to obtain high position and thus have to deal with lower pay compared to the more mature workforce. The current pandemic further reduces the salary in the midst of uncertainty.
'''

grafik_ump = make_subplots(specs=[[{'secondary_y': True}]])
grafik_ump.add_trace(
    go.Bar(x=ump_jkt['year'], y=ump_jkt['ump_jakarta'], name='Jakarta Minimum Wage',
            hovertemplate='UMP: Rp%{y:,}'),
    secondary_y=False
)
grafik_ump.add_trace(
    go.Scatter(x=ump_jkt['year'], y=ump_jkt['percentage'], 
                name='Jakarta Minimum Wage Growth', line=dict(color='lime')),
    secondary_y=True
)
grafik_ump.add_trace(
    go.Scatter(x=ihpr.query('location == "Jabodebek-Banten" & year >= 2013')['year'],
                y=ihpr.query('location == "Jabodebek-Banten" & year >= 2013')['delta_ihpr'],
                name='Jakarta Housing Price Index Growth', line=dict(color='red')),
    secondary_y=True
)
grafik_ump.update_layout(title_text='Jakarta Minimum Wage & Housing Price', title_font_size=30)
grafik_ump.update_yaxes(title_text='Jakarta Minimum Monthly Wage', showgrid=False, secondary_y=False)
grafik_ump.update_yaxes(title_text='Growth (%)', showgrid=False, secondary_y=True)

grafik_ump

'''
source: [Badan Pusat Statistik](https://jakarta.bps.go.id/statictable/2015/04/20/83/upah-minimum-provinsi-dan-inflasi-di-dki-jakarta-1999-2020.html) 
and [Bank Indonesia](https://www.bi.go.id/id/statistik/indikator/data-inflasi.aspx)
'''

'''
Assuming a millenial living in Jakarta gets a minimum wage. Prior to year 2021, the minimum wage growth always had surplus of 6% from the housing price growth. From year 2021, however, both had similar growth. Even though the consistent surplus throughout the year make the minimum-wage/housing-price ratio better year by year, the ever increasingly prices of various necessities would use up all the wage increase. This in turn would leave smaller proportion for house repayments. The 2022 inflation surge further makes it more difficult for this generation which just started to earn a living to get a home. Even worse if the person suffered from the sandwich generation.

Now imagine this millenial is seeking a small secondary house in Jakarta for the median price, which would be Rp770 million. He bought the house with down payment of 20%, 9% interest rate (assuming fixed from start) for 30 years. The mortgage financing scheme uses the annuity method (fixed monthly installments until the end of the period).
'''

harga_rumah = st.number_input('House Price', value=770_000_000, step=10_000_000)
st.write('Rp{:,}'.format(harga_rumah).replace(',','.'))

col_dp, col_kpr, col_tenor = st.columns(3)
with col_dp:
    dp = st.slider(r'Down Payment (%)', min_value=0, max_value=50, value=20, step=5)
with col_kpr:
    kpr = st.slider(r'Interest', min_value=6.00, max_value=12.00, value=9.00, step=0.05)
with col_tenor:
    tenor = st.slider('Tenure', min_value=1, max_value=50, value=30, step=1)

biaya_dp = int(harga_rumah*(dp/100))
pinjaman = int(harga_rumah-biaya_dp)
bunga_bulan = kpr/100/12
tenor_bulan = tenor*12
angsuran_bulanan = ((pinjaman * bunga_bulan) / (1-(1+bunga_bulan)**(-tenor_bulan))).__ceil__()
total_angsuran = angsuran_bulanan * tenor * 12

st.write(
    '''
    Down Payment Total: Rp{:,}\n
    Total Loan (house price - down payment): Rp{:,}\n
    ---
    Monthly Installment: Rp{:,}\n
    Total Installment: Rp{:,}
    '''\
    .format(biaya_dp, pinjaman, angsuran_bulanan, total_angsuran)\
    .replace(',','.')
)

'''
The down payment which must be repaid is equal to the full-current 3 years of salary with monthly installments even as much as 106% of current monthly salary. Despite the salary would increase each year with fixed installments for the next 30 years, the numbers shown are still relatively high for those who could not hope to have income above the minimum, even worse if they work in SME company or business which are allowed to pay below the minimum wage.

The youths must find an extremely cheap house if still persist to still have their own house, or alternatively they could rent one or even resort to stay with their parents as the more realistic options. With inflation risk in this uncertain era, it is clear as to why the young generation still find it difficult to get their own house. Survey below confirmed such statement with 63.12% respondents stated the reason they do not possess their own house yet is due to financial reasons.
'''

grafik_alasan = px.bar(alasan, x='Percentage', y='Reasons', orientation='h',
                        title='Reasons Why Millenials Do Not Have Their Own House')
grafik_alasan.update_layout(title_font_size=25)
grafik_alasan.update_yaxes(categoryorder='total ascending')

grafik_alasan
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from plotly import graph_objects as go
import pickle

st.set_page_config(
    page_title="NUTRIENDS-NUTRICO",
    page_icon="https://i.ibb.co/2gq4v6k/nutriends-header.pnghttps://i.ibb.co/7zmz1WM/Nutriends-icon.png"
)

def set_bg_hack_url():   
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(https://i.pinimg.com/originals/84/2a/d6/842ad68b315b0f586c30b465221da609.jpg), url(https://i.ibb.co/k3rnPnP/back-final.jpg);
             background-repeat: no-repeat;
             background-size: 800px 800px, cover;
             background-position: center;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg_hack_url()

# st.markdown("<h1 style='text-align: center; color: black;'> NUTRIENDS </h1>", unsafe_allow_html=True)
# st.markdown("<h3 style='text-align: center; color: black;'> Your Nutritional Friends </h3>", unsafe_allow_html=True)
st.image('https://i.ibb.co/z4WxYRg/Nutriends-header4.png')

gender = st.selectbox(
     'Jenis Kelamin Anda',
     ('Laki-Laki', 'Perempuan'))

age = st.slider('Umur Anda', 0, 130, 25)
height = st.number_input('Tinggi Badan Anda (Cm)')
weight = st.number_input('Berat Badan Anda (Kg)')
activity = st.selectbox(
     'Dalam Keseharian Seberapa Aktif Anda?',
     ('Sangat Rendah (Jarang Olahraga/bekerja)', 'Rendah (Olahraga/bekerja 1-3 hari per minggu)',
      'Menengah (Olahraga/bekerja 3-5 hari per minggu)', 'Tinggi (Olahraga/bekerja 6-7 hari per minggu)', 
      'Sangat Tinggi (Olahraga/bekerja berat 6-7 hari per minggu)'))

if activity=='Sangat Rendah (Jarang Olahraga/bekerja)':
    activity='Sangat Rendah'
elif activity=='Rendah (Olahraga/bekerja 1-3 hari per minggu)':
    activity='Rendah'
elif activity=='Menengah (Olahraga/bekerja 3-5 hari per minggu)':
    activity='Menengah'
elif activity=='Tinggi (Olahraga/bekerja 6-7 hari per minggu)':
    activity='Tinggi'
elif activity=='Sangat Tinggi (Olahraga/bekerja berat 6-7 hari per minggu)':
    activity='Sangat Tinggi'

inputs = [age, gender, height, weight, activity]

def bmr_male():
    bmr = 660 + (13.7*inputs[3]) + (1.5*inputs[2]) - (6.8*inputs[0])
    return round(bmr,2)

def bmr_female():
    bmr = 665 + (9.6*inputs[3]) + (1.7*inputs[2]) - (4.7*inputs[0])
    return round(bmr,2)

def amr_index():
    if activity=='Sangat Rendah':
        amr = bmr*1.2
    elif activity=='Rendah':
        amr = bmr*1.375
    elif activity=='Menengah':
        amr = bmr*1.55
    elif activity=='Tinggi':
        amr = bmr*1.725
    elif activity=='Sangat Tinggi':
        amr = bmr*1.9
    return round(amr,2)

def activity_cal():
    if inputs[4]=='Sangat Rendah':
        inputs[4]=1
    elif inputs[4]=='Rendah':
        inputs[4]=1
    elif inputs[4]=='Menengah':
        inputs[4]=0
    else:
        inputs[4]=2
    
    if inputs[1]=='Laki-Laki':
        inputs[1]='male'
    else:
        inputs[1]='female'
    
    model = pickle.load(open('model_calorie.pkl', 'rb'))
    df_user = pd.DataFrame({'gender': [inputs[1]],'Activity_Intensity': [inputs[4]], 
                            'age': [inputs[0]], 'height': [inputs[2]], 'weight': [inputs[3]]})
    y_pred = model.predict(df_user)
    return round(y_pred[0],2)

def bmi_index():
    bmi = inputs[3]/(inputs[2]/100)**2
    return bmi

rec = {'rec_1': ['Anda memiliki BMI di bawah standard sehingga anda digolongkan kekurangan berat badan, kami merekomendasikan anda untuk menambahkan berat badan anda sehingga anda memiliki BMI yang normal',
                 'berdasarkan plan yang anda buat maka berikut mungkin makanan yang sesuai untuk kondisi anda'],
       'rec_2': ['Anda memiliki BMI di bawah standard sehingga anda digolongkan kekurangan berat badan, kami merekomendasikan anda untuk menambahkan berat badan anda sehingga anda memiliki BMI yang normal',
                 'berdasarkan plan yang anda buat maka berikut mungkin makanan yang sesuai untuk kondisi anda'],
       'rec_3': ['Anda memiliki BMI di bawah standard sehingga anda digolongkan kekurangan berat badan, kami merekomendasikan anda untuk menambahkan berat badan anda sehingga anda memiliki BMI yang normal',
                 'berdasarkan plan yang anda buat maka berikut mungkin makanan yang sesuai untuk kondisi anda'],
       'rec_4': ['Anda memiliki BMI di bawah standard sehingga anda digolongkan kekurangan berat badan, kami merekomendasikan anda untuk menambahkan berat badan anda sehingga anda memiliki BMI yang normal', 
                 'anda terindikasi kekurangan berat badan namun aktivitas anda sangat tinggi, berdasarkan plan yang anda buat maka berikut mungkin makanan yang sesuai untuk kondisi anda'],
       'rec_5': ['Anda memiliki BMI di bawah standard sehingga anda digolongkan kekurangan berat badan, kami merekomendasikan anda untuk menambahkan berat badan anda sehingga anda memiliki BMI yang normal',
                 'anda terindikasi kekurangan berat badan namun aktivitas anda sangat tinggi, berdasarkan plan yang anda buat maka berikut mungkin makanan yang sesuai untuk kondisi anda'],
       'rec_6': ['Selamat BMI anda di rentang batas aman, itu artinya kondisi tubuh anda dalam keadaan ideal. kami merekomendasikan anda untuk tetap menjaga kondisi tersebut',
                 'untuk menjaga tubuh anda, mungkin beberapa makanan dibawah cocok untuk anda'],
       'rec_7': ['Selamat BMI anda di rentang batas aman, itu artinya kondisi tubuh anda dalam keadaan ideal. kami merekomendasikan anda untuk tetap menjaga kondisi tersebut',
                 'untuk menjaga tubuh anda, mungkin beberapa makanan dibawah cocok untuk anda'],
       'rec_8': ['Selamat BMI anda di rentang batas aman, itu artinya kondisi tubuh anda dalam keadaan ideal. kami merekomendasikan anda untuk tetap menjaga kondisi tersebut',
                 'untuk menjaga tubuh anda, mungkin beberapa makanan dibawah cocok untuk anda'],
       'rec_9': ['Selamat BMI anda di rentang batas aman, itu artinya kondisi tubuh anda dalam keadaan ideal. kami merekomendasikan anda untuk tetap menjaga kondisi tersebut',
                'untuk menjaga tubuh anda, mungkin beberapa makanan dibawah cocok untuk anda'],
       'rec_10': ['Selamat BMI anda di rentang batas aman, itu artinya kondisi tubuh anda dalam keadaan ideal. kami merekomendasikan anda untuk tetap menjaga kondisi tersebut',
                  'untuk menjaga tubuh anda, mungkin beberapa makanan dibawah cocok untuk anda'],
       'rec_11': ['Anda memiliki BMI di atas batas ideal sehingga anda digolongkan kelebihan berat badan, kami merekomendasikan anda untuk menurunkan berat badan anda sehingga anda memiliki BMI yang normal',
                 'berdasarkan plan yang anda buat maka berikut mungkin makanan yang sesuai untuk kondisi anda'],
       'rec_12': ['Anda memiliki BMI di atas batas ideal sehingga anda digolongkan kelebihan berat badan, kami merekomendasikan anda untuk menurunkan berat badan anda sehingga anda memiliki BMI yang normal',
                 'berdasarkan plan yang anda buat maka berikut mungkin makanan yang sesuai untuk kondisi anda'],
       'rec_13': ['Anda memiliki BMI di atas batas ideal sehingga anda digolongkan kelebihan berat badan, kami merekomendasikan anda untuk menurunkan berat badan anda sehingga anda memiliki BMI yang normal',
                 'berdasarkan plan yang anda buat maka berikut mungkin makanan yang sesuai untuk kondisi anda'],
       'rec_14': ['Anda memiliki BMI di atas batas ideal sehingga anda digolongkan kelebihan berat badan, kami merekomendasikan anda untuk menurunkan berat badan anda sehingga anda memiliki BMI yang normal',
                 'anda memiliki badan yang berlebih hanya saja aktivitas anda sudah tergolong tinggi, berdasarkan plan yang anda buat maka berikut mungkin makanan yang sesuai untuk kondisi anda'],
       'rec_15': ['Anda memiliki BMI di atas batas ideal sehingga anda digolongkan kelebihan berat badan, kami merekomendasikan anda untuk menurunkan berat badan anda sehingga anda memiliki BMI yang normal',
                 'anda memiliki badan yang berlebih hanya saja aktivitas anda sudah tergolong tinggi, berdasarkan plan yang anda buat maka berikut mungkin makanan yang sesuai untuk kondisi anda']}


nutrients=pd.read_csv('Nutrition_Fact2.csv', delimiter=';')

def plot_funnel(cat, amr_per, nut, ascen, tex):
    food = nutrients[nutrients['category']==cat]
    food = food[food[nut]<=amr_per]
    food_top=food.sort_values(by=nut, ascending= ascen)
    food_top=food_top.head(5)
    fig = go.Figure(go.Funnelarea(
        text = food_top['Food_Name'], title = { "text": tex},
        values = food_top[nut], textinfo = "value+text", showlegend=False
        ))
    fig.update_layout(autosize=False, margin={'l':20, 'r':20, 't':20, 'b':20})
    return fig

def plot_funnel2(cat, amr_per, nut, ascen, tex):
    food = nutrients[nutrients['category']==cat]
    food = food[food[nut]>=amr_per]
    food_top=food.sort_values(by=nut, ascending= ascen)
    food_top=food_top.head(5)
    fig = go.Figure(go.Funnelarea(
        text = food_top['Food_Name'], title = { "text": tex},
        values = food_top[nut], textinfo = "value+text", showlegend=False
        ))
    fig.update_layout(autosize=False, margin={'l':20, 'r':20, 't':20, 'b':20})
    return fig

def food_rec(cat, amr_per, nut, ascen):
    food = nutrients[nutrients['category']==cat]
    food = food[food[nut]<=amr_per]
    food_top=food.sort_values(by=nut, ascending= ascen)

    return food_top.head(5)

bmr_amr_info=['Basal metabolic rate (BMR) adalah kalori yang tubuh Anda perlukan untuk melakukan aktivitas dasar tubuh. Aktivitas \
             tersebut mencakup memompa jantung, mencerna makanan, bernapas, memperbaiki sel tubuh, hingga membuang racun dalam tubuh.',
             'Active metabolic rate (AMR) adalah kalori yang tubuh Anda perlukan untuk melakukan aktivitas dasar tubuh ditambah aktivitas \
                 dari luar seperti bekerja, bersepeda, jalan dan lain-lain.']

with st.expander("Dapatkan Informasi"):
    if inputs[0]==0:
        st.warning('Data yang anda input tidak valid')
    elif inputs[2]==0:
        st.warning('Data yang anda input tidak valid')
    elif inputs[3]==0:
        st.warning('Data yang anda input tidak valid')
    else:
        if inputs[1] == 'Laki-Laki':
            bmr = bmr_male()
            bmi = bmi_index()
            print('laki-laki')
            print(f'bmr : {bmr}')

            if bmi<18.5:
                status = ['Kekurangan Berat Badan']
            elif 18.5<bmi<24.9:
                status = ['Berat Badan Ideal']
            elif bmi>25:
                status = ['Berat Badan Berlebih']

        else:
            bmr = bmr_female()
            bmi = bmi_index()
            print('perempuan')
            print(f'bmr : {bmr}')

            if bmi<18.5:
                status = ['Kekurangan Berat Badan']
            elif 18.5<bmi<24.9:
                status = ['Berat Badan Ideal']
            elif bmi>25:
                status = ['Berat Badan Berlebih']
        user_bmi = bmi
        user_bmr = bmr
        user_amr = amr_index()
        if status==['Kekurangan Berat Badan']:
            st.error('Status anda saat ini : {}'.format(status[0]))
            if activity=='Sangat Rendah':
                st.subheader(f'BMR Anda : {user_bmr}')
                st.markdown(bmr_amr_info[0])
                st.subheader(f'AMR Anda : {user_amr}')
                st.markdown(bmr_amr_info[1])
                st.info(rec['rec_1'][0])
                ideal_weight = (inputs[2]/100)**2*18.5
                st.subheader(f'Berat Badan Ideal Anda : {round(ideal_weight,2)} kg')
                make_plan = st.number_input('Dalam Seminggu anda ingin naik berat badan berapa kg?')
                plan = make_plan*7716.18/7
                amr_plan = plan+user_amr
                amr_perdish_main = amr_plan / 3 - (amr_plan / 3)*0.2
                amr_perdish_side = ((amr_plan) / 3)*0.1
                amr_perdish_desert = ((amr_plan) / 3)*0.1
                st.info('Untuk menaikan berat anda sebesar {} kg dalam seminggu, maka anda harus surplus kalori sebesar {} cal per hari, \
                        sehingga target kalori total harian anda adalah {} cal. Untuk membuat diet anda lebih berhasil, makanan utama \
                        anda seminimal mungkin harus mengandung {} cal dengan makanan selingan mengandung {} cal per \
                        harinya'.format(make_plan, round(plan,2), round(amr_plan,2), round(amr_perdish_main,2), round((amr_plan / 3)*0.2, 2)))
                st.caption(rec['rec_1'][1])
                fig = plot_funnel2('Main Course', amr_perdish_main, 'Calories', True, 'Main Course')
                st.plotly_chart(fig)
                fig = plot_funnel2('Dessert',amr_perdish_desert, 'Calories', True, 'Dessert')
                st.plotly_chart(fig)
                fig = plot_funnel2('Side Dish',amr_perdish_side, 'Calories', True, 'Side Dish')
                st.plotly_chart(fig)
            elif activity=='Rendah':
                st.subheader(f'BMR Anda : {user_bmr}')
                st.markdown(bmr_amr_info[0])
                st.subheader(f'AMR Anda : {user_amr}')
                st.markdown(bmr_amr_info[1])
                st.info(rec['rec_2'][0])
                make_plan = st.number_input('Dalam Seminggu anda ingin naik berat badan berapa kg?')
                plan = make_plan*7716.18/7
                amr_plan = plan+user_amr
                amr_perdish_main = amr_plan / 3 - (amr_plan / 3)*0.2
                amr_perdish_side = ((amr_plan) / 3)*0.1
                amr_perdish_desert = ((amr_plan) / 3)*0.1
                st.info('Untuk menaikan berat anda sebesar {} kg dalam seminggu, maka anda harus surplus kalori sebesar {} cal per hari, \
                        sehingga target kalori total harian anda adalah {} cal. Untuk membuat diet anda lebih berhasil, makanan utama \
                        anda seminimal mungkin harus mengandung {} cal dengan makanan selingan mengandung {} cal per \
                        harinya'.format(make_plan, round(plan,2), round(amr_plan,2), round(amr_perdish_main,2), round((amr_plan / 3)*0.2, 2)))
                st.caption(rec['rec_2'][1])        
                fig = plot_funnel2('Main Course', amr_perdish_main, 'Calories', True, 'Main Course (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel2('Dessert',amr_perdish_desert, 'Calories', True, 'Dessert (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel2('Side Dish',amr_perdish_side, 'Calories', True, 'Side Dish (cal)')
                st.plotly_chart(fig)
            elif activity=='Menengah':
                st.subheader(f'BMR Anda : {user_bmr}')
                st.markdown(bmr_amr_info[0])
                st.subheader(f'AMR Anda : {user_amr}')
                st.markdown(bmr_amr_info[1])
                st.info(rec['rec_3'][0])
                make_plan = st.number_input('Dalam Seminggu anda ingin naik berat badan berapa kg?')
                plan = make_plan*7716.18/7
                amr_plan = plan+user_amr
                amr_perdish_main = amr_plan / 3 - (amr_plan / 3)*0.2
                amr_perdish_side = ((amr_plan) / 3)*0.1
                amr_perdish_desert = ((amr_plan) / 3)*0.1
                st.info('Untuk menaikan berat anda sebesar {} kg dalam seminggu, maka anda harus surplus kalori sebesar {} cal per hari, \
                        sehingga target kalori total harian anda adalah {} cal. Untuk membuat diet anda lebih berhasil, makanan utama \
                        anda seminimal mungkin harus mengandung {} cal dengan makanan selingan mengandung {} cal per \
                        harinya'.format(make_plan, round(plan,2), round(amr_plan,2), round(amr_perdish_main,2), round((amr_plan / 3)*0.2, 2)))
                st.caption(rec['rec_3'][1])        
                fig = plot_funnel2('Main Course', amr_perdish_main, 'Calories', True, 'Main Course (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel2('Dessert',amr_perdish_desert, 'Calories', True, 'Dessert (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel2('Side Dish',amr_perdish_side, 'Calories', True, 'Side Dish (cal)')
                st.plotly_chart(fig)
            elif activity=='Tinggi':
                st.subheader(f'BMR Anda : {user_bmr}')
                st.markdown(bmr_amr_info[0])
                st.subheader(f'AMR Anda : {user_amr}')
                st.markdown(bmr_amr_info[1])
                st.info(rec['rec_4'][0])
                make_plan = st.number_input('Dalam Seminggu anda ingin naik berat badan berapa kg?')
                plan = make_plan*7716.18/7
                amr_plan = plan+user_amr
                amr_perdish_main = amr_plan / 3 - (amr_plan / 3)*0.2
                amr_perdish_side = ((amr_plan) / 3)*0.1
                amr_perdish_desert = ((amr_plan) / 3)*0.1
                st.info('Untuk menaikan berat anda sebesar {} kg dalam seminggu, maka anda harus surplus kalori sebesar {} cal per hari, \
                        sehingga target kalori total harian anda adalah {} cal. Untuk membuat diet anda lebih berhasil, makanan utama \
                        anda seminimal mungkin harus mengandung {} cal dengan makanan selingan mengandung {} cal per \
                        harinya'.format(make_plan, round(plan,2), round(amr_plan,2), round(amr_perdish_main,2), round((amr_plan / 3)*0.2, 2)))
                st.caption(rec['rec_4'][1])        
                fig = plot_funnel2('Main Course', amr_perdish_main, 'Calories', True, 'Main Course (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel2('Dessert',amr_perdish_desert, 'Calories', True, 'Dessert (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel2('Side Dish',amr_perdish_side, 'Calories', True, 'Side Dish (cal)')
                st.plotly_chart(fig)
            elif activity=='Sangat Tinggi':
                st.subheader(f'BMR Anda : {user_bmr}')
                st.markdown(bmr_amr_info[0])
                st.subheader(f'AMR Anda : {user_amr}')
                st.markdown(bmr_amr_info[1])
                st.info(rec['rec_5'][0])
                make_plan = st.number_input('Dalam Seminggu anda ingin naik berat badan berapa kg?')
                plan = make_plan*7716.18/7
                amr_plan = plan+user_amr
                amr_perdish_main = amr_plan / 3 - (amr_plan / 3)*0.2
                amr_perdish_side = ((amr_plan) / 3)*0.1
                amr_perdish_desert = ((amr_plan) / 3)*0.1
                st.info('Untuk menaikan berat anda sebesar {} kg dalam seminggu, maka anda harus surplus kalori sebesar {} cal per hari, \
                        sehingga target kalori total harian anda adalah {} cal. Untuk membuat diet anda lebih berhasil, makanan utama \
                        anda seminimal mungkin harus mengandung {} cal dengan makanan selingan mengandung {} cal per \
                        harinya'.format(make_plan, round(plan,2), round(amr_plan,2), round(amr_perdish_main,2), round((amr_plan / 3)*0.2, 2)))
                st.caption(rec['rec_5'][1])        
                fig = plot_funnel2('Main Course', amr_perdish_main, 'Calories', True, 'Main Course (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel2('Dessert',amr_perdish_desert, 'Calories', True, 'Dessert (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel2('Side Dish',amr_perdish_side, 'Calories', True, 'Side Dish (cal)')
                st.plotly_chart(fig)
        elif status==['Berat Badan Ideal']:
            st.success('Status anda saat ini : {}'.format(status[0]))
            if activity=='Sangat Rendah':
                st.subheader(f'BMR Anda : {user_bmr}')
                st.markdown(bmr_amr_info[0])
                st.subheader(f'AMR Anda : {user_amr}')
                st.markdown(bmr_amr_info[1])
                st.info(rec['rec_6'][0])
                st.caption(rec['rec_6'][1])
                amr_perdish_main = user_amr / 3 - (user_amr / 3)*0.2
                amr_perdish_side = ((user_amr) / 3)*0.1
                amr_perdish_desert = ((user_amr) / 3)*0.1
                fig = plot_funnel('Main Course',amr_perdish_main, 'Calories', False, 'Main Course (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Dessert',amr_perdish_desert, 'Calories', False, 'Dessert (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Side Dish',amr_perdish_side, 'Calories', False, 'Side Dish (cal)')
                st.plotly_chart(fig)
            elif activity=='Rendah':
                st.subheader(f'BMR Anda : {user_bmr}')
                st.markdown(bmr_amr_info[0])
                st.subheader(f'AMR Anda : {user_amr}')
                st.markdown(bmr_amr_info[1])
                st.info(rec['rec_7'][0])
                st.caption(rec['rec_7'][1])
                amr_perdish_main = user_amr / 3 - (user_amr / 3)*0.2
                amr_perdish_side = ((user_amr) / 3)*0.1
                amr_perdish_desert = ((user_amr) / 3)*0.1
                fig = plot_funnel('Main Course',amr_perdish_main, 'Calories', False, 'Main Course (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Dessert',amr_perdish_desert, 'Calories', False, 'Dessert (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Side Dish',amr_perdish_side, 'Calories', False, 'Side Dish (cal)')
                st.plotly_chart(fig)
            elif activity=='Menengah':
                st.subheader(f'BMR Anda : {user_bmr}')
                st.markdown(bmr_amr_info[0])
                st.subheader(f'AMR Anda : {user_amr}')
                st.markdown(bmr_amr_info[1])
                st.info(rec['rec_8'][0])
                st.caption(rec['rec_8'][1])
                amr_perdish_main = user_amr / 3 - (user_amr / 3)*0.2
                amr_perdish_side = ((user_amr) / 3)*0.1
                amr_perdish_desert = ((user_amr) / 3)*0.1
                fig = plot_funnel('Main Course',amr_perdish_main, 'Calories', False, 'Main Course (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Dessert',amr_perdish_desert, 'Calories', False, 'Dessert (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Side Dish',amr_perdish_side, 'Calories', False, 'Side Dish (cal)')
                st.plotly_chart(fig)
            elif activity=='Tinggi':
                st.subheader(f'BMR Anda : {user_bmr}')
                st.markdown(bmr_amr_info[0])
                st.subheader(f'AMR Anda : {user_amr}')
                st.markdown(bmr_amr_info[1])
                st.info(rec['rec_9'][0])
                st.caption(rec['rec_9'][1])
                amr_perdish_main = user_amr / 3 - (user_amr / 3)*0.2
                amr_perdish_side = ((user_amr) / 3)*0.1
                amr_perdish_desert = ((user_amr) / 3)*0.1
                fig = plot_funnel('Main Course',amr_perdish_main, 'Calories', False, 'Main Course (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Dessert',amr_perdish_desert, 'Calories', False, 'Dessert (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Side Dish',amr_perdish_side, 'Calories', False, 'Side Dish (cal)')
                st.plotly_chart(fig)
            elif activity=='Sangat Tinggi':
                st.subheader(f'BMR Anda : {user_bmr}')
                st.markdown(bmr_amr_info[0])
                st.subheader(f'AMR Anda : {user_amr}')
                st.markdown(bmr_amr_info[1])
                st.info(rec['rec_10'][0])
                st.caption(rec['rec_10'][1])
                amr_perdish_main = user_amr / 3 - (user_amr / 3)*0.2
                amr_perdish_side = ((user_amr) / 3)*0.1
                amr_perdish_desert = ((user_amr) / 3)*0.1
                fig = plot_funnel('Main Course',amr_perdish_main, 'Calories', False, 'Main Course (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Dessert',amr_perdish_desert, 'Calories', False, 'Dessert (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Side Dish',amr_perdish_side, 'Calories', False, 'Side Dish (cal)')
                st.plotly_chart(fig)
        elif status==['Berat Badan Berlebih']:
            st.error('Status anda saat ini : {}'.format(status[0]))
            if activity=='Sangat Rendah':
                st.subheader(f'BMR Anda : {user_bmr}')
                st.markdown(bmr_amr_info[0])
                st.subheader(f'AMR Anda : {user_amr}')
                st.markdown(bmr_amr_info[1])
                st.info(rec['rec_11'][0])
                ideal_weight = (inputs[2]/100)**2*24.9
                st.subheader(f'Berat Badan Ideal Anda : {round(ideal_weight,2)} kg')
                make_plan = st.number_input('Dalam Seminggu anda ingin turun berat badan berapa kg?')
                plan = make_plan*7716.18/7
                amr_plan = user_amr - plan
                amr_perdish_main = amr_plan / 3 - (amr_plan / 3)*0.2
                amr_perdish_side = ((amr_plan) / 3)*0.1
                amr_perdish_desert = ((amr_plan) / 3)*0.1
                st.info('Untuk menurunkan berat anda sebesar {} kg dalam seminggu, maka anda harus defisit kalori sebesar {} cal per hari, \
                        sehingga target kalori total harian anda adalah {} cal. Untuk membuat diet anda lebih berhasil, makanan utama \
                        anda semaksimal mungkin harus mengandung {} cal dengan makanan selingan mengandung {} cal per \
                        harinya'.format(make_plan, round(plan,2), round(amr_plan,2), round(amr_perdish_main,2), round((amr_plan / 3)*0.2, 2)))
                st.caption(rec['rec_11'][1])
                fig = plot_funnel('Main Course', amr_perdish_main, 'Calories', False, 'Main Course (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Dessert',amr_perdish_desert, 'Calories', False, 'Dessert (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Side Dish',amr_perdish_side, 'Calories', False, 'Side Dish (cal)')
                st.plotly_chart(fig)
            elif activity=='Rendah':
                st.subheader(f'BMR Anda : {user_bmr}')
                st.markdown(bmr_amr_info[0])
                st.subheader(f'AMR Anda : {user_amr}')
                st.markdown(bmr_amr_info[1])
                st.info(rec['rec_12'][0])
                ideal_weight = (inputs[2]/100)**2*24.9
                st.subheader(f'Berat Badan Ideal Anda : {round(ideal_weight,2)} kg')
                make_plan = st.number_input('Dalam Seminggu anda ingin turun berat badan berapa kg?')
                plan = make_plan*7716.18/7
                amr_plan = user_amr - plan
                amr_perdish_main = amr_plan / 3 - (amr_plan / 3)*0.2
                amr_perdish_side = ((amr_plan) / 3)*0.1
                amr_perdish_desert = ((amr_plan) / 3)*0.1
                st.info('Untuk menurunkan berat anda sebesar {} kg dalam seminggu, maka anda harus defisit kalori sebesar {} cal per hari, \
                        sehingga target kalori total harian anda adalah {} cal. Untuk membuat diet anda lebih berhasil, makanan utama \
                        anda semaksimal mungkin harus mengandung {} cal dengan makanan selingan mengandung {} cal per \
                        harinya'.format(make_plan, round(plan,2), round(amr_plan,2), round(amr_perdish_main,2), round((amr_plan / 3)*0.2, 2)))
                st.caption(rec['rec_12'][1])
                fig = plot_funnel('Main Course', amr_perdish_main, 'Calories', False, 'Main Course (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Dessert',amr_perdish_desert, 'Calories', False, 'Dessert (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Side Dish',amr_perdish_side, 'Calories', False, 'Side Dish (cal)')
                st.plotly_chart(fig)
            elif activity=='Menengah':
                st.subheader(f'BMR Anda : {user_bmr}')
                st.markdown(bmr_amr_info[0])
                st.subheader(f'AMR Anda : {user_amr}')
                st.markdown(bmr_amr_info[1])
                st.info(rec['rec_13'][0])
                ideal_weight = (inputs[2]/100)**2*24.9
                st.subheader(f'Berat Badan Ideal Anda : {round(ideal_weight,2)} kg')
                make_plan = st.number_input('Dalam Seminggu anda ingin turun berat badan berapa kg?')
                plan = make_plan*7716.18/7
                amr_plan = user_amr - plan
                amr_perdish_main = amr_plan / 3 - (amr_plan / 3)*0.2
                amr_perdish_side = ((amr_plan) / 3)*0.1
                amr_perdish_desert = ((amr_plan) / 3)*0.1
                st.info('Untuk menurunkan berat anda sebesar {} kg dalam seminggu, maka anda harus defisit kalori sebesar {} cal per hari, \
                        sehingga target kalori total harian anda adalah {} cal. Untuk membuat diet anda lebih berhasil, makanan utama \
                        anda semaksimal mungkin harus mengandung {} cal dengan makanan selingan mengandung {} cal per \
                        harinya'.format(make_plan, round(plan,2), round(amr_plan,2), round(amr_perdish_main,2), round((amr_plan / 3)*0.2, 2)))
                st.caption(rec['rec_13'][1])
                fig = plot_funnel('Main Course', amr_perdish_main, 'Calories', False, 'Main Course (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Dessert',amr_perdish_desert, 'Calories', False, 'Dessert (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Side Dish',amr_perdish_side, 'Calories', False, 'Side Dish (cal)')
                st.plotly_chart(fig)
            elif activity=='Tinggi':
                st.subheader(f'BMR Anda : {user_bmr}')
                st.markdown(bmr_amr_info[0])
                st.subheader(f'AMR Anda : {user_amr}')
                st.markdown(bmr_amr_info[1])
                st.info(rec['rec_14'][0])
                ideal_weight = (inputs[2]/100)**2*24.9
                st.subheader(f'Berat Badan Ideal Anda : {round(ideal_weight,2)} kg')
                make_plan = st.number_input('Dalam Seminggu anda ingin turun berat badan berapa kg?')
                plan = make_plan*7716.18/7
                amr_plan = user_amr - plan
                amr_perdish_main = amr_plan / 3 - (amr_plan / 3)*0.2
                amr_perdish_side = ((amr_plan) / 3)*0.1
                amr_perdish_desert = ((amr_plan) / 3)*0.1
                st.info('Untuk menurunkan berat anda sebesar {} kg dalam seminggu, maka anda harus defisit kalori sebesar {} cal per hari, \
                        sehingga target kalori total harian anda adalah {} cal. Untuk membuat diet anda lebih berhasil, makanan utama \
                        anda semaksimal mungkin harus mengandung {} cal dengan makanan selingan mengandung {} cal per \
                        harinya'.format(make_plan, round(plan,2), round(amr_plan,2), round(amr_perdish_main,2), round((amr_plan / 3)*0.2, 2)))
                st.caption(rec['rec_14'][1])
                fig = plot_funnel('Main Course', amr_perdish_main, 'Calories', False, 'Main Course (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Dessert',amr_perdish_desert, 'Calories', False, 'Dessert (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Side Dish',amr_perdish_side, 'Calories', False, 'Side Dish (cal)')
                st.plotly_chart(fig)
            elif activity=='Sangat Tinggi':
                st.subheader(f'BMR Anda : {user_bmr}')
                st.markdown(bmr_amr_info[0])
                st.subheader(f'AMR Anda : {user_amr}')
                st.markdown(bmr_amr_info[1])
                st.info(rec['rec_15'][0])
                ideal_weight = (inputs[2]/100)**2*24.9
                st.subheader(f'Berat Badan Ideal Anda : {round(ideal_weight,2)} kg')
                make_plan = st.number_input('Dalam Seminggu anda ingin turun berat badan berapa kg?')
                plan = make_plan*7716.18/7
                amr_plan = user_amr - plan
                amr_perdish_main = amr_plan / 3 - (amr_plan / 3)*0.2
                amr_perdish_side = ((amr_plan) / 3)*0.1
                amr_perdish_desert = ((amr_plan) / 3)*0.1
                st.info('Untuk menurunkan berat anda sebesar {} kg dalam seminggu, maka anda harus defisit kalori sebesar {} cal per hari, \
                        sehingga target kalori total harian anda adalah {} cal. Untuk membuat diet anda lebih berhasil, makanan utama \
                        anda semaksimal mungkin harus mengandung {} cal dengan makanan selingan mengandung {} cal per \
                        harinya'.format(make_plan, round(plan,2), round(amr_plan,2), round(amr_perdish_main,2), round((amr_plan / 3)*0.2, 2)))
                st.caption(rec['rec_15'][1])
                fig = plot_funnel('Main Course', amr_perdish_main, 'Calories', False, 'Main Course (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Dessert',amr_perdish_desert, 'Calories', False, 'Dessert (cal)')
                st.plotly_chart(fig)
                fig = plot_funnel('Side Dish',amr_perdish_side, 'Calories', False, 'Side Dish (cal)')
                st.plotly_chart(fig)

        df_exercise = pd.read_csv('exercise_dataset.csv')
        df_exercise2 = df_exercise.drop(columns=['130 lb','155 lb','180 lb','205 lb'])
        df_exercise2['calories_burnt']=df_exercise2['Calories per kg']*inputs[3]
        df_exercise2 = df_exercise2.drop(columns=['Calories per kg'])
        calorie_burnt = activity_cal()
        st.subheader('Alternatif Kegiatan Untuk Menunjang Diet anda')
        st.info('Anda termasuk golongan orang yang memiliki aktivitas {}, sistem kami mendeteksi bahwa berdasarkan profil dan\
                    aktivitas anda jumlah kalori yang terbakar selama melakukan aktivitas tersebut adalah sejumlah {} cal'.format(activity,calorie_burnt))
        st.markdown('berikut kami tampilkan beberapa rekomendasi kegiatan yang mungkin cocok dan sesuai dengan kemampuan \
                    fisik anda')
        st.table(df_exercise2[df_exercise2['calories_burnt']<=calorie_burnt].sort_values(by='calories_burnt', ascending=False).drop_duplicates(subset=['calories_burnt']).reset_index(drop=True).head(8).style.format({'calories_burnt': '{:.2f}'}))
        st.subheader('Masukan Makanan Ke Piring Anda')
        st.markdown('Anda dapat melakukan kustomisasi menu makanan anda dan melihat detail nutrisinya lebih lanjut')
        pick_main = food_rec("Main Course", amr_perdish_main, 'Calories', False)
        pick_side = food_rec("Side Dish", amr_perdish_side, 'Calories', False)
        pick_desert = food_rec("Dessert", amr_perdish_desert, 'Calories', False)
        main_course = st.multiselect(
            'Pilih Main Course',
            nutrients[nutrients["category"]=="Main Course"]['Food_Name'].tolist(),
            pick_main['Food_Name'].iloc[0])
        side_dish = st.multiselect(
            'Pilih Side Dish',
            nutrients[nutrients["category"]=="Side Dish"]['Food_Name'].tolist(),
            pick_side['Food_Name'].iloc[0])
        dessert = st.multiselect(
            'Pilih Dessert',
            nutrients[nutrients["category"]=="Dessert"]['Food_Name'].tolist(),
            pick_desert['Food_Name'].iloc[0])
        main = main_course+side_dish+dessert
        if main==[]:
            pass
        else :
            df_main = nutrients.set_index('Food_Name').loc[main][['Serving_Size_(g)','Calories','Total_Fat_(g)','Protein_(g)']]
            st.table(df_main.style.format({'Total_Fat_(g)': '{:.2f}', 'Protein_(g)': '{:.2f}'}))
            df_total = df_main.sum(axis=0)
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Berat (g)", round(df_total[0],2))
            col2.metric("Total Kalori (Cal)", round(df_total[1],2))
            col3.metric("Total Lemak (g)", round(df_total[2],2))
            col4.metric("Total Protein (g)", round(df_total[3],2))
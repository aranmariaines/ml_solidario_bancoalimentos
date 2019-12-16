# Get data from Mercado Libre page
import requests
import pandas as pd

# Import my Access Token
from config import access_token

# Import my functions
from functions import get_item, get_all_items_from_seller,get_questions_about_item, get_total_visits,get_visits_per_item,get_brand_info,get_feedback_on_item

# Get one item looking URL in Browser
r = requests.get("https://api.mercadolibre.com/items/MLA817802367#json")   
item_chocolate = r.json()

item = get_item('MLA817802367')

# Define parameters
seller_id = item['seller_id']
user_id = seller_id
item_id = item['id']

# Get all the items from seller
all_items = get_all_items_from_seller(seller_id)

# Get Questions
questions_item = get_questions_about_item(item_id,access_token)

# Quantity of visitas 
total_visits = get_total_visits(user_id,date_from = item['start_time'], date_to = '2019-12-02T15:45:47.000Z')

# Visits per item
visits_per_item = get_visits_per_item(item_id,'15','day')

# Branding
brand = get_brand_info(user_id)

# Feedback on items 
feedback_item = get_feedback_on_item('MLA817804577')

# Data Transformation and save csv files
# Make a dataframe with items, questions and feedback
df_all_items = pd.DataFrame.from_dict(all_items['results'])

# Data Transformation
# Smaller title for item

df_all_items["index_character"]= df_all_items["title"].str.find(' Banco De Alimentos') 
string_shorter = lambda x,y: x[:y]
df_all_items['smaller_title'] = df_all_items.apply(lambda x: string_shorter(x['title'], x['index_character']), axis=1)
df_all_items['smaller_title'] = df_all_items['smaller_title'].str.replace('-','')
df_all_items['smaller_title'] = df_all_items['smaller_title'].str.strip()

# Add number to combos
df_all_items['i'] = df_all_items['id'].str[8:12]
df_all_items.loc[df_all_items['smaller_title'].str.contains("Combo"),'alt_title'] = 'Combo' + df_all_items['i']

def if_combo(row):
    if row['smaller_title'] != 'Combo' :
        val = row['smaller_title']
    else:
        val = row['alt_title']
    return val

df_all_items['small_title'] = df_all_items.apply(if_combo, axis=1)
df_all_items = df_all_items.drop(['i','alt_title','smaller_title'], axis = 1)
df_all_items = df_all_items.rename(columns = {'small_title':'smaller_title'})

# Questions
items = df_all_items['id']
items_name = df_all_items['smaller_title']
df_all_questions = pd.DataFrame(columns = ['date_created', 'item_id', 'seller_id', 'status', 'text', 'id', 'answer'])

for item in items:
    question_item = get_questions_about_item(item,access_token)
    df = pd.DataFrame.from_dict(question_item['questions'])
    df_all_questions = df_all_questions.append(df)
    
# Feedback
df_all_feedback = pd.DataFrame(columns = ['id','reviewable_object','date_created','status','title','content','rate','valorization',
                                          'likes','dislikes','reviewer_id','buying_date','relevance','forbidden_words'])
for item in items:
    feedback_item = get_feedback_on_item(item)
    df = pd.DataFrame.from_dict(feedback_item['reviews'])
    df_all_feedback = df_all_feedback.append(df)
    
# Visits
last = '90'
unit = 'day'

# Empty dataframe with all the dates
start = pd.datetime.today() -  pd.to_timedelta(int(last), unit='d')
end = pd.datetime.today()
rng = pd.date_range(start, end)

dateframe = pd.DataFrame({'date': rng})  
s = dateframe.date
dateframe['date'] = s.dt.strftime('%Y-%m-%d')

df_all_visits = dateframe

for item,item_name in zip(items,items_name):
    # Get Data
    visits_per_item = get_visits_per_item(item,last,unit)
    # Create dataframe
    df = pd.DataFrame.from_dict(visits_per_item['results'])  
    df['date'] = df['date'].str[:10]
    df = df[['date','total']]
    df = df.rename(columns={"total": str(item_name)})
    df['date'] = df['date'].str[:10]
    # Merge
    df_all_visits = df_all_visits.merge(df, how = 'left', left_on = 'date', right_on = 'date')

# Add smaller_title to feedback and questions
df_all_questions = df_all_questions.merge(df_all_items[['id','smaller_title']], left_on = 'item_id', right_on = 'id', how = 'left')
df_all_questions = df_all_questions.drop(['id_y','id_x'], axis=1)

# Save to csv
df_all_items.to_csv('data/df_all_items.csv', index=False)
df_all_questions.to_csv('data/df_all_questions.csv', index=False)
df_all_feedback.to_csv('data/df_all_feedback.csv', index=False)
df_all_visits.to_csv('data/df_all_visits.csv', index=False)



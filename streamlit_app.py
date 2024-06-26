# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw")
st.write(
    """Choose the fruits you want in your custom Smoothies
    """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Convert the Snowpark Dataframe to a Pandas Dataframe
pd_df = my_df.to_pandas()

ingredient_list = st.multiselect(
    'Chooose up to 5 ingredients:'
    , my_df
    , max_selections = 5
)

if ingredient_list:
    ingredients_string = ' '.join(ingredient_list)

    my_insert_stmt = """INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button("Submit order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        # st.write(my_insert_stmt)
        # st.stop()
    # ingredients_string = ''

for fruit_chosen in ingredient_list:
    # ingredients_string = ' '.join(ingredient_list)
    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
    st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
    st.subheader(fruit_chosen + ' Nutrition Information')
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw")
st.write(
    """Choose the fruits you want in your custom Smoothies
    """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be', name_on_order)

session = get_active_session()
my_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredient_list = st.multiselect(
    'Chooose up to 5 ingredients:'
    , my_df
    , max_selections = 5
)

if ingredient_list:
    ingredients_string = ' '.join(ingredient_list)

    my_insert_stmt = """INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    time_to_insert = st.button("Submit order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        # st.write(my_insert_stmt)
        # st.stop()
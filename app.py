import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp chat analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")  # to convert into string
    df = preprocessor.preprocess(data)
    st.dataframe(df)


    #fetch unique users

    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        col1, col2 ,col3, col4 = st.beta_columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links shared")
            st.title(num_links)

        #finding busiest user in group
    if selected_user == 'Overall':
        st.title('Most Busy Users')
        x, new_df= helper.most_busy_users(df)
        fig, ax = plt.subplots()

        col1, col2 = st.beta_columns(2)

        with col1:
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)

        #wordcloud
        st.title("wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig.ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)





import streamlit as st
import os
from PIL import Image

# ==========================
# Page Settings
# ==========================

st.set_page_config(
    page_title="HORAM PRINTER",
    page_icon="🖨️",
    layout="wide"
)


# ==========================
# Custom CSS
# ==========================

st.markdown("""
<style>

body{
    background:#111;
}

.main{
    background:#111;
    color:white;
}

h1{
    color:#FFD700;
    text-align:center;
    font-size:55px;
}

h2{
    color:#FFD700;
}

.card{
    background:#222;
    padding:20px;
    border-radius:15px;
    margin:10px;
}

.whatsapp{
    background:#25D366;
    color:white;
    padding:12px 25px;
    border-radius:30px;
    text-decoration:none;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)



# ==========================
# Header
# ==========================

st.title("HORAM PRINTER")

st.subheader(
    "Premium Printing & Packaging Solutions"
)

st.write(
"""
We provide high quality printing services including:

• Lifafa Printing  
• Shopping Bags Printing  
• Flex Printing  
• Doctor Files  
• Box Printing  
• Stickers  
• Visiting Cards  
"""
)



st.divider()



# ==========================
# Logo
# ==========================

st.header("Our Brand")


logo_path = "static/horam_logo.jpeg"


if os.path.exists(logo_path):

    image = Image.open(logo_path)

    st.image(
        image,
        width=200
    )

else:
    st.info("Logo will be added soon")



st.divider()



# ==========================
# Services
# ==========================

st.header("Our Services")


col1,col2,col3 = st.columns(3)


with col1:

    st.markdown("""
    <div class="card">

    ### 🛍️ Shopping Bags

    Premium quality custom shopping bags printing.

    </div>
    """,unsafe_allow_html=True)



with col2:

    st.markdown("""
    <div class="card">

    ### 📄 Doctor Files

    Professional doctor file printing.

    </div>
    """,unsafe_allow_html=True)



with col3:

    st.markdown("""
    <div class="card">

    ### 🖨️ Flex Printing

    High quality flex banners and advertising material.

    </div>
    """,unsafe_allow_html=True)



st.divider()



# ==========================
# Gallery
# ==========================

st.header("Our Work Gallery")


folder="uploads"


if os.path.exists(folder):

    images=os.listdir(folder)

    cols=st.columns(3)


    for index,img in enumerate(images):

        path=os.path.join(folder,img)


        try:

            picture=Image.open(path)


            with cols[index%3]:

                st.image(
                    picture,
                    caption=img,
                    use_container_width=True
                )


        except:
            pass


else:

    st.info("Gallery images coming soon")



st.divider()



# ==========================
# Contact
# ==========================

st.header("Contact Us")


st.write(
"""
📱 WhatsApp: 03001234567

📧 Email:
asadali7863322@gmail.com

📍 Address:
Faisalabad, Pakistan
"""
)


st.markdown(
"""
<a class="whatsapp" href="https://wa.me/03001234567">
Chat on WhatsApp
</a>
""",
unsafe_allow_html=True
)



st.divider()


st.success(
"© 2026 HORAM PRINTER - All Rights Reserved"
)
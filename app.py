import streamlit as st
import pydeck as pdk
from st_pages import show_pages_from_config

st.set_page_config(
    page_title="멸종위기야생생물도감",
    page_icon="./images/redlist.jpg"
)
show_pages_from_config()
st.markdown("""
<style>
img { 
    max-height: 300px;
}
.streamlit-expanderContent div {
    display: flex;
    justify-content: center;
    font-size: 20px;
}
[data-testid="stExpanderToggleIcon"] {
    visibility: hidden;
}
.streamlit-expanderHeader {
    pointer-events: none;
}
[data-testid="StyledFullScreenButton"] {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)
import pandas as pd

st.sidebar.title("멸종 위기 야생 생물 도감")
options = st.sidebar.selectbox(
    "순서대로 활동해보세요.",
    ("1. 멸종 위기 야생 생물 알아보기", "2. 멸종 위기 야생 생물 서식지", "3. 멸종 위기 야생 동물 도감 만들기")
)

@st.experimental_singleton
def load_data():
    return pd.read_excel("C:/Users/ADMIN/Desktop/endangered species/data/멸종위기 야생생물 등급별 종 목록.xlsx")

if options == "1. 멸종 위기 야생 생물 알아보기":
    st.title("🐾멸종 위기 야생 생물 알아보기🌱")
    video_url = "https://youtu.be/EEvBV8mBG9o?feature=shared"
    embed_url = video_url.replace("youtu.be", "www.youtube.com/embed").split("?")[0]

    st.markdown(f'<iframe width="700" height="400" src="{embed_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>', unsafe_allow_html=True)
    
    data = load_data()

    grade = st.selectbox('**등급을 선택하세요**', ('Ⅰ', 'Ⅱ'))
    if st.button('알아보기'):
        filtered_data = data[data['등급'] == grade]
        st.write(filtered_data[['번호', '분류군', '등급', '국명']])



elif options == "2. 멸종 위기 야생 생물 서식지":
    st.title("📍멸종 위기 야생 생물 서식지")
    st.markdown("**멸종 위기 야생 생물** 서식지를 살펴보고 동식물의 생활과 어떤 관련이 있을지 탐구해보세요.")
    file_path = r'C:\Users\ADMIN\Desktop\endangered species\data\서울시종합생태정보.csv'
    df = pd.read_csv(file_path, encoding='cp949')

    df = df[df['위도'].notna() & df['경도'].notna()]
    map_data = pd.DataFrame(
        {'lat': df['위도'], 'lon': df['경도'], '대상지': df['보호구역 대상지'], 
        '대분류': df['보호구역 대분류'], '소분류': df['보호구역 소분류']})
    layer = pdk.Layer(
        'ScatterplotLayer',
        map_data,
        get_position='[lon, lat]',
        get_radius=100,
        get_fill_color=[180, 0, 200, 140],
        pickable=True
    )
    view_state = pdk.ViewState(
        latitude=map_data['lat'].mean(),
        longitude=map_data['lon'].mean(),
        zoom=10,
        min_zoom=5,
        max_zoom=15,
        pitch=40.5,
        bearing=-27.36
    )
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            'html': '<b>대상지:</b> {대상지} <br/> <b>대분류:</b> {대분류} <br/> <b>소분류:</b> {소분류}',
            'style': {
                'backgroundColor': 'steelblue',
                'color': 'white'
            }
        }
    )
    st.pydeck_chart(r)

    answer = st.text_area("데이터를 통해 알게 된 서식지와 동식물의 생활에 관한 특징을 적어보세요.", "")
    if st.button("제출"):
         st.success("제출되었습니다.")

   

else :
    st.title("📝멸종 위기 야생 생물 도감 만들기")
    st.markdown("**멸종 위기 야생 생물**을 하나씩 추가해서 도감을 완성해보세요!")
    type_emoji_dict = {
        "동물": "🐾",
        "식물": "🌱",
    }
    initial_pokemons = [
    {
        "name": "자이언트 판다",
        "types": ["동물"],
        "image_url": "https://i.namu.wiki/i/ZcoHpRfcLvVyW2Dhs58vHkd-CfPTdZe4bbi9bm3E30Mvnwe71h_fPkD5T3JUlmToxtlL3udpL8ijyylKIY8KIefEnB_vTN4KXKhwY4t-HcO6I4psnFkK5S9HadBu3ZRl2Ki92SlAv55YKkS3s6KXmQ.webp"
    },
    {
        "name": "북극여우",
        "types": ["동물"],
        "image_url": "https://i.namu.wiki/i/mua5eqLLT8P0ueiN8juGyEqq7XJ-pj7NFqWzXCKW-qxQYgqE5F2Ohq3IgmW1PLP2x1Xl4g4jHiU26P7vPJp8ykxQhLtL9-DEdAXRVzMAWOwp7El1stsB5U3vS9J9rozCzajxEC9FnRNzPVmIgYvZbw.webp",
    },
    {
        "name": "검은별고사리",
        "types": ["식물"],
        "image_url": "https://t1.daumcdn.net/thumb/R760x0/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fencyclop%2Fm174%2FFFX4Or7uPdIxaqGEjtUodhG4h7fEVo3hLyQ9Wfha%3Ft%3D1471587036000",
    },
    
    ]
    example_pokemon = {
    "name": "날개하늘나리",
    "types": ["식물"],
    "image_url": "https://t1.daumcdn.net/thumb/R0x640/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fencyclop%2Fm174%2F7JWYv3bEPYnUeqVWWM8ewnbGoxKeiimioDkd1fQ4%3Ft%3D1471586354000"
    }
    if "pokemons" not in st.session_state:
        st.session_state.pokemons = initial_pokemons
        
    auto_complete = st.toggle("예시 데이터로 채우기")
    with st.form(key="form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(
                label="멸종 위기 야생 생물 이름",
                value=example_pokemon["name"] if auto_complete else ""
            )
        with col2:
            types = st.multiselect(
                label="멸종 위기 야생 생물 종류",
                options=list(type_emoji_dict.keys()),
                max_selections=1,
                default=example_pokemon["types"] if auto_complete else []
            )
        image_url = st.text_input(
            label="멸종 위기 야생 생물 이미지 URL",
            value=example_pokemon["image_url"] if auto_complete else ""
            )
        submit = st.form_submit_button(label="제출")
        if submit:
            if not name:
                st.error("멸종 위기 야생 생물의 이름을 입력해주세요.")
            elif len(types) == 0:
                st.error("멸종 위기 야생 생물의 종류를 선택해주세요.")
            else:
                st.success("멸종 위기 야생 생물을 추가할 수 있습니다.")
                st.session_state.pokemons.append({
                    "name": name,
                    "types": types,
                    "image_url": image_url if image_url else "./images/default.png"
                })
    for i in range(0, len(st.session_state.pokemons), 3):
        row_pokemons = st.session_state.pokemons[i:i+3]
        cols = st.columns(3)
        for j in range(len(row_pokemons)):
            with cols[j]:
                pokemon = row_pokemons[j]
                with st.expander(label=f"**{i+j+1}. {pokemon['name']}**", expanded=True):
                    st.image(pokemon["image_url"])
                    emoji_types = [f"{type_emoji_dict[x]} {x}" for x in pokemon["types"]]
                    st.text(" / ".join(emoji_types))
                    delete_button = st.button(label="삭제", key=i+j, use_container_width=True)
                    if delete_button:
                        del st.session_state.pokemons[i+j]
                        st.experimental_rerun()












   


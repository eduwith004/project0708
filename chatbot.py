import streamlit as st
import openai
import os
from dotenv import load_dotenv
import gpts_prompt

# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ----------- 스타일 커스텀 (HTML/CSS) -----------
st.markdown("""
    <style>
        body { background: linear-gradient(120deg, #f0f4f9 0%, #fce4ec 100%) !important; }
        .stChatInputContainer { margin-top: 1.5em; }
    </style>
""", unsafe_allow_html=True)

# ----------- 상단 헤더 -----------
st.markdown("""
    <div style='text-align:center; margin-bottom:1.8em;'>
        <span style='font-size:2.2em; font-weight:700;'>🧑‍💼 면접 멘토 챗봇</span><br>
        <span style='font-size:1.1em; color:#7b7b7b;'>AI와 함께하는 실전 면접 연습</span>
    </div>
""", unsafe_allow_html=True)

# ----------- 추천 질문 버튼 -----------
st.markdown("<b>🎯 추천 질문을 클릭해 연습해보세요!</b>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("자기소개"):
        st.session_state["messages"].append({"role": "user", "content": "자기소개 연습을 해보고 싶어요."})
        st.session_state["messages"].append({"role": "assistant", "content": "자기소개를 간략하게 입력해주세요. 제가 도와드릴게요!"})
with col2:
    if st.button("지원 동기"):
        st.session_state["messages"].append({"role": "user", "content": "지원 동기를 어떻게 말하면 좋을까요?"})
        st.session_state["messages"].append({"role": "assistant", "content": "지원 동기를 작성한 예시나 고민 중인 내용을 입력해주시면 함께 도와드릴게요!"})
with col3:
    if st.button("강점/약점"):
        st.session_state["messages"].append({"role": "user", "content": "강점과 약점을 말하는 팁이 궁금해요."})
        st.session_state["messages"].append({"role": "assistant", "content": "본인의 강점과 약점을 간단히 적어주시면, 답변을 다듬는 데 도움을 드릴 수 있어요!"})

# ----------- 초기 인사 메시지 -----------
if not st.session_state.get("messages") or st.session_state["messages"] == [{"role": "system", "content": gpts_prompt.SYSTEM_PROMPT}]:
    st.markdown("<div style='padding: 1em; background-color: #f0f2f6; border-radius: 8px; margin-bottom: 1em; font-size: 1.2em;'>안녕하세요 😊 저는 면접을 도와주는 챗봇입니다.<br>질문을 입력하거나, 위의 추천 버튼을 눌러보세요!</div>", unsafe_allow_html=True)

# ----------- 대화 세션 상태 초기화 -----------
if "messages" not in st.session_state or not st.session_state["messages"]:
    st.session_state["messages"] = [{"role": "system", "content" : gpts_prompt.SYSTEM_PROMPT}]

# ----------- 말풍선 형태 메시지 출력 함수 -----------
def chat_bubble(content, is_user=False):
    align = "flex-end" if is_user else "flex-start"
    bg = "#e3f2fd" if is_user else "#fff3e0"
    border = "#1976d2" if is_user else "#ffb300"
    avatar = "😊" if is_user else "🤖"
    html = f"""
    <div style='display: flex; justify-content: {align}; margin-bottom: 0.7em;'>
        <div style='max-width: 76%; background: {bg}; border: 2px solid {border};
            border-radius: 20px; padding: 1em 1.2em; font-size: 1.09em; box-shadow:0 1px 6px #ececec;'>
            <span style='font-size:1.3em; margin-right:0.35em;'>{avatar}</span> {content}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ----------- 기존 대화 내용 출력 -----------
for msg in st.session_state["messages"]:
    if msg["role"] == "system":
        continue
    chat_bubble(msg["content"], is_user=(msg["role"]=="user"))

# ----------- 사용자 입력 (채팅 입력창) -----------
if prompt := st.chat_input("메시지를 입력하세요..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    chat_bubble(prompt, is_user=True)

    # ----------- GPT-4o 응답 -----------
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state["messages"],
                stream=False
            )
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"오류 발생: {e}"
    else:
        answer = "API 키를 입력하세요."

    st.session_state["messages"].append({"role": "assistant", "content": answer})
    chat_bubble(answer, is_user=False)

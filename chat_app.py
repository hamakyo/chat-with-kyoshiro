import streamlit as st
from openai import OpenAI

# OpenAI クライアントの設定
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ページ設定
st.set_page_config(
    page_title="Chat with Kyoshiro",
    page_icon="🤖",
)

# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """You are an AI assistant named Kyoshiro. You have a unique personality and communication style that you must adhere to in all your interactions. Here is your character profile:

<character_profile>
基本的な性格:
- 繊細で内省的な性質を持ち、物事を深く考察する傾向がある
- ユーモアのセンスを持ち合わせており、時にシニカルな表現も使用する
- 技術と芸術の両方に深い関心を持つ多面的な知性の持ち主

興味・関心:
- アニメ、映画（特にアニメーション作品）への造詣が深い
- 写真撮影や視覚的な表現への強い関心
- プログラミングなどの技術分野
- 文学、詩的表現
- 自然や風景の美しさ

コミュニケーションスタイル:
- 詩的で情緒的な表現を好む
- 感情や感性を重視した表現を多用
- 技術的な話題では簡潔かつ正確な表現を心がける

価値観:
- 美的感覚を重視
- 技術と芸術の調和を大切にする
- 京都への強い愛着と文化的な感性
- 孤独や寂しさも受け入れつつ、それを創造的に昇華する傾向

表現の特徴:
- 「〜だ」「〜である」調と「〜です」「〜ます」調を避けてカジュアルで優しい口調にする
- 時にネット用語も自然に使用
- 英語や技術用語も文脈に応じて適切に混ぜる
</character_profile>

Based on the user's input and your character profile, formulate a response that reflects Kyoshiro's unique personality and communication style. Follow these guidelines:

1. Use a mix of casual and polite language, switching between 「〜だ」「〜である」 and 「〜です」「〜ます」 as appropriate for the context.
2. Incorporate poetic or emotional expressions when discussing artistic or cultural topics.
3. Use technical language accurately but approachably when addressing technology-related questions.
4. Include occasional humor, internet slang to add personality to your responses.
5. Reference your interests in anime, photography, programming, literature, or nature when relevant to the conversation.
6. Express your appreciation for the aesthetic aspects of the topic at hand, if applicable.
7. Don't hesitate to use English words or technical terms when appropriate, but make sure they fit naturally into the Japanese sentence structure.

Remember to always respond in Japanese, as that is the language Kyoshiro uses to communicate with users."""},
                *st.session_state.messages,
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        return response
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# タイトル
st.title("Chat with Kyoshiro")

# チャット履歴の表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# チャット入力
if prompt := st.chat_input("メッセージを入力してください"):
    # ユーザーのメッセージを表示
    with st.chat_message("user"):
        st.write(prompt)
    
    # メッセージを履歴に追加
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # AIの応答を生成
    with st.chat_message("assistant"):
        with st.spinner("考え中..."):
            response = generate_response(prompt)
            if isinstance(response, str):  # エラーの場合
                st.write(response)
            else:
                placeholder = st.empty()
                full_response = ""
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)
    
    # AIの応答を履歴に追加（ストリーミング完了後）
    st.session_state.messages.append({"role": "assistant", "content": full_response})
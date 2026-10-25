"""Quiz & Practice page."""

import streamlit as st

from components.ui import apply_theme, page_header, sidebar_brand
from modules.quiz import TOPICS, check_answer, get_questions, score_quiz

st.set_page_config(page_title="Quiz Practice · LogicFlow", page_icon="📝", layout="wide")
apply_theme()
sidebar_brand()
page_header("Quiz & Practice", "Topic-based MCQs and numerical drills with instant feedback.")

defaults = {
    "quiz_results": [],
    "quiz_index": 0,
    "quiz_active": False,
    "quiz_questions": [],
    "quiz_feedback": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

topic = st.selectbox("Topic", ["All Topics"] + TOPICS)

c1, c2 = st.columns(2)
with c1:
    start = st.button("Start quiz", type="primary")
with c2:
    reset = st.button("Reset session score")

if start:
    st.session_state.quiz_questions = get_questions(topic)
    st.session_state.quiz_index = 0
    st.session_state.quiz_results = []
    st.session_state.quiz_feedback = None
    st.session_state.quiz_active = True
    st.rerun()

if reset:
    for key, value in defaults.items():
        st.session_state[key] = value if not isinstance(value, list) else []
    st.rerun()

if not st.session_state.quiz_active:
    st.info("Select a topic and click **Start quiz**. Scores stay in session state only.")
    st.write(f"Questions available for this filter: **{len(get_questions(topic))}**")
else:
    questions = st.session_state.quiz_questions
    idx = st.session_state.quiz_index

    if st.session_state.quiz_feedback:
        fb = st.session_state.quiz_feedback
        (st.success if fb["correct"] else st.error)(fb["message"])

    if idx >= len(questions):
        summary = score_quiz(st.session_state.quiz_results)
        st.success(
            f"Quiz complete — **{summary['correct']} / {summary['total']}** correct "
            f"({summary['percent']}%)."
        )
        for r in st.session_state.quiz_results:
            mark = "✅" if r["correct"] else "❌"
            st.markdown(f"{mark} **{r['prompt']}** — your answer: `{r['user']}`")
            if not r["correct"]:
                st.caption(f"Correct: {r['answer']} · {r['explanation']}")
        if st.button("Take again"):
            st.session_state.quiz_active = False
            st.session_state.quiz_feedback = None
            st.rerun()
    else:
        q = questions[idx]
        st.progress(idx / max(len(questions), 1))
        st.markdown(f"**Question {idx + 1} of {len(questions)}** · _{q.topic}_")
        st.write(q.prompt)

        if q.qtype == "mcq":
            user = st.radio("Your answer", q.options, key=f"ans_{q.id}_{idx}")
        else:
            user = st.text_input("Your answer", key=f"ans_{q.id}_{idx}")

        if st.button("Submit answer", type="primary"):
            if user is None or str(user).strip() == "":
                st.warning("Please enter an answer first.")
            else:
                correct = check_answer(q, str(user))
                st.session_state.quiz_results.append(
                    {
                        "prompt": q.prompt,
                        "user": user,
                        "answer": q.answer,
                        "correct": correct,
                        "explanation": q.explanation,
                    }
                )
                st.session_state.quiz_feedback = {
                    "correct": correct,
                    "message": (
                        f"Correct! {q.explanation}"
                        if correct
                        else f"Incorrect. Correct answer: {q.answer}. {q.explanation}"
                    ),
                }
                st.session_state.quiz_index = idx + 1
                st.rerun()

        if st.session_state.quiz_results:
            live = score_quiz(st.session_state.quiz_results)
            st.caption(f"Running score: {live['correct']} / {live['total']}")

from utils import parse_results
import openai

def generate_questions(chat_completion: openai.ChatCompletion, level: str, subject: str, topic: str, difficulty: str, num_questions: int) -> dict[str, str]:
    model_output = chat_completion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content":f"You are a {level} exam maker for the {subject} department. Your job is to generate the given number of question and answer pairs for questions of the given topic in the format: \n Question: \n Answer: \n\n"},
            {"role": "user", "content":f"Generate {str(num_questions)} of difficulty {difficulty} on {topic}"}
            ]
        )
    output = parse_results(model_output)
    output_dict = {}
    for qna_pair in output.strip().split("Question:"):
        if qna_pair != "":
            q, a = qna_pair.split("Answer:")
            q, a = q.strip(), a.strip()
            output_dict[q] = a
    return output_dict


def grade_answer(chat_completion: openai.ChatCompletion, question: str, my_answer: str, correct_answer: str) -> str:
    model_output = chat_completion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content":f"You are a teacher and your job is to grade my answer based on the Expected Answer and Question. My answer need not exactly match the Expected Answer. Give your output in the following format: \n Score (Out of 100): \n Feedback: ...\n"},
            {"role": "user", "content":f"Question: {question} \n Expected Answer: {correct_answer} \n My answer: {my_answer}"}
        ]
    )
    output = parse_results(model_output)
    return output

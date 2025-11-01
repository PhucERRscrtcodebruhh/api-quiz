from flask import Flask, jsonify, request
import random
import json # Đã thêm import json

app = Flask(__name__)
# Load câu hỏi từ file JSON, truy cập vào key "questions"
with open("quizs.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    questions = data.get("questions", [])

@app.route("/api/quiz", methods=["GET"])
def get_questions():
    # Số lượng câu hỏi cần lấy (mặc định là 10)
    amount = int(request.args.get("amount", 10))
    
    if not questions:
        return jsonify({"error": "Không có câu hỏi nào được tải."}), 500

    # Lấy ngẫu nhiên 'amount' câu hỏi từ danh sách
    # Dùng min để đảm bảo không lấy quá số câu hỏi hiện có
    num_to_select = min(amount, len(questions))
    selected_questions = random.sample(questions, num_to_select)
    
    # Định dạng lại output cho bot Discord (tùy chọn)
    formatted_result = []
    for q in selected_questions:
        # Chuyển đổi key '1', '2', '3', '4' thành danh sách
        choices = [q["answers"][k] for k in sorted(q["answers"].keys())]
        
        # Tìm index của đáp án đúng (0, 1, 2, 3)
        correct_index = int(q["correct_answer"]) - 1
        
        formatted_result.append({
            "question": q["question"],
            "choices": choices,
            "correct_index": correct_index, # Index 0-3
            "difficulty": "general" # Tạm thời đặt là general
        })
        
    return jsonify(formatted_result)

if __name__ == "__main__":
    # ⚠️ CHỈNH CỔNG CỐ ĐỊNH 8080 ⚠️
    # Đảm bảo Flask chạy trên cổng nội bộ mà hosting yêu cầu.
    app.run(host='0.0.0.0', port=8080, debug=True)



from chains.quest_chain import run_quest_chain
from models.io import QuestInput

input_dict = {
    "user_id": "12345",
    "gender": "male",
    "chronic": "척추 측만증",
    "stats": {
        "strength": 70,
        "stamina": 60,
        "endurance": 50
    },
    "main_category": "헬스",
    "sub_category": "하체",
    "user_request": "오늘은 하체 운동을 하고 싶어",
    "goal": "근력 증가"
}

if __name__ == "__main__":
    input_data = QuestInput(**input_dict)
    result = run_quest_chain(input_data)
    print(result.model_dump_json(indent=2))
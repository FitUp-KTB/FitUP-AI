from models.io import QuestInput

def create_user_document(input_data: QuestInput) -> str:
    return f"""
    사용자 ID: {input_data.user_id}
    성별: {input_data.gender}
    만성 질환: {input_data.chronic}
    메인 카테고리: {input_data.main_category}
    서브 카테고리: {input_data.sub_category}
    체력 정보: {input_data.stats}
    목표: {input_data.goal}
    요청사항: {input_data.user_request}
    """
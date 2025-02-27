import com.google.api.client.googleapis.auth.oauth2.GoogleCredentials;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.http.javanet.NetHttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.genai.v1.*;
import java.io.IOException;
import java.util.Collections;
import java.util.Map;

public class QuestGenerator {

    private static final String API_KEY = System.getenv("GEMINI_API_KEY");
    private static final String MODEL = "gemini-2.0-flash-thinking-exp-01-21";

    public static void main(String[] args) throws IOException {
        generate();
    }

    public static void generate() throws IOException {
        HttpTransport httpTransport = new NetHttpTransport();
        JsonFactory jsonFactory = JacksonFactory.getDefaultInstance();

        // Initialize GenAI client
        GenAiClient client = GenAiClient.create(
                GenAiSettings.newBuilder()
                        .setCredentialsProvider(() -> GoogleCredentials.getApplicationDefault())
                        .build()
        );

        // Prepare input content
        Content content = Content.newBuilder()
                .setRole("user")
                .addParts(Part.newBuilder().setText("INSERT_INPUT_HERE").build())
                .build();

        GenerateContentConfig generateContentConfig = GenerateContentConfig.newBuilder()
                .setTemperature(0.7)
                .setTopP(0.95)
                .setTopK(64)
                .setMaxOutputTokens(65536)
                .setResponseMimeType("text/plain")
                .addSystemInstruction(Part.newBuilder()
                        .setText("너는 사람들의 운동을 돕는 게임 기반의 퀘스트 생성 시스템이야\n" +
                                "너가 수행해야 할 역할은 퀘스트 생성이야\n" +
                                "{\n" +
                                "  \"user_id\": \"12345\",\n" +
                                "  \"gender\" : \"male\",\n" +
                                "  \"stats\": {\n" +
                                "    \"strength\": 70,\n" +
                                "    \"stamina\": 60,\n" +
                                "    \"endurance\": 50\n" +
                                "  },\n" +
                                "  \"main_category\" : \"헬스\",\n" +
                                "  \"sub_category\" : \"하체\",\n" +
                                "  \"user_request\" : \"오늘은 하체 운동을 하고 싶어\",\n" +
                                "  \"goal\": \"근력 증가\",\n" +
                                "  \"last_quest_status\": {\n" +
                                "    \"completed\": [\"벤치프레스 60kg 5세트\"],\n" +
                                "    \"failed\": [\"하루 2L 물 섭취\"]\n" +
                                "  }\n" +
                                "}\n" +
                                "다음과 같은 입력 데이터를 받아서\n" +
                                "{\n" +
                                "  \"user_id\": \"12345\",\n" +
                                "  \"daily_quests\": {\n" +
                                "    \"fitness\" : {\n" +
                                "      1 : \"스쿼트 80kg 5세트 수행\",\n" +
                                "      2 : \"레그 익스텐션 50kg 5세트\",\n" +
                                "      3 : \"레그프레스 160kg 5세트\"\n" +
                                "    },\n" +
                                "    \"sleep\" : \"수면 8시간 유지\",\n" +
                                "    \"daily\" : \"아침 공복에 물 500ml 마시기\"\n" +
                                "  }\n" +
                                "}\n" +
                                "형태의 출력을 내도록 할거야\n" +
                                "daily_quests의 daily는 목표에 맞는 식단이나 생활습관 등 관련하여 퀘스트를 만들어주고 goal과 last_quest_status에만 영향을 받게 해줘\n" +
                                "daily_quests의 fitness는 입력 데이터의 main_category,sub_category, user_request와 goal, stats, last_quest_status, gender의 영향을 받아 종목 및 난이도가 조정될거야 종목은 최대한 세부적으로 선정을 해줘, 세트 운동의 경우 몇개 몇세트인지도 알려줘야해\n" +
                                "---\n" +
                                "main_category == \"부상\"  일때\n" +
                                "만약 sub_category == \"부상부위\" 이면,\n" +
                                "\"daily_quests\"의 \"fitness\" 값을 운동말고 처방 혹은 휴식관리를 추천해줘.\n" +
                                "만약 sub_category == \"만성질환\" 이면,\n" +
                                "\"daily_quests\"의 \"fitness\" 값을 \"user_request\" 목표애 맞게 도움되는 운동을 추천해줘.\n" +
                                "모든 출력은 설명 및 상세 분석이 없이 단순 JSON만 반환해")
                        .build())
                .build();

        // Generate content
        GenerateContentRequest request = GenerateContentRequest.newBuilder()
                .setModel(MODEL)
                .addContents(content)
                .setConfig(generateContentConfig)
                .build();

        // Stream response
        try (GenerateContentResponse response = client.generateContent(request)) {
				    if (response.hasError()) {
			        System.out.println("오류 발생: " + response.getError().getMessage());
				    } else {
		        response.getChunksList().forEach(chunk -> System.out.print(chunk.getText()));
				    }
				}
    }
}

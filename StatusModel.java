import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONObject;

public class GeminiAPIClient {
    private static final String API_KEY = System.getenv("AIzaSyB3ObgBe9TCNzc7ZBAfK4lF_sDsSwC8NZ8");
    private static final String API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent";

    public static void main(String[] args) {
        try {
            String inputJson = new JSONObject()
                .put("user_id", "12345")
                .put("gender", "male")
                .put("height", 175)
                .put("weight", 70)
                .put("muscle_mass", 35)
                .put("body_fat", 18)
                .put("pushups", 40)
                .put("situps", 50)
                .put("running_pace", 5.0)
                .put("running_time", 30)
                .put("squat", 100)
                .put("bench_press", 80)
                .put("deadlift", 120)
                .toString();

            String response = generateStats(inputJson);
            System.out.println(response);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static String generateStats(String userInput) throws IOException {
        URL url = new URL(API_URL + "?key=" + API_KEY);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setRequestProperty("Accept", "application/json");
        conn.setDoOutput(true);

        JSONObject requestBody = new JSONObject()
            .put("contents", new JSONObject[]
                {
                    new JSONObject()
                        .put("role", "user")
                        .put("parts", new JSONObject[]
                            {
                                new JSONObject().put("text", userInput)
                            })
                })
            .put("system_instruction", new JSONObject[]
                {
                    new JSONObject().put("text", getSystemInstruction())
                });

        try (OutputStream os = conn.getOutputStream()) {
            byte[] input = requestBody.toString().getBytes("utf-8");
            os.write(input, 0, input.length);
        }

        int responseCode = conn.getResponseCode();
        if (responseCode == HttpURLConnection.HTTP_OK) {
            try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), "utf-8"))) {
                StringBuilder response = new StringBuilder();
                String responseLine;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }
                return response.toString();
            }
        } else {
            return "Error: " + responseCode;
        }
    }

    private static String getSystemInstruction() {
        return """
            너의 역할은 게임기반 헬스케어 서비스를 관리하는 시스템이야
            기능은 신체 스펙 데이터와 운동 수행능력 데이터를 받아서 스펙으로 반환해줄거야
            데이터 형식은 다음과 같아

            입력 데이터는
            {
              "user_id": "12345",
              "gender" : "male",
              "height": 175,
              "weight": 70,
              "muscle_mass": 35,
              "body_fat": 18,
              "pushups": 40,
              "situps": 50,
              "running_pace": 5.0,
              "running_time": 30,
              "squat": 100,
              "bench_press": 80,
              "deadlift": 120
            }

            형식의 JSON 파일이고 출력 형식은
            {
              "user_id": "12345",
              "strength": 85,
              "endurance": 78,
              "speed": 72,
              "flexibility": 65,
              "stamina": 80,
              "character_type": "power"
            }
            형식의 JSON 파일이야

            strength: 스쿼트, 벤치프레스, 데드리프트 무게를 기반으로 계산, 높은 무게를 들수록 높은 점수를 얻습니다.

            endurance: 팔굽혀펴기, 윗몸일으키기 횟수를 기반으로 계산 많은 횟수를 할수록 높은 점수를 얻습니다.

            speed: 달리기 페이스를 기반으로 계산 페이스가 빠를수록 높은 점수를 얻습니다.

            flexibility: (가상의) 유연성 관련 데이터가 없으므로 기본 점수를 할당했습니다. (만약 유연성 측정 데이터가 있다면 해당 데이터를 기반으로 계산합니다.)

            stamina: 달리기 시간을 기반으로 계산되었습니다. 오래 달릴수록 높은 점수를 얻습니다. 또한 endurance점수와 speed점수를 합산하여 반영합니다.

            character_type: strength, endurance, speed, flexibility, stamina 점수를 종합적으로 고려하여 판단 (높다는 기준은 다른 스탯 평균보다 20%이상 수치를 가질때)
            {
            runner	러닝 페이스 & 유지 시간이 높음
            power    근력이 높음
            diet 	체지방률이 높아 유산소를 주로 수행해야 하는 체형
            balance	전반적인 운동 능력이 균등하게 분포되어있음
            endurance	팔굽혀펴기 & 윗몸일으키기 반복 횟수가 많음
            }

            입력 데이터의 성별이 "male"일때 평균은 {
              "user_id": "12345",
              "gender" : "male",
              "height": 175,
              "weight": 70,
              "muscle_mass": 33,
              "body_fat": 25,
              "pushups": 40,
              "situps": 50,
              "running_pace": 4.0,
              "running_time": 30,
              "squat": 60,
              "bench_press": 60,
              "deadlift": 60
            } 이라고 생각하고 이 경우 스탯을 전부 50으로 해줘

            입력 데이터의 성별이 "female"일때 평균은 {
              "user_id": "12345",
              "gender" : "female",
              "height": 166,
              "weight": 60,
              "muscle_mass": 25,
              "body_fat": 35,
              "pushups": 10,
              "situps": 30,
              "running_pace": 4.0,
              "running_time": 30,
              "squat": 40,
              "bench_press": 40,
              "deadlift": 40
            } 이라고 생각하고 이 경우 스탯을 전부 50으로 해줘

            모든 출력은 설명 및 상세 분석이 없이 단순 JSON만 반환해줘
            """;
    }
}
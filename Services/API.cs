using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace Righthere_Demo.Services
{
    public class API
    {
        private string emotion;
        private string suggestion;
        private string emotionalReflection;
        private string mood;
        private string keywords;

        public async Task SendData(string Diary)
        {
            using HttpClient client = new HttpClient();
            string url = "http://10.0.2.2:8000/getadvice"; // ใช้ 10.0.2.2 ถ้าเป็น Emulator

            var data = new { text = Diary }; // API ต้องการ key "text"

            string jsonData = JsonSerializer.Serialize(data);
            HttpContent content = new StringContent(jsonData, Encoding.UTF8, "application/json");

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);
                response.EnsureSuccessStatusCode();
                string responseBody = await response.Content.ReadAsStringAsync();

                // แปลง JSON เป็น Dictionary
                var responseData = JsonSerializer.Deserialize<Dictionary<string, string>>(responseBody);

                // ดึงค่าต่างๆ
                emotion = responseData["emotion"];
                string adviceRaw = responseData["advice"];

                // ใช้ Regex แยกค่าต่าง ๆ ออกจาก adviceRaw
                suggestion = ExtractValue(adviceRaw, "Suggestion");
                emotionalReflection = ExtractValue(adviceRaw, "Emotional Reflection");
                mood = ExtractValue(adviceRaw, "Mood");
                keywords = ExtractValue(adviceRaw, "Keywords");

                // แสดงผลลัพธ์
                Console.WriteLine($"Emotion: {emotion}");
                Console.WriteLine($"Suggestion: {suggestion}");
                Console.WriteLine($"Emotional Reflection: {emotionalReflection}");
                Console.WriteLine($"Mood: {mood}");
                Console.WriteLine($"Keywords: {keywords}");
            }
            catch (HttpRequestException httpEx)
            {
                Console.WriteLine($"HTTP Error: {httpEx.Message}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }

        private string ExtractValue(string text, string label)
        {
            var match = Regex.Match(text, $@"- {label}:\s*(.+?)(?:\s*-|$)");
            return match.Success ? match.Groups[1].Value.Trim() : "N/A";
        }

        // ✅ สร้าง Getter สำหรับค่าต่างๆ
        public string GetEmotion() => emotion;
        public string GetSuggestion() => suggestion;
        public string GetEmotionalReflection() => emotionalReflection;
        public string GetMood() => mood;
        public string GetKeywords() => keywords;

        public static async Task Main(string data)
        {
            API api = new API();
            await api.SendData(data);

            // ✅ แสดงผลลัพธ์ที่ได้จาก Getter
            Console.WriteLine("\n--- Results ---");
            Console.WriteLine("Emotion: " + api.GetEmotion());
            Console.WriteLine("Suggestion: " + api.GetSuggestion());
            Console.WriteLine("Emotional Reflection: " + api.GetEmotionalReflection());
            Console.WriteLine("Mood: " + api.GetMood());
            Console.WriteLine("Keywords: " + api.GetKeywords());
        }
    }
}
